from __future__ import annotations

import csv
import hashlib
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent
MANIFEST = ROOT / "manifest" / "files_sha256.csv"
PRIMARY = ROOT / "data" / "internal37" / "outputs" / "primary_statistics.csv"
CALIBRATION_RUNS = ROOT / "data" / "calibration" / "subject_fold_calibration_runs.csv"
CALIBRATION_SUMMARY = ROOT / "data" / "calibration" / "subject_fold_calibration_summary.csv"
EXPECTED_PRIMARY = {
    "foreground_dice": (-0.0014706567567567468, -0.0038258230405405227, 0.00041474628378378447, 0.20034979965020036),
    "identification_rate": (-0.005542535135135135, -0.019014789594594593, 0.005811671486486485, 0.43985156014843985),
}
TEXT_SUFFIXES = {".cff", ".csv", ".json", ".md", ".py", ".txt", ".yaml", ".yml"}


def canonical_payload(path: Path) -> bytes:
    """Return platform-stable bytes for manifests while preserving binaries."""
    payload = path.read_bytes()
    is_text = (
        path.suffix.lower() in TEXT_SUFFIXES
        or path.name.startswith("LICENSE")
        or path.name == ".gitignore"
    )
    return payload.replace(b"\r\n", b"\n") if is_text else payload


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    digest.update(canonical_payload(path))
    return digest.hexdigest()


def package_files(root: Path = ROOT, manifest: Path = MANIFEST) -> list[Path]:
    return sorted(
        path
        for path in root.rglob("*")
        if path.is_file()
        and path != manifest
        and ".git" not in path.relative_to(root).parts
        and ".worktrees" not in path.relative_to(root).parts
        and "__pycache__" not in path.relative_to(root).parts
    )


def write_manifest() -> None:
    MANIFEST.parent.mkdir(parents=True, exist_ok=True)
    with MANIFEST.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(["relative_path", "size_bytes", "sha256"])
        for path in package_files():
            writer.writerow([path.relative_to(ROOT).as_posix(), len(canonical_payload(path)), sha256(path)])
    print(f"Wrote {MANIFEST.relative_to(ROOT)}")


def validate_release() -> list[str]:
    failures: list[str] = []
    required = [
        "LICENSE", "LICENSE-CODE", "LICENSE-DATA", "CITATION.cff", ".zenodo.json",
        "scripts/analysis/subject_equal_primary.py", "scripts/analysis/subject_fold_calibration.py",
    ]
    for relative in required:
        if not (ROOT / relative).is_file():
            failures.append(f"missing release file: {relative}")

    if PRIMARY.is_file():
        with PRIMARY.open(encoding="utf-8", newline="") as handle:
            rows = {row["metric"]: row for row in csv.DictReader(handle)}
        if set(rows) != set(EXPECTED_PRIMARY):
            failures.append("primary metric set changed")
        for metric, expected in EXPECTED_PRIMARY.items():
            if metric not in rows:
                continue
            row = rows[metric]
            actual = tuple(float(row[name]) for name in ("mean_difference", "bootstrap_ci_low", "bootstrap_ci_high", "permutation_p"))
            if any(abs(value - target) > 1e-14 for value, target in zip(actual, expected)):
                failures.append(f"primary statistics changed: {metric}")
            if (int(row["cases"]), int(row["subjects"]), int(row["folds_averaged_before_subject_inference"])) != (40, 37, 5):
                failures.append(f"primary counts changed: {metric}")
    else:
        failures.append("missing primary statistics")

    for path, expected_rows in ((CALIBRATION_RUNS, 1800), (CALIBRATION_SUMMARY, 6)):
        if not path.is_file():
            failures.append(f"missing calibration output: {path.name}")
            continue
        with path.open(encoding="utf-8", newline="") as handle:
            count = sum(1 for _ in csv.DictReader(handle))
        if count != expected_rows:
            failures.append(f"calibration row count changed: {path.name}={count}")

    try:
        json.loads((ROOT / ".zenodo.json").read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        failures.append(f"invalid .zenodo.json: {exc}")

    stale_terms = ("CMIG_BOOTSTRAP_OUTPUT", "Small Pseudo-Label Gains", "will be added before")
    active_files = [ROOT / "README.md", ROOT / "data_dictionary.md", ROOT / "CITATION.cff"]
    active_files.extend((ROOT / "scripts" / "analysis").glob("*.py"))
    for path in active_files:
        if not path.is_file():
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        for term in stale_terms:
            if term in text:
                failures.append(f"stale active wording: {path.relative_to(ROOT)}:{term}")
    return failures


def main() -> None:
    if "--write-manifest" in sys.argv:
        write_manifest()
        return
    with MANIFEST.open("r", encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))

    failures: list[str] = []
    expected_paths = {row["relative_path"] for row in rows}
    actual_paths = {path.relative_to(ROOT).as_posix() for path in package_files()}

    for missing in sorted(expected_paths - actual_paths):
        failures.append(f"missing: {missing}")
    for unexpected in sorted(actual_paths - expected_paths):
        failures.append(f"not in manifest: {unexpected}")

    for row in rows:
        path = ROOT / row["relative_path"]
        if not path.is_file():
            continue
        if len(canonical_payload(path)) != int(row["size_bytes"]):
            failures.append(f"size mismatch: {row['relative_path']}")
        if sha256(path) != row["sha256"]:
            failures.append(f"hash mismatch: {row['relative_path']}")

    failures.extend(validate_release())

    if failures:
        raise SystemExit("Package verification failed:\n" + "\n".join(failures))
    print(f"Verified {len(rows)} files against {MANIFEST.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
