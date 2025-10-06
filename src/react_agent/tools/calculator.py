from sympy import sympify, solve, symbols, pi, sin

class Calculator:
    """Simple calculator tool for evaluating math expressions """
    name = "calculator"
    description = "Perform arithmetic calculations like addition, multiplication, etc."

    def run(self, expression: str) -> str:
        try:
            result = sympify(expression).evalf()
            return str(result)
        except Exception as e:
            return f"Error in calculator: {e}"
