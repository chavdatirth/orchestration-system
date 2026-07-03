"""Base and In-memory Storage Adapters."""

import uuid
from typing import Any

from app.use_cases.ports import MemoryPort


class InMemoryMemoryAdapter(MemoryPort):
    """An in-memory simulated database for storing agent memories.

    Implements MemoryPort.
    """

    def __init__(self) -> None:
        """Initialize empty database dictionary."""
        self._store: dict[str, dict[str, Any]] = {}

    def save(self, content: str, metadata: dict[str, Any]) -> str:
        """Save text content in dictionary store.

        Args:
            content: Information text.
            metadata: Associated dictionary parameters.

        Returns:
            The primary key string identifier of the stored record.
        """
        record_id = str(uuid.uuid4())
        self._store[record_id] = {"content": content, "metadata": metadata}
        return record_id

    def search(self, query: str, limit: int = 5) -> list[dict[str, Any]]:
        """Search contents using exact or substring matching.

        Args:
            query: Term query criteria.
            limit: Return limit.

        Returns:
            Matched results from store.
        """
        results: list[dict[str, Any]] = []
        for record_id, record in self._store.items():
            if query.lower() in record["content"].lower():
                results.append({"id": record_id, **record})
            if len(results) >= limit:
                break
        return results
