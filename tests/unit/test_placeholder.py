"""Unit tests verifying project setup, mock adapters, and configuration parsing."""

from pathlib import Path

import pytest
from pydantic import ValidationError

from app.adapters.llm.base import MockLlmAdapter
from app.adapters.memory.base import InMemoryMemoryAdapter
from app.core.entities.message import Message
from app.infrastructure.config.loader import Settings, load_settings


def test_mock_llm_adapter_generates_message(mock_llm_adapter: MockLlmAdapter) -> None:
    """Verify that MockLlmAdapter generates response messages."""
    result = mock_llm_adapter.generate([])
    assert isinstance(result, Message)
    assert result.content == "Mocked LLM Response"
    assert result.role == "assistant"


def test_in_memory_memory_adapter(in_memory_memory_adapter: InMemoryMemoryAdapter) -> None:
    """Verify that InMemoryMemoryAdapter correctly saves and searches for content."""
    adapter = in_memory_memory_adapter
    record_id = adapter.save(
        "JARVIS is an AI orchestration operating system.", {"category": "test"}
    )
    assert isinstance(record_id, str)
    assert len(record_id) > 0

    search_results = adapter.search("orchestration")
    assert len(search_results) == 1
    assert search_results[0]["id"] == record_id
    assert "AI orchestration" in search_results[0]["content"]

    empty_results = adapter.search("nonexistent")
    assert len(empty_results) == 0


def test_load_settings(test_settings: Settings) -> None:
    """Verify default configurations load properly from the workspace environment."""
    assert test_settings.app.name == "JARVIS"
    assert test_settings.logging.level in {"INFO", "DEBUG"}
    assert test_settings.llm.default_provider == "gemini"


def test_load_settings_override(tmp_path: Path) -> None:
    """Verify default configurations merge correctly with custom environment overrides."""
    base_env = tmp_path / "base.env"
    override_env = tmp_path / "override.env"

    base_env.write_text(
        "JARVIS_APP_NAME='Base'\nJARVIS_APP_ENV='production'\nJARVIS_LOGGING_LEVEL='INFO'\nJARVIS_LLM_TEMPERATURE=0.5",
        encoding="utf-8",
    )
    override_env.write_text(
        "JARVIS_APP_ENV='development'\nJARVIS_LOGGING_LEVEL='DEBUG'\nJARVIS_LLM_TEMPERATURE=0.7",
        encoding="utf-8",
    )

    settings = load_settings(
        env_name="development", base_env_path=base_env, override_env_path=override_env
    )
    assert settings.app.name == "Base"
    assert settings.app.env == "development"
    assert settings.logging.level == "DEBUG"
    assert settings.llm.temperature == 0.7


def test_invalid_temperature_raises_validation_error(tmp_path: Path) -> None:
    """Verify validator blocks invalid temperature configurations."""
    invalid_env = tmp_path / "invalid.env"
    invalid_env.write_text("JARVIS_LLM_TEMPERATURE=2.5", encoding="utf-8")

    with pytest.raises(ValidationError) as excinfo:
        load_settings(base_env_path=invalid_env)
    assert "Temperature must be between 0.0 and 2.0" in str(excinfo.value)


def test_invalid_max_tokens_raises_validation_error(tmp_path: Path) -> None:
    """Verify validator blocks negative max tokens values."""
    invalid_env = tmp_path / "invalid.env"
    invalid_env.write_text("JARVIS_LLM_MAX_TOKENS=-50", encoding="utf-8")

    with pytest.raises(ValidationError) as excinfo:
        load_settings(base_env_path=invalid_env)
    assert "Max tokens must be a positive integer" in str(excinfo.value)


def test_invalid_logging_level_raises_validation_error(tmp_path: Path) -> None:
    """Verify validator blocks unsupported logging levels."""
    invalid_env = tmp_path / "invalid.env"
    invalid_env.write_text("JARVIS_LOGGING_LEVEL='TRACE'", encoding="utf-8")

    with pytest.raises(ValidationError) as excinfo:
        load_settings(base_env_path=invalid_env)
    assert "Logging level must be one of" in str(excinfo.value)


def test_secret_api_key_masking(tmp_path: Path) -> None:
    """Verify that SecretStr API keys are masked when represented as strings."""
    secret_env = tmp_path / "secret.env"
    secret_env.write_text("JARVIS_GEMINI_API_KEY='super_secret_api_token'", encoding="utf-8")

    settings = load_settings(base_env_path=secret_env)
    assert settings.llm.gemini_api_key is not None
    assert settings.llm.gemini_api_key.get_secret_value() == "super_secret_api_token"
    # String representation must mask the value
    assert "super_secret_api_token" not in str(settings.llm.gemini_api_key)
    assert "**********" in str(settings.llm.gemini_api_key)
