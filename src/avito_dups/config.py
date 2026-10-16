import os
from pathlib import Path

DATA_DIR = Path(os.environ.get("AVITO_DUPS_DATA_DIR", Path.cwd() / "data"))
RAW_DIR = DATA_DIR / "raw"
PROCESSED_DIR = DATA_DIR / "processed"

SAMPLE_URL = (
    "https://raw.githubusercontent.com/joostgp/kaggle_ad_detection/master/"
    "ItemPairs_train_merged_20000.csv.zip"
)
SAMPLE_CSV_NAME = "ItemPairs_train_merged_20000.csv"
SAMPLE_MD5 = "4d0b6fba46924db96c2ef120683ec2f9"
SAMPLE_SIZE_BYTES = 33_474_134
SAMPLE_LOCAL_NAME = "avito_pairs_sample.csv"
