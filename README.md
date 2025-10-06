Preliminary README: 

# Bachelor Thesis – ReAct Agent

This repository contains the implementation for my bachelor thesis project on developing a ReAct-inspired agent for reasoning and tool use with local Large Language Models (LLMs).

## Quick Start

After activating your virtual environment, you can run the agent from the command line:

```bash

python -m react_agent "<Your Prompt>"

```

## Structure

```bash
src/
├── react_agent/
│   ├── __init__.py
│   ├── __main__.py          # Entry point of the project
│   ├── llm_client.py        # Handles local LLM calls via Ollama
│   ├── steps/               # Core ReAct framework (subtasks, execution, evaluation)
│   ├── tools/               # Built-in tools (calculator, web search, Wikipedia, vector search)
│   └── adapters/            # Interfaces/adapters for tool input and output
│
├── data/
│   └── ai_research.txt      # (Small) Example data for vector search
│
└── tests/                   # Tests for individual parts of the code 

```

# Testing

The tests folder contains integration and unit tests for individual components of the system.
These tests can be run independently, without executing the entire pipeline.

To run all tests (not recommended): 
```bash
pytest -q
````

To run a specific test file (for example, the web search tool tests):
```bash
pytest tests/test_websearch_tool.py -q
```


