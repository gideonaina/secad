FROM python:3.11-bullseye

RUN apt-get update && apt-get install curl git \
&& curl --proto '=https' --tlsv1.2 -sSf https://just.systems/install.sh | bash -s -- --to /usr/local/bin \
&& chmod +x /usr/local/bin/just

WORKDIR /workspaces

COPY ./secad/ /workspaces/
RUN pip install . && pip install -e .

EXPOSE 8501

ENV STREAMLIT_SERVER_HEADLESS=true
ENV STREAMLIT_SERVER_ENABLECORS=false
ENV PYTHONUNBUFFERED=1

CMD ["just", "start"]