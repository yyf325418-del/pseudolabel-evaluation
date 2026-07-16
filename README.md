# Provenance-Audited Evaluation of Morphology-Based Pseudo-Label Filtering in CT Vertebra Segmentation: A Split-Controlled Case Study

This repository contains the path-free inputs, executable analyses, statistical
outputs, figure source data, and provenance records supporting the manuscript.

## Primary result

The primary internal comparison is D175 minus D129 after averaging five folds
within each scan, repeated scans within each subject, and then giving all 37
subjects equal weight. The fixed evaluation set contains 40 scans from 37
subjects.

- Foreground Dice: `-0.00147066` (subject-bootstrap 95% CI
  `[-0.00382582, 0.00041475]`; paired sign-flip permutation `p=0.200350`).
- Identification rate: `-0.00554254` (95% CI
  `[-0.01901479, 0.00581167]`; `p=0.439852`).

These values are the manuscript's primary internal results. The earlier
40-scan and 200 case-fold analyses are retained under `data/legacy_case_level/`
for historical traceability and are not the primary estimand.

## Reproduce the primary analysis

```text
python -m pip install -r requirements.txt
python scripts/analysis/subject_equal_primary.py
python -m unittest discover -s tests -v
```

Optional path overrides use repository-neutral names:

```text
PSEUDOLABEL_INTERNAL37_INPUT
PSEUDOLABEL_PRIMARY_OUTPUT
PSEUDOLABEL_CALIBRATION_OUTPUT
```

Primary outputs are written to `data/internal37/outputs/`.

## Reproduce the design-specific calibration

```text
python scripts/analysis/subject_fold_calibration.py
```

The calibration uses the primary D175-D129 foreground-Dice residual matrix
(37 subjects x 5 folds), grand-mean centering, six injected shifts, 300
pseudo-experiments per shift, and 2,000 two-level bootstrap resamples per
pseudo-experiment. Detection means that the percentile 95% interval excludes
zero. The fixed seed is `20260716`. This is a design-specific sensitivity
calibration, not an equivalence test or a universal power analysis.

## Repository contents

- `data/internal37/`: primary subject-fold input, subject-level effects, and
  subject-equal statistics.
- `data/external42/`: complete 42-subject external validation, ROI sensitivity,
  and missing-label penalty analyses.
- `data/calibration/`: run-level and summary output for the reproducible primary
  residual calibration.
- `data/mechanism/`: endpoint-family statistics and multiplicity results.
- `data/provenance/`: checkpoint and fold-role provenance.
- `data/legacy_case_level/`: superseded case/fold analyses retained only for
  audit history.
- `figures/current/`: the five current manuscript figures; Fig. 4 uses the
  single reproducible D175-D129 calibration background.
- `figures/legacy_cmig/` and `docs/legacy_case_level/`: superseded materials
  retained only for provenance and not used by the current manuscript.
- `scripts/analysis/`: current primary analysis and calibration entry points.
- `tests/`: numerical and release-integrity checks.
- `manifest/files_sha256.csv`: generated file sizes and SHA-256 digests.

## Verify repository integrity

```text
python verify_package.py
```

The checksum manifest excludes itself and Git metadata.

## Data boundaries

No CT volumes, source annotations, DICOM files, model checkpoints, or prediction
masks are redistributed. VerSe and TotalSegmentator must be obtained from their
official repositories under their original terms. See
`THIRD_PARTY_DATA_LICENSES.md`.

The manuscript's merged-foreground Dice is not directly comparable with
published per-vertebra DSC values.

## Citation and release

Repository: https://github.com/yyf325418-del/pseudolabel-evaluation

Preferred software citation metadata are provided in `CITATION.cff`. Release
metadata for Zenodo are provided in `.zenodo.json`; no archive DOI is claimed
until Zenodo has minted and resolved it.

## Licence

Original software is licensed under the MIT License (`LICENSE-CODE`).
Author-generated tables, manifests, figure source data, and documentation are
licensed under CC BY 4.0 (`LICENSE-DATA`). Third-party datasets and materials
are excluded from these grants.
