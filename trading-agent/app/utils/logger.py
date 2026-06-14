"""
Logging Module for XAUUSD Automated Trading System.
Provides structured logging to both console and a rotating file.
"""

import os
import sys
import logging
from logging.handlers import RotatingFileHandler
from app.utils.config import settings, BASE_DIR

# Ensure logs directory exists
LOGS_DIR = os.path.join(BASE_DIR, "logs")
os.makedirs(LOGS_DIR, exist_ok=True)
LOG_FILE_PATH = os.path.join(LOGS_DIR, "trading_agent.log")

# Define log formatters
CONSOLE_FORMAT = "%(asctime)s | %(levelname)-8s | %(name)s:%(funcName)s:%(lineno)d - %(message)s"
FILE_FORMAT = "%(asctime)s | %(levelname)-8s | %(name)s:%(funcName)s:%(lineno)d - %(message)s"


def setup_logger(name: str = "trading_agent") -> logging.Logger:
    """
    Sets up a logger with handlers for console and rotating file output.
    
    Args:
        name: Name of the logger (typically __name__)
        
    Returns:
        logging.Logger: Configured logger instance
    """
    logger = logging.getLogger(name)
    
    # Avoid duplicate handlers if setup_logger is called multiple times for the same logger name
    if logger.handlers:
        return logger

    # Determine logging level
    log_level = logging.DEBUG if settings.DEBUG else logging.INFO
    logger.setLevel(log_level)
    logger.propagate = False

    # Console Handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(log_level)
    console_formatter = logging.Formatter(CONSOLE_FORMAT)
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)

    # Rotating File Handler (Max 10MB per file, keeping 5 backup files)
    file_handler = RotatingFileHandler(
        filename=LOG_FILE_PATH,
        maxBytes=10 * 1024 * 1024,  # 10 MB
        backupCount=5,
        encoding="utf-8"
    )
    file_handler.setLevel(logging.DEBUG)  # Keep file logging detailed
    file_formatter = logging.Formatter(FILE_FORMAT)
    file_handler.setFormatter(file_formatter)
    logger.addHandler(file_handler)

    # Configure external library loggers to be less verbose
    logging.getLogger("urllib3").setLevel(logging.WARNING)
    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.getLogger("sqlalchemy").setLevel(logging.WARNING)
    logging.getLogger("uvicorn").setLevel(logging.INFO)
    logging.getLogger("fastapi").setLevel(logging.INFO)

    return logger


# Default application-wide logger
app_logger = setup_logger("trading_agent")
