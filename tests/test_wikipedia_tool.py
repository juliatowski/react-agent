from react_agent.tools.wikipedia import WikipediaTool


def test_wikipedia_tool_integration():
    tool = WikipediaTool()
    query = "GPT-3"
    result = tool.run(query, sentences=1)

    assert isinstance(result, str)
    assert result.strip() != ""
    assert "GPT" in result or "Wikipedia error" in result

    print(f"\nQuery: {query}\nResult: {result}")
