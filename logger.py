"""
Logging configuration module for Autolauncher.
Sets up file and console logging with appropriate formatting and rotation.
Only active during development when DEBUG mode is enabled.
"""

import logging
from logging.handlers import RotatingFileHandler
import sys
from config import (
    LOG_FILE,
    LOG_LEVEL,
    CONSOLE_LOG_LEVEL,
    FILE_LOG_LEVEL,
    MAX_LOG_SIZE,
    BACKUP_COUNT,
    DEBUG_MODE
)


def setup_logger(name: str = "Autolauncher") -> logging.Logger:
    """
    Configure and return a logger instance with console and file handlers.
    
    Args:
        name: Name of the logger (typically the module name)
        
    Returns:
        Configured logger instance
    """
    # Create logger
    logger = logging.getLogger(name)
    logger.setLevel(LOG_LEVEL)
    
    # Avoid duplicate handlers if logger already exists
    if logger.handlers:
        return logger
    
    # Create formatters
    detailed_formatter = logging.Formatter(
        fmt='%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    simple_formatter = logging.Formatter(
        fmt='%(levelname)s - %(message)s'
    )
    
    # Console Handler - Always enabled for warnings and errors
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(CONSOLE_LOG_LEVEL)
    
    if DEBUG_MODE:
        console_handler.setFormatter(detailed_formatter)
    else:
        console_handler.setFormatter(simple_formatter)
    
    logger.addHandler(console_handler)
    
    # File Handler - Only enabled in DEBUG mode
    if DEBUG_MODE:
        try:
            file_handler = RotatingFileHandler(
                LOG_FILE,
                maxBytes=MAX_LOG_SIZE,
                backupCount=BACKUP_COUNT,
                encoding='utf-8'
            )
            file_handler.setLevel(FILE_LOG_LEVEL)
            file_handler.setFormatter(detailed_formatter)
            logger.addHandler(file_handler)
            
            logger.debug(f"Logging initialized - Debug mode: {DEBUG_MODE}")
            logger.debug(f"Log file: {LOG_FILE}")
        except Exception as e:
            logger.error(f"Failed to create file handler: {e}")
    
    return logger


# Create a default logger for the application
logger = setup_logger()


def get_logger(name: str) -> logging.Logger:
    """
    Get a logger instance for a specific module.
    
    Args:
        name: Name for the logger (typically __name__)
        
    Returns:
        Logger instance
    """
    return setup_logger(name)
