from react_agent.adapters.calculator_adapter import CalculatorAdapter


def test_calculator_adapter_integration():
    adapter = CalculatorAdapter(model="qwen2.5")
    subtask = "What is 12 * (3 + 2)?"
    result = adapter.run(subtask)


    assert isinstance(result, str)
    assert result.strip() != ""  # should not be empty
    # should look like a number (integer or float)
    assert result.replace(".", "", 1).isdigit()

    print(f"\nSubtask: {subtask}")
    print(f"Result: {result}")
