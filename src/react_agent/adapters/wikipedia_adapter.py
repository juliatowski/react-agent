from react_agent.llm_client import LLMClient
from react_agent.tools.wikipedia import WikipediaTool


class WikipediaAdapter:
    """
    Adapter for the Wikipedia tool.
    Uses an LLM to rewrite a subtask into a clean Wikipedia query,
    then runs the tool.
    """

    name = "wikipedia"
    description = "Rewrite a task into a Wikipedia query and fetch a summary."

    def __init__(self, model: str = "qwen2.5"):
        self.model = model
        self.client = LLMClient(model)
        self.tool = WikipediaTool()

    def run(self, subtask: str, sentences: int = 2) -> str:
        instruction = (
            "Rewrite the following task as a short, clean query suitable for Wikipedia search. "
            "Return only the query.\n\n"
            f"Task: {subtask}"
        )
        query = self.client.chat(instruction).strip()
        return self.tool.run(query=query, sentences=sentences)
