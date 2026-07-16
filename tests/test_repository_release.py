from __future__ import annotations

import unittest
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import verify_package
TITLE = (
    "Provenance-Audited Evaluation of Morphology-Based Pseudo-Label Filtering "
    "in CT Vertebra Segmentation: A Split-Controlled Case Study"
)


class RepositoryReleaseTests(unittest.TestCase):
    def test_required_release_files_exist(self) -> None:
        for relative in ("LICENSE", "LICENSE-CODE", "LICENSE-DATA", "CITATION.cff", ".zenodo.json"):
            self.assertTrue((ROOT / relative).is_file(), f"missing {relative}")

    def test_readme_uses_current_title_and_primary_estimand(self) -> None:
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        self.assertIn(TITLE, readme)
        self.assertIn("37 subjects", readme)
        self.assertIn("-0.00147066", readme)
        self.assertIn("-0.00554254", readme)
        self.assertNotIn("CMIG_BOOTSTRAP_OUTPUT", readme)
        self.assertNotIn("Small Pseudo-Label Gains", readme)
        self.assertNotIn("will be added before", readme)

    def test_release_validator_finds_no_failures(self) -> None:
        self.assertEqual(verify_package.validate_release(), [])


if __name__ == "__main__":
    unittest.main()
