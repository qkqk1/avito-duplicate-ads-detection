import argparse
import sys
from pathlib import Path

from avito_dups import data


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="avito-dups")
    commands = parser.add_subparsers(dest="command", required=True)

    commands.add_parser("build-dataset", help="перевести таблицы Kaggle в Parquet")

    md5_parser = commands.add_parser("md5", help="вывести md5 файла")
    md5_parser.add_argument("path", type=Path)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if args.command == "build-dataset":
        for name, rows in data.build_dataset().items():
            print(f"{name}: {rows}")
    if args.command == "md5":
        print(data.md5_of_file(args.path))
    return 0


if __name__ == "__main__":
    sys.exit(main())
