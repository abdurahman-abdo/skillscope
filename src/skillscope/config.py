import os
from pathlib import Path
from dotenv import load_dotenv

# Path to this file's location
CURRENT_DIR = Path(__file__).resolve().parent

# Move up 2 levels (skillscope/src/skillscope/config.py -> skillscope/)
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Load .env from that parent directory
load_dotenv(dotenv_path=BASE_DIR / ".env")

ADZUNA_APP_ID: str = os.getenv("ADZUNA_APP_ID")
ADZUNA_APP_KEY: str = os.getenv("ADZUNA_APP_KEY")

DATA_PATH = Path.cwd() / ".." / "data"
DATA_PATH.parent.mkdir(parents=True, exist_ok=True)

RAW_DATA_PATH = DATA_PATH / "raw-scored"
RAW_DATA_PATH.parent.mkdir(parents=True, exist_ok=True)

CLEANED_DATA_PATH = DATA_PATH / "cleaned"
CLEANED_DATA_PATH.parent.mkdir(parents=True, exist_ok=True)
