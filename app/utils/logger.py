import logging
import os

LOG_DIR = "logs"

os.makedirs(LOG_DIR, exist_ok=True)

logger = logging.getLogger("rag-assistant")

logger.setLevel(logging.INFO)

formatter = logging.Formatter(
    "%(asctime)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s"
)

# 控制台日志
console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)

# 文件日志
file_handler = logging.FileHandler(
    f"{LOG_DIR}/app.log",
    encoding="utf-8"
)
file_handler.setFormatter(formatter)

logger.addHandler(console_handler)
logger.addHandler(file_handler)