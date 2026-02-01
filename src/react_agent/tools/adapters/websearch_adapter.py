from __future__ import annotations
from react_agent.llm.llm_client import LLMClient
from react_agent.tools.websearch import WebSearch

_STRIP = "`\"'\n\t "

def _sanitize_query(text: str) -> str:
    """Keep first line, strip quotes/backticks/punctuation, cap length."""
    q = (text or "").strip()
    q = q.splitlines()[0][:200]
    q = q.strip(_STRIP)
    while q and q[-1] in "?.!,;:":
        q = q[:-1]
    return q


class WebSearchAdapter:
    """
    Adapter for WebSearch.
    Uses the LLM to rewrite a task into a concise search query,
    then runs the WebSearch tool.
    """

    name = "websearch"
    description = "Rewrite a task into a web query and search DuckDuckGo."

    def __init__(self, model: str = "qwen2.5:7b"):
        self.model = model
        self.client = LLMClient(model)
        self.tool = WebSearch()

    def run(self, subtask: str, k: int = 3) -> str:
        """Extract a concise query with LLM, then run WebSearch."""
        instruction = (
            "Rewrite the following task into a concise web search query. "
            "Output ONLY the query, no quotes, no trailing punctuation, max 12 words."
        )

        try:
            try:
                raw = self.client.chat(f"{instruction}\n\nTask: {subtask}")
            except TypeError:
                raw = self.client.chat([
                    {"role": "system", "content": instruction},
                    {"role": "user", "content": subtask},
                ])
        except Exception:
            raw = subtask  # fallback

        query = _sanitize_query(str(raw)) or _sanitize_query(subtask)
        return self.tool.run(query=query, k=k)
