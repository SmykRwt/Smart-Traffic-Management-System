"""
Application Logger

Provides a single logger instance for the entire project.
"""

import logging


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

logger = logging.getLogger("AIVision")