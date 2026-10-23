import hashlib
from pathlib import Path

import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq

from avito_dups import config

CHUNK_BYTES = 1 << 20
CHUNK_ROWS = 100_000

ITEMS_CSV = "ItemInfo_train.csv"
PAIRS_CSV = "ItemPairs_train.csv"
ITEMS_PARQUET = "items.parquet"
PAIRS_PARQUET = "pairs.parquet"

ITEMS_DTYPES = {
    "itemID": "int64",
    "categoryID": "int64",
    "title": "str",
    "description": "str",
    "images_array": "str",
    "attrsJSON": "str",
    "price": "float64",
    "locationID": "int64",
    "metroID": "float64",
    "lat": "float64",
    "lon": "float64",
}


class ChecksumError(RuntimeError):
    pass


def md5_of_file(path: Path) -> str:
    digest = hashlib.md5()
    with open(path, "rb") as handle:
        for chunk in iter(lambda: handle.read(CHUNK_BYTES), b""):
            digest.update(chunk)
    return digest.hexdigest()


def verify_md5(path: Path, expected: str) -> None:
    actual = md5_of_file(path)
    if actual != expected.lower():
        raise ChecksumError(f"{path.name}: ожидался md5 {expected}, получен {actual}")


def csv_to_parquet(
    source: Path,
    target: Path,
    dtypes: dict[str, str] | None = None,
    chunk_rows: int = CHUNK_ROWS,
) -> int:
    target.parent.mkdir(parents=True, exist_ok=True)
    writer = None
    total = 0
    try:
        for chunk in pd.read_csv(source, dtype=dtypes, chunksize=chunk_rows):
            table = pa.Table.from_pandas(chunk, preserve_index=False)
            if writer is None:
                writer = pq.ParquetWriter(target, table.schema)
            writer.write_table(table)
            total += len(chunk)
    finally:
        if writer is not None:
            writer.close()
    return total


def build_dataset(
    raw_dir: Path = config.KAGGLE_DIR,
    out_dir: Path = config.PROCESSED_DIR,
) -> dict[str, int]:
    return {
        "items": csv_to_parquet(raw_dir / ITEMS_CSV, out_dir / ITEMS_PARQUET, ITEMS_DTYPES),
        "pairs": csv_to_parquet(raw_dir / PAIRS_CSV, out_dir / PAIRS_PARQUET),
    }
