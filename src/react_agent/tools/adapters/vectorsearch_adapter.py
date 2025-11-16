from react_agent.llm_client import LLMClient
from react_agent.tools.vectorsearch import VectorSearch


class VectorSearchAdapter:
    """
    Adapter for the VectorSearch tool.
    Uses an LLM to rewrite a subtask into a clean search query,
    then runs the VectorSearch tool.
    """

    name = "vector_search"
    description = "Rewrite a task into a query and search a local knowledge base."

    def __init__(self, model: str = "qwen2.5", data_file: str = "data/ai_research.txt"):
        self.model = model
        self.client = LLMClient(model)
        self.tool = VectorSearch(model=model, data_file=data_file)

    def run(self, subtask: str, k: int = 3) -> str:
        """Rewrite subtask into a query with LLM, then run vector search."""
        instruction = (
            "Rewrite the following task into a short, clear search query "
            "that could retrieve relevant passages from a knowledge base. "
            "Output ONLY the query, nothing else.\n\n"
            f"Task: {subtask}"
        )
        query = self.client.chat(instruction).strip()
        return self.tool.run(query=query, k=k)
