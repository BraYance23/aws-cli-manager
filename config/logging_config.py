import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

def setup_logging() -> None:

    BASE_DIR = Path(__file__).parent.parent
    PATH_LOG = BASE_DIR/"logs"/"manager_aws.log"
    PATH_LOG.parent.mkdir(parents=True,exist_ok=True)
    
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        handlers=[
            RotatingFileHandler(
                PATH_LOG,
                maxBytes=1 * 1024 * 1024,
                backupCount = 3,
                encoding="utf-8"
            )
        ]
    )

    logging.getLogger("botocore").setLevel(logging.WARNING)
    logging.getLogger("boto3").setLevel(logging.WARNING)
    logging.getLogger("urllib3").setLevel(logging.WARNING)


