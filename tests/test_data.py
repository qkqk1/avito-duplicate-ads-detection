import hashlib

import pytest

from avito_dups import cli, data


def write_file(tmp_path, payload: bytes):
    path = tmp_path / "sample.bin"
    path.write_bytes(payload)
    return path


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
