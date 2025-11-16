Bachelor Thesis – ReAct Agent

This repository contains the implementation for my bachelor thesis project on developing a ReAct-inspired agent for reasoning and tool use with local Large Language Models (LLMs).

Quick Start

Follow these steps after cloning the repository.

1. Clone the repository
git clone https://github.com/juliatowski/react-agent.git
cd react-agent

2. Create and activate a virtual environment

macOS / Linux:

python3 -m venv venv
source venv/bin/activate


Windows (PowerShell):

python -m venv venv
venv\Scripts\Activate.ps1

3. Install dependencies
pip install -e .
pip install langchain langchain-community langchain-text-splitters langchain-ollama faiss-cpu wikipedia


Note: To use local LLMs, install Ollama: https://ollama.com

4. Run the agent
python -m react_agent "Your prompt here"


Example:

python -m react_agent "Summarize the history of AI"

Structure
src/
├── react_agent/
│   ├── __init__.py
│   ├── __main__.py          # Entry point of the project
│   ├── llm_client.py        # Handles local LLM calls via Ollama
│   ├── steps/               # Core ReAct framework (subtasks, execution, evaluation)
│   ├── tools/               # Built-in tools (calculator, web search, Wikipedia, vector search)
│       └── adapters/        # Interfaces/adapters for tool input and output
│
├── data/
│   └── ai_research.txt      # Example data for vector search
│
└── tests/                   # Tests for individual parts of the code

Testing

The tests folder contains integration and unit tests for individual components of the system. These tests can be run independently, without executing the entire pipeline.

Run all tests:

pytest -q


Run a specific test file:

pytest tests/test_websearch_tool.py -q
