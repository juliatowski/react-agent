from typing import Dict, List
from react_agent.steps.subtask_excecutor import execute_single_subtask


def execute_subtasks(
    subtasks: List[str],
    tool_mapping: Dict[str, str],
    model: str
) -> List[dict]:
    """
    Execute each subtask sequentially.
    Returns a list of JSON dictionaries.
    """

    results = []

    for subtask in subtasks:
        tool_name = tool_mapping.get(subtask)

        result = execute_single_subtask(
            subtask=subtask,
            tool_name=tool_name,
            model=model
        )

        results.append(result)

    return results
