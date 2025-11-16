# src/react_agent/steps/pipeline.py

from react_agent.steps.subtask_splitter import split_into_subtasks
from react_agent.steps.tool_selector import assign_tools_to_subtasks
from react_agent.steps.subtask_handler import execute_subtasks
from react_agent.steps.final_answer import synthesize_final_answer


def react_pipeline(original_prompt: str, model: str = "qwen2.5") -> str:
    """
    Full ReAct-inspired pipeline:
      1. Split user prompt into subtasks
      2. Select the best tool for each subtask
      3. Execute tools through the registry
      4. Combine all results into a final answer
    """

    subtasks = split_into_subtasks(original_prompt, model=model)

    tool_mapping = assign_tools_to_subtasks(subtasks, model=model)

    results = execute_subtasks(subtasks, tool_mapping, model=model)

    final_answer = synthesize_final_answer(original_prompt, results, model=model)

    return final_answer
