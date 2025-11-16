from react_agent.tools import get_tool
from react_agent.tools.json_protocol import tool_error
from react_agent.llm_client import LLMClient


def execute_single_subtask(subtask: str, tool_name: str, model: str) -> dict:
    """
    Execute a single subtask.
       - If no tool is selected, fallback to LLM
       - Otherwise use registry to fetch tool and run it
    Returns a dictionary in the standard tool JSON format.
    """

    # Case 1: No tool selected → fall back to LLM
    if not tool_name:
        client = LLMClient(model)
        reply = client.chat(subtask)
        return {
            "tool": "llm",
            "subtask": subtask,
            "ok": True,
            "result": reply,
            "error": None,
        }

    # Case 2: Tool selected, but not found in registry
    tool_spec = get_tool(tool_name)
    if tool_spec is None:
        return tool_error(tool_name, subtask, f"Tool '{tool_name}' not found.")

    # Case 3: Execute the tool
    try:
        return tool_spec.runner(subtask)
    except Exception as e:
        return tool_error(tool_name, subtask, str(e))
