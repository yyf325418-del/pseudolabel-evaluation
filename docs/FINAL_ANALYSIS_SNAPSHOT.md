# Final analysis snapshot

This repository snapshot supports the manuscript titled:

> Provenance-Audited Evaluation of Morphology-Based Pseudo-Label Filtering in
> CT Vertebra Segmentation: A Split-Controlled Case Study

## Primary internal estimand

The primary internal comparison is the subject-equal paired arithmetic mean
difference (D175 minus D129). Five fold-specific predictions are averaged
within each scan, repeated scans are averaged within subject, and all 37
subjects receive equal weight.

- Foreground Dice: `-0.0014706567567567468`; subject-bootstrap 95% CI
  `[-0.0038258230405405227, 0.00041474628378378447]`; paired mean sign-flip
  permutation `p=0.20034979965020036`.
- Identification rate: `-0.005542535135135135`; subject-bootstrap 95% CI
  `[-0.019014789594594593, 0.005811671486486485]`; paired mean sign-flip
  permutation `p=0.43985156014843985`.

The fixed internal evaluation contains 40 scans from 37 subjects. The
case-equal and two-way case-fold analyses from the earlier repository version
are retained under `data/legacy_case_level/` but are not manuscript-primary.

## Design-specific calibration

The active calibration uses only the observed 37-subject-by-five-fold
D175-minus-D129 foreground-Dice matrix. After grand-mean centering, shifts of
`0`, `0.001`, `0.003`, `0.005`, `0.010`, and `0.020` are injected. Each shift
uses 300 pseudo-experiments and 2,000 subject-and-fold bootstrap replicates per
pseudo-experiment with seed `20260716`. Detection means that the percentile
95% interval excludes zero. This is not an equivalence test or a universal
power analysis.

## Source-of-record files

- `data/internal37/outputs/primary_statistics.csv`
- `data/internal37/outputs/subject_level_effects.csv`
- `data/calibration/subject_fold_calibration_summary.csv`
- `data/calibration/subject_fold_calibration_runs.csv`
- `data/external42/`
- `data/mechanism/`
- `data/provenance/`

Run `python verify_package.py` to validate the numerical locks, release
metadata, active-directory wording, and the SHA-256 manifest.
