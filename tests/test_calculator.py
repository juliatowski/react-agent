import pytest
from react_agent.tools.calculator import Calculator


def test_calculator_basic_operations():
    calc = Calculator()
    assert calc.run("2+2") == "4"
    assert calc.run("10/2") == "5.0"
    assert calc.run("3*7") == "21"


def test_calculator_invalid_expression_returns_error():
    calc = Calculator()
    result = calc.run("2+++")
    assert result.startswith("Error in calculator:")
