import argparse
import os

import boto3
from dotenv import load_dotenv
from rag_management.embedding_creation import create_embeddings
from rag_management.utils import file_exists_in_catalog, get_file_hash
from langchain.text_splitter import RecursiveCharacterTextSplitter

# from langchain.document_loaders import TextLoader  # Adjust this import based on your actual loader
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from datetime import datetime

load_dotenv()

def download_file_from_s3(bucket_name, s3_key, local_path):
    s3 = boto3.client('s3')
    s3.download_file(bucket_name, s3_key, local_path)
    print(f"Downloaded {s3_key} from bucket {bucket_name} to {local_path}")
    # return local_path

def load_and_split_file(file_path):
    _, file_extension = os.path.splitext(file_path)
    loader = TextLoader(file_path)
    split_docs=''

    #To move this into a separate function later.
    if file_extension.lower() == '.pdf':
        # print(f'************ file extension - {file_extension}')
        loader = PyPDFLoader(file_path)
        documents = loader.load_and_split()
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=2600, chunk_overlap=100)
        split_docs = text_splitter.split_documents(documents)
    else:
        documents = loader.load()
        splitter = RecursiveCharacterTextSplitter(chunk_size=2600, chunk_overlap=100)
        split_docs = splitter.split_text(documents)
    
    return split_docs

def save_as_embedding(uploaded_file, collection_name):
    """Save the file as an embedding in the database."""
    
    if uploaded_file is not None:

        POSTGRES_USERNAME=os.getenv("POSTGRES_USERNAME")
        POSTGRES_PASSWORD=os.getenv("POSTGRES_PASSWORD")
        POSTGRES_HOST=os.getenv("POSTGRES_HOST")
        POSTGRES_DATABASE=os.getenv("POSTGRES_DATABASE")
        POSTGRES_PORT=os.getenv("POSTGRES_PORT")
        POSTGRES_CONNECTION_PREFIX=os.getenv("POSTGRES_CONNECTION_PREFIX")

        db_config = {
            'dbname': POSTGRES_DATABASE,
            'user': POSTGRES_USERNAME,
            'password': POSTGRES_PASSWORD,
            'host': POSTGRES_HOST,
            'port': POSTGRES_PORT
        }
        file_hash = get_file_hash(uploaded_file)

        if file_exists_in_catalog(db_config, file_hash, collection_name):
            return {"message": "File already exists in the RAG."}
            
        # now = datetime.now()
        # now.strftime("%Y-%m-%d_%H-%M-%S")

        # TODO: Use file stream (ByteIO) directly instead of saving to disk.
        upload_dir = "/tmp"
        os.makedirs(upload_dir, exist_ok=True)
        save_path = os.path.join(upload_dir, uploaded_file.name)
        with open(save_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        # save_path = uploaded_file.upload_url

        splits = load_and_split_file(save_path)

        CONNECTION_STRING = f"{POSTGRES_CONNECTION_PREFIX}://{POSTGRES_USERNAME}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DATABASE}"
        os.environ["CONNECTION_STRING"] = CONNECTION_STRING

        file_details = {
            "file_hash": file_hash,
            "metadata": f"""
                filename: {uploaded_file.name},
                type: {uploaded_file.type},
                size: {uploaded_file.size}
            """,
            "collection": collection_name,
        }

        create_embeddings(splits, CONNECTION_STRING, collection_name, db_config, file_details)
        return {"message": f"Uploaded {uploaded_file.name} to RAG"}
    else:
        raise ValueError("No file uploaded.")

    
def main():
    COLLECTION_NAME = os.getenv("COLLECTION_NAME")
    parser = argparse.ArgumentParser(description="Embedding Creation")
    parser.add_argument("-s", "--s3-file", action="store_true", help="Create embeddings and store them in the database.")
    parser.add_argument("-f", "--file-path", required=True, type=str, help="Path to local or S3 file (without prefix).")
    parser.add_argument("-c", "--collection-name", default=COLLECTION_NAME, type=str, help="collection of the data being imported in RAG")


    args = parser.parse_args()
    file_path = args.file_path

    if args.s3_file:
        S3_BUCKET=os.getenv("S3_BUCKET")
        filename, file_extension = os.path.splitext(file_path)
        file_path = f'/tmp/{filename}{file_extension}'
        download_file_from_s3(S3_BUCKET, args.file_path, file_path)

    splits = load_and_split_file(file_path)

    POSTGRES_USERNAME=os.getenv("POSTGRES_USERNAME")
    POSTGRES_PASSWORD=os.getenv("POSTGRES_PASSWORD")
    POSTGRES_HOST=os.getenv("POSTGRES_HOST")
    POSTGRES_DATABASE=os.getenv("POSTGRES_DATABASE")
    POSTGRES_PORT=os.getenv("POSTGRES_PORT")
    POSTGRES_CONNECTION_PREFIX=os.getenv("POSTGRES_CONNECTION_PREFIX")

    CONNECTION_STRING = f"{POSTGRES_CONNECTION_PREFIX}://{POSTGRES_USERNAME}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DATABASE}"
    os.environ["CONNECTION_STRING"] = CONNECTION_STRING
    COLLECTION_NAME = args.collection_name

    create_embeddings(splits, CONNECTION_STRING, COLLECTION_NAME)


if __name__ == "__main__":
    main()
