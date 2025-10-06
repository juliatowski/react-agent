from react_agent.tools.calculator import Calculator
from react_agent.tools.websearch import WebSearch
from react_agent.tools.wikipedia import WikipediaTool
from react_agent.tools.vectorsearch import VectorSearch

TOOLS = {
    "calculator": Calculator(),
    "web_search": WebSearch(),
    "wikipedia": WikipediaTool(),
    "vector_search": VectorSearch(),
}
