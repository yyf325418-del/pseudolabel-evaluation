from __future__ import annotations

import csv
import hashlib
from pathlib import Path


ROOT = Path(__file__).resolve().parent
MANIFEST = ROOT / "manifest" / "files_sha256.csv"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> None:
    with MANIFEST.open("r", encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))

    failures: list[str] = []
    expected_paths = {row["relative_path"] for row in rows}
    actual_paths = {
        path.relative_to(ROOT).as_posix()
        for path in ROOT.rglob("*")
        if path.is_file()
        and path != MANIFEST
        and ".git" not in path.relative_to(ROOT).parts
    }

    for missing in sorted(expected_paths - actual_paths):
        failures.append(f"missing: {missing}")
    for unexpected in sorted(actual_paths - expected_paths):
        failures.append(f"not in manifest: {unexpected}")

    for row in rows:
        path = ROOT / row["relative_path"]
        if not path.is_file():
            continue
        if path.stat().st_size != int(row["size_bytes"]):
            failures.append(f"size mismatch: {row['relative_path']}")
        if sha256(path) != row["sha256"]:
            failures.append(f"hash mismatch: {row['relative_path']}")

    if failures:
        raise SystemExit("Package verification failed:\n" + "\n".join(failures))
    print(f"Verified {len(rows)} files against {MANIFEST.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
