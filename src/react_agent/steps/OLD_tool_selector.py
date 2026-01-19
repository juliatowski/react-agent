import json
from typing import Dict, List
from react_agent.tools import list_tools
from react_agent.llm_client import LLMClient
from react_agent.logging_config import log, vlog, time_block


def assign_tools_to_subtasks(subtasks: List[str], model: str = "qwen2.5") -> Dict[str, str | None]:
    """
    Decide which tool to use for each subtask.

    Behaviour:
      - For each subtask, evaluate ALL tools.
      - Ask the LLM for a score between 0.0 and 1.0 for how well the tool fits.
      - Pick the tool with the highest score.
      - If all scores are 0.0 or evaluation fails, return None for that subtask.

    Input:
      subtasks: list of subtask strings

    Output:
      mapping: dict {subtask: best_tool_name or None}
    """

    with time_block("TOOL_SELECTOR"):
        client = LLMClient(model)
        tools = list_tools()

        if not tools:
            log("TOOL_SELECTOR: no tools available")
            return {subtask: None for subtask in subtasks}

        tool_infos = [(t.name, t.description) for t in tools]
        vlog(f"TOOL_SELECTOR available tools: {[name for name, _ in tool_infos]}")

        mapping: Dict[str, str | None] = {}

        for subtask in subtasks:
            vlog(f"TOOL_SELECTOR evaluating subtask: {subtask}")
            scores_for_subtask: Dict[str, float] = {}

            for tool_name, tool_desc in tool_infos:
                prompt = f"""
You are evaluating how suitable a tool is for a subtask.

Subtask:
"{subtask}"

Candidate tool:
Name: {tool_name}
Description: {tool_desc}

On a scale from 0.0 to 1.0, how suitable is this tool to solve the subtask?

Respond ONLY with valid JSON of the form:
{{
  "tool": "{tool_name}",
  "score": <float between 0.0 and 1.0>
}}
"""
                raw = client.chat(prompt)

                try:
                    parsed = json.loads(raw)
                    score = float(parsed.get("score", 0.0))
                    score = max(0.0, min(1.0, score))  # clamp to [0.0, 1.0]
                except Exception:
                    score = 0.0

                scores_for_subtask[tool_name] = score
                vlog(f"Score for tool='{tool_name}' on subtask='{subtask}': {score}")

            # pick best tool by score
            if scores_for_subtask:
                best_tool = max(scores_for_subtask, key=scores_for_subtask.get)
                best_score = scores_for_subtask[best_tool]
                # if all scores are 0.0, treat as no suitable tool
                if best_score == 0.0:
                    best_tool_name: str | None = None
                else:
                    best_tool_name = best_tool
                log(f"Best tool for subtask='{subtask}' → {best_tool_name} (score={best_score})")
            else:
                best_tool_name = None

            mapping[subtask] = best_tool_name

        vlog(f"TOOL_SELECTOR mapping: {mapping}")
        return mapping
