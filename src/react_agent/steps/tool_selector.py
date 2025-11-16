from typing import Dict, List
from react_agent.tools import list_tools
from react_agent.llm_client import LLMClient


def assign_tools_to_subtasks(subtasks: List[str], model: str = "qwen2.5"):
    """
    Decide which tool to use for each subtask.
    Uses the registry to access available tools.

    Returns:
      {subtask: tool_name or None}
    """

    client = LLMClient(model)
    available = list_tools()

    # Build tool descriptions for LLM ranking
    tools_descr = "\n".join(
        f"- {t.name}: {t.description}" for t in available
    )

    mapping: Dict[str, str] = {}

    for subtask in subtasks:
        prompt = f"""
You are a tool selector.

Available tools:
{tools_descr}

For the subtask below, choose the most appropriate tool by name.
If none fits, reply: none

Subtask: "{subtask}"
"""

        choice = client.chat(prompt).strip().lower()
        tool_names = [t.name.lower() for t in available]

        if choice in tool_names:
            mapping[subtask] = choice
        else:
            mapping[subtask] = None

    return mapping
