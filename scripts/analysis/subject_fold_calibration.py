#!/usr/bin/env python3
"""Design-specific small-effect calibration for the primary D175-D129 comparison."""

from __future__ import annotations

import csv
import json
import os
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[2]
INPUT = Path(os.environ.get("PSEUDOLABEL_INTERNAL37_INPUT", ROOT / "data" / "internal37" / "subject_fold_metrics.csv"))
OUTPUT = Path(os.environ.get("PSEUDOLABEL_CALIBRATION_OUTPUT", ROOT / "data" / "calibration"))
DELTAS = (0.0, 0.001, 0.003, 0.005, 0.010, 0.020)
SIMULATIONS_PER_DELTA = 300
BOOTSTRAP_REPETITIONS = 2_000
SEED = 20260716


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def repository_neutral_path(path: Path) -> str:
    """Describe an input without leaking or requiring a machine-specific path."""
    try:
        return path.resolve().relative_to(ROOT.resolve()).as_posix()
    except ValueError:
        return f"<EXTERNAL_INPUT>/{path.name}"


def load_primary_matrix(path: Path) -> np.ndarray:
    """Load a subject-by-fold matrix of foreground-Dice D175-minus-D129 effects."""
    values: dict[tuple[str, int, str], float] = {}
    with path.open(encoding="utf-8", newline="") as handle:
        for row in csv.DictReader(handle):
            if row["metric"] != "foreground_dice":
                continue
            key = (row["subject_id"], int(row["fold"]), row["model"])
            require(key not in values, f"duplicate row: {key}")
            values[key] = float(row["value"])
    subjects = sorted({key[0] for key in values})
    require(len(subjects) == 37, f"expected 37 subjects, found {len(subjects)}")
    matrix = np.empty((len(subjects), 5), dtype=float)
    for row_index, subject in enumerate(subjects):
        for fold in range(5):
            matrix[row_index, fold] = values[(subject, fold, "d175")] - values[(subject, fold, "d129")]
    require(np.isfinite(matrix).all(), "non-finite primary residuals")
    return matrix


def center_matrix(matrix: np.ndarray) -> np.ndarray:
    centered = np.asarray(matrix, dtype=float) - float(np.asarray(matrix, dtype=float).mean())
    require(abs(float(centered.mean())) < 1e-15, "residual matrix did not center")
    return centered


def bootstrap_interval(experiment: np.ndarray, rng: np.random.Generator) -> tuple[float, float]:
    subject_indices = rng.integers(0, experiment.shape[0], size=(BOOTSTRAP_REPETITIONS, experiment.shape[0]))
    fold_indices = rng.integers(0, experiment.shape[1], size=(BOOTSTRAP_REPETITIONS, experiment.shape[1]))
    samples = experiment[subject_indices[:, :, None], fold_indices[:, None, :]]
    means = samples.mean(axis=(1, 2))
    low, high = np.quantile(means, [0.025, 0.975])
    return float(low), float(high)


def simulate(centered: np.ndarray) -> tuple[list[dict[str, object]], list[dict[str, object]]]:
    rng = np.random.default_rng(SEED)
    runs: list[dict[str, object]] = []
    summaries: list[dict[str, object]] = []
    for delta in DELTAS:
        delta_rows = []
        for simulation in range(SIMULATIONS_PER_DELTA):
            subject_indices = rng.integers(0, centered.shape[0], size=centered.shape[0])
            fold_indices = rng.integers(0, centered.shape[1], size=centered.shape[1])
            experiment = centered[np.ix_(subject_indices, fold_indices)] + delta
            estimate = float(experiment.mean())
            low, high = bootstrap_interval(experiment, rng)
            detected = bool(low > 0.0 or high < 0.0)
            row = {
                "background": "D175_minus_D129_foreground_dice",
                "delta": delta,
                "simulation": simulation,
                "mean_estimate": estimate,
                "ci_low": low,
                "ci_high": high,
                "detected": detected,
                "subjects": centered.shape[0],
                "folds": centered.shape[1],
                "bootstrap_repetitions": BOOTSTRAP_REPETITIONS,
                "seed": SEED,
            }
            runs.append(row)
            delta_rows.append(row)
        summaries.append({
            "background": "D175_minus_D129_foreground_dice",
            "delta": delta,
            "simulations": SIMULATIONS_PER_DELTA,
            "mean_estimate": float(np.mean([row["mean_estimate"] for row in delta_rows])),
            "median_ci_low": float(np.median([row["ci_low"] for row in delta_rows])),
            "median_ci_high": float(np.median([row["ci_high"] for row in delta_rows])),
            "detection_rate": float(np.mean([row["detected"] for row in delta_rows])),
            "subjects": centered.shape[0],
            "folds": centered.shape[1],
            "bootstrap_repetitions": BOOTSTRAP_REPETITIONS,
            "seed": SEED,
        })
    return runs, summaries


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    matrix = load_primary_matrix(INPUT)
    centered = center_matrix(matrix)
    runs, summaries = simulate(centered)
    write_csv(OUTPUT / "subject_fold_calibration_runs.csv", runs)
    write_csv(OUTPUT / "subject_fold_calibration_summary.csv", summaries)
    provenance = {
        "background": "D175 minus D129 foreground Dice",
        "input": repository_neutral_path(INPUT),
        "matrix_shape": list(matrix.shape),
        "centering": "grand mean subtracted before effect injection",
        "deltas": list(DELTAS),
        "simulations_per_delta": SIMULATIONS_PER_DELTA,
        "bootstrap_repetitions_per_simulation": BOOTSTRAP_REPETITIONS,
        "resampling": "subjects and folds independently sampled with replacement at outer and bootstrap levels",
        "detection": "percentile 95% bootstrap interval excludes zero",
        "seed": SEED,
        "scope": "design-specific calibration; not an equivalence test or universal power analysis",
    }
    (OUTPUT / "subject_fold_calibration_provenance.json").write_text(json.dumps(provenance, indent=2), encoding="utf-8")
    print(f"Wrote {len(runs)} calibration runs and {len(summaries)} summary rows to {OUTPUT}")


if __name__ == "__main__":
    main()
