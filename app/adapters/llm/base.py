"""Base and Mock LLM Adapters."""

from app.core.entities.message import Message
from app.use_cases.ports import LlmPort


class MockLlmAdapter(LlmPort):
    """A simulated LLM adapter for testing and initialization verification.

    Implements LlmPort.
    """

    def __init__(self, response_text: str = "Mocked LLM Response") -> None:
        """Initialize mock settings.

        Args:
            response_text: Text that this mock LLM should always return.
        """
        self._response_text = response_text

    def generate(
        self,
        messages: list[Message],
        system_prompt: str | None = None,
        temperature: float | None = None,
        max_tokens: int | None = None,
    ) -> Message:
        """Simulate LLM text generation.

        Args:
            messages: Conversation context.
            system_prompt: Guiding directives.
            temperature: Sampling parameters.
            max_tokens: Maximum token count.

        Returns:
            A pre-configured mock Message.
        """
        return Message(
            id="mock-msg-123",
            role="assistant",
            content=self._response_text,
            sender_id="mock-llm-agent",
        )
