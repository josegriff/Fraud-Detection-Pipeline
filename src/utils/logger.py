from loguru import logger
from pathlib import Path

LOG_PATH = Path("logs/pipeline.log")
LOG_PATH.mkdir(exist_ok=True)

logger.add(
    LOG_PATH / "pipeline.log", rotation="1 MB",
    retention="7 days", compression="zip")

__all__ = ["logger"]
