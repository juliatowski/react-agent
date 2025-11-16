import json
from react_agent.steps.subtask_splitter import split_into_subtasks
from react_agent.steps.tool_selector import assign_tools_to_subtasks
from react_agent.steps.subtask_handler import execute_subtasks
from react_agent.steps.final_answer import synthesize_final_answer


def react_pipeline(original_prompt: str, model: str = "qwen2.5") -> str:

    subtasks_json = split_into_subtasks(original_prompt, model=model)

    mapping_json = assign_tools_to_subtasks(subtasks_json, model=model)

    results_json = execute_subtasks(subtasks_json, mapping_json, model=model)

    final_answer = synthesize_final_answer(
        original_prompt,
        results_json,
        model=model,
    )

    return final_answer
