import json
from react_agent.llm_client import LLMClient
from react_agent.tools import get_tool
from react_agent.tools.json_protocol import tool_error


def execute_single_subtask(subtask_json: str, tool_name: str, model: str) -> str:
    """
    JSON-only version.
    Input:
        subtask_json = {"subtask": "..."}
        tool_name = string or None
    Output:
        JSON string
    """

    subtask = json.loads(subtask_json)["subtask"]

    # Case 1 — no tool selected → LLM fallback
    if not tool_name:
        client = LLMClient(model)
        answer = client.chat(subtask)
        return json.dumps({
            "tool": "llm",
            "subtask": subtask,
            "ok": True,
            "result": answer,
            "error": None
        })

    # Case 2 — tool missing
    tool = get_tool(tool_name)
    if tool is None:
        return json.dumps(tool_error(tool_name, subtask, f"Tool '{tool_name}' not found."))

    # Case 3 — run tool
    try:
        result_dict = tool.runner(subtask)
        return json.dumps(result_dict)
    except Exception as e:
        return json.dumps(tool_error(tool_name, subtask, str(e)))
