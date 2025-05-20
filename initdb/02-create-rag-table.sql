-- CREATE TABLE knowledge_catalog (
--     id SERIAL PRIMARY KEY,
--     description TEXT NOT NULL,
--     creation_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
-- );

CREATE TABLE knowledge_catalog (
    file_hash TEXT NOT NULL,
    metadata TEXT,
    collection TEXT NOT NULL,
    creation_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (file_hash, collection)
);
