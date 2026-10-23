import hashlib

import pandas as pd
import pytest

from avito_dups import cli, data


def write_file(tmp_path, payload: bytes):
    path = tmp_path / "sample.bin"
    path.write_bytes(payload)
    return path


def make_items(rows: int) -> pd.DataFrame:
    return pd.DataFrame(
        {
            "itemID": range(1, rows + 1),
            "categoryID": [10 + i % 3 for i in range(rows)],
            "title": [f"title {i}" for i in range(rows)],
            "description": [f"описание, {i}\nвторая строка" for i in range(rows)],
            "images_array": [None if 3 <= i < 6 else f"{i}, {i + 1}" for i in range(rows)],
            "attrsJSON": ['{"a": "b"}'] * rows,
            "price": [None if i % 2 else 100.0 * i for i in range(rows)],
            "locationID": [650000 + i for i in range(rows)],
            "metroID": [None if i >= 3 else 250000.0 + i for i in range(rows)],
            "lat": [55.0 + i / 100 for i in range(rows)],
            "lon": [37.0 + i / 100 for i in range(rows)],
        }
    )


def make_pairs() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "itemID_1": [1, 2, 3],
            "itemID_2": [4, 5, 6],
            "isDuplicate": [1, 0, 1],
            "generationMethod": [1, 2, 3],
        }
    )


def test_md5_matches_hashlib(tmp_path):
    payload = b"duplicate ads" * 100_000
    path = write_file(tmp_path, payload)
    assert data.md5_of_file(path) == hashlib.md5(payload).hexdigest()


def test_verify_md5_accepts_correct_hash(tmp_path):
    payload = b"abc"
    path = write_file(tmp_path, payload)
    data.verify_md5(path, hashlib.md5(payload).hexdigest().upper())


def test_verify_md5_rejects_wrong_hash(tmp_path):
    path = write_file(tmp_path, b"abc")
    with pytest.raises(data.ChecksumError):
        data.verify_md5(path, "0" * 32)


def test_cli_md5_prints_hash(tmp_path, capsys):
    path = write_file(tmp_path, b"abc")
    assert cli.main(["md5", str(path)]) == 0
    assert capsys.readouterr().out.strip() == "900150983cd24fb0d6963f7d28e17f72"


def test_csv_to_parquet_matches_csv_across_chunks(tmp_path):
    source = tmp_path / "items.csv"
    make_items(7).to_csv(source, index=False)
    target = tmp_path / "out" / "items.parquet"

    rows = data.csv_to_parquet(source, target, data.ITEMS_DTYPES, chunk_rows=3)

    expected = pd.read_csv(source, dtype=data.ITEMS_DTYPES)
    assert rows == 7
    pd.testing.assert_frame_equal(pd.read_parquet(target), expected)


def test_build_dataset_writes_both_tables(tmp_path):
    raw = tmp_path / "raw"
    raw.mkdir()
    make_items(7).to_csv(raw / data.ITEMS_CSV, index=False)
    make_pairs().to_csv(raw / data.PAIRS_CSV, index=False)
    out = tmp_path / "processed"

    counts = data.build_dataset(raw, out)

    assert counts == {"items": 7, "pairs": 3}
    assert (out / data.ITEMS_PARQUET).exists()
    assert (out / data.PAIRS_PARQUET).exists()
