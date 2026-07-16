#!/usr/bin/env python3
"""Reproduce the internal 37-subject D175-minus-D129 primary analysis."""

from __future__ import annotations

import csv
import json
import os
from collections import defaultdict
from pathlib import Path

import numpy as np
from scipy.stats import rankdata, wilcoxon


ROOT = Path(__file__).resolve().parents[2]
INPUT = Path(os.environ.get("PSEUDOLABEL_INTERNAL37_INPUT", ROOT / "data" / "internal37" / "subject_fold_metrics.csv"))
OUTPUT = Path(os.environ.get("PSEUDOLABEL_PRIMARY_OUTPUT", ROOT / "data" / "internal37" / "outputs"))
BOOTSTRAP_REPETITIONS = 100_000
PERMUTATION_REPETITIONS = 1_000_000
BASE_SEED = 20260715
METRICS = ("foreground_dice", "identification_rate")


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def repository_neutral_path(path: Path) -> str:
    """Describe an input without leaking or requiring a machine-specific path."""
    try:
        return path.resolve().relative_to(ROOT.resolve()).as_posix()
    except ValueError:
        return f"<EXTERNAL_INPUT>/{path.name}"


def load_subject_fold_effects(path: Path) -> tuple[dict[str, dict[str, np.ndarray]], int]:
    """Return metric -> subject -> five D175-D129 fold effects and scan count."""
    values: dict[tuple[str, str, int, str], float] = {}
    case_counts: dict[tuple[str, int], int] = {}
    with path.open(encoding="utf-8", newline="") as handle:
        for row in csv.DictReader(handle):
            metric = row["metric"]
            if metric not in METRICS:
                continue
            subject = row["subject_id"]
            fold = int(row["fold"])
            model = row["model"]
            key = (metric, subject, fold, model)
            require(key not in values, f"duplicate row: {key}")
            values[key] = float(row["value"])
            case_key = (subject, fold)
            count = int(row["cases_aggregated"])
            if case_key in case_counts:
                require(case_counts[case_key] == count, f"case count changed: {case_key}")
            else:
                case_counts[case_key] = count

    subjects = sorted({key[1] for key in values})
    require(len(subjects) == 37, f"expected 37 subjects, found {len(subjects)}")
    require({key[2] for key in values} == set(range(5)), "folds must be 0-4")
    cases_per_fold = {
        fold: sum(count for (subject, current_fold), count in case_counts.items() if current_fold == fold)
        for fold in range(5)
    }
    require(set(cases_per_fold.values()) == {40}, f"expected 40 scans/fold: {cases_per_fold}")

    result: dict[str, dict[str, np.ndarray]] = defaultdict(dict)
    for metric in METRICS:
        for subject in subjects:
            effects = []
            for fold in range(5):
                d129 = values[(metric, subject, fold, "d129")]
                d175 = values[(metric, subject, fold, "d175")]
                effects.append(d175 - d129)
            result[metric][subject] = np.asarray(effects, dtype=float)
    return dict(result), 40


def bootstrap_ci(differences: np.ndarray, seed: int) -> tuple[float, float]:
    rng = np.random.default_rng(seed)
    indices = rng.integers(0, len(differences), size=(BOOTSTRAP_REPETITIONS, len(differences)))
    means = differences[indices].mean(axis=1)
    low, high = np.quantile(means, [0.025, 0.975])
    return float(low), float(high)


def sign_flip_p(differences: np.ndarray, seed: int, chunk_size: int = 50_000) -> float:
    rng = np.random.default_rng(seed)
    observed = abs(float(differences.mean()))
    extreme = 0
    completed = 0
    while completed < PERMUTATION_REPETITIONS:
        size = min(chunk_size, PERMUTATION_REPETITIONS - completed)
        signs = rng.integers(0, 2, size=(size, len(differences)), dtype=np.int8) * 2 - 1
        permuted = (signs @ differences) / len(differences)
        extreme += int((np.abs(permuted) >= observed - 1e-15).sum())
        completed += size
    return float((extreme + 1) / (PERMUTATION_REPETITIONS + 1))


def wilcoxon_p_secondary(differences: np.ndarray) -> float:
    """Return a deterministic two-sided Wilcoxon p value across SciPy versions."""
    nonzero = np.asarray(differences, dtype=float)
    nonzero = nonzero[nonzero != 0.0]
    if len(nonzero) == 0:
        return 1.0
    absolute = np.abs(nonzero)
    ranks = rankdata(absolute)
    no_ties = len(np.unique(absolute)) == len(absolute)
    if no_ties:
        integer_ranks = ranks.astype(int)
        observed = int(integer_ranks[nonzero > 0].sum())
        total_rank = int(integer_ranks.sum())
        observed = min(observed, total_rank - observed)
        counts = [0] * (total_rank + 1)
        counts[0] = 1
        for rank in integer_ranks:
            for value in range(total_rank, rank - 1, -1):
                counts[value] += counts[value - rank]
        return float(min(1.0, 2.0 * sum(counts[: observed + 1]) / (2 ** len(integer_ranks))))

    kwargs = {"zero_method": "wilcox", "correction": False, "alternative": "two-sided"}
    try:
        return float(wilcoxon(differences, method="approx", **kwargs).pvalue)
    except TypeError:  # SciPy < 1.9 used ``mode`` for the same option.
        return float(wilcoxon(differences, mode="approx", **kwargs).pvalue)


def infer(metric: str, subject_effects: dict[str, np.ndarray], cases: int, seed: int) -> tuple[dict[str, object], list[dict[str, object]]]:
    subject_rows = []
    for subject in sorted(subject_effects):
        folds = subject_effects[subject]
        subject_rows.append({
            "subject_id": subject,
            "metric": metric,
            "mean_difference": float(folds.mean()),
            **{f"fold{fold}": float(folds[fold]) for fold in range(5)},
        })
    differences = np.asarray([row["mean_difference"] for row in subject_rows], dtype=float)
    low, high = bootstrap_ci(differences, seed)
    permutation_p = sign_flip_p(differences, seed)
    wilcoxon_p = wilcoxon_p_secondary(differences)
    row = {
        "comparison": "D175_minus_D129",
        "cohort": "internal37",
        "metric": metric,
        "cases": cases,
        "subjects": len(differences),
        "folds_averaged_before_subject_inference": 5,
        "estimand": "subject_equal_paired_mean_difference",
        "mean_difference": float(differences.mean()),
        "bootstrap_ci_low": low,
        "bootstrap_ci_high": high,
        "permutation_p": permutation_p,
        "wilcoxon_p_secondary": wilcoxon_p,
        "positive": int((differences > 0).sum()),
        "negative": int((differences < 0).sum()),
        "zero": int((differences == 0).sum()),
        "bootstrap_repetitions": BOOTSTRAP_REPETITIONS,
        "permutation_repetitions": PERMUTATION_REPETITIONS,
        "seed": seed,
        "favorable_direction_for_d175": "higher",
    }
    return row, subject_rows


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    require(bool(rows), f"no rows for {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def run_analysis(input_path: Path = INPUT, output_dir: Path = OUTPUT) -> None:
    effects, cases = load_subject_fold_effects(input_path)
    statistics = []
    subject_rows = []
    for index, metric in enumerate(METRICS):
        row, rows = infer(metric, effects[metric], cases, BASE_SEED + index)
        statistics.append(row)
        subject_rows.extend(rows)

    write_csv(output_dir / "primary_statistics.csv", statistics)
    write_csv(output_dir / "subject_level_effects.csv", subject_rows)
    provenance = {
        "comparison": "D175 minus D129",
        "input": repository_neutral_path(input_path),
        "aggregation": "folds within scan; repeated scans within subject; subjects equally weighted",
        "cases": cases,
        "subjects": 37,
        "folds": 5,
        "bootstrap_repetitions": BOOTSTRAP_REPETITIONS,
        "permutation_repetitions": PERMUTATION_REPETITIONS,
        "base_seed": BASE_SEED,
    }
    (output_dir / "analysis_provenance.json").write_text(json.dumps(provenance, indent=2), encoding="utf-8")
    print(f"Wrote {len(statistics)} primary rows and {len(subject_rows)} subject rows to {output_dir}")


if __name__ == "__main__":
    run_analysis()
