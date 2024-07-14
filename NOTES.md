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