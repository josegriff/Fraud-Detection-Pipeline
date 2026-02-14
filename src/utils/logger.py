"""
This script configures and initializes the centralized logging system for the ETL pipeline:
1. Uses loguru for simple and powerful logging
2. Creates a logs directory if needed
3. Writes logs to pipeline.log with automatic rotation (1 MB) and retention (7 days)
4. Compresses old logs with zip
5. Exports the configured logger for use across the project
"""

from loguru import logger
from pathlib import Path

LOG_PATH = Path("logs/pipeline.log")
LOG_PATH.mkdir(exist_ok=True)

logger.add(
    LOG_PATH / "pipeline.log", 
    rotation="1 MB",            # New file every time log reaches 1 megabyte
    retention="7 days",         # Delete files older than 7 days
    compression="zip")          # Compress old rotated files to save space

__all__ = ["logger"]
