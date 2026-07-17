from __future__ import annotations

import unittest
from pathlib import Path
import sys
from tempfile import TemporaryDirectory


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import verify_package
TITLE = (
    "Provenance-Audited Evaluation of Morphology-Based Pseudo-Label Filtering "
    "in CT Vertebra Segmentation: A Split-Controlled Case Study"
)


class RepositoryReleaseTests(unittest.TestCase):
    def test_text_manifest_hash_is_line_ending_independent(self) -> None:
        with TemporaryDirectory() as directory:
            root = Path(directory)
            lf = root / "lf.csv"
            crlf = root / "crlf.csv"
            lf.write_bytes(b"a,b\n1,2\n")
            crlf.write_bytes(b"a,b\r\n1,2\r\n")
            self.assertEqual(verify_package.canonical_payload(lf), verify_package.canonical_payload(crlf))
            self.assertEqual(verify_package.sha256(lf), verify_package.sha256(crlf))

    def test_gitignore_hash_is_line_ending_independent(self) -> None:
        with TemporaryDirectory() as directory:
            root = Path(directory)
            lf = root / "lf" / ".gitignore"
            crlf = root / "crlf" / ".gitignore"
            lf.parent.mkdir()
            crlf.parent.mkdir()
            lf.write_bytes(b".worktrees/\n")
            crlf.write_bytes(b".worktrees/\r\n")
            self.assertEqual(verify_package.canonical_payload(lf), verify_package.canonical_payload(crlf))
            self.assertEqual(verify_package.sha256(lf), verify_package.sha256(crlf))

    def test_package_files_excludes_linked_worktrees(self) -> None:
        with TemporaryDirectory() as directory:
            root = Path(directory)
            manifest = root / "manifest" / "files_sha256.csv"
            readme = root / "README.md"
            nested = root / ".worktrees" / "branch" / "README.md"
            readme.write_text("current\n", encoding="utf-8")
            nested.parent.mkdir(parents=True)
            nested.write_text("linked worktree\n", encoding="utf-8")
            files = verify_package.package_files(root=root, manifest=manifest)
            self.assertEqual([path.relative_to(root).as_posix() for path in files], ["README.md"])

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
