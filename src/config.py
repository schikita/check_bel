import os

TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "")
THRESHOLD = int(os.environ.get("THRESHOLD", 0))
USER_IDS = os.environ.get("USER_IDS", "").split(",") if os.environ.get("USER_IDS") else []
DEBUG = os.environ.get("DEBUG", "False").lower() in ("true", "1")