import cv2
import mediapipe as mp
import numpy as np
import joblib
from collections import deque

# Carregar modelo
modelo = joblib.load("modelo_libras.pkl")

# Configuração MediaPipe
mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils
hands = mp_hands.Hands(static_image_mode=False,
                       max_num_hands=1,
                       min_detection_confidence=0.7,
                       model_complexity=0)

# Fila para armazenar frames
clip_size = 30
frames_clip = deque(maxlen=clip_size)

# Histórico para confirmação
ultimo_gesto = None
confirmacoes = 0

cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Espelhar a câmera
    frame = cv2.flip(frame, 1)

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            coords = []
            for lm in hand_landmarks.landmark:
                coords.extend([lm.x, lm.y, lm.z])

            frames_clip.append(coords)

    # Quando tiver frames suficientes, prever
    if len(frames_clip) == clip_size:
        entrada = np.array(frames_clip).flatten().reshape(1, -1)
        gesto_predito = modelo.predict(entrada)[0]

        if gesto_predito == ultimo_gesto:
            confirmacoes += 1
        else:
            confirmacoes = 1
            ultimo_gesto = gesto_predito

        if confirmacoes >= 2:  # exige 2 clipes iguais seguidos
            cv2.putText(frame, f"Gesto confirmado: {gesto_predito}",
                        (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    cv2.imshow("Reconhecimento em tempo real", frame)

    if cv2.waitKey(1) & 0xFF == 27:  # ESC
        break

cap.release()
cv2.destroyAllWindows()
