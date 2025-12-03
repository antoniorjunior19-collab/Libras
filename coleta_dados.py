import cv2
import mediapipe as mp
import numpy as np
import os

# Configurações
gesto = "nao"  # altere para "sim" ou "nao"
saida = f"dataset/{gesto}"
os.makedirs(saida, exist_ok=True)

mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils
hands = mp_hands.Hands(static_image_mode=False,
                       max_num_hands=1,
                       min_detection_confidence=0.7,
                       model_complexity=0)

cap = cv2.VideoCapture(0)  # troque para 1 ou 2 se quiser outra câmera
clip_size = 30  # 30 frames = ~1,5s
frames_clip = []
contador = 0

print(f"[INFO] Gravando gestos do tipo: {gesto}")

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

    # Mostrar texto e cruz central
    h, w, _ = frame.shape
    cv2.putText(frame, f"Gesto: {gesto} | Frames: {len(frames_clip)}",
                (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    cv2.line(frame, (w//2 - 20, h//2), (w//2 + 20, h//2), (0, 0, 255), 2)
    cv2.line(frame, (w//2, h//2 - 20), (w//2, h//2 + 20), (0, 0, 255), 2)

    cv2.imshow("Coleta de Dados", frame)

    # Quando tiver N frames, salva um clipe
    if len(frames_clip) == clip_size:
        arquivo = os.path.join(saida, f"clip_{contador}.npy")
        np.save(arquivo, np.array(frames_clip))
        print(f"[INFO] Salvo: {arquivo}")
        frames_clip = []
        contador += 1

    if cv2.waitKey(1) & 0xFF == 27:  # ESC para sair
        break

cap.release()
cv2.destroyAllWindows()
