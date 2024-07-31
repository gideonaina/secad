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