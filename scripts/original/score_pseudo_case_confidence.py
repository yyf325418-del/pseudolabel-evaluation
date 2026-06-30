#!/usr/bin/env python
"""Score pseudo-label masks with lightweight case-level quality heuristics."""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

import nibabel as nib
import numpy as np
from scipy import ndimage


def parse_args():
    parser = argparse.ArgumentParser(
        description=(
            "Estimate case-level pseudo-label confidence from segmentation masks only. "
            "Useful for V1 confidence filtering before re-training."
        )
    )
    parser.add_argument(
        "--pred-dir",
        required=True,
        help="Directory containing pseudo-label masks (*.nii.gz).",
    )
    parser.add_argument(
        "--out-csv",
        required=True,
        help="Path to write the per-case score table.",
    )
    parser.add_argument(
        "--out-json",
        required=True,
        help="Path to write the filtered case lists and summary.",
    )
    parser.add_argument(
        "--tiny-label-threshold",
        type=int,
        default=400,
        help="Labels smaller than this many voxels are treated as tiny/noisy.",
    )
    parser.add_argument(
        "--high-threshold",
        type=float,
        default=0.75,
        help="Final confidence score threshold for recommended high-confidence cases.",
    )
    parser.add_argument(
        "--medium-threshold",
        type=float,
        default=0.60,
        help="Final confidence score threshold for medium-confidence cases.",
    )
    return parser.parse_args()


def longest_consecutive_run(labels: list[int]) -> int:
    if not labels:
        return 0
    longest = 1
    current = 1
    for prev_label, next_label in zip(labels[:-1], labels[1:]):
        if next_label == prev_label + 1:
            current += 1
            longest = max(longest, current)
        else:
            current = 1
    return longest


def compute_component_ratio(binary_mask: np.ndarray) -> tuple[float, int]:
    labeled, n_components = ndimage.label(binary_mask)
    if n_components == 0:
        return 0.0, 0
    component_sizes = np.bincount(labeled.ravel())[1:]
    largest = int(component_sizes.max())
    total = int(component_sizes.sum())
    return largest / total if total > 0 else 0.0, n_components


def score_case(mask_path: Path, tiny_label_threshold: int) -> dict:
    data = np.asanyarray(nib.load(str(mask_path)).dataobj)
    labels = sorted(int(i) for i in np.unique(data) if int(i) > 0)
    label_sizes = {}
    largest_cc_ratios = []
    component_counts = []

    for label_value in labels:
        label_mask = data == label_value
        label_voxels = int(label_mask.sum())
        label_sizes[label_value] = label_voxels
        largest_ratio, n_components = compute_component_ratio(label_mask)
        largest_cc_ratios.append(largest_ratio)
        component_counts.append(n_components)

    num_labels = len(labels)
    total_foreground = int(sum(label_sizes.values()))
    longest_run = longest_consecutive_run(labels)
    gap_count = sum(1 for a, b in zip(labels[:-1], labels[1:]) if b - a > 1)
    tiny_labels = sum(1 for v in label_sizes.values() if v < tiny_label_threshold)
    tiny_fraction = tiny_labels / num_labels if num_labels else 1.0
    mean_largest_cc_ratio = float(np.mean(largest_cc_ratios)) if largest_cc_ratios else 0.0
    max_components = max(component_counts) if component_counts else 0

    coverage_score = min(num_labels / 10.0, 1.0)
    run_score = min(longest_run / 8.0, 1.0)
    continuity_score = max(0.0, 1.0 - gap_count / max(num_labels - 1, 1))
    component_score = mean_largest_cc_ratio
    size_score = max(0.0, 1.0 - tiny_fraction)

    final_score = (
        0.15 * coverage_score
        + 0.35 * run_score
        + 0.20 * continuity_score
        + 0.20 * component_score
        + 0.10 * size_score
    )

    return {
        "case_id": mask_path.name[:-7],
        "mask_path": str(mask_path),
        "num_labels": num_labels,
        "labels": labels,
        "total_foreground_voxels": total_foreground,
        "longest_run": longest_run,
        "gap_count": gap_count,
        "tiny_labels": tiny_labels,
        "tiny_fraction": round(tiny_fraction, 6),
        "mean_largest_cc_ratio": round(mean_largest_cc_ratio, 6),
        "max_components_per_label": max_components,
        "coverage_score": round(coverage_score, 6),
        "run_score": round(run_score, 6),
        "continuity_score": round(continuity_score, 6),
        "component_score": round(component_score, 6),
        "size_score": round(size_score, 6),
        "final_score": round(final_score, 6),
    }


def write_csv(rows: list[dict], out_csv: Path):
    fieldnames = [
        "case_id",
        "num_labels",
        "total_foreground_voxels",
        "longest_run",
        "gap_count",
        "tiny_labels",
        "tiny_fraction",
        "mean_largest_cc_ratio",
        "max_components_per_label",
        "coverage_score",
        "run_score",
        "continuity_score",
        "component_score",
        "size_score",
        "final_score",
        "labels",
        "mask_path",
    ]
    with out_csv.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            row_to_write = dict(row)
            row_to_write["labels"] = " ".join(str(i) for i in row["labels"])
            writer.writerow(row_to_write)


def main():
    args = parse_args()
    pred_dir = Path(args.pred_dir).resolve()
    out_csv = Path(args.out_csv).resolve()
    out_json = Path(args.out_json).resolve()

    mask_paths = sorted(pred_dir.glob("sub-verse*.nii.gz"))
    if not mask_paths:
        raise FileNotFoundError(f"No pseudo-label masks found in {pred_dir}")

    rows = [score_case(p, args.tiny_label_threshold) for p in mask_paths]
    rows.sort(key=lambda x: x["final_score"], reverse=True)

    high_conf = []
    medium_conf = []
    low_conf = []
    for row in rows:
        if row["final_score"] >= args.high_threshold:
            high_conf.append(row["case_id"])
        elif row["final_score"] >= args.medium_threshold:
            medium_conf.append(row["case_id"])
        else:
            low_conf.append(row["case_id"])

    out_csv.parent.mkdir(parents=True, exist_ok=True)
    out_json.parent.mkdir(parents=True, exist_ok=True)
    write_csv(rows, out_csv)
    out_json.write_text(
        json.dumps(
            {
                "pred_dir": str(pred_dir),
                "num_cases": len(rows),
                "high_threshold": args.high_threshold,
                "medium_threshold": args.medium_threshold,
                "tiny_label_threshold": args.tiny_label_threshold,
                "high_confidence_cases": high_conf,
                "medium_confidence_cases": medium_conf,
                "low_confidence_cases": low_conf,
                "top5": rows[:5],
                "bottom5": rows[-5:],
            },
            indent=2,
        ),
        encoding="utf-8",
    )

    print("pred_dir =", pred_dir)
    print("num_cases =", len(rows))
    print("high_confidence =", len(high_conf))
    print("medium_confidence =", len(medium_conf))
    print("low_confidence =", len(low_conf))
    print("best_case =", rows[0]["case_id"], rows[0]["final_score"])
    print("worst_case =", rows[-1]["case_id"], rows[-1]["final_score"])
    print("out_csv =", out_csv)
    print("out_json =", out_json)


if __name__ == "__main__":
    main()
