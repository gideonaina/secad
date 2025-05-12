import argparse
import os

import psycopg
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
from langchain_postgres.vectorstores import PGVector

load_dotenv()


# class QueryEmbedding:
#         def __init__(self) -> None:
#                 pass
# map = {
#     "Security Review": "security_requirement"
# }
POSTGRES_USER=os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD=os.getenv("POSTGRES_PASSWORD")
POSTGRES_HOST=os.getenv("POSTGRES_HOST", "localhost")
POSTGRES_DB=os.getenv("POSTGRES_DB")
POSTGRES_PORT=os.getenv("POSTGRES_PORT")
POSTGRES_CONNECTION_PREFIX=os.getenv("POSTGRES_CONNECTION_PREFIX")
CONNECTION_STRING = f"{POSTGRES_CONNECTION_PREFIX}://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
os.environ["CONNECTION_STRING"] = CONNECTION_STRING

collection_name = os.getenv("COLLECTION_NAME")
connection_string = os.getenv("CONNECTION_STRING")


def similarity_search(prompt: str, collection_name = collection_name) -> str:
            
    embeddings = OpenAIEmbeddings()  # Provide your OpenAI API key
    # connection_string = os.getenv("CONNECTION_STRING")
    print(f"PGVector parameters: connection: {connection_string}, collection_name: {collection_name}")
    vector_store = PGVector(connection=connection_string, embeddings=embeddings, collection_name=collection_name)
    
    print(f". . . create embedding for prompt - {prompt}")
    query_embedding = embeddings.embed_query(prompt)
    # print(f"query embedding: {query_embedding}")

    print(". . . performing similarity search")       
    results_with_scores = vector_store.similarity_search_with_score_by_vector(query_embedding, k=3)

    # Print the results with scores
    context=""
    if not results_with_scores:
        print("No results found with LangChain similarity search.")
    else:
        for result in results_with_scores:
            # context = f"{context}\n\n".join(result[0].page_content)
            # print(result[0].page_content)
            context = context + "\n" + result[0].page_content

    # print(context)
    return context




def test(prompt: str) -> None:
    #  Define your database connection details
    POSTGRES_USER=os.getenv("POSTGRES_USER")
    POSTGRES_PASSWORD=os.getenv("POSTGRES_PASSWORD")
    POSTGRES_HOST=os.getenv("POSTGRES_HOST", "localhost")
    POSTGRES_DB=os.getenv("POSTGRES_DB")
    POSTGRES_PORT=os.getenv("POSTGRES_PORT")

    db_config = {
        'dbname': POSTGRES_DB,
        'user': POSTGRES_USER,
        'password': POSTGRES_PASSWORD,
        'host': POSTGRES_HOST,
        'port': POSTGRES_PORT
    }

    # Connect to your PostgreSQL database
    conn = psycopg.connect(**db_config)

    # Initialize your embeddings and vector store
    embeddings = OpenAIEmbeddings()  # Provide your OpenAI API key
    connection_string = os.getenv("CONNECTION_STRING")
    collection_name = os.getenv("COLLECTION_NAME")
    vector_store = PGVector(connection=connection_string, embeddings=embeddings, collection_name=collection_name)
    # Ensure the table name and column names are correct
    # vector_store = PGVector(
    #     connection=f"postgresql://{db_config['user']}:{db_config['password']}@{db_config['host']}:{db_config['port']}/{db_config['dbname']}",
    #     embedding_function=embeddings.embed_query,
    #     table_name="langchain_pg_embedding",  # Ensure this matches your table name
    #     vector_column_name="embedding"        # Ensure this matches your column name
    # )


    # Define your query embedding
    query_embedding = embeddings.embed_query(prompt)

    cur = conn.cursor()
    # cur.execute("""
    # SELECT id, (embedding <=> [ %s, ]) as cos_dist
    # FROM langchain_pg_embedding
    # ORDER BY cos_dist
    # LIMIT 5;
    # """, (query_embedding,))

    cur.execute(f"""
    SELECT id, embedding <=> CAST(ARRAY {query_embedding} AS vector) as cos_dist
    FROM langchain_pg_embedding
    ORDER BY cos_dist
    LIMIT 5;
    """)

    results = cur.fetchall()
    for result in results:
        print(f"Direct Query - ID: {result[0]}, Embedding: {result[1]}")

    cur.close()

    # Perform the similarity search using LangChain
    # results_with_scores = vector_store.similarity_search_with_relevance_scores(prompt, k=5)
    # results_with_scores = vector_store.similarity_search_by_vector(query_embedding, k=5)
    results_with_scores = vector_store.similarity_search_with_score_by_vector(query_embedding, k=3)


    # Print the results with scores
    if not results_with_scores:
        print("No results found with LangChain similarity search.")
    else:
        for result in results_with_scores:
            # print(f"LangChain Query - ID: {result['id']}, Score: {result['score']}, Embedding: {result['embedding']}")
            # print(result)
            # Tuple (Document, relevance_score)
            # Document(
                # page_content="Hello, world!",
                # metadata={"source": "https://example.com"}
            #)
            print(f"{result[0]}")
    conn.close()


def main(): 
    parser = argparse.ArgumentParser(description="Query Embedding")
    parser.add_argument("-p", "--prompt", required=True, type=str, help="User Prompt")


    args = parser.parse_args()
    resp = similarity_search(args.prompt)
    print(resp)
    # test(args.prompt)

if __name__ == "__main__":
      main()