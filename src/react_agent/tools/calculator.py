from sympy import sympify, solve, symbols, pi, sin
from react_agent.logging_config import log, vlog, time_block  # <-- add this

class Calculator:
    """Simple calculator tool for evaluating math expressions """
    name = "calculator"
    description = (
        "A math calculator for solving numeric and symbolic expressions. "
        "Use this tool for arithmetic (+, -, *, /), powers, roots, algebraic expressions, "
        "fractions, equations, trigonometry (sin, cos, tan), logarithms, and constants like pi. "
        "The input must be a valid mathematical expression (e.g., '2 + 3*4', 'sin(pi/2)', "
        "'solve(x**2 - 4, x)'). "
        "Do NOT use this tool for general knowledge, definitions, research, or text processing. "
        "Only use it when the subtask requires a numeric calculation, symbolic math, algebra, "
        "or evaluating a formula."
    )

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
