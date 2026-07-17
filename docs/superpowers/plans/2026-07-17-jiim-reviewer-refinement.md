# JIIM Reviewer Refinement Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Produce a new JIIM submission package whose manuscript wording, captions, table labels, reproducibility checks, and public repository match the approved 2026-07-17 refinement specification without changing scientific results.

**Architecture:** Copy the verified 2026-07-16 package to a new non-destructive 2026-07-17 package, strengthen its verifier first, then update the deterministic Word builder until the verifier passes. Export the generated Word files to PDF, render every page for visual QA, and finally synchronize the public repository README and SHA-256 manifest.

**Tech Stack:** Python 3, python-docx, PyMuPDF, Pillow, Matplotlib, Microsoft Word COM automation, PowerShell, Git, GitHub.

---

### Task 1: Create the isolated submission package

**Files:**
- Copy: `D:/桌面/yyf3/JIIM_Submission_20260716_ConsistencyFixed/`
- Create: `D:/桌面/yyf3/JIIM_Submission_20260717_ReviewerRefined/`
- Modify: `D:/桌面/yyf3/JIIM_Submission_20260717_ReviewerRefined/README_SUBMISSION.md`

- [ ] **Step 1: Copy the package without modifying the source**

Run:

```powershell
Copy-Item -LiteralPath 'D:\桌面\yyf3\JIIM_Submission_20260716_ConsistencyFixed' -Destination 'D:\桌面\yyf3\JIIM_Submission_20260717_ReviewerRefined' -Recurse
```

Expected: the destination exists and contains `scripts`, `manuscript`, `supplement`, `submission`, `figures`, `source_data`, and `qa`.

- [ ] **Step 2: Record source immutability evidence**

Run:

```powershell
Get-ChildItem -LiteralPath 'D:\桌面\yyf3\JIIM_Submission_20260716_ConsistencyFixed' -Recurse -File | Get-FileHash -Algorithm SHA256 | Export-Csv -LiteralPath 'D:\桌面\yyf3\JIIM_Submission_20260717_ReviewerRefined\qa\source_package_sha256_before.csv' -NoTypeInformation -Encoding UTF8
```

Expected: `qa/source_package_sha256_before.csv` contains one row per source-package file.

- [ ] **Step 3: Update the package identity text**

Modify `README_SUBMISSION.md` so its heading is `# JIIM reviewer-refined submission package — 2026-07-17` and every deliverable filename ends in `20260717`.

- [ ] **Step 4: Confirm no source files changed**

Run the same source hash command to `qa/source_package_sha256_after.csv`, then compare `Hash` and source-relative `Path` values.

Expected: no differences.

### Task 2: Make the manuscript verifier encode the approved wording

**Files:**
- Modify: `D:/桌面/yyf3/JIIM_Submission_20260717_ReviewerRefined/scripts/verify_outputs.py:96-100`
- Modify: `D:/桌面/yyf3/JIIM_Submission_20260717_ReviewerRefined/scripts/verify_outputs.py:180-260`

- [ ] **Step 1: Point validation at the 20260717 deliverables**

Replace the five DOCX paths and four rendered PDF paths with:

```python
full = PKG / "manuscript" / "JIIM_Manuscript_Full_20260717.docx"
blind = PKG / "manuscript" / "JIIM_Manuscript_Blinded_20260717.docx"
supp_full = PKG / "supplement" / "JIIM_Online_Resource_1_Full_20260717.docx"
supp_blind = PKG / "supplement" / "JIIM_Online_Resource_1_Blinded_20260717.docx"
cover = PKG / "submission" / "JIIM_Cover_Letter_20260717.docx"
```

- [ ] **Step 2: Add exact positive checks**

Add required checks for these strings:

```python
refinement_checks = {
    "article_type": "Article type: Hypothesis-driven research" in full_text,
    "running_title": "Running title: Provenance audit of pseudo-label filtering" in full_text,
    "abstract_filter_specific": "Small performance changes attributed to pseudo-label filtering can be confounded" in full_text,
    "teacher_checkpoint": "A supervised teacher checkpoint generated 70 pseudo labels" in full_text,
    "surrogate_wording": "cannot be used as a surrogate for" in full_text,
    "internal_identifiers": "D129 and D175 are internal model identifiers" in full_text,
    "tiny_label_definition": "fewer than 400 voxels" in full_text,
    "score_weights": all(term in full_text for term in ["weight 0.15", "indices (0.35)", "continuity (0.20)", "occupancy (0.20)", "size score (0.10)"]),
    "fold_resampling_rationale": "five fold-specific model estimates" in full_text,
    "observed_residual_caption": "under the observed D175–D129 foreground-Dice residual background" in full_text,
    "table5_title_case": all(term in full_text for term in ["Foreground Dice", "Macro-label Dice", "Label-set Jaccard"]),
    "controlled_split_wording": "controlled this source of split variation" in full_text,
    "sagittal_caption": "Representative sagittal CT views" in full_text,
    "reference8_nlm_abbreviation": "J Imaging Inform Med. 2025;38:2524-2536" in full_text,
    "foreground_dice_term": "merged-foreground Dice" not in full_text,
    "contrast_en_dash": all(term in full_text for term in ["D175–D129", "D134–D129"]),
}
```

Merge `refinement_checks` into the failure-producing check dictionary.

- [ ] **Step 3: Add negative regression checks**

Require absence of:

```python
superseded_phrases = [
    "Article type: Hypothesis-driven Research",
    "Running title: Calibrated pseudo-label evaluation",
    "Small pseudo-label effects can be confounded",
    "A fully supervised teacher generated",
    "used as shorthand for",
    "fraction of very small labels",
    "single reproducible D175−D129",
    "removed this split confounding",
    "Matched qualitative examples from the D175−D129 comparison",
    "J Digit Imaging Inform Med",
    "merged-foreground Dice",
    "D175-D129",
    "D134-D129",
]
```

- [ ] **Step 4: Run the verifier and confirm the expected red state**

Run:

```powershell
python scripts/verify_outputs.py
```

Expected: failure because the copied 20260716 documents and old manuscript wording do not satisfy the new checks.

### Task 3: Update the deterministic manuscript builder

**Files:**
- Modify: `D:/桌面/yyf3/JIIM_Submission_20260717_ReviewerRefined/scripts/build_submission.py:289-644`
- Test: `D:/桌面/yyf3/JIIM_Submission_20260717_ReviewerRefined/scripts/verify_outputs.py`

- [ ] **Step 1: Update identifiers, article type, and abstract**

Use these exact values:

```python
RUNNING = "Provenance audit of pseudo-label filtering"
```

```text
Article type: Hypothesis-driven research
Purpose: Small performance changes attributed to pseudo-label filtering can be confounded by data splits, repeated observations, teacher exposure, and endpoint definitions.
Methods: A supervised teacher checkpoint generated 70 pseudo labels from source scans that were visible during teacher training or validation but were not used as manual student supervision.
```

- [ ] **Step 2: Tighten Introduction and first model definition**

Replace `cannot be used as shorthand for` with `cannot be used as a surrogate for`.

Start the study-design paragraph with:

```text
The study compared an unfiltered student (D129) with a filtered student (D175); D129 and D175 are internal model identifiers.
```

- [ ] **Step 3: Make the morphology score reproducible**

Replace the vague score description with:

```text
The morphology score was computed from each pseudo-label mask rather than softmax probabilities. It combined label coverage (weight 0.15), the longest consecutive run of label indices (0.35), label continuity (0.20), mean largest-connected-component occupancy (0.20), and a size score (0.10), where the size score equaled one minus the fraction of vertebral labels containing fewer than 400 voxels.
```

Keep the following sentence stating that the fixed filtering threshold was 0.80 and was not optimized on evaluation data.

- [ ] **Step 4: Explain fold resampling**

After the sentence describing independent subject and fold resampling, add:

```text
Fold resampling was included because the observed design contained five fold-specific model estimates.
```

- [ ] **Step 5: Correct Fig. 4, Table 5, Discussion, and Fig. 5 wording**

Use:

```text
Fig. 4(a): CI-exclusion rates under the observed D175–D129 foreground-Dice residual background
Discussion: Exact fold matching in D175 controlled this source of split variation.
Fig. 5: Representative sagittal CT views from matched D175–D129 qualitative examples.
```

Replace the Table 5 metric formatter with a map:

```python
endpoint_display = {
    "foreground_dice": "Foreground Dice",
    "identification_rate": "Identification Rate",
    "macro_label_dice": "Macro-label Dice",
    "label_set_jaccard": "Label-set Jaccard",
    "complete_label_set_indicator": "Complete-label-set Indicator",
    "missing_label_count": "Missing-label Count",
    "common_matched_hd95_mm": "Common-matched HD95 (mm)",
    "common_matched_assd_mm": "Common-matched ASSD (mm)",
    "hd95_penalized_mm": "Penalized HD95 (mm)",
    "assd_penalized_mm": "Penalized ASSD (mm)",
}
```

- [ ] **Step 6: Correct reference [8], endpoint terminology, typography, and display precision**

Use the NLM abbreviation in reference [8]:

```text
J Imaging Inform Med. 2025;38:2524-2536. doi:10.1007/s10278-024-01282-9.
```

Replace every manuscript use of `merged-foreground Dice` with `foreground Dice`.
Use `D175–D129` and `D134–D129` for human-readable model contrasts; retain
machine-readable underscore keys unchanged. Format negative numeric values with
the true minus sign `−`.

Add metric-aware display helpers:

```python
def display_number(value: str | float, digits: int) -> str:
    return f"{float(value):.{digits}f}".replace("-", "−")


def display_effect(metric: str, value: str | float) -> str:
    digits = 2 if metric.endswith("_mm") else 4
    return display_number(value, digits)
```

Use four decimals for Dice/rate/unitless effects, two decimals for distances
and break-even distances, and `p_text()` for three-decimal p values in the
Abstract, Results, Tables 3–5, and online resources. Keep source CSV files
unchanged.

- [ ] **Step 7: Rename generated deliverables and update the cover date**

Generate only:

```text
manuscript/JIIM_Manuscript_Full_20260717.docx
manuscript/JIIM_Manuscript_Blinded_20260717.docx
supplement/JIIM_Online_Resource_1_Full_20260717.docx
supplement/JIIM_Online_Resource_1_Blinded_20260717.docx
submission/JIIM_Cover_Letter_20260717.docx
```

Set the cover-letter date to `July 17, 2026`.

- [ ] **Step 8: Build and run textual validation**

Run:

```powershell
python scripts/build_submission.py
python scripts/verify_outputs.py
```

Expected after PDF export in Task 4: `VERIFY PASS`; before PDF export, only missing/stale rendered-PDF checks may remain.

### Task 4: Export and visually verify every document

**Files:**
- Create: `D:/桌面/yyf3/JIIM_Submission_20260717_ReviewerRefined/qa/rendered/JIIM_Manuscript_Full_20260717.pdf`
- Create: `D:/桌面/yyf3/JIIM_Submission_20260717_ReviewerRefined/qa/rendered/JIIM_Cover_Letter_20260717.pdf`
- Create: `D:/桌面/yyf3/JIIM_Submission_20260717_ReviewerRefined/supplement/JIIM_Online_Resource_1_Full_20260717.pdf`
- Create: `D:/桌面/yyf3/JIIM_Submission_20260717_ReviewerRefined/supplement/JIIM_Online_Resource_1_Blinded_20260717.pdf`
- Verify: `D:/桌面/yyf3/JIIM_Submission_20260717_ReviewerRefined/qa/pages/*.png`

- [ ] **Step 1: Export DOCX to fresh temporary PDFs with Word COM**

Open each DOCX with Word automation, call `ExportAsFixedFormat(..., 17)`, close without saving, then quit Word. Export to new `_new.pdf` paths to avoid overwriting locked files.

- [ ] **Step 2: Atomically replace target PDFs**

Use `Copy-Item -Force` from each `_new.pdf` to its final target and remove only the temporary `_new.pdf` after checking the resolved paths are inside the new package.

- [ ] **Step 3: Run the full verifier**

Run:

```powershell
python scripts/verify_outputs.py
```

Expected: `VERIFY PASS`, no blank or near-blank pages, no prohibited phrase hits, no blinded identity leaks, and a refreshed `qa/generated_file_manifest.csv`.

- [ ] **Step 4: Inspect every generated contact sheet**

Open all `qa/pages/main_contact_*.png`, `supplement_full_contact_*.png`, `supplement_blinded_contact_*.png`, and `cover_contact_*.png`.

Expected: no clipped text, overlap, broken glyphs, blank pages, stranded captions, missing repeated table headers, or unreadable Fig. 1/Fig. 4/Table 5/Fig. 5 captions.

### Task 5: Synchronize and verify the public repository

**Files:**
- Modify: `D:/桌面/yyf3/pseudolabel-evaluation/README.md`
- Modify: `D:/桌面/yyf3/pseudolabel-evaluation/manifest/files_sha256.csv`
- Create: `D:/桌面/yyf3/pseudolabel-evaluation/docs/superpowers/plans/2026-07-17-jiim-reviewer-refinement.md`

- [ ] **Step 1: Remove the active former-journal acronym from README**

Replace the active `figures/legacy_cmig/` mention with neutral wording such as `the archived legacy-figure directory`; do not rename or delete historical artifacts.

- [ ] **Step 2: Regenerate and verify the repository manifest**

Run:

```powershell
python verify_package.py --write-manifest
python -m unittest discover -s tests -v
python verify_package.py
git diff --check
```

Expected: 9 tests pass, every manifest entry verifies, and `git diff --check` emits no errors.

- [ ] **Step 3: Verify release files and public remote references**

Run:

```powershell
git ls-remote origin refs/heads/main refs/tags/v1.0.0
git status --short
```

Expected: both refs resolve; repository contains `LICENSE`, `README.md`, `CITATION.cff`, and the current data/code availability text.

- [ ] **Step 4: Commit the verified repository changes**

Run:

```powershell
git add README.md manifest/files_sha256.csv docs/superpowers/plans/2026-07-17-jiim-reviewer-refinement.md
git commit -m "Refine JIIM submission wording and repository guidance"
git push origin main
```

Expected: clean worktree and remote `main` at the new commit.

### Task 6: Final delivery audit

**Files:**
- Verify: `D:/桌面/yyf3/JIIM_Submission_20260717_ReviewerRefined/`
- Verify: `D:/桌面/yyf3/JIIM_Submission_20260716_ConsistencyFixed/`

- [ ] **Step 1: Re-run all package and repository checks from a clean state**

Run the manuscript verifier, repository unit tests, repository SHA-256 verifier, and `git diff --check` again.

Expected: all checks pass with fresh output.

- [ ] **Step 2: Compare source-package hashes**

Compare the before/after source hashes recorded in Task 1.

Expected: zero differences, proving the 20260716 package was not modified.

- [ ] **Step 3: Report exact deliverables**

Provide clickable absolute links to the new full manuscript, blinded manuscript, both online resources, cover letter, verification report, and package README. Report test counts, page counts, visual-QA result, repository commit, and any remaining author-only item without claiming an unverified ORCID or Zenodo DOI.
