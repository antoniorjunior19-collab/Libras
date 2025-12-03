# Usar uma imagem base leve do Python
FROM python:3.10-slim

# Definir diretório de trabalho
WORKDIR /app

# Instalar dependências do sistema necessárias para OpenCV e MediaPipe
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Copiar arquivos de requisitos
COPY requirements.txt .

# Instalar dependências Python
# O --no-cache-dir ajuda a manter a imagem menor
RUN pip install --no-cache-dir -r requirements.txt

# Copiar o resto do código do projeto
COPY . .

# Expor a porta que o Flask usa
EXPOSE 5000

# Comando para rodar a aplicação usando Gunicorn (servidor de produção)
# Usamos eventlet para melhor performance com WebSockets
CMD ["gunicorn", "--worker-class", "eventlet", "-w", "1", "--bind", "0.0.0.0:5000", "app:app"]
