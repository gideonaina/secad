# LLM Local Deployment

This repository provides a local deployment setup for a Large Language Model (LLM) using Docker and Docker Compose. The setup uses ollama LLM with Open Web UI.
NOTE: All information artifacts related to this deployment is local.

## Setup and Deployment

To run locally
- Run  `make start` at the root of this project. This will setup Open Web UI for chatting and deploys it with `llama3` model. 
- ~~ To setup this stack with a different LLM like say `gemma2`, issue this command `make start LOCAL_LLM=gemma2` ~~

### Chat UI
2. To access the chat UI, got to `http://localhost:3000`
3. Sign up with a local account and login (Login information is local to the host machine).
4. Select a model to use for chat.
5. Chat away :)

### API Access.
Ollama exposes some endpoint that one can use to intereact with the LLM model.
Some examples are below:

**Chat Endpoint**
```
$ curl http://localhost:11434/api/generate -d '{
  "model": "llama3",
  "prompt":"Why is the sky blue?"
}'
```

**Pull Model**
One can use multiple model in the Open Web UI. To pull a model run

`curl http://localhost:11434/api/pull -d '{"name": "llama3"}'`

**Check Models Avalible locally**
`curl http://localhost:11434/api/tags`



 