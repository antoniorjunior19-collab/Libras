import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import joblib

# Carregar dados
X = np.load("X.npy")   # (n, 30, 63)
y = np.load("y.npy")

# Achatar sequência (30x63 = 1890 features)
n_amostras, n_frames, n_features = X.shape
X = X.reshape((n_amostras, n_frames * n_features))

# Dividir em treino/teste
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Modelo mais robusto
modelo = RandomForestClassifier(n_estimators=500, random_state=42)
modelo.fit(X_train, y_train)

# Avaliação
y_pred = modelo.predict(X_test)
acc = accuracy_score(y_test, y_pred)
print("Acurácia do modelo:", acc)

# Salvar
joblib.dump(modelo, "modelo_libras.pkl")
print("[INFO] Modelo salvo como modelo_libras.pkl")
