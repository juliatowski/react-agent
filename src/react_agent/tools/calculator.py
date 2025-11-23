from sympy import sympify, solve, symbols, pi, sin
from react_agent.logging_config import log, vlog, time_block  # <-- add this

class Calculator:
    """Simple calculator tool for evaluating math expressions """
    name = "calculator"
    description = "Perform arithmetic calculations like addition, multiplication, etc."

    def run(self, expression: str) -> str:
        with time_block("calculator"):
            vlog(f"Calculator input: {expression}")
            try:
                result = sympify(expression).evalf()
                vlog(f"Calculator result: {result}")
                return str(result)
            except Exception as e:
                log(f"Calculator error: {e}")
                return f"Error in calculator: {e}"
