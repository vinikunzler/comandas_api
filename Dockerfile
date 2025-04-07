# Utiliza a imagem base Python 3.13 - Debian
FROM python:3.13-slim

# Define metadados da imagem (boas práticas para Podman/Docker)
LABEL maintainer="Vinicius Kunzler <vini.kunzler@uniplaclages.edu.br>"
LABEL description="API Python com FastAPI, Hypercorn e QUIC"
LABEL version="1.0.0"

# Define o diretório de trabalho
WORKDIR /code

# Instala dependências do sistema
RUN apt-get update && apt-get install -y \
    build-essential \
    default-libmysqlclient-dev \
    pkg-config \
    libssl-dev \
    libffi-dev \
    gcc \
    && apt-get clean

# --- Instalação de Dependências ---
# Copia apenas o arquivo de requisitos primeiro para aproveitar o cache do Docker
COPY ./requirements.txt .

# Atualiza o pip e Instala as dependências do Python listadas em requirements.txt
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir --upgrade -r requirements.txt

#RUN pip install hypercorn[h3]
#RUN pip install aioquic

# Copia o código-fonte da aplicação para o diretório de trabalho
COPY ./src .

# Copia os certificados para um diretório separado
COPY ./cert /cert

# --- Execução ---
# Expõe a porta 4443 para TCP (HTTPS) e UDP (QUIC/H3)
# EXPOSE apenas documenta, não publica a porta.

EXPOSE 4443/tcp
EXPOSE 4443/udp
# Comando para iniciar o servidor Hypercorn
# REMOVIDO: --reload (não usar em produção)
# CAMINHOS: Usando caminhos absolutos para clareza
CMD ["hypercorn", \
"--certfile=/cert/cert.pem", "--keyfile=/cert/ecc-key.pem",\
"--bind", "0.0.0.0:4443", "--quic-bind", "0.0.0.0:4443",\
"main:app"]