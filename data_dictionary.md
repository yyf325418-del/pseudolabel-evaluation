# Data dictionary

## Current primary analysis

### `data/internal37/subject_fold_metrics.csv`

One row per subject, fold, endpoint, and model after repeated scans have been
averaged within subject for that fold. `cases_aggregated` records whether a
subject contributed one or two scans. The table contains 37 subjects and five
folds. Current primary inference uses foreground Dice and identification rate.

### `data/internal37/outputs/subject_level_effects.csv`

One row per subject and primary endpoint. `fold0`-`fold4` are paired D175-minus-
D129 effects; `mean_difference` is the five-fold subject effect. Subjects, not
scans, are the independent inferential units.

### `data/internal37/outputs/primary_statistics.csv`

Two primary rows. The arithmetic mean gives all 37 subjects equal weight.
Confidence intervals resample subjects; p values use paired sign flips of the
mean. Wilcoxon p values are secondary rank-based summaries.

## Design-specific calibration

### `data/calibration/subject_fold_calibration_runs.csv`

One row for each of 1,800 pseudo-experiments: six injected effects multiplied
by 300 runs. Each row records the experiment mean, percentile interval,
detection indicator, sample dimensions, bootstrap repetitions, and seed.

### `data/calibration/subject_fold_calibration_summary.csv`

Six rows summarizing mean recovered effect, median confidence limits, and the
fraction of runs whose 95% interval excluded zero. The only residual background
is the primary D175-minus-D129 foreground-Dice matrix.

## External validation and mechanism endpoints

- `data/external42/external42_mean_estimand_statistics.csv`: paired results for
  all 42 eligible TotalSegmentator subjects under the primary ROI.
- `data/external42/external42_model_summary.csv`: five-fold ensemble summaries
  for D119, D129, D162, and D175.
- `data/external42/external42_penalty_sensitivity.csv`: paired penalized surface
  distances under alternative missing-label penalties.
- `data/external42/external42_penalty_break_even.csv`: penalty values at which
  paired penalized-distance means change sign.
- `data/external42/external42_roi_sensitivity.csv`: tight and loose ROI paired
  analyses.
- `data/mechanism/mechanism_endpoint_statistics.csv`: endpoint-family results,
  multiplicity adjustments, and favorable directions.
- `data/provenance/checkpoint_provenance_manifest.csv`: model, fold, checkpoint,
  training, validation, pseudo-generation, and evaluation provenance.

## Other retained data

- `data/pseudo_quality/`: path-sanitized pseudo-label quality audit.
- `data/literature/`: literature-positioning source values.
- `data/supplementary/`: current historical-context statistics.
- `data/legacy_case_level/`: superseded scan/fold analyses and three-background
  calibration artifacts retained only to document the earlier estimand.
- `manifest/study/`: historical dataset-role manifests. Files explicitly named
  `external40` describe the earlier 40-case audit and are not the current
  complete 42-subject external validation.

## Sign and unit conventions

All paired differences are D175 minus D129. Positive values favor D175 for
overlap, identification, completeness, and detection endpoints. Negative
values favor D175 for distances and missing-label counts. Distance units are
millimetres. Dice and rate endpoints are proportions unless a table explicitly
scales them to percentage points.

## Redistribution boundary

No raw CT volumes, annotations, prediction masks, DICOM files, or checkpoints
are included. Case identifiers and path-free derived outputs are retained so
that data pairing and aggregation can be audited without redistributing the
third-party image data.
