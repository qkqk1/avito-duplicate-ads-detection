import hashlib
from pathlib import Path

CHUNK_BYTES = 1 << 20


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
