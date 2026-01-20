from react_agent.llm_client import LLMClient

def test_chat_returns_answer():
    client = LLMClient(model="llama3")  # Change Model 
    answer = client.chat("What is 2+2?")
    print(answer)
    assert isinstance(answer, str)
    assert len(answer) > 0
