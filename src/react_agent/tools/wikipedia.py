import wikipedia
from react_agent.logging_config import log, vlog  # <-- add this


class WikipediaTool:
    """
    A simple tool for searching and summarizing from Wikipedia.
    """

    name = "wikipedia"
    description = "Look up factual information from Wikipedia articles."

    def run(self, query: str, sentences: int = 2) -> str:
        """
        Search Wikipedia and return a short summary.
        """
        vlog(f"Wikipedia query: {query}")
        try:
            hits = wikipedia.search(query)
            if not hits:
                log(f"Wikipedia: no results for query='{query}'")
                return f"No results for '{query}'."
            title = hits[0]
            summary = wikipedia.summary(
                title, sentences=sentences, auto_suggest=False, redirect=True
            )
            out = f"{title}: {summary}"
            vlog(f"Wikipedia summary (first 200 chars): {out[:200]}")
            return out
        except Exception as e:
            log(f"Wikipedia error for query='{query}': {e}")
            return f"Wikipedia error: {e}"
