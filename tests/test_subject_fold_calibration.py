from __future__ import annotations

import csv
import importlib.util
import unittest
from pathlib import Path

from scripts.analysis.subject_fold_calibration import repository_neutral_path

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "analysis" / "subject_fold_calibration.py"
RUNS = ROOT / "data" / "calibration" / "subject_fold_calibration_runs.csv"
SUMMARY = ROOT / "data" / "calibration" / "subject_fold_calibration_summary.csv"


class SubjectFoldCalibrationTests(unittest.TestCase):
    def test_external_input_path_is_neutralized(self) -> None:
        rendered = repository_neutral_path(Path("Z:/private-study/subject_fold_metrics.csv"))
        self.assertEqual(rendered, "<EXTERNAL_INPUT>/subject_fold_metrics.csv")

    def test_source_matrix_is_37_by_5_and_centered(self) -> None:
        self.assertTrue(SCRIPT.is_file(), f"missing {SCRIPT}")
        spec = importlib.util.spec_from_file_location("subject_fold_calibration", SCRIPT)
        module = importlib.util.module_from_spec(spec)
        assert spec.loader is not None
        spec.loader.exec_module(module)
        matrix = module.load_primary_matrix(module.INPUT)
        self.assertEqual(matrix.shape, (37, 5))
        centered = module.center_matrix(matrix)
        self.assertAlmostEqual(float(centered.mean()), 0.0, places=15)

    def test_outputs_have_prespecified_rows_and_detection_definition(self) -> None:
        self.assertTrue(RUNS.is_file(), f"missing {RUNS}")
        self.assertTrue(SUMMARY.is_file(), f"missing {SUMMARY}")
        with RUNS.open(encoding="utf-8", newline="") as handle:
            runs = list(csv.DictReader(handle))
        with SUMMARY.open(encoding="utf-8", newline="") as handle:
            summary = list(csv.DictReader(handle))
        self.assertEqual(len(runs), 6 * 300)
        self.assertEqual(len(summary), 6)
        self.assertEqual(sorted({float(row["delta"]) for row in runs}), [0.0, 0.001, 0.003, 0.005, 0.01, 0.02])
        for row in runs:
            expected = float(row["ci_low"]) > 0.0 or float(row["ci_high"]) < 0.0
            self.assertEqual(row["detected"].lower() == "true", expected)
            self.assertEqual(int(row["bootstrap_repetitions"]), 2000)
            self.assertEqual(int(row["seed"]), 20260716)
        for row in summary:
            subset = [run for run in runs if run["delta"] == row["delta"]]
            rate = np.mean([run["detected"].lower() == "true" for run in subset])
            self.assertAlmostEqual(float(row["detection_rate"]), float(rate), places=15)


if __name__ == "__main__":
    unittest.main()
