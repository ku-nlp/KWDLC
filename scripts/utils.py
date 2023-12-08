import sys
from collections.abc import Iterator
from pathlib import Path


def list_files(paths: list[str], ext: str = "knp") -> Iterator[Path]:
    for path_str in paths:
        path = Path(path_str)
        if path.exists() is False:
            print(f"{path} not found and skipped", file=sys.stderr)
            continue
        if path.is_dir():
            yield from path.glob(f"**/*.{ext}")
        else:
            yield path
