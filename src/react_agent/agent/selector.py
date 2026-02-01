import json
from typing import Dict, List, Any
from react_agent.tools import list_tools
from react_agent.llm.llm_client import LLMClient
from react_agent.config.logging_config import log, vlog, time_block
from react_agent.config.logging_config import set_logging



def assign_tools_to_subtasks(subtasks: List[str], model: str = "qwen2.5") -> Dict[str, str | None]:
    """
      - Run the subtask with all tools.
      - Collect outputs from every tool.
      - Log all tool outputs (full).
      - Log available tools list.
      - Ask an LLM evaluator which output is best.
      - Choose the best-scoring tool.
    """

    with time_block("TOOL_SELECTOR"):
        print("hello")
        tools = list_tools()
        if not tools:
            log("TOOL_SELECTOR: no tools available")
            return {s: None for s in subtasks}

        # Log available tools
        log("\n=== AVAILABLE TOOLS ===")
        for t in tools:
            log(f"- {t.name}: {t.description}")
        log("========================\n")

        mapping = {}
        evaluator = LLMClient(model)

        for subtask in subtasks:
            log(f"\n\n===============================")
            log(f"Evaluating Subtask:\n{subtask}")
            log("===============================\n")

            tool_outputs = {}

            # 1) RUN ALL TOOLS
            for tool in tools:
                try:
                    out = tool.runner(subtask)
                except Exception as e:
                    out = f"[ERROR running {tool.name}: {e}]"


                # store full output
                tool_outputs[tool.name] = out

                # log full output
                log(f"Full Output from {tool.name}:\n{out}\n")
                log("----------------------------------------")

            # 2) LET AI EVALUATE ALL OUTPUTS
            best_tool = evaluate_tool_outputs(subtask, tool_outputs, evaluator)

            log(f"\n📌 BEST TOOL for '{subtask}': {best_tool}\n")
            mapping[subtask] = best_tool

        return mapping


def evaluate_tool_outputs(subtask: str, outputs: Dict[str, str], evaluator: LLMClient) -> str | None:
    """
    Ask the LLM to judge all tool outputs and pick the best one.
    Returns tool_name or None.
    """

    formatted = json.dumps(outputs, indent=2)

    prompt = f"""
You are evaluating which tool produced the best answer for a subtask.

### Subtask
{subtask}

### Tool Outputs
{formatted}

### Instructions
For each tool:
- Consider correctness, usefulness, completeness, and relevance.
- Score each output 0.0–1.0.

Respond with STRICT JSON:
{{
  "winner": "<tool name or null>",
  "scores": {{
      "<tool>": float,
      "<tool>": float
  }}
}}
"""

    # Log the evaluator prompt (full)
    vlog("\n[EVALUATOR PROMPT — FULL]\n" + prompt + "\n")

    # Call evaluator LLM
    raw = evaluator.chat(prompt)

    # Log raw evaluator output (full)
    log("\n[EVALUATOR RAW OUTPUT — FULL]")
    log(raw)
    log("====================================\n")

    # Parse JSON
    try:
        parsed = json.loads(raw)

        #Log parsed result
        log(f"[EVALUATOR PARSED] Winner = {parsed.get('winner')}")
        log(f"[Scores] {parsed.get('scores')}\n")

        return parsed.get("winner", None)

    except Exception:
        log(f"[EVALUATOR JSON PARSE FAILED] Raw output was:\n{raw}\n")
        return None
