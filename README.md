# Calibrated evaluation of small pseudo-label gains

This repository contains the data, provenance manifests, statistical outputs,
figure source files, and reproducibility scripts supporting the manuscript
**Calibrated Evaluation of Small Pseudo-Label Gains in CT Vertebra
Segmentation**.

The repository reports the final five-fold D129/D175 analysis. The primary
D175-minus-D129 binary foreground Dice difference was `-0.00093447` (two-way
case-fold bootstrap 95% CI `[-0.00296629, 0.00098474]`), and the identification-
rate difference was `0.00166567` (95% CI `[-0.01285747, 0.01965320]`).

## Repository contents

- `data/paired_filtering/`: final 40-case, five-fold paired results and primary
  statistical outputs.
- `data/pseudo_quality/`: 70-case pseudo-label confidence/quality audit and
  path-sanitized historical confidence output.
- `data/calibration/`: three-background small-effect calibration source data.
- `data/literature/`: literature-positioning table source.
- `data/supplementary/`: machine-readable supplementary tables.
- `manifest/study/`: dataset pool, fold-role, pseudo-generation, and fixed
  external-test manifests.
- `provenance/`: path-free provenance for selected qualitative cases.
- `figures/`: final main and supplementary manuscript figures.
- `scripts/`: figure generation, manifest construction, historical confidence
  scoring, and two-way case-fold bootstrap analysis.
- `manifest/files_sha256.csv`: repository file sizes and SHA-256 digests.

## Verify repository integrity

```text
python verify_package.py
```

The checksum manifest intentionally excludes itself.

## Python environment

```text
python -m pip install -r requirements.txt
```

The primary paired bootstrap script uses 100,000 repetitions and seed
`20260629`. Set `D129_D175_LONG_CSV` to
`data/paired_filtering/server_export/d129_d175_case_fold_eval_long.csv` and set
`CMIG_BOOTSTRAP_OUTPUT` to a writable output directory before running:

```text
python scripts/posthoc/paired_two_way_case_fold_bootstrap.py
```

The calibration figure script is self-contained. The qualitative figure and
historical confidence-scoring scripts require licensed source images or masks,
which are not redistributed here.

## Data boundaries

No raw CT volumes, source annotations, DICOM files, model checkpoints, or
prediction masks are included. VerSe and TotalSegmentator data must be obtained
from their official repositories under their respective licenses. See
`THIRD_PARTY_DATA_LICENSES.md`.

The manuscript value near `0.929` is binary foreground Dice after merging
vertebral labels. It is not directly comparable with published per-vertebra
DSC values.

## Citation and archive

Repository: https://github.com/yyf325418-del/pseudolabel-evaluation

`CITATION.cff.template` and `zenodo_metadata.json.template` will be completed
with the final author metadata and archive DOI before the submission release.

## License

A license for original code and derived research outputs will be added before
the repository is made public. Third-party materials retain their original
licenses.

