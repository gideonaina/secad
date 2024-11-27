from langchain_openai import OpenAIEmbeddings
from langchain_postgres.vectorstores import PGVector
import os
from dotenv import load_dotenv
load_dotenv()

 
POSTGRES_USERNAME=os.getenv("POSTGRES_USERNAME")
POSTGRES_PASSWORD=os.getenv("POSTGRES_PASSWORD")
POSTGRES_HOST=os.getenv("POSTGRES_HOST")
POSTGRES_DATABASE=os.getenv("POSTGRES_DATABASE")
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