import os
import numpy as np

# Pastas dos gestos
gestos = ["ola", "sim", "nao"]

X = []  # sequências de frames
y = []  # rótulos

for gesto in gestos:
    pasta = f"dataset/{gesto}"
    for arquivo in os.listdir(pasta):
        if arquivo.endswith(".npy"):
            caminho = os.path.join(pasta, arquivo)
            clip = np.load(caminho)  # formato (30, 63)
            X.append(clip)
            y.append(gesto)

X = np.array(X)  # (n_amostras, 30, 63)
y = np.array(y)

print("Formato de X:", X.shape)
print("Formato de y:", y.shape)

np.save("X.npy", X)
np.save("y.npy", y)
print("[INFO] Arquivos X.npy e y.npy salvos com sucesso!")
