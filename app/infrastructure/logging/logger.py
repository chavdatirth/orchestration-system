"""Logging configuration setup."""

import logging
from pathlib import Path

from app.infrastructure.config.loader import LoggingConfig


def setup_logger(config: LoggingConfig, logger_name: str | None = None) -> logging.Logger:
    """Setup and configure system loggers.

    Args:
        config: Logging configuration parameters.
        logger_name: Name of the logger to retrieve/setup.

    Returns:
        Configured logger instance.
    """
    logger = logging.getLogger(logger_name or "JARVIS")
    logger.setLevel(config.level)

    # Prevent duplicating handlers
    if not logger.handlers:
        formatter = logging.Formatter(config.format)

        # Stream Handler (Stdout)
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

        # File Handler if enabled
        if config.file_logging:
            log_file = Path(config.file_path)
            log_file.parent.mkdir(parents=True, exist_ok=True)
            file_handler = logging.FileHandler(log_file, encoding="utf-8")
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)

    return logger
