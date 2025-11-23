# src/react_agent/steps/pipeline.py

from react_agent.steps.subtask_splitter import split_into_subtasks
from react_agent.steps.tool_selector import assign_tools_to_subtasks
from react_agent.steps.subtask_handler import execute_subtasks
from react_agent.steps.final_answer import synthesize_final_answer

from react_agent.logging_config import log, vlog, time_block


def react_pipeline(original_prompt: str, model: str = "qwen2.5") -> str:
    """
    Full ReAct-inspired pipeline:
      1. Split user prompt into subtasks
      2. Select the best tool for each subtask
      3. Execute tools through the registry
      4. Combine all results into a final answer
    """

    with time_block("SUBTASK_SPLITTER"):
        subtasks = split_into_subtasks(original_prompt, model=model)
        vlog(f"subtasks = {subtasks}")

    with time_block("TOOL_SELECTOR"):
        tool_mapping = assign_tools_to_subtasks(subtasks, model=model)
        vlog(f"tool_mapping = {tool_mapping}")

    with time_block("SUBTASK_EXECUTION"):
        results = execute_subtasks(subtasks, tool_mapping, model=model)
        vlog(f"results = {results}")

    with time_block("FINAL_ANSWER"):
        final_answer = synthesize_final_answer(original_prompt, results, model=model)

    return final_answer
