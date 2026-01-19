from sympy import sympify, solve, symbols, pi, sin, cos, tan
from react_agent.llm_client import LLMClient
from react_agent.logging_config import log, vlog, time_block


class Calculator:
    """AI-assisted math calculator that extracts expressions from natural language."""

    name = "calculator"
    description = (
        "An AI-assisted calculator for numeric and symbolic expressions. "
        "It uses an LLM to convert natural-language math queries into clean expressions "
        "before evaluating them with SymPy."
    )

    def preprocess_with_ai(self, text: str) -> str | None:
        """
        Use an LLM to convert natural language into a pure math expression.
        Returns either a valid expression string or None.
        """
        prompt = f"""
Convert the following natural-language math request into a clean SymPy-friendly expression.

### Rules:
- Respond ONLY with the expression, nothing else.
- Do NOT include backticks or code fences.
- Use ** for powers (e.g., 5**2).
- Use pi, sin(), cos(), tan() for trig.
- For equations, return something like: solve(x**2 - 4, x)
- For numeric calculations, output the direct expression like: 25*18

### Input:
{text}

### Output (ONLY the math expression):
"""

        llm = LLMClient("qwen2.5")  # Or use get_model("calculator_preprocessor")
        raw = llm.chat(prompt).strip()

        vlog(f"[AI preprocess] raw output: {raw}")

        # clean accidental markdown formatting
        cleaned = raw.strip().replace("```", "").replace("`", "").strip()

        if cleaned:
            return cleaned

        return None

    def run(self, text: str) -> str:
        with time_block("calculator"):
            vlog(f"Calculator raw input: {text}")

            expr = self.preprocess_with_ai(text)

            if not expr:
                return "Error: The calculator could not understand the expression."

            vlog(f"Calculator extracted expression: {expr}")

            try:
                # Handle equations: "solve(....)"
                if expr.startswith("solve("):
                    result = eval(expr, {"solve": solve, "symbols": symbols, "pi": pi})
                    return f"Solution: {result}"

                # Normal math expressions
                result = sympify(expr).evalf()
                return str(result)

            except Exception as e:
                log(f"Calculator error evaluating '{expr}': {e}")
                return f"Error in calculator: {e}"
