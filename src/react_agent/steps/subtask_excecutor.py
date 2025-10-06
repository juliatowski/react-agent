
from typing import Dict, Tuple
from react_agent.steps.subtask_evaluator import evaluate_subtask
from react_agent.tools import TOOLS


def execute_one_subtask(
    subtask: str,
    tool_name: str,
    previous_results: Dict[str, str],
    model: str = "qwen2.5",
    threshold: float = 0.7,
    max_retries: int = 2,
) -> Tuple[str, float, bool]:
    """
    Execute a single subtask with its tool, optionally using previous results as context.

    Args:
        subtask: the subtask string.
        tool_name: which tool to use (key from TOOLS).
        previous_results: mapping of earlier subtasks -> results.
        model: LLM used for evaluation.
        threshold: minimum score for acceptance.
        max_retries: max retries before giving up.

    Returns:
        (final_result, score, is_correct)
    """
    tool = TOOLS.get(tool_name)
    if tool is None:
        return (f"No suitable tool found for: {subtask}", 0.0, False)

    # Build input: include previous results if available
    if previous_results:
        context = "\n".join(f"{t}: {r}" for t, r in previous_results.items())
        tool_input = f"Context:\n{context}\n\nTask: {subtask}"
    else:
        tool_input = subtask

    attempt = 0
    final_result, final_score, is_correct = "", 0.0, False

    while attempt <= max_retries:
        attempt += 1
        try:
            raw_result = tool.run(tool_input)
        except Exception as e:
            return (f"Error running tool {tool_name}: {e}", 0.0, False)

        evaluated_result, score, ok = evaluate_subtask(subtask, raw_result, model=model)
        final_result, final_score, is_correct = evaluated_result, score, ok

        if is_correct and score >= threshold:
            break  # accept result

    return (final_result, final_score, is_correct)

