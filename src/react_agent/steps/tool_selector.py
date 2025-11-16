import json
from typing import List
from react_agent.tools import list_tools
from react_agent.llm_client import LLMClient


def assign_tools_to_subtasks(subtasks_json: str, model: str = "qwen2.5") -> str:
    """
    JSON-only version.

    Input:
        subtasks_json = {"subtasks": [...]}

    Output:
        JSON string: {"mapping": {subtask: tool_name or null}}
    """

    subtasks = json.loads(subtasks_json)["subtasks"]

    client = LLMClient(model)
    available = list_tools()

    tools_descr = "\n".join(f"- {t.name}: {t.description}" for t in available)
    tool_names = [t.name.lower() for t in available]

    mapping = {}

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

        mapping[subtask] = choice if choice in tool_names else None

    return json.dumps({"mapping": mapping})
