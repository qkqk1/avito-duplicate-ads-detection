import hashlib
import shutil
import urllib.request
import zipfile
from pathlib import Path

from avito_dups import config

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


def download_sample(raw_dir: Path = config.RAW_DIR) -> Path:
    raw_dir.mkdir(parents=True, exist_ok=True)
    target = raw_dir / config.SAMPLE_LOCAL_NAME
    if target.exists():
        verify_md5(target, config.SAMPLE_MD5)
        return target

    archive = raw_dir / (config.SAMPLE_CSV_NAME + ".zip")
    urllib.request.urlretrieve(config.SAMPLE_URL, archive)
    with zipfile.ZipFile(archive) as bundle:
        with bundle.open(config.SAMPLE_CSV_NAME) as source, open(target, "wb") as sink:
            shutil.copyfileobj(source, sink)
    archive.unlink()

    try:
        verify_md5(target, config.SAMPLE_MD5)
    except ChecksumError:
        target.unlink()
        raise
    return target
