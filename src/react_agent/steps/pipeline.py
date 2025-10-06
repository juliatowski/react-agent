from react_agent.steps.subtask_splitter import split_into_subtasks
from react_agent.steps.tool_selector import assign_tools_to_subtasks
from react_agent.steps.subtask_handler import execute_subtasks  
from react_agent.steps.final_answer import synthesize_final_answer


def react_pipeline(original_prompt: str, model: str = "qwen2.5") -> str:
    """
    Full ReAct-inspired pipeline:
    1. Split into subtasks
    2. Assign tools
    3. Execute subtasks sequentially 
    4. Synthesize final answer
    """
    #takes model as an argument for flexibility and potentially speeding up the excecution time

    #Step 1: Split into subtasks
    subtasks = split_into_subtasks(original_prompt, model=model)
    #Step 2: To each subtask assign the most suitable tool
    tool_mapping = assign_tools_to_subtasks(subtasks, model=model)
    #Step 3: Execute each subtask sequentially, taking previous results into account
    results = execute_subtasks(subtasks, tool_mapping, model=model)
    #Step 4: Synthesize final answer from all results
    return synthesize_final_answer(original_prompt, results, model=model)

