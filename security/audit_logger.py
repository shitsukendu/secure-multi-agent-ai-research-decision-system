import logging
from pathlib import Path


# =========================================================
# LOG DIRECTORY
# =========================================================

LOG_DIR = Path("logs")

LOG_DIR.mkdir(
    parents=True,
    exist_ok=True
)


# =========================================================
# SECURITY LOGGER
# =========================================================

logger = logging.getLogger(
    "security_audit"
)

logger.setLevel(
    logging.INFO
)


# Prevent duplicate handlers
if not logger.handlers:

    file_handler = logging.FileHandler(
        LOG_DIR / "security.log",
        encoding="utf-8"
    )

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(message)s"
    )

    file_handler.setFormatter(
        formatter
    )

    logger.addHandler(
        file_handler
    )


# =========================================================
# AUDIT EVENT
# =========================================================

def log_security_event(
    event: str,
    details: str = ""
):
    """
    Record a security-related event.
    """

    message = event

    if details:
        message += f" | {details}"

    logger.info(message)