"""
Logging configuration for the application.
"""
import logging
import sys
from logging import Filter, Formatter, Logger, StreamHandler
from typing import Optional

from app.core.config import get_settings

settings = get_settings()

class BcryptWarningFilter(Filter):
    """
    Suppress noisy bcrypt/passlib warnings such as:
    - Using a pure-python bcrypt implementation
    - bcrypt rounds too low/high
    """

    SUPPRESSED_SUBSTRINGS = [
        "bcrypt",
        "Using a pure-python bcrypt backend",
        "password hashing cycle",
    ]

    def filter(self, record: logging.LogRecord) -> bool:
        message = record.getMessage().lower()

        # If any known noisy substring appears → suppress
        return not any(substring.lower() in message for substring in self.SUPPRESSED_SUBSTRINGS)


class ColoredFormatter(Formatter):
    """
    Custom formatter that adds colors to log levels for better readability.
    """

    # ANSI color codes
    COLORS = {
        "DEBUG": "\033[36m",  # Cyan
        "INFO": "\033[32m",  # Green
        "WARNING": "\033[33m",  # Yellow
        "ERROR": "\033[31m",  # Red
        "CRITICAL": "\033[35m",  # Magenta
    }
    RESET = "\033[0m"

    def format(self, record: logging.LogRecord) -> str:
        # Add color to levelname if outputting to terminal
        # Check both stdout and stderr since handlers can use either
        is_tty = (
            (hasattr(sys.stdout, "isatty") and sys.stdout.isatty())
            or (hasattr(sys.stderr, "isatty") and sys.stderr.isatty())
        )
        if is_tty:
            levelname = record.levelname
            color = self.COLORS.get(levelname, "")
            record.levelname = f"{color}{levelname}{self.RESET}"
        return super().format(record)


def setup_logging(log_level: Optional[str] = None) -> None:
    """
    Configure the application's logging system.

    Args:
        log_level: Optional log level override. If not provided, uses LOG_LEVEL from settings.
    """
    level = log_level or settings.LOG_LEVEL
    log_level_num = getattr(logging, level.upper(), logging.INFO)

    # Root logger configuration
    root_logger = logging.getLogger()
    root_logger.setLevel(log_level_num)

    # Remove existing handlers to avoid duplicates
    root_logger.handlers.clear()

    # Create console handler
    console_handler = StreamHandler(sys.stdout)
    console_handler.setLevel(log_level_num)

    # Create formatter
    if settings.APP_ENV == "dev":
        # More detailed format for development
        formatter = ColoredFormatter(
            fmt="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
    else:
        # Simpler format for production
        formatter = Formatter(
            fmt="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )

    console_handler.setFormatter(formatter)

    # Add bcrypt warning filter
    bcrypt_filter = BcryptWarningFilter()
    console_handler.addFilter(bcrypt_filter)

    # Add handler to root logger
    root_logger.addHandler(console_handler)

    # Configure third-party loggers
    configure_third_party_loggers(log_level_num)

    # Log the configuration
    logger = logging.getLogger(__name__)
    logger.info(f"Logging configured: level={level}, env={settings.APP_ENV}")


def configure_third_party_loggers(log_level: int) -> None:
    """
    Configure logging levels for third-party libraries.

    Args:
        log_level: The log level to use for third-party loggers.
    """
    # SQLAlchemy logging - remove existing handlers and propagate to root
    sqlalchemy_loggers = [
        "sqlalchemy.engine",
        "sqlalchemy.pool",
        "sqlalchemy.dialects",
        "sqlalchemy.orm",
    ]
    for logger_name in sqlalchemy_loggers:
        sqlalchemy_logger = logging.getLogger(logger_name)
        # Remove any existing handlers to prevent duplicate logs
        sqlalchemy_logger.handlers.clear()
        # Propagate to root logger so it uses our formatter
        sqlalchemy_logger.propagate = True
        if settings.LOG_SQL_QUERIES and logger_name == "sqlalchemy.engine":
            sqlalchemy_logger.setLevel(logging.INFO)
        else:
            sqlalchemy_logger.setLevel(logging.WARNING)

    # Uvicorn logging - remove handlers and propagate
    uvicorn_loggers = ["uvicorn", "uvicorn.access", "uvicorn.error"]
    for logger_name in uvicorn_loggers:
        uvicorn_logger = logging.getLogger(logger_name)
        uvicorn_logger.handlers.clear()
        uvicorn_logger.propagate = True
        uvicorn_logger.setLevel(log_level)

    # FastAPI logging
    fastapi_logger = logging.getLogger("fastapi")
    fastapi_logger.handlers.clear()
    fastapi_logger.propagate = True
    fastapi_logger.setLevel(log_level)



def get_logger(name: str) -> Logger:
    """
    Get a logger instance for a module.

    Args:
        name: The name of the logger (typically __name__ of the module).

    Returns:
        A configured Logger instance.
    """
    return logging.getLogger(name)

