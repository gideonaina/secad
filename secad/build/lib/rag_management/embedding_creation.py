import os

from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
from langchain_postgres.vectorstores import PGVector

load_dotenv()

 
POSTGRES_USER=os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD=os.getenv("POSTGRES_PASSWORD")
POSTGRES_HOST=os.getenv("POSTGRES_HOST", "localhost")
POSTGRES_DB=os.getenv("POSTGRES_DB")
POSTGRES_PORT=os.getenv("POSTGRES_PORT")


def create_embeddings(texts, connection_string, collection_name):
    """Create embeddings and store them in the database."""
    embeddings = OpenAIEmbeddings()
    PGVector.from_documents(
        embedding=embeddings,
        documents=texts,
        collection_name=collection_name,
        connection=connection_string,
        use_jsonb=True,
        async_mode=False,
        create_extension=True,
    )
    print("Embeddings created and stored in the database.")