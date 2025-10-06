from react_agent.llm_client import LLMClient
from react_agent.tools.calculator import Calculator


class CalculatorAdapter:
    """
    Adapter for the Calculator tool.
    Uses an LLM to extract a math expression from a subtask,
    then evaluates it with the Calculator.
    """

    name = "calculator"
    description = "Extract math expressions from tasks and evaluate them."

    def __init__(self, model: str = "qwen2.5"):
        self.model = model
        self.client = LLMClient(model)
        self.calculator = Calculator()

    def run(self, subtask: str) -> str:
        """
        Extract a math expression from the subtask with the LLM,
        then evaluate it with the Calculator.
        """
        instruction = (
            "You are a math expression extractor.\n"
            "Your job is to read a natural language task and return only the equivalent "
            "math expression in valid Python/Sympy syntax.\n\n"
            "Rules:\n"
            "- Output ONLY the expression, nothing else.\n"
            "- Use standard operators: +, -, *, /, ** for powers.\n"
            "- For square roots or nth roots, use sqrt() or **(1/n).\n"
            "- For trigonometry, use sin(), cos(), tan() with arguments in radians.\n"
            "- For logarithms, use log(x) for natural log, log(x,10) for base-10.\n"
            "- For constants, use pi and e.\n"
            "- Do not include explanations, text, or units — only the pure expression.\n\n"
            f"Task: {subtask}"
        )

        expression = self.client.chat(instruction).strip()
        return self.calculator.run(expression)
