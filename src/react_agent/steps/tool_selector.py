import json
from react_agent.llm_client import LLMClient
from react_agent.tools import TOOLS


def assign_tools_to_subtasks(subtasks: list[str], model: str = "qwen2.5") -> dict[str, str]:
    """
    Step 2: Ask the LLM which tool is best for each subtask.
    Returns a dict mapping subtask -> tool_name.
    """
    client = LLMClient(model)

    tool_descriptions = "\n".join(
        f"- {name}: {tool.description}" for name, tool in TOOLS.items()
    )

    prompt = f"""
You are a tool selector.

Available tools:
{tool_descriptions}

Return a JSON object where:
- Keys are the exact subtasks.
- Values are EXACT tool names from the list above.
No explanations, no extra text.

Subtasks:
{json.dumps(subtasks, indent=2)}

Now return ONLY valid JSON:
"""

    raw = client.chat(prompt)

    # Try strict JSON parsing
    try:
        return json.loads(raw)
    except Exception:
        # Fallback: keyword heuristics per subtask, will be improved/extended later or use different method 
        def heuristic(sub: str) -> str:
            s = sub.lower()
            if any(w in s for w in ["calculate", "sum", "multiply", "add", "divide", "evaluate", "number"]):
                return "calculator"
            if any(w in s for w in ["wikipedia", "wiki", "article", "encyclopedia"]):
                return "wikipedia"
            if any(w in s for w in ["search", "google", "latest", "news", "find"]):
                return "web_search"
            if any(w in s for w in ["knowledge base", "vector", "embedding", "semantic"]):
                return "vector_search"
            return "unknown"

        return {sub: heuristic(sub) for sub in subtasks}
