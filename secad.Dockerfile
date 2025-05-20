FROM python:3.11-bookworm

RUN apt-get update && apt-get install -y curl git \
&& curl --proto '=https' --tlsv1.2 -sSf https://just.systems/install.sh | bash -s -- --to /usr/local/bin \
&& chmod +x /usr/local/bin/just

WORKDIR /workspaces

# Install Python dependencies first before copying the rest of the code
COPY ./secad/pyproject.toml /workspaces/
RUN pip install .

#
COPY ./secad/ /workspaces/
RUN pip install -e .

EXPOSE 8501

ENV STREAMLIT_SERVER_HEADLESS=true
ENV STREAMLIT_SERVER_ENABLECORS=false
ENV PYTHONUNBUFFERED=1

ENTRYPOINT ["just", "start"]