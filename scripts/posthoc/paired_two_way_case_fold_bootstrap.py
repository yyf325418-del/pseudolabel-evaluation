"""
Repository reconstruction of the primary D175-D129 paired analysis.

This script operates only on the frozen per-case/per-fold evaluation table.
It does not claim to be the original interactive analysis command.
"""

import hashlib
import json
import os
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import ttest_1samp, wilcoxon

ROOT = Path(
    os.environ.get("VERSE_PROJECT_ROOT", ".")
).resolve()

INPUT = Path(
    os.environ.get(
        "D129_D175_LONG_CSV",
        str(
            ROOT / "data/derived/"
            "d129_d175_case_fold_eval_long.csv"
        ),
    )
).resolve()

OUT = Path(
    os.environ.get(
        "CMIG_BOOTSTRAP_OUTPUT",
        str(ROOT / "repository_outputs/derived_statistics"),
    )
).resolve()
OUT.mkdir(parents=True, exist_ok=True)

SEED = 20260629
N_BOOT = 100000
CHUNK_SIZE = 5000


def sha256(path):
    h = hashlib.sha256()
    with path.open("rb") as f:
        while chunk := f.read(8 * 1024 * 1024):
            h.update(chunk)
    return h.hexdigest()


def percentile_bootstrap(values, rng):
    values = np.asarray(values, dtype=float)
    n = len(values)
    indices = rng.integers(0, n, size=(N_BOOT, n))
    estimates = values[indices].mean(axis=1)
    return (
        float(np.quantile(estimates, 0.025)),
        float(np.quantile(estimates, 0.975)),
    )


def two_way_bootstrap(matrix, rng):
    matrix = np.asarray(matrix, dtype=float)
    n_folds, n_cases = matrix.shape
    estimates = np.empty(N_BOOT, dtype=float)

    for start in range(0, N_BOOT, CHUNK_SIZE):
        stop = min(start + CHUNK_SIZE, N_BOOT)
        batch = stop - start

        fold_indices = rng.integers(
            0, n_folds, size=(batch, n_folds)
        )
        case_indices = rng.integers(
            0, n_cases, size=(batch, n_cases)
        )

        sampled = matrix[
            fold_indices[:, :, None],
            case_indices[:, None, :],
        ]
        estimates[start:stop] = sampled.mean(axis=(1, 2))

    return (
        float(np.quantile(estimates, 0.025)),
        float(np.quantile(estimates, 0.975)),
    )


def paired_tests(values):
    values = np.asarray(values, dtype=float)

    try:
        w = wilcoxon(
            values,
            zero_method="pratt",
            alternative="two-sided",
            method="approx",
        )
    except TypeError:
        w = wilcoxon(
            values,
            zero_method="pratt",
            alternative="two-sided",
        )

    t = ttest_1samp(values, popmean=0.0)

    return (
        float(w.statistic),
        float(w.pvalue),
        float(t.statistic),
        float(t.pvalue),
    )


if not INPUT.exists():
    raise FileNotFoundError(INPUT)

df = pd.read_csv(INPUT)

required = {"model", "fold", "case_id", "dice", "id_rate"}
missing = required - set(df.columns)
if missing:
    raise ValueError(f"Missing columns: {sorted(missing)}")

if df.duplicated(["model", "fold", "case_id"]).any():
    raise ValueError("Duplicate model/fold/case_id rows detected")

models = set(df["model"].astype(str))
if models != {"D129", "D175"}:
    raise ValueError(f"Expected D129 and D175, found: {sorted(models)}")

df["fold"] = df["fold"].astype(int)

if set(df["fold"]) != {0, 1, 2, 3, 4}:
    raise ValueError(f"Unexpected folds: {sorted(set(df['fold']))}")

model_counts = (
    df.groupby("model")[["fold", "case_id"]]
    .agg({"fold": "nunique", "case_id": "nunique"})
)

for model in ["D129", "D175"]:
    if model_counts.loc[model, "fold"] != 5:
        raise ValueError(f"{model}: expected 5 folds")
    if model_counts.loc[model, "case_id"] != 40:
        raise ValueError(f"{model}: expected 40 cases")

rng = np.random.default_rng(SEED)

statistics_rows = []
paired_outputs = []
fold_outputs = []
case_outputs = []

for metric in ["dice", "id_rate"]:
    wide = (
        df.pivot(
            index=["fold", "case_id"],
            columns="model",
            values=metric,
        )
        .reset_index()
        .sort_values(["fold", "case_id"])
    )

    if wide[["D129", "D175"]].isna().any().any():
        raise ValueError(f"{metric}: incomplete D129/D175 pairing")

    if len(wide) != 200:
        raise ValueError(
            f"{metric}: expected 200 paired observations, "
            f"found {len(wide)}"
        )

    diff_column = f"diff_{metric}_D175_minus_D129"
    wide[diff_column] = wide["D175"] - wide["D129"]

    paired_metric = wide.rename(columns={
        "D129": f"{metric}_D129",
        "D175": f"{metric}_D175",
    })
    paired_outputs.append(
        paired_metric[
            [
                "fold",
                "case_id",
                f"{metric}_D129",
                f"{metric}_D175",
                diff_column,
            ]
        ]
    )

    fold_diff = (
        wide.groupby("fold", as_index=False)[diff_column]
        .mean()
    )
    fold_diff["metric"] = metric
    fold_outputs.append(fold_diff)

    case_diff = (
        wide.groupby("case_id", as_index=False)[diff_column]
        .mean()
    )
    case_diff["metric"] = metric
    case_outputs.append(case_diff)

    matrix = (
        wide.pivot(
            index="fold",
            columns="case_id",
            values=diff_column,
        )
        .sort_index()
        .sort_index(axis=1)
    )

    if matrix.shape != (5, 40):
        raise ValueError(
            f"{metric}: expected matrix (5, 40), "
            f"found {matrix.shape}"
        )

    flattened = matrix.to_numpy().ravel()
    fold_values = fold_diff[diff_column].to_numpy()
    case_values = case_diff[diff_column].to_numpy()

    fold_ci = percentile_bootstrap(fold_values, rng)
    case_ci = percentile_bootstrap(case_values, rng)
    two_way_ci = two_way_bootstrap(matrix.to_numpy(), rng)

    fold_tests = paired_tests(fold_values)
    case_tests = paired_tests(case_values)

    for analysis, values, ci, tests in [
        ("fold_level", fold_values, fold_ci, fold_tests),
        ("case_averaged", case_values, case_ci, case_tests),
        (
            "two_way_case_fold_bootstrap",
            flattened,
            two_way_ci,
            (np.nan, np.nan, np.nan, np.nan),
        ),
    ]:
        statistics_rows.append({
            "comparison": "D175_minus_D129",
            "metric": metric,
            "analysis": analysis,
            "n": len(values),
            "mean_diff": float(np.mean(values)),
            "sd_diff": float(np.std(values, ddof=1)),
            "median_diff": float(np.median(values)),
            "q1_diff": float(np.quantile(values, 0.25)),
            "q3_diff": float(np.quantile(values, 0.75)),
            "bootstrap_ci_low": ci[0],
            "bootstrap_ci_high": ci[1],
            "wilcoxon_statistic": tests[0],
            "wilcoxon_p": tests[1],
            "paired_t_statistic": tests[2],
            "paired_t_p": tests[3],
            "bootstrap_repetitions": N_BOOT,
            "bootstrap_seed": SEED,
        })

statistics = pd.DataFrame(statistics_rows)

dice_mean = statistics.loc[
    (statistics["metric"] == "dice")
    & (
        statistics["analysis"]
        == "two_way_case_fold_bootstrap"
    ),
    "mean_diff",
].iloc[0]

id_mean = statistics.loc[
    (statistics["metric"] == "id_rate")
    & (
        statistics["analysis"]
        == "two_way_case_fold_bootstrap"
    ),
    "mean_diff",
].iloc[0]

# Frozen-result regression checks.
assert abs(dice_mean - (-0.000934)) < 5e-6, dice_mean
assert abs(id_mean - 0.001666) < 5e-6, id_mean

paired_long = (
    paired_outputs[0]
    .merge(
        paired_outputs[1],
        on=["fold", "case_id"],
        validate="one_to_one",
    )
)

fold_differences = pd.concat(
    fold_outputs, ignore_index=True
)
case_differences = pd.concat(
    case_outputs, ignore_index=True
)

paired_path = OUT / "d129_d175_primary_paired_long.csv"
fold_path = OUT / "d129_d175_primary_fold_differences.csv"
case_path = OUT / "d129_d175_primary_case_differences.csv"
statistics_path = OUT / "d129_d175_primary_statistics.csv"
provenance_path = OUT / "d129_d175_primary_provenance.json"

paired_long.to_csv(paired_path, index=False)
fold_differences.to_csv(fold_path, index=False)
case_differences.to_csv(case_path, index=False)
statistics.to_csv(statistics_path, index=False)

provenance = {
    "status": "repository reconstruction from frozen outputs",
    "original_interactive_command_preserved": False,
    "input": str(INPUT),
    "input_sha256": sha256(INPUT),
    "models": ["D129", "D175"],
    "folds": 5,
    "cases": 40,
    "paired_observations": 200,
    "difference_direction": "D175 minus D129",
    "metrics": ["dice", "id_rate"],
    "primary_uncertainty_method": (
        "two-way case-fold percentile bootstrap"
    ),
    "bootstrap_repetitions": N_BOOT,
    "bootstrap_seed": SEED,
    "note": (
        "Fold-specific training-pool intervention status is "
        "reported separately in the split manifest."
    ),
}

provenance_path.write_text(
    json.dumps(provenance, indent=2)
)

print("=== PRIMARY BOOTSTRAP RECONSTRUCTION PASSED ===")
print(statistics.to_string(index=False))

print("\nwrote:")
for path in [
    paired_path,
    fold_path,
    case_path,
    statistics_path,
    provenance_path,
]:
    print(path)
