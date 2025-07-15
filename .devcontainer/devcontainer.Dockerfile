FROM mcr.microsoft.com/devcontainers/python:1-3.12-bullseye

RUN apt-get update && apt-get install -y curl git postgresql-client \
&& curl --proto '=https' --tlsv1.2 -sSf https://just.systems/install.sh | bash -s -- --to /usr/local/bin \
&& chmod +x /usr/local/bin/just

RUN apt-get update && apt-get install -y \
    build-essential \
    wget \
    libreadline-dev \
    libsqlite3-dev \
    && rm -rf /var/lib/apt/lists/*