"""Configuration loading and validation system using pydantic-settings."""

import os
from pathlib import Path

from pydantic import BaseModel, SecretStr, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class AppConfig(BaseModel):
    """Application general metadata configurations.

    Attributes:
        name: Name of the operating system instance.
        env: Target running environment ('development', 'production', 'test').
        debug: Toggles verbose tracebacks and debugging outputs.
        secret_key: Key used for cryptographic operations and session signatures.
    """

    name: str
    env: str
    debug: bool
    secret_key: str


class LlmConfig(BaseModel):
    """LLM client orchestration default configurations.

    Attributes:
        default_provider: Fallback API provider to use (e.g. 'gemini', 'openai').
        temperature: Creativity sampling parameter.
        max_tokens: Generated output length limit constraints.
        gemini_api_key: Secret api key for Google Gemini.
        openai_api_key: Secret api key for OpenAI.
        anthropic_api_key: Secret api key for Anthropic.
    """

    default_provider: str
    temperature: float
    max_tokens: int
    gemini_api_key: SecretStr | None = None
    openai_api_key: SecretStr | None = None
    anthropic_api_key: SecretStr | None = None


class VectorDbConfig(BaseModel):
    """Vector database connectivity parameters.

    Attributes:
        host: Endpoint domain/address hosting the vector search instance.
        port: Connection port of the vector service.
        collection: Target database partition name.
    """

    host: str
    port: int
    collection: str


class MemoryConfig(BaseModel):
    """Cognitive storage architecture parameters.

    Attributes:
        default_storage: Toggles storage backing ('in_memory' or 'vector_db').
        vector_db: Database connectivity credentials and endpoint details.
    """

    default_storage: str
    vector_db: VectorDbConfig


class LoggingConfig(BaseModel):
    """Logging thresholds and target telemetry options.

    Attributes:
        level: Minimum importance severity filter.
        format: Format string for log messages.
        file_logging: Toggles writing runtime logs onto files.
        file_path: Output logging path target.
    """

    level: str
    format: str
    file_logging: bool
    file_path: str


class Settings(BaseSettings):
    """Global configuration settings for the JARVIS operating system.

    Constructs and validates all sub-models (AppConfig, LlmConfig, MemoryConfig,
    LoggingConfig) by reading environment variables and .env configuration files.
    """

    # AppConfig fields loaded from env
    app_name: str = "JARVIS"
    app_env: str = "development"
    app_debug: bool = False
    app_secret_key: str = "replace_me_with_a_secure_random_key_in_production"

    # LlmConfig fields loaded from env
    llm_default_provider: str = "gemini"
    llm_temperature: float = 0.2
    llm_max_tokens: int = 4096
    gemini_api_key: SecretStr | None = None
    openai_api_key: SecretStr | None = None
    anthropic_api_key: SecretStr | None = None

    # MemoryConfig / VectorDbConfig fields loaded from env
    memory_default_storage: str = "in_memory"
    memory_vector_db_host: str = "localhost"
    memory_vector_db_port: int = 6333
    memory_vector_db_collection: str = "jarvis_memory"

    # LoggingConfig fields loaded from env
    logging_level: str = "INFO"
    logging_format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    logging_file_logging: bool = False
    logging_file_path: str = "logs/app.log"

    # Settings configurations matching env variables with prefix
    model_config = SettingsConfigDict(
        env_prefix="JARVIS_",
        extra="ignore",
    )

    # Validators
    @field_validator("llm_temperature")
    @classmethod
    def validate_temperature(cls, v: float) -> float:
        """Validate LLM temperature is within standard limits."""
        if not 0.0 <= v <= 2.0:
            raise ValueError("Temperature must be between 0.0 and 2.0")
        return v

    @field_validator("llm_max_tokens")
    @classmethod
    def validate_max_tokens(cls, v: int) -> int:
        """Validate LLM max tokens parameter is positive."""
        if v <= 0:
            raise ValueError("Max tokens must be a positive integer")
        return v

    @field_validator("logging_level")
    @classmethod
    def validate_logging_level(cls, v: str) -> str:
        """Validate logging level is a standard level string."""
        valid_levels = {"DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"}
        if v.upper() not in valid_levels:
            raise ValueError(f"Logging level must be one of {valid_levels}")
        return v.upper()

    # Properties to expose nested models to use cases and entities cleanly
    @property
    def app(self) -> AppConfig:
        """Expose validated general App configurations."""
        return AppConfig(
            name=self.app_name,
            env=self.app_env,
            debug=self.app_debug,
            secret_key=self.app_secret_key,
        )

    @property
    def llm(self) -> LlmConfig:
        """Expose validated LLM configurations."""
        return LlmConfig(
            default_provider=self.llm_default_provider,
            temperature=self.llm_temperature,
            max_tokens=self.llm_max_tokens,
            gemini_api_key=self.gemini_api_key,
            openai_api_key=self.openai_api_key,
            anthropic_api_key=self.anthropic_api_key,
        )

    @property
    def memory(self) -> MemoryConfig:
        """Expose validated storage Memory configurations."""
        return MemoryConfig(
            default_storage=self.memory_default_storage,
            vector_db=VectorDbConfig(
                host=self.memory_vector_db_host,
                port=self.memory_vector_db_port,
                collection=self.memory_vector_db_collection,
            ),
        )

    @property
    def logging(self) -> LoggingConfig:
        """Expose validated Telemetry Logging configurations."""
        return LoggingConfig(
            level=self.logging_level,
            format=self.logging_format,
            file_logging=self.logging_file_logging,
            file_path=self.logging_file_path,
        )


def load_settings(
    env_name: str | None = None,
    base_env_path: Path | None = None,
    override_env_path: Path | None = None,
) -> Settings:
    """Dynamic builder loading base settings and environment-specific overrides.

    Args:
        env_name: Override env target. If none, reads 'JARVIS_APP_ENV' or defaults to 'development'.
        base_env_path: Optional custom path to base .env file for testing.
        override_env_path: Optional custom path to environment override file for testing.

    Returns:
        Validated global Settings instance.
    """
    # 1. Determine env target name
    active_env = env_name
    if not active_env:
        # Check active system env or default to development
        active_env = os.getenv("JARVIS_APP_ENV", "development").lower()

    # 2. Compile order of dotenv configuration files to overlay
    env_files = []

    # Add base .env
    base_path = base_env_path or Path(".env")
    if base_path.exists():
        env_files.append(base_path)

    # Add environment specific .env.{env} file
    override_path = override_env_path or Path(f".env.{active_env}")
    if override_path.exists():
        env_files.append(override_path)

    # Convert list of paths to tuple of strings for Pydantic Settings builder compatibility
    env_file_paths = tuple(str(path) for path in env_files)

    return Settings(
        _env_file=env_file_paths,  # type: ignore[call-arg]
        _env_file_encoding="utf-8",
    )
