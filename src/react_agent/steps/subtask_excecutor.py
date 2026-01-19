import json
from react_agent.llm_client import LLMClient
from react_agent.tools import get_tool
from react_agent.tools.json_protocol import tool_error
from react_agent.logging_config import log, vlog, time_block


def execute_single_subtask(subtask: str, tool_name: str, model: str) -> dict:
    """
    Execute a single subtask.
       - If no tool is selected, fallback to LLM
       - Otherwise use registry to fetch tool and run it
    Returns a dictionary in the standard tool JSON format.
    """
    
    with time_block("SUBTASK_EXECUTOR"):
        log(f"Executing subtask: '{subtask}' with tool={tool_name}")

        # Case 1: No tool selected → fall back to LLM
        if not tool_name:
            client = LLMClient(model)
            reply = client.chat(subtask)
            result = {
                "tool": "llm",
                "subtask": subtask,
                "ok": True,
                "result": reply,
                "error": None,
            }
            vlog(f"LLM fallback result: {result}")
            return result

        # Case 2: Tool selected, but not found in registry
        tool_spec = get_tool(tool_name)
        if tool_spec is None:
            err = tool_error(tool_name, subtask, f"Tool '{tool_name}' not found.")
            log(f"Tool not found: {tool_name}")
            return err

        # Case 3: Execute the tool
        try:
            result = tool_spec.runner(subtask)
            vlog(f"Tool '{tool_name}' result: {result}")
            return result
        except Exception as e:
            err = tool_error(tool_name, subtask, str(e))
            log(f"Error running tool '{tool_name}' on subtask '{subtask}': {e}")
            return err
