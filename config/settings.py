import os
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent

BOT_TOKEN = os.getenv("NES_TELEGRAM_BOT_TOKEN")

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///db/db.sqlite3")

MSG_PARSE_MODE = 'HTML'

