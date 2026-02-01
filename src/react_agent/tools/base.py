from __future__ import annotations
from react_agent.config.logging_config import log, vlog, time_block


from abc import ABC, abstractmethod
from typing import Any, Dict


class BaseTool(ABC):
    """
    Base interface for all tools.

    Every tool must define:
      - name (unique identifier used in prompts / plans)
      - description (used for tool selection / prompting)
      - run(...) method that returns a string result
    """

    name: str
    description: str

    def __init__(self, name: str | None = None, description: str | None = None) -> None:
        if name is not None:
            self.name = name
        if description is not None:
            self.description = description

    @abstractmethod
    def run(self, *args: Any, **kwargs: Any) -> str:  # pragma: no cover - interface
        """
        Execute the tool. Signatures are free-form, but callers should
        always pass arguments via kwargs in the pipeline.
        """
        raise NotImplementedError

    def to_metadata(self) -> Dict[str, str]:
        """
        Minimal metadata for LLM prompting and tool selection.
        """
        return {
            "name": self.name,
            "description": self.description,
        }
        vlog(f"Tool metadata: {meta}")

