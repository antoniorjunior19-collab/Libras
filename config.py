"""
Configurações do Libras Bridge
Edite este arquivo para personalizar o comportamento do sistema
"""

# ============ CONFIGURAÇÕES DO SERVIDOR ============
SERVER_HOST = '0.0.0.0'  # '0.0.0.0' permite acesso externo, '127.0.0.1' apenas local
SERVER_PORT = 5000
DEBUG_MODE = False

# ============ CONFIGURAÇÕES DA CÂMERA ============
CAMERA_INDEX = 0  # Mude para 1 ou 2 se tiver múltiplas câmeras
CAMERA_WIDTH = 320
CAMERA_HEIGHT = 240
CAMERA_FPS = 30

# ============ CONFIGURAÇÕES DO MEDIAPIPE ============
MIN_DETECTION_CONFIDENCE = 0.7  # 0.5 = mais sensível, 0.9 = mais preciso
MIN_TRACKING_CONFIDENCE = 0.5
MAX_NUM_HANDS = 1  # Detectar apenas 1 mão

# ============ CONFIGURAÇÕES DO MODELO ============
MODEL_PATH = "modelo_libras.pkl"
CLIP_SIZE = 30  # Número de frames por predição (~1.5s a 20fps)
NUM_CONFIRMATIONS = 2  # Quantos clips iguais seguidos para confirmar

# ============ GESTOS SUPORTADOS ============
GESTOS_LABELS = ["ola", "sim", "nao"]  # Adicione mais gestos aqui

# ============ CONFIGURAÇÕES DE VISUALIZAÇÃO ============
# Cores em BGR (OpenCV)
COLOR_LANDMARKS = (0, 255, 0)  # Verde
COLOR_CONNECTIONS = (255, 255, 255)  # Branco
COLOR_TEXT = (0, 255, 0)  # Verde
COLOR_CONFIDENCE_BAR_BG = (50, 50, 50)  # Cinza escuro
COLOR_CONFIDENCE_BAR_FG = (0, 200, 255)  # Laranja

# Tamanhos
TEXT_SIZE = 1.2
TEXT_THICKNESS = 3
LANDMARK_THICKNESS = 2
LANDMARK_CIRCLE_RADIUS = 2

# ============ CONFIGURAÇÕES DE PERFORMANCE ============
JPEG_QUALITY = 50  # 1-100, menor = mais rápido mas pior qualidade
FRAME_SKIP = 2  # Processar 1 a cada N frames (1 = todos)
WEBSOCKET_FPS = 30  # Frames por segundo enviados ao navegador

# ============ CONFIGURAÇÕES DE HISTÓRICO ============
MAX_HISTORY_ITEMS = 10  # Quantas traduções manter no histórico

# ============ CONFIGURAÇÕES DE ÁUDIO (FUTURO) ============
ENABLE_TEXT_TO_SPEECH = False  # Ainda não implementado
TTS_LANGUAGE = 'pt-BR'
TTS_SPEED = 1.0

# ============ CONFIGURAÇÕES DE EXPORTAÇÃO (FUTURO) ============
ENABLE_EXPORT = False  # Ainda não implementado
EXPORT_FORMAT = 'txt'  # 'txt', 'pdf', 'csv'

# ============ CONFIGURAÇÕES DE SEGURANÇA ============
SECRET_KEY = 'libras_bridge_secret_key_change_in_production'
CORS_ALLOWED_ORIGINS = "*"  # Em produção, especifique domínios permitidos

# ============ MENSAGENS PERSONALIZADAS ============
MESSAGES = {
    'pt-BR': {
        'camera_starting': 'Iniciando câmera...',
        'camera_started': 'Câmera iniciada com sucesso!',
        'camera_stopped': 'Câmera parada',
        'waiting_hand': 'Aguardando mão...',
        'detecting_hand': 'Detectando mão...',
        'no_model': 'Modelo não carregado. Treine o modelo primeiro.',
        'gesture_confirmed': 'Gesto confirmado',
        'collecting_frames': 'Coletando frames',
    },
    'en': {
        'camera_starting': 'Starting camera...',
        'camera_started': 'Camera started successfully!',
        'camera_stopped': 'Camera stopped',
        'waiting_hand': 'Waiting for hand...',
        'detecting_hand': 'Detecting hand...',
        'no_model': 'Model not loaded. Train the model first.',
        'gesture_confirmed': 'Gesture confirmed',
        'collecting_frames': 'Collecting frames',
    }
}

DEFAULT_LANGUAGE = 'pt-BR'

# ============ MODO DE DESENVOLVIMENTO ============
DEV_MODE = {
    'show_fps': True,  # Mostrar FPS no vídeo
    'show_landmarks_ids': False,  # Mostrar IDs dos landmarks
    'log_predictions': True,  # Logar predições no console
    'save_debug_frames': False,  # Salvar frames para debug
}

# ============ VALIDAÇÃO DE CONFIGURAÇÕES ============
def validate_config():
    """Valida as configurações"""
    errors = []
    
    if not 0 <= MIN_DETECTION_CONFIDENCE <= 1:
        errors.append("MIN_DETECTION_CONFIDENCE deve estar entre 0 e 1")
    
    if not 0 <= MIN_TRACKING_CONFIDENCE <= 1:
        errors.append("MIN_TRACKING_CONFIDENCE deve estar entre 0 e 1")
    
    if CLIP_SIZE < 10:
        errors.append("CLIP_SIZE deve ser >= 10")
    
    if NUM_CONFIRMATIONS < 1:
        errors.append("NUM_CONFIRMATIONS deve ser >= 1")
    
    if not 1 <= JPEG_QUALITY <= 100:
        errors.append("JPEG_QUALITY deve estar entre 1 e 100")
    
    if errors:
        print("❌ ERROS DE CONFIGURAÇÃO:")
        for error in errors:
            print(f"   - {error}")
        return False
    
    return True

# ============ EXPORTAR CONFIGURAÇÕES ============
def get_config():
    """Retorna um dicionário com todas as configurações"""
    return {
        'server': {
            'host': SERVER_HOST,
            'port': SERVER_PORT,
            'debug': DEBUG_MODE,
        },
        'camera': {
            'index': CAMERA_INDEX,
            'width': CAMERA_WIDTH,
            'height': CAMERA_HEIGHT,
            'fps': CAMERA_FPS,
        },
        'mediapipe': {
            'min_detection_confidence': MIN_DETECTION_CONFIDENCE,
            'min_tracking_confidence': MIN_TRACKING_CONFIDENCE,
            'max_num_hands': MAX_NUM_HANDS,
        },
        'model': {
            'path': MODEL_PATH,
            'clip_size': CLIP_SIZE,
            'num_confirmations': NUM_CONFIRMATIONS,
            'gestos': GESTOS_LABELS,
        },
        'performance': {
            'jpeg_quality': JPEG_QUALITY,
            'frame_skip': FRAME_SKIP,
            'websocket_fps': WEBSOCKET_FPS,
        }
    }

if __name__ == "__main__":
    print("="*50)
    print("🔧 CONFIGURAÇÕES DO LIBRAS BRIDGE")
    print("="*50 + "\n")
    
    if validate_config():
        print("✅ Todas as configurações são válidas!\n")
        
        config = get_config()
        for section, settings in config.items():
            print(f"[{section.upper()}]")
            for key, value in settings.items():
                print(f"  {key}: {value}")
            print()
    else:
        print("\n❌ Corrija os erros acima.")