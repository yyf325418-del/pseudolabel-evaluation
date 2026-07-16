# JIIM Manuscript–Repository Consistency Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make the JIIM manuscript and public `pseudolabel-evaluation` repository reproduce and report the same 37-subject primary analysis, replace the unsupported three-background calibration with a fully executable primary calibration, and satisfy the identified JIIM submission requirements.

**Architecture:** The July server audit is the immutable evidence source. A clean GitHub clone receives path-free primary inputs, deterministic analysis/calibration scripts, tests, licences, and release metadata. A separate copy of the submission package consumes only those verified outputs to regenerate figures and Word/PDF artifacts; repository and manuscript verification scripts enforce cross-layer agreement.

**Tech Stack:** Python 3, NumPy, pandas, SciPy, matplotlib, python-docx, PyMuPDF, Pillow, pytest/unittest, Git, Word PDF export.

---

### Task 1: Prepare isolated working copies

**Files:**
- Create: `D:/桌面/yyf3/pseudolabel-evaluation/`
- Create: `D:/桌面/yyf3/JIIM_Submission_20260716_ConsistencyFixed/`
- Preserve: `D:/桌面/yyf3/JIIM_Submission_20260716_Revised/`

- [ ] **Step 1: Clone the current public repository**

Run:

```powershell
git clone https://github.com/yyf325418-del/pseudolabel-evaluation.git <WORKSPACE>/pseudolabel-evaluation
```

Expected: clean `main` branch at the current public commit.

- [ ] **Step 2: Create a feature branch**

Run:

```powershell
git -C <WORKSPACE>/pseudolabel-evaluation switch -c codex/jiim-consistency
```

Expected: active branch `codex/jiim-consistency`.

- [ ] **Step 3: Copy the current submission package**

Copy `JIIM_Submission_20260716_Revised` to `JIIM_Submission_20260716_ConsistencyFixed`, excluding generated QA contact sheets that will be rebuilt.

- [ ] **Step 4: Record clean baselines**

Run repository integrity verification and the manuscript `verify_outputs.py`. Save the outputs under the new package's `qa/baseline/` directory.

### Task 2: Add failing repository consistency tests

**Files:**
- Create: `D:/桌面/yyf3/pseudolabel-evaluation/tests/test_primary_subject_equal.py`
- Create: `D:/桌面/yyf3/pseudolabel-evaluation/tests/test_repository_release.py`

- [ ] **Step 1: Write the primary-result test**

The test reads `data/internal37/outputs/primary_statistics.csv` and asserts:

```python
EXPECTED = {
    "foreground_dice": (-0.0014706567567567468, -0.0038258230405405227, 0.00041474628378378447, 0.20034979965020036),
    "identification_rate": (-0.005542535135135135, -0.019014789594594593, 0.005811671486486485, 0.43985156014843985),
}
```

It also asserts 40 cases, 37 subjects, five folds, subject-equal estimand, and signs matching the manuscript.

- [ ] **Step 2: Write the release-language test**

The test scans active README/documentation for stale title text, `CMIG_BOOTSTRAP_OUTPUT`, pre-release promises, and an unsupported claim of three subject-clustered residual backgrounds. It checks for `LICENSE`, `LICENSE-CODE`, `LICENSE-DATA`, `CITATION.cff`, and `.zenodo.json`.

- [ ] **Step 3: Verify RED**

Run:

```powershell
python -m pytest tests/test_primary_subject_equal.py tests/test_repository_release.py -v
```

Expected: failures because `data/internal37`, release files, and corrected README do not yet exist.

### Task 3: Implement the 37-subject primary analysis

**Files:**
- Create: `data/internal37/subject_cluster_map.csv`
- Create: `data/internal37/d175_d129_dice_case_fold_residuals.csv`
- Create: `data/internal37/d175_d129_id_rate_case_fold_residuals.csv`
- Create: `data/internal37/subject_fold_metrics.csv`
- Create: `scripts/analysis/subject_equal_primary.py`
- Create: `data/internal37/outputs/primary_statistics.csv`
- Create: `data/internal37/outputs/subject_level_effects.csv`
- Create: `data/internal37/outputs/analysis_provenance.json`
- Move: `scripts/posthoc/paired_two_way_case_fold_bootstrap.py` to `scripts/legacy_case_level/paired_two_way_case_fold_bootstrap.py`
- Move: old primary case-level outputs to `data/legacy_case_level/`

- [ ] **Step 1: Extract path-free audited inputs**

Extract only the required subject mapping, residual matrices, subject-fold metrics, archived analysis script, and archived tests from `jiim_final_server_audit_20260715.tar.gz`. Do not add CT volumes, masks, predictions, checkpoints, logs, or machine-specific paths.

- [ ] **Step 2: Implement aggregation and inference**

`subject_equal_primary.py` will expose:

```python
def subject_equal_effects(case_ids, subject_ids, fold_effects): ...
def bootstrap_ci(differences, seed, repetitions=100_000): ...
def sign_flip_p(differences, seed, repetitions=1_000_000): ...
def run_analysis(input_dir, output_dir): ...
```

The implementation averages folds within scan, scans within subject, then gives all 37 subjects equal weight. It writes machine-readable outputs with the archived seeds and exact counts.

- [ ] **Step 3: Run the analysis**

Run:

```powershell
python scripts/analysis/subject_equal_primary.py
```

Expected: two primary rows and 74 subject-level metric rows.

- [ ] **Step 4: Verify GREEN**

Run the primary-result test. Expected: all subject-equal assertions pass.

- [ ] **Step 5: Preserve legacy analysis without primary wording**

Move old case/fold outputs and update their provenance metadata so they are explicitly named `legacy_case_level` and never selected by the README quick-start command.

### Task 4: Rebuild the primary small-effect calibration with TDD

**Files:**
- Create: `tests/test_subject_fold_calibration.py`
- Create: `scripts/analysis/subject_fold_calibration.py`
- Create: `data/calibration/subject_fold_calibration_runs.csv`
- Create: `data/calibration/subject_fold_calibration_summary.csv`
- Create: `data/calibration/subject_fold_calibration_provenance.json`

- [ ] **Step 1: Write the calibration tests**

Tests assert:

```python
DELTAS = [0.0, 0.001, 0.003, 0.005, 0.010, 0.020]
SIMULATIONS_PER_DELTA = 300
BOOTSTRAP_REPETITIONS = 2_000
SEED = 20260716
```

They require 1,800 run rows, six summary rows, a 37x5 source matrix, zero-centered residual mean within `1e-15`, deterministic repeated output, and detection defined exactly as `ci_low > 0 or ci_high < 0`.

- [ ] **Step 2: Verify RED**

Run the calibration test. Expected: failure because the script and outputs are absent.

- [ ] **Step 3: Implement the simulation**

The script will load D129/D175 foreground Dice from `subject_fold_metrics.csv`, pivot to the 37x5 paired matrix, center the grand mean, resample rows and fold columns, inject each delta, and calculate two-level percentile intervals.

- [ ] **Step 4: Generate run and summary files**

Run:

```powershell
python scripts/analysis/subject_fold_calibration.py
```

Expected: deterministic long-form and summary CSV files plus provenance metadata.

- [ ] **Step 5: Verify GREEN and deterministic rerun**

Run the test, hash both output CSVs, rerun the script, and confirm hashes are unchanged.

### Task 5: Correct repository documentation, licences, and release metadata

**Files:**
- Modify: `README.md`
- Modify: `data_dictionary.md`
- Modify: `THIRD_PARTY_DATA_LICENSES.md`
- Create: `LICENSE`
- Create: `LICENSE-CODE`
- Create: `LICENSE-DATA`
- Replace: `CITATION.cff.template` with `CITATION.cff`
- Replace: `zenodo_metadata.json.template` with `.zenodo.json`
- Modify: `requirements.txt`
- Modify: `verify_package.py`
- Modify: `manifest/files_sha256.csv`
- Add: `docs/superpowers/specs/2026-07-16-jiim-repository-manuscript-consistency-design.md`

- [ ] **Step 1: Rewrite the README around the verified primary analysis**

Lead with the exact manuscript title, the two 37-subject estimates, the primary quick-start command, calibration command, output locations, external42 scope, and legacy-analysis boundary.

- [ ] **Step 2: Add dual licensing**

`LICENSE-CODE` contains the MIT text and 2026 copyright attribution to the authors. `LICENSE-DATA` applies CC BY 4.0 to author-generated tables, manifests, figure source data, and documentation. `LICENSE` maps file categories and excludes third-party material.

- [ ] **Step 3: Finalize citation/archive metadata**

Use the four supplied authors, current title, version `1.0.0`, release date `2026-07-16`, repository URL, and no fabricated DOI.

- [ ] **Step 4: Strengthen package verification**

`verify_package.py` will check checksums, required release files, primary statistics, calibration row counts, stale strings, and repository-relative paths.

- [ ] **Step 5: Regenerate checksums and verify GREEN**

Regenerate `manifest/files_sha256.csv`, run all repository tests plus `verify_package.py`, and require exit code 0.

### Task 6: Add failing manuscript editorial checks

**Files:**
- Modify: `D:/桌面/yyf3/JIIM_Submission_20260716_ConsistencyFixed/scripts/verify_outputs.py`

- [ ] **Step 1: Add checks for the review findings**

The verifier will require:

- article type exactly `Hypothesis-driven Research`;
- both consent statements;
- body citations covering references 1-19, expanding numeric ranges;
- narrative mentions of Tables 1-5 and Figs. 1-5 in consecutive order, excluding captions;
- a Methods subsection describing six deltas, 300 simulations, 2,000 bootstrap resamples, detection definition, and seed;
- one-background Figure 4 source-data agreement;
- no stale repository title, three-background claim, or case-level primary numbers;
- accurate AI wording;
- existing anonymity, abstract-length, format, and page checks.

- [ ] **Step 2: Verify RED**

Run `verify_outputs.py`. Expected: failures for missing references [3]-[8], missing figure/table mentions, missing calibration Methods, consent, and article type.

### Task 7: Modify the manuscript builder and redraw Figure 4

**Files:**
- Modify: `D:/桌面/yyf3/JIIM_Submission_20260716_ConsistencyFixed/scripts/build_submission.py`
- Copy: repository calibration CSVs into `source_data/`
- Generate: `figures/Fig4.*` and `figures/Figure_4_calibration_penalty.*`
- Generate: full/blinded manuscripts, supplements, and cover letter

- [ ] **Step 1: Replace hard-coded calibration curves**

Read `subject_fold_calibration_summary.csv` and draw one D175-D129 line in panel (a). Retain panel (b) from the verified external42 penalty CSV. Save PNG, PDF, EPS, and TIFF.

- [ ] **Step 2: Add the calibration Methods subsection**

Insert subsection 2.7 with all prespecified simulation details and renumber the AI subsection to 2.8.

- [ ] **Step 3: Repair Introduction citations**

Add [3-7] to vertebra-method context and [8] to the reproducibility paragraph. Add a restrained RIDGE alignment sentence in Discussion.

- [ ] **Step 4: Repair all narrative cross-references**

Add sequential references for Table 1/Fig. 1 through Table 5/Fig. 5 in narrative paragraphs, not captions.

- [ ] **Step 5: Correct front matter and availability text**

Use the exact article type, add both consent statements, preserve ethics and funding, keep the verified OpenAI ChatGPT/Codex disclosure, and describe the versioned repository without inventing a DOI or ORCID.

- [ ] **Step 6: Regenerate all Word artifacts**

Run `build_submission.py`; expected output includes updated full/blinded manuscripts, supplements, cover letter, figure files, and source-data copies.

- [ ] **Step 7: Verify GREEN**

Export PDFs and run `verify_outputs.py`. Expected: all new and existing checks pass.

### Task 8: Render and visually inspect every document page

**Files:**
- Generate: `qa/rendered/*.pdf`
- Generate: `qa/rendered/pages/*_contact_*.png`

- [ ] **Step 1: Export Word files to PDF**

Export full manuscript, blinded manuscript, full/blinded supplement, and cover letter individually.

- [ ] **Step 2: Render page contact sheets**

Use the document renderer or PyMuPDF pipeline to render all pages.

- [ ] **Step 3: Inspect every page at readable scale**

Check title page, Methods insertion, every table/figure, captions, Discussion, declarations, references, blind identity removal, blank pages, clipping, and pagination.

- [ ] **Step 4: Correct layout defects and rerun QA**

Any change to text, figures, tables, or OOXML triggers a full rebuild, PDF export, verifier run, and page review.

### Task 9: Commit, tag, and publish the repository update

**Files:**
- Commit all verified repository changes
- Tag: `v1.0.0`

- [ ] **Step 1: Review the complete diff**

Run `git status`, `git diff --check`, and inspect every renamed/deleted file. Confirm no CT data, masks, checkpoints, credentials, local absolute paths, or temporary outputs are included.

- [ ] **Step 2: Run fresh final verification**

Run the full repository test suite, package verifier, manuscript verifier, and hash-stability test in the same turn. All must exit 0.

- [ ] **Step 3: Commit**

Commit with message:

```text
Align JIIM manuscript with subject-equal reproducibility analysis
```

- [ ] **Step 4: Tag the verified release**

Create annotated tag `v1.0.0` describing the subject-equal JIIM submission package.

- [ ] **Step 5: Push through authenticated GitHub access**

Push the verified branch, fast-forward `main` only if remote authentication and branch policy permit it, then push `v1.0.0`. If authentication or branch protection blocks the push, preserve the local commit and report the exact command/error without claiming the public repository changed.

- [ ] **Step 6: Report Zenodo action separately**

After the GitHub release is public, the author must connect or refresh Zenodo and mint the DOI. Update the manuscript availability statement only after the DOI resolves; do not invent or prepopulate it.
