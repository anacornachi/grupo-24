import logging
import os
from typing import Optional

from dotenv import load_dotenv

load_dotenv()


def get_logger(name: str) -> logging.Logger:
    """
    Returns a configured logger instance with a standard format.
    """
    logger = logging.getLogger(name)

    if not logger.handlers:
        logger.setLevel(logging.INFO)

        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            "[%(asctime)s] [%(name)s] [%(levelname)s] %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    return logger


def get_env_var(key: str, default: Optional[str] = None, required: bool = False) -> str:
    """
    Safely get an environment variable.

    :param key: Environment variable name.
    :param default: Default value if not found.
    :param required: If True, raises an error when variable is missing.
    """
    value = os.getenv(key, default)

    if required and value is None:
        raise RuntimeError(f"Environment variable '{key}' is required but not set.")

    return value
