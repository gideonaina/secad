from crewai_tools import BaseTool
from rag_management.query_embedding import similarity_search

class ControlsRagTool(BaseTool):
    name: str = "RAG Knowledge Retriever"
    description: str = "Retrieves relevant controls from a knowledge base for threat scenarios."

    def _run(self, query: str):
        result = similarity_search(query, collection_name="controls")
        return result
