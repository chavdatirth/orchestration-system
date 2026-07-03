"""Abstract Port Interfaces for Use Cases.

Defines the contracts that external interface adapters (LLMs, databases)
must satisfy to be used by the orchestration layer.
"""

from abc import ABC, abstractmethod
from typing import Any

from app.core.entities.message import Message


class LlmPort(ABC):
    """Abstract port for Large Language Model communication."""

    @abstractmethod
    def generate(
        self,
        messages: list[Message],
        system_prompt: str | None = None,
        temperature: float | None = None,
        max_tokens: int | None = None,
    ) -> Message:
        """Generate a response message from the LLM based on conversation history.

        Args:
            messages: Chronological conversation history.
            system_prompt: Directives that override or guide model persona.
            temperature: Sampling temperature.
            max_tokens: Limit on length of response.

        Returns:
            The generated response Message.
        """
        raise NotImplementedError


class MemoryPort(ABC):
    """Abstract port for memory persistence and search (e.g., Vector DB)."""

    @abstractmethod
    def save(self, content: str, metadata: dict[str, Any]) -> str:
        """Persist a memory snippet.

        Args:
            content: The text description of the memory.
            metadata: Custom attributes associated with the memory.

        Returns:
            The generated memory snippet ID.
        """
        raise NotImplementedError

    @abstractmethod
    def search(self, query: str, limit: int = 5) -> list[dict[str, Any]]:
        """Retrieve relevant memory snippets matching the query.

        Args:
            query: The search criteria or semantic query.
            limit: Maximum number of snippets to return.

        Returns:
            A list of retrieved memory dictionary records.
        """
        raise NotImplementedError
