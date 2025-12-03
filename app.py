from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit
import cv2
import mediapipe as mp
import numpy as np
import joblib
from collections import deque
import base64
import io
import os
from PIL import Image

app = Flask(__name__)
app.config['SECRET_KEY'] = 'libras_bridge_secret'
socketio = SocketIO(app, cors_allowed_origins="*", max_http_buffer_size=10000000) # Aumentar buffer para imagens grandes

# Carregar modelo
try:
    modelo = joblib.load("modelo_libras.pkl")
    print("[INFO] Modelo carregado com sucesso!")
except:
    print("[AVISO] Modelo não encontrado. Execute treinamento.py primeiro.")
    modelo = None

# Configuração MediaPipe
mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils

# Configuração simplificada para evitar uso de GPU
hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.5,
    model_complexity=0 # 0 = Lite (mais rápido, menos preciso, menos dependente de GPU)
)

# ==========================================
# Gerenciamento de Estado por Cliente (Mobile/Web)
# ==========================================
class ClientState:
    def __init__(self):
        self.clip_size = 30
        self.frames_clip = deque(maxlen=self.clip_size)
        self.ultimo_gesto = None
        self.confirmacoes = 0
        self.last_hand_detected = False

client_states = {}

def get_client_state():
    sid = request.sid
    if sid not in client_states:
        client_states[sid] = ClientState()
    return client_states[sid]

# ==========================================
# Lógica de Processamento (Reutilizável)
# ==========================================
def process_frame_logic(frame, state):
    # Redimensionar se necessário para consistência
    if frame.shape[1] > 320:
        frame = cv2.resize(frame, (320, 240))

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb)
    
    gesto_atual = None
    confianca = 0
    
    if results.multi_hand_landmarks:
        state.last_hand_detected = True
        for hand_landmarks in results.multi_hand_landmarks:
            coords = []
            for lm in hand_landmarks.landmark:
                coords.extend([lm.x, lm.y, lm.z])
            state.frames_clip.append(coords)
    else:
        state.last_hand_detected = False
    
    # Predição
    if len(state.frames_clip) == state.clip_size and modelo is not None:
        try:
            entrada = np.array(state.frames_clip).flatten().reshape(1, -1)
            gesto_predito = modelo.predict(entrada)[0]
            
            if gesto_predito == state.ultimo_gesto:
                state.confirmacoes += 1
            else:
                state.confirmacoes = 1
                state.ultimo_gesto = gesto_predito
            
            if state.confirmacoes >= 2:
                gesto_atual = gesto_predito
                confianca = min(state.confirmacoes * 30, 95)
        except Exception as e:
            print(f"[ERRO] Predição: {e}")
            
    return {
        'gesto': gesto_atual,
        'confianca': confianca,
        'frames_coletados': len(state.frames_clip),
        'hand_detected': state.last_hand_detected
    }

# ==========================================
# Startup Check
# ==========================================
def check_mediapipe():
    print("[INFO] Verificando MediaPipe...")
    try:
        dummy_frame = np.zeros((240, 320, 3), dtype=np.uint8)
        results = hands.process(dummy_frame)
        print("[INFO] MediaPipe inicializado com sucesso (teste de inferência ok)")
    except Exception as e:
        print(f"[ERRO] Falha na verificação do MediaPipe: {e}")

# Executar verificação na inicialização
with app.app_context():
    check_mediapipe()

# ==========================================
# Rotas e Eventos
# ==========================================
@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('connect')
def handle_connect():
    print(f'[INFO] Cliente conectado: {request.sid}')
    emit('status', {'message': 'Conectado ao servidor'})

@socketio.on('disconnect')
def handle_disconnect():
    print(f'[INFO] Cliente desconectado: {request.sid}')
    if request.sid in client_states:
        del client_states[request.sid]

@socketio.on('start_camera')
def handle_start_camera():
    sid = request.sid
    print(f'[INFO] Iniciando câmera para: {sid}')
    # Reiniciar estado do cliente
    client_states[sid] = ClientState()

@socketio.on('stop_camera')
def handle_stop_camera():
    sid = request.sid
    print(f'[INFO] Parando câmera para: {sid}')
    if sid in client_states:
        # Opcional: limpar buffer ou manter histórico
        client_states[sid].frames_clip.clear()

@socketio.on('process_frame_web')
def handle_process_frame(data):
    try:
        # Debug simples para verificar se está chegando
        print(f"Frame recebido: {len(data['image'])} bytes")

        image_data = base64.b64decode(data['image'])
        image = Image.open(io.BytesIO(image_data))
        
        # DEBUG: Verificar imagem
        # print(f"Imagem decodificada: {image.size} modo={image.mode}")

        frame = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
        
        # Processamento
        state = get_client_state()
        result = process_frame_logic(frame, state)
        
        # Debug se detectou mão
        if result['hand_detected']:
             print(f"[DEBUG] Mão detectada! Gesto: {result['gesto']} Confiança: {result['confianca']}")
        
        # Enviar resultado
        emit('frame_processed', {
            'gesto': result['gesto'],
            'confianca': result['confianca'],
            'hand_detected': result['hand_detected']
        })
        
    except Exception as e:
        print(f"[ERRO] Processamento de frame: {e}")
        pass

    
    
if __name__ == '__main__':
    print("[INFO] Iniciando servidor Libras Bridge...")
    print("[INFO] Acesse (Web): http://localhost:5000")
        
    socketio.run(app, debug=False, host='0.0.0.0', port=5000)