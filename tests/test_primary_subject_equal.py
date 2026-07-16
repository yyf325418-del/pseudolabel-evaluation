from __future__ import annotations

import csv
import unittest
from pathlib import Path

from scripts.analysis.subject_equal_primary import repository_neutral_path


ROOT = Path(__file__).resolve().parents[1]
STATISTICS = ROOT / "data" / "internal37" / "outputs" / "primary_statistics.csv"

EXPECTED = {
    "foreground_dice": (
        -0.0014706567567567468,
        -0.0038258230405405227,
        0.00041474628378378447,
        0.20034979965020036,
        0.0774078067188384,
    ),
    "identification_rate": (
        -0.005542535135135135,
        -0.019014789594594593,
        0.005811671486486485,
        0.43985156014843985,
        0.42643498438261274,
    ),
}


class PrimarySubjectEqualTests(unittest.TestCase):
    def test_external_input_path_is_neutralized(self) -> None:
        rendered = repository_neutral_path(Path("Z:/private-study/subject_fold_metrics.csv"))
        self.assertEqual(rendered, "<EXTERNAL_INPUT>/subject_fold_metrics.csv")

    def test_primary_statistics_match_locked_subject_equal_results(self) -> None:
        self.assertTrue(STATISTICS.is_file(), f"missing {STATISTICS}")
        with STATISTICS.open(encoding="utf-8", newline="") as handle:
            rows = {row["metric"]: row for row in csv.DictReader(handle)}

        self.assertEqual(set(rows), set(EXPECTED))
        for metric, expected in EXPECTED.items():
            row = rows[metric]
            self.assertEqual(int(row["cases"]), 40)
            self.assertEqual(int(row["subjects"]), 37)
            self.assertEqual(int(row["folds_averaged_before_subject_inference"]), 5)
            self.assertEqual(row["estimand"], "subject_equal_paired_mean_difference")
            actual = tuple(
                float(row[column])
                for column in (
                    "mean_difference",
                    "bootstrap_ci_low",
                    "bootstrap_ci_high",
                    "permutation_p",
                    "wilcoxon_p_secondary",
                )
            )
            for observed, target in zip(actual, expected):
                self.assertAlmostEqual(observed, target, places=14)


if __name__ == "__main__":
    unittest.main()
