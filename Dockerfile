# Use uma imagem oficial do Python como imagem base (slim para reduzir tamanho)
FROM python:3.12-slim

# Define variáveis de ambiente úteis
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=8501

# Define o diretório de trabalho dentro do container
WORKDIR /app

# Instala dependências de sistema necessárias para alguns pacotes Python (ex: scipy, h5py)
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copia o arquivo de requisitos primeiro para aproveitar o cache de camadas do Docker
COPY requirements.txt .

# Atualiza o pip e instala as dependências do Python
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copia o restante do código do projeto para o container
COPY . .

# Expõe a porta que o Streamlit usará
EXPOSE 8501

# O comando de inicialização reproduz o que era feito no App Platform
CMD sh setup.sh && streamlit run app/app.py --server.enableXsrfProtection false
