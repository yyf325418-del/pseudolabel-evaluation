# JIIM Online Resources and Cross-Artifact Consistency Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Produce a submission-ready JIIM package with a cited publication PDF, a reproducibility ZIP, a complete 27-checkpoint manifest, and one canonical penalized-HD95 permutation result across the manuscript, supplement, archive, and repository.

**Architecture:** Keep the existing deterministic package builder as the single document-generation entry point. Canonicalize the primary current-penalty statistics at the server-audit output layer, copy those outputs into the repository and submission package, and make the verifier enforce all cross-artifact contracts before rendering and visual review.

**Tech Stack:** Python 3, NumPy/Pandas/SciPy, python-docx, Microsoft Word PDF export, ZIP/TAR archives, PowerShell, Git.

---

## File map

- Modify `D:/桌面/yyf3/jiim_final_server_audit/03_penalty/penalty_sensitivity_external42.py`: allow a local audit root and reuse the primary-analysis bootstrap/permutation seeds for the primary 1.0x ROI-diagonal penalized-HD95 row.
- Regenerate `D:/桌面/yyf3/jiim_final_server_audit/03_penalty/penalty_sensitivity.csv` and its log/output evidence.
- Modify `D:/桌面/yyf3/JIIM_Submission_20260717_ReviewerRefined/scripts/build_submission.py`: manuscript resource citations, complete S1, readable S2-S5, canonical p value, cover-letter wording/footer, and resource packaging.
- Modify `D:/桌面/yyf3/JIIM_Submission_20260717_ReviewerRefined/scripts/verify_outputs.py`: add failing checks for the new contracts.
- Modify `D:/桌面/yyf3/JIIM_Submission_20260717_ReviewerRefined/README_SUBMISSION.md`: upload names and captions.
- Modify repository files under `data/external42/`, `data/provenance/`, and `README.md` only where generated statistics or submission-facing provenance guidance must be synchronized.
- Create `supplement/Online_Resource_1.pdf` and `supplement/Online_Resource_2.zip`.

### Task 1: Add failing package-contract verification

**Files:**
- Modify: `D:/桌面/yyf3/JIIM_Submission_20260717_ReviewerRefined/scripts/verify_outputs.py`

- [ ] **Step 1: Add assertions for the approved contracts**

Add checks equivalent to:

```python
assert "provided in Online Resource 1" in full_text
assert "provided in Online Resource 2" in full_text
assert "0.992" not in supplement_text
assert "0.993" in supplement_text
assert supplement_checkpoint_row_count == 27
assert "Direction reversed vs conditional result" in supplement_text
assert "Difference at evaluated penalty" in supplement_text
assert "The revised analysis" not in cover_text
assert (SUP / "Online_Resource_1.pdf").is_file()
assert (SUP / "Online_Resource_2.zip").is_file()
```

- [ ] **Step 2: Run the verifier and confirm the new checks fail before implementation**

Run:

```powershell
python scripts\verify_outputs.py
```

Expected: nonzero exit with missing Online Resource citations/files, incomplete 15-row S1, or old cover-letter wording.

### Task 2: Canonicalize the primary current-penalty analysis

**Files:**
- Modify: `D:/桌面/yyf3/jiim_final_server_audit/03_penalty/penalty_sensitivity_external42.py`
- Regenerate: `D:/桌面/yyf3/jiim_final_server_audit/03_penalty/penalty_sensitivity.csv`
- Regenerate: `D:/桌面/yyf3/jiim_final_server_audit/03_penalty/penalty_sensitivity_subject_effects.csv`

- [ ] **Step 1: Make the audit root portable**

Use an environment override while retaining the server default:

```python
import os
ROOT = Path(os.environ.get("JIIM_AUDIT_ROOT", "/home/sust/yyf/lunwen/verse-main"))
```

- [ ] **Step 2: Reuse the primary-analysis seeds for the canonical row**

For `variant == "primary"`, `penalty_scheme == "diagonal_1p00_current"`, and `metric == "hd95"`, set bootstrap seed `20260824` and permutation seed `20260825`; otherwise retain the existing deterministic row-index seed schedule.

- [ ] **Step 3: Regenerate the penalty outputs locally**

Run with `JIIM_AUDIT_ROOT=D:/桌面/yyf3` using the bundled Python runtime.

Expected canonical row:

```text
mean_difference=0.46455852521622004
bootstrap_ci_low=-0.6299318083632772
bootstrap_ci_high=2.3448129406707743
paired_sign_flip_permutation_p=0.9925290074709925
permutation_seed=20260825
```

- [ ] **Step 4: Verify the regenerated row matches the primary mean-estimand output exactly**

Compare the current-penalty row with `04_mean_estimand/external42_mean_estimand_statistics.csv` using a Python assertion for mean, CI, p value, repetition counts, and seeds.

### Task 3: Rebuild the manuscript, supplement, cover letter, and resource archive

**Files:**
- Modify: `D:/桌面/yyf3/JIIM_Submission_20260717_ReviewerRefined/scripts/build_submission.py`
- Modify: `D:/桌面/yyf3/JIIM_Submission_20260717_ReviewerRefined/README_SUBMISSION.md`
- Create/regenerate: package DOCX/PDF/ZIP deliverables

- [ ] **Step 1: Add manuscript resource citations**

Append the approved sentence to Section 2.2 in both full and blinded manuscripts and record both resource captions in `README_SUBMISSION.md`.

- [ ] **Step 2: Expand Table S1 to all 27 checkpoints**

Remove the three-role filter and map all nine roles to readable labels. Preserve fold, train/validation counts, checkpoint type, and 12-character SHA-256 prefix.

- [ ] **Step 3: Revise Tables S2-S5 and notes**

Map machine labels to readable cohort/penalty labels; use `Yes`/`No` plus the defined note in S4; source the current penalized-HD95 display from the primary statistics row; and restructure S5 into penalty family, evaluated penalty, break-even, and evaluated difference.

- [ ] **Step 4: Revise the cover letter**

Insert the approved contribution paragraph and disable the footer page number for the cover-letter document only.

- [ ] **Step 5: Build resource files**

Generate the working full/blinded supplement DOCX files, export the publication version as `Online_Resource_1.pdf`, and build `Online_Resource_2.zip` with source data, server archive/checksum, evidence ledger, figure contracts, builder/verifier scripts, and archive README.

- [ ] **Step 6: Run the package builder**

Expected: all DOCX files and resource archives are regenerated without exceptions.

### Task 4: Synchronize the public repository and archive evidence

**Files:**
- Modify: `D:/桌面/yyf3/pseudolabel-evaluation/data/external42/external42_penalty_sensitivity.csv`
- Verify: `D:/桌面/yyf3/pseudolabel-evaluation/data/external42/external42_mean_estimand_statistics.csv`
- Verify: `D:/桌面/yyf3/pseudolabel-evaluation/data/provenance/checkpoint_provenance_manifest.csv`
- Modify: `D:/桌面/yyf3/pseudolabel-evaluation/README.md`
- Regenerate: `D:/桌面/yyf3/pseudolabel-evaluation/manifest/files_sha256.csv`

- [ ] **Step 1: Copy the regenerated canonical CSV to the repository and submission package**

Use exact file copies from the audited output; do not hand-edit statistical digits.

- [ ] **Step 2: Add concise README provenance/resource guidance**

State that the 27-row checkpoint manifest is complete and that the primary current-penalty penalized-HD95 permutation result is `0.9925290074709925` (`p=0.993` for manuscript display).

- [ ] **Step 3: Rebuild audit archives and checksums**

Recreate the server TAR archive and its SHA-256 file, then rebuild `Online_Resource_2.zip` so all nested evidence reflects the canonical output.

- [ ] **Step 4: Run repository integrity checks**

Run:

```powershell
python verify_package.py
python -m unittest discover -s tests -v
```

Expected: both commands exit zero.

### Task 5: Render and visually inspect every publication-facing page

**Files:**
- Verify: full and blinded manuscript DOCX/PDF
- Verify: `supplement/Online_Resource_1.pdf`
- Verify: cover-letter DOCX/PDF

- [ ] **Step 1: Export fresh PDFs through Microsoft Word**

Export full manuscript, blinded manuscript, full supplement, blinded supplement, and cover letter after the final build.

- [ ] **Step 2: Render each PDF to page PNGs/contact sheets**

Use the existing verifier/render pipeline and ensure page counts are nonzero with no blank or near-blank pages.

- [ ] **Step 3: Inspect every page**

Check all pages at readable resolution for clipped text, broken/wrapped identifiers, table overflow, orphaned notes, footer remnants, missing figures, or unexpected blank areas. Rebuild and repeat if any defect is found.

### Task 6: Final cross-artifact verification and commits

**Files:**
- Verify all changed package and repository files

- [ ] **Step 1: Run the strengthened package verifier**

Run:

```powershell
python scripts\verify_outputs.py
```

Expected: `VERIFY PASS`, 27 checkpoint rows, both Online Resource citations and files, `p=0.993`, no AI-disclosure text, no blinded identity leaks, and no blank PDF pages.

- [ ] **Step 2: Inspect ZIP contents and checksums**

Open `Online_Resource_2.zip`, confirm every expected item, reject prohibited imaging/model binaries, and verify the TAR SHA-256 value.

- [ ] **Step 3: Run Git whitespace/status checks and commit repository changes**

Run:

```powershell
git diff --check
git status --short
```

Commit only the intended repository outputs, README, tests/verifier support, spec, and plan. Do not push unless separately authorized in the active request.
