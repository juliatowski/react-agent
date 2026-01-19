# Config for all LLM models used in the React Agent framework
# Global default model used everywhere unless explicitly overridden
DEFAULT_MODEL = "llama3.2:1b"


# Optional per-component model overrides
COMPONENT_MODELS = {
    "splitter": None,        
    "evaluator": None,       
    "pipeline": "llama3.2:1b",
    "final_answer": None,
    "tool_selector": None,
}

def get_model(component: str = None) -> str:
    """
    Returns the LLM model to use for a given component.
    Falls back to DEFAULT_MODEL if no override exists.
    """
    if component and component in COMPONENT_MODELS and COMPONENT_MODELS[component]:
        return COMPONENT_MODELS[component]
    return DEFAULT_MODEL
