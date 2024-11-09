## Database Snippet
```
psql postgresql://langflow:langflow@localhost:5432/langflow

-- Inside the psql prompt
CREATE TABLE security_requirements (
    id SERIAL PRIMARY KEY,
    requirement_description TEXT NOT NULL,
    creation_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

\dt
```

## Check tables
```
select * from langchain_pg_collection limit 5;
```

## Embedding with langchain
https://bugbytes.io/posts/vector-databases-pgvector-and-langchain/

## Ollama LLM API docs
https://github.com/ollama/ollama/blob/main/docs/api.md 


### Container connection
export PGPASSWORD='langflow'
psql -U langflow -d langflow

### host machine connection
export PGPASSWORD='langflow'
psql -U langflow -d langflow -h localhost
  
### Similarity search query
```
SELECT document, (embedding <=> '[0.008690234273672104, -0.020522210747003555]') as cos_dist
FROM langchain_pg_embedding
ORDER by cos_dist
LIMIT 2
```

## 2.0 Deployment
This repository provides a local deployment setup for a Large Language Model (LLM) using Docker and Docker Compose. The setup uses ollama LLM with Open Web UI.


### 2.1 Setup and Deployment

To run locally
- Run  `make start` at the root of this project. This will setup Open Web UI for chatting and deploys it with `llama3` model. 
- ~~ To setup this stack with a different LLM like say `gemma2`, issue this command `make start LOCAL_LLM=gemma2` ~~

#### 2.1.1 Chat UI
2. To access the chat UI, got to `http://localhost:3000`
3. Sign up with a local account and login (Login information is local to the host machine).
4. Select a model to use for chat.
5. Chat away :)

#### 2.1.2 API Access.
Ollama exposes some endpoint that one can use to intereact with the LLM model.
Some examples are below:

**Chat Endpoint**
```
curl http://localhost:11434/api/generate -d '{
  "model": "llama3",
  "prompt":"Name the planets in the solar system?"
}'
```

**Pull Model**
One can use multiple model in the Open Web UI. To pull a model run

`curl http://localhost:11434/api/pull -d '{"name": "llama3"}'`

**Check Models Avalible locally**
`curl http://localhost:11434/api/tags`

#### 2.2 LANGFLOW
https://github.com/langflow-ai/langflow/tree/main/docker_example

#### 2.3 RAG
To deploy the RAG, run `make rag`. This will start the RAG service at `http://localhost:7860`

### Tools
- https://tavily.com/ - Search API. See repo for samples and web scraper code - https://github.com/assafelovic/gpt-researcher

### llava
```
curl http://localhost:11434/api/generate -d '{
  "model": "llava",
  "prompt":"What is in this picture?",
  "images": ["iVBORw0KGgoAAAANSUhEUgAAAG0AAABmCAYAAADBPx ........C"]
}'
```

CREW AI Docs
https://chatgpt.com/g/g-qqTuUWsBY-crewai-assistant/c/2ee65a77-006f-491a-af2d-8d9a26777576