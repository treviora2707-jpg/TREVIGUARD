r"""
TREVIORA AI DEFENDER - Security Logger
Strictly logs to D:\projects\antivirus\data\logs\defender.log
"""
import logging
import sys
from logging.handlers import RotatingFileHandler
from pathlib import Path
from treviora_defender.config.constants import LOGS_DIR

_logger = None

def get_logger():
    global _logger
    if _logger is not None:
        return _logger

    LOGS_DIR.mkdir(parents=True, exist_ok=True)
    log_file = LOGS_DIR / "defender.log"

    _logger = logging.getLogger("TrevioraDefender")
    _logger.setLevel(logging.DEBUG)

    # Avoid adding duplicate handlers if re-called
    if not _logger.handlers:
        # File handler (10 MB max, 5 backups)
        file_handler = RotatingFileHandler(
            str(log_file), maxBytes=10 * 1024 * 1024, backupCount=5, encoding="utf-8"
        )
        file_fmt = logging.Formatter(
            "%(asctime)s [%(levelname)s] [%(name)s:%(threadName)s] %(message)s"
        )
        file_handler.setFormatter(file_fmt)
        file_handler.setLevel(logging.INFO)
        _logger.addHandler(file_handler)

        # Console handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_fmt = logging.Formatter("[%(levelname)s] %(message)s")
        console_handler.setFormatter(console_fmt)
        console_handler.setLevel(logging.INFO)
        _logger.addHandler(console_handler)

    return _logger
