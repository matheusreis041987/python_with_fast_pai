import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

# Garante que a pasta existe
Path("logs").mkdir(exist_ok=True)

formatter = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

file_handler = RotatingFileHandler(
    "logs/app.log",
    maxBytes=5_000_000,
    backupCount=3,
    encoding="utf-8"
)

file_handler.setFormatter(formatter)

logging.basicConfig(
    level=logging.INFO,
    handlers=[file_handler]
)

# Logs do SQLAlchemy
logging.getLogger("sqlalchemy.engine").setLevel(logging.INFO)

logger = logging.getLogger("api")