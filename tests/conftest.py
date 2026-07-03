"""Shared pytest fixtures."""

import pytest

from app.adapters.llm.base import MockLlmAdapter
from app.adapters.memory.base import InMemoryMemoryAdapter
from app.infrastructure.config.loader import Settings, load_settings


@pytest.fixture
def mock_llm_adapter() -> MockLlmAdapter:
    """Fixture returning MockLlmAdapter."""
    return MockLlmAdapter()


@pytest.fixture
def in_memory_memory_adapter() -> InMemoryMemoryAdapter:
    """Fixture returning InMemoryMemoryAdapter."""
    return InMemoryMemoryAdapter()


@pytest.fixture
def test_settings() -> Settings:
    """Fixture returning base Settings configuration."""
    return load_settings()
