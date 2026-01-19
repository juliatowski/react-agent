from react_agent.logging_config import vlog
from langchain_text_splitters import CharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_ollama import OllamaEmbeddings


from pathlib import Path

class VectorSearch:
    name = "vector_search"
    description = "Search a local knowledge base using embeddings"

    def __init__(
        self,
        model: str = "qwen2.5",
        data_file: str = None,
        chunk_size: int = 200,
    ):
        # Build correct absolute path
        if data_file is None:
            data_file = Path(__file__).resolve().parents[2] / "data" / "ai_research.txt"

        # Load text
        with open(data_file, "r", encoding="utf-8") as f:
            text = f.read()


        # Split into chunks
        splitter = CharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=50)
        docs = splitter.create_documents([text])

        # Use Ollama embeddings
        embeddings = OllamaEmbeddings(model=model)

        # Build FAISS index
        self.db = FAISS.from_documents(docs, embeddings)

    def run(self, query: str, k: int = 3) -> str:
        """Embed query and return top-k relevant chunks."""
        vlog(f"VectorSearch query: {query}")
        results = self.db.similarity_search(query, k=k)
        formatted = "\n\n".join([f"- {r.page_content}" for r in results])
        vlog(f"VectorSearch returned {len(results)} results")
        return formatted
