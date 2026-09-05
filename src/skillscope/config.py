import os
from pathlib import Path
from dotenv import load_dotenv

# Path to this file's location
CURRENT_DIR = Path(__file__).resolve().parent

# Move up 2 levels (skillscope/src/skillscope/config.py -> skillscope/)
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Load .env from that parent directory
load_dotenv(dotenv_path=BASE_DIR / ".env")

ADZUNA_APP_ID = os.getenv("ADZUNA_APP_ID")
ADZUNA_APP_KEY = os.getenv("ADZUNA_APP_KEY")