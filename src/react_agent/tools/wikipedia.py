import wikipedia


class WikipediaTool:
    """A simple tool for searching and summarizing from Wikipedia."""

    name = "wikipedia"
    description = "Look up factual information from Wikipedia articles."

    def run(self, query: str, sentences: int = 2) -> str:
        """
        Search Wikipedia and return a short summary.
        """
        try:
            hits = wikipedia.search(query)
            if not hits:
                return f"No results for '{query}'."
            title = hits[0]
            summary = wikipedia.summary(
                title, sentences=sentences, auto_suggest=False, redirect=True
            )
            return f"{title}: {summary}"
        except Exception as e:
            return f"Wikipedia error: {e}"
