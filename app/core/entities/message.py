"""Message Entity Module."""

from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Any


@dataclass(frozen=True)
class Message:
    """Represents a discrete communication unit in the JARVIS system.

    Attributes:
        id: Unique identifier for the message.
        role: The role of the message sender (e.g., user, assistant, system, tool).
        content: The text content of the message.
        sender_id: Unique identifier of the sender (agent id or 'user').
        recipient_id: Optional unique identifier of the recipient agent.
        timestamp: Creation datetime of the message.
        metadata: Extensible dictionary of contextual values or metrics.
    """

    id: str
    role: str
    content: str
    sender_id: str
    recipient_id: str | None = None
    timestamp: datetime = field(default_factory=lambda: datetime.now(UTC))
    metadata: dict[str, Any] = field(default_factory=dict)
