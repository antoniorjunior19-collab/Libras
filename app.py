from flask import Flask, render_template, Response, jsonify, request
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
import threading
import time
import socket

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
hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.5,
    model_complexity=0
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
# Câmera do Servidor (Apenas para versão Web Local)
# ==========================================
camera = None
frame_count = 0 

class VideoCamera:
    def __init__(self):
        # Tentar índices diferentes e backends diferentes
        self.video = None
        self.stopped = False
        
        # Lista de tentativas: (index, backend)
        attempts = []
        if os.name == 'nt':
            attempts = [(0, cv2.CAP_DSHOW), (0, cv2.CAP_MSMF), (1, cv2.CAP_DSHOW), (1, cv2.CAP_MSMF)]
        else:
            attempts = [(0, cv2.CAP_ANY), (1, cv2.CAP_ANY)]
            
        for idx, backend in attempts:
            try:
                print(f"[DEBUG] Tentando abrir câmera índice {idx} com backend {backend}...")
                cap = cv2.VideoCapture(idx, backend)
                if cap.isOpened():
                    # Tentar ler um frame para confirmar
                    ret, frame = cap.read()
                    if ret and frame is not None and frame.size > 0:
                        self.video = cap
                        self.grabbed = ret
                        self.frame = frame
                        print(f"[INFO] Câmera aberta com sucesso: Índice {idx}")
                        break
                    else:
                        cap.release()
            except Exception as e:
                print(f"[ERRO] Falha ao tentar índice {idx}: {e}")
                
        if self.video is None or not self.video.isOpened():
            raise RuntimeError("Não foi possível abrir nenhuma câmera. Verifique se a câmera está conectada e não está sendo usada por outro programa.")
        
        self.video.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
        self.video.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)
        self.video.set(cv2.CAP_PROP_FPS, 30)
            
        self.thread = threading.Thread(target=self.update, args=())
        self.thread.daemon = True
        self.thread.start()
    
    def update(self):
        while not self.stopped:
            if self.video.isOpened():
                grabbed, frame = self.video.read()
                if grabbed:
                    self.grabbed = grabbed
                    self.frame = frame
                else:
                    self.stopped = True
            else:
                self.stopped = True
            time.sleep(0.01)
            
    def stop(self):
        self.stopped = True
        if self.thread.is_alive():
            self.thread.join(timeout=1.0)
        if self.video.isOpened():
            self.video.release()
    
    def get_frame(self):
        if not self.grabbed or self.stopped:
            return None
        frame = self.frame.copy()
        frame = cv2.flip(frame, 1)
        return frame

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
    
    # Se for o dono da câmera web (simplificado: se câmera está ativa e usuário sai)
    # Aqui poderíamos melhorar para saber quem iniciou a câmera
    pass

@socketio.on('process_frame')
def handle_process_frame(data):
    try:
        image_data = base64.b64decode(data['image'])
        image = Image.open(io.BytesIO(image_data))
        frame = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
        
        # Processamento
        state = get_client_state()
        result = process_frame_logic(frame, state)
        
        # Enviar apenas o resultado (não precisa devolver a imagem)
        emit('translation_result', {
            'gesto': result['gesto'],
            'confianca': result['confianca'],
            'hand_detected': result['hand_detected']
        })
        
    except Exception as e:
        # Silenciar erros de imagem corrompida ocasional
        pass

    
    
if __name__ == '__main__':
    print("[INFO] Iniciando servidor Libras Bridge...")
    print("[INFO] Acesse (Web): http://localhost:5000")
        
    socketio.run(app, debug=False, host='0.0.0.0', port=5000)