import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID_STR = os.getenv("ADMIN_ID", "")
ADMIN_IDS = [int(id.strip()) for id in ADMIN_ID_STR.split(",") if id.strip().isdigit()]

CHANNEL_ID = os.getenv("CHANNEL_ID")
INSTAGRAM_LINK = os.getenv("INSTAGRAM_LINK")

DATABASE_PATH = "database.db"
