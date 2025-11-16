import json
from react_agent.steps.subtask_excecutor import execute_single_subtask


def execute_subtasks(subtasks_json: str, mapping_json: str, model: str) -> str:
    """
    JSON-only version.

    Inputs:
        subtasks_json: {"subtasks": [...]}
        mapping_json:  {"mapping": {...}}

    Output:
        JSON string: {"results": [ {...}, {...} ]}
    """

    subtasks = json.loads(subtasks_json)["subtasks"]
    mapping = json.loads(mapping_json)["mapping"]

    results = []

    for subtask in subtasks:
        tool_name = mapping.get(subtask)
        result_json = execute_single_subtask(
            subtask_json=json.dumps({"subtask": subtask}),
            tool_name=tool_name,
            model=model
        )
        results.append(json.loads(result_json))

    return json.dumps({"results": results})
