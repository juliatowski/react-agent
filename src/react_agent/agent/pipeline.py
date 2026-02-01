import json

from react_agent.agent.splitter import split_into_subtasks
from react_agent.agent.selector import assign_tools_to_subtasks
from react_agent.agent.handler import execute_subtasks
from react_agent.agent.finalizer import synthesize_final_answer
from react_agent.config.llm_config import get_model


from react_agent.config.logging_config import log, vlog, time_block


def react_pipeline(original_prompt: str, model: str = None) -> str:
    
    #add option to parse model in main/promt?
    model = model or get_model("pipeline")

    """
    Full ReAct-inspired pipeline:
      1. Split user prompt into subtasks
      2. Select the best tool for each subtask
      3. Execute tools through the registry
      4. Combine all results into a final answer
    """

    # 1) SUBTASK SPLITTING
    with time_block("SUBTASK_SPLITTER"):
        raw_subtasks_json = split_into_subtasks(original_prompt, model=model)
        vlog(f"raw_subtasks_json = {raw_subtasks_json}")

        try:
            parsed = json.loads(raw_subtasks_json)
            subtasks = parsed.get("subtasks", [])
            if not isinstance(subtasks, list):
                log("[REACT_PIPELINE] 'subtasks' is not a list, falling back to single-step.")
                subtasks = [original_prompt]
        except json.JSONDecodeError as e:
            log(f"[REACT_PIPELINE] Failed to parse subtasks JSON: {e}. Falling back to single-step.")
            subtasks = [original_prompt]

        vlog(f"subtasks (list) = {subtasks}")



    # 2) TOOL SELECTION
    with time_block("TOOL_SELECTOR"):
        tool_mapping = assign_tools_to_subtasks(subtasks, model=model)
        vlog(f"tool_mapping (dict) = {tool_mapping}")

        # Handler expects JSON: {"mapping": {...}}
        mapping_json = json.dumps({"mapping": tool_mapping})

    # 3) SUBTASK EXECUTION
    with time_block("SUBTASK_EXECUTION"):
        # Handler expects JSON for subtasks: {"subtasks": [...]}
        results_json = execute_subtasks(raw_subtasks_json, mapping_json, model=model)
        vlog(f"results_json = {results_json}")

        try:
            results_parsed = json.loads(results_json)
            results = results_parsed.get("results", [])
        except json.JSONDecodeError as e:
            log(f"[REACT_PIPELINE] Failed to parse results JSON: {e}. Using empty results.")
            results = []

        vlog(f"results (list[dict]) = {results}")

    # 4) FINAL ANSWER
    with time_block("FINAL_ANSWER"):
        final_answer = synthesize_final_answer(original_prompt, results, model=model)

    return final_answer
