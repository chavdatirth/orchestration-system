"""Memory Entity Module."""

from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Any


@dataclass(frozen=True)
class MemorySnippet:
    """Represents a discrete memory block, such as an observation or a past interaction.

    Attributes:
        id: Unique identifier for the memory block.
        content: The text content of the memory.
        timestamp: Time when this memory was stored/observed.
        importance: Score indicating the relevance or importance of the memory.
        metadata: Associated contextual flags or vector embedding indices.
    """

    id: str
    content: str
    timestamp: datetime = field(default_factory=lambda: datetime.now(UTC))
    importance: float = 1.0
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class Session:
    """Represents an active interactive session maintaining historical context.

    Attributes:
        session_id: Unique identifier for the session.
        created_at: Time when the session was initialized.
        memory_snippets: History or observations retrieved for this session.
        metadata: Metadata detailing active participants, tokens, etc.
    """

    session_id: str
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    memory_snippets: list[MemorySnippet] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)
