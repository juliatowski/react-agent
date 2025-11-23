import json
from react_agent.steps.subtask_excecutor import execute_single_subtask
from react_agent.logging_config import log, vlog, time_block


def execute_subtasks(subtasks_json: str, mapping_json: str, model: str) -> str:
    """
    JSON-only version.

    Inputs:
        subtasks_json: {"subtasks": [...]}
        mapping_json:  {"mapping": {...}}

    Output:
        JSON string: {"results": [ {...}, {...} ]}
    """

    with time_block("SUBTASK_HANDLER"):
        subtasks = json.loads(subtasks_json)["subtasks"]
        mapping = json.loads(mapping_json)["mapping"]

        results = []

        for subtask in subtasks:
            tool_name = mapping.get(subtask)
            log(f"Handling subtask='{subtask}' with tool={tool_name}")
            result_json = execute_single_subtask(
                subtask_json=json.dumps({"subtask": subtask}),
                tool_name=tool_name,
                model=model
            )
            results.append(json.loads(result_json))

        result = json.dumps({"results": results})
        vlog(f"SUBTASK_HANDLER output: {result}")
        return result
