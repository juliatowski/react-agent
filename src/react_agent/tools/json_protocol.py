from typing import Any, Dict, Optional


def tool_success(
    tool: str,
    subtask: str,
    result: Any,
    score: Optional[float] = None,
    meta: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:

    data = {
        "tool": tool,
        "subtask": subtask,
        "ok": True,
        "result": result,
        "error": None,
    }
    if score is not None:
        data["score"] = score
    if meta is not None:
        data["meta"] = meta
    return data


def tool_error(
    tool: str,
    subtask: str,
    error: str,
    meta: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:

    data = {
        "tool": tool,
        "subtask": subtask,
        "ok": False,
        "result": None,
        "error": error,
    }
    if meta is not None:
        data["meta"] = meta
    return data
