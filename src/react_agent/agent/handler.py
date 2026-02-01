import json
from react_agent.agent.executor import execute_single_subtask
from react_agent.config.logging_config import log, vlog, time_block


def execute_subtasks(subtasks_json, mapping_json, model: str) -> str:
    """
    Execute all subtasks according to a tool mapping.

    Inputs (can be JSON strings OR already-parsed dicts):
        subtasks_json: {"subtasks": [...]}  or that dict
        mapping_json:  {"mapping": {...}}   or that dict

    Output:
        JSON string: {"results": [ {...}, {...} ]}
    """

    with time_block("SUBTASK_HANDLER"):
        # Normalize subtasks
        if isinstance(subtasks_json, str):
            subtasks = json.loads(subtasks_json)["subtasks"]
        else:
            subtasks = subtasks_json["subtasks"]

        # Normalize mapping
        if isinstance(mapping_json, str):
            mapping = json.loads(mapping_json)["mapping"]
        else:
            mapping = mapping_json["mapping"]

        results = []

        for subtask in subtasks:
            tool_name = mapping.get(subtask)
            log(f"Handling subtask='{subtask}' with tool={tool_name}")

            # Use the plain API of execute_single_subtask (returns dict)
            result = execute_single_subtask(
                subtask=subtask,
                tool_name=tool_name,
                model=model,
            )
            results.append(result)

        result_json = json.dumps({"results": results})
        vlog(f"SUBTASK_HANDLER output: {result_json}")
        return result_json
