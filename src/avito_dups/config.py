import os
from pathlib import Path

DATA_DIR = Path(os.environ.get("AVITO_DUPS_DATA_DIR", Path.cwd() / "data"))
RAW_DIR = DATA_DIR / "raw"
KAGGLE_DIR = RAW_DIR / "kaggle"
PROCESSED_DIR = DATA_DIR / "processed"
