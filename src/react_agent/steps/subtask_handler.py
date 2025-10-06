from typing import Dict, List, Tuple
from react_agent.steps.subtask_excecutor import execute_one_subtask
from react_agent.tools import TOOLS
from react_agent.steps.subtask_evaluator import evaluate_subtask


def execute_subtasks(
    subtasks: List[str],
    tool_mapping: Dict[str, str],
    model: str = "qwen2.5",
) -> Dict[str, str]:
    """
    Run a list of subtasks sequentially, each with its assigned tool.
    """
    results: Dict[str, str] = {}

    for subtask in subtasks:
        tool_name = tool_mapping.get(subtask, "")
        result, score, ok = execute_one_subtask(
            subtask=subtask,
            tool_name=tool_name,
            previous_results=results,
            model=model,
        )
        results[subtask] = result

    return results

