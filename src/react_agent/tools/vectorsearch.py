from react_agent.logging_config import log, vlog  

try:
    # Most recent ecosystem: separate langchain-text-splitters package
    from langchain_text_splitters import CharacterTextSplitter
except ImportError:
    try:
        # Some langchain versions
        from langchain.text_splitters import CharacterTextSplitter
    except ImportError:
        # Older langchain versions
        from langchain.text_splitter import CharacterTextSplitter

from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import OllamaEmbeddings

class VectorSearch:
    """
    Simplified FAISS-based vector search using LangChain.
    """

    name = "vector_search"
    description = "Search a local knowledge base using embeddings"

    def __init__(self, model: str = "qwen2.5", data_file: str = "src/data/ai_research.txt", chunk_size: int = 200):
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