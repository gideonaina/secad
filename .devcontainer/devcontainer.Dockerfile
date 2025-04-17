FROM mcr.microsoft.com/devcontainers/python:1-3.12-bullseye

RUN apt-get update && apt-get install curl git \
&& curl --proto '=https' --tlsv1.2 -sSf https://just.systems/install.sh | bash -s -- --to /usr/local/bin \
&& chmod +x /usr/local/bin/just