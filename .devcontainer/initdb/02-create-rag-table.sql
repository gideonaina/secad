CREATE TABLE knowledge_catalog (
    id SERIAL PRIMARY KEY,
    description TEXT NOT NULL,
    creation_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);