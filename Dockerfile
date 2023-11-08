# app/Dockerfile

FROM python:3.9-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    git \
    && rm -rf /var/lib/apt/lists/*

RUN git clone https://github.com/paulwababu/chat-with-pdf-and-code.git .

RUN pip3 install -r requirements.txt

EXPOSE 3000

HEALTHCHECK CMD curl --fail http://localhost:3000/_stcore/health

ENTRYPOINT ["streamlit", "run", "app_code.py", "--server.port=3000", "--server.address=0.0.0.0"]