# Data dictionary

## `data/paired_filtering/all_case_fold_differences_sanitized.csv`

One row per evaluation case and fold (40 unique cases across five folds; 200
rows). `D129` is the unfiltered pseudo-label training condition and `D175` is
the train-only confidence-filtered condition. Difference columns are D175 minus
D129. Dice is binary foreground Dice; identification rate is the fraction of
reference vertebral labels identified under the study definition. Filesystem
paths present in the internal export were removed.

## `data/paired_filtering/selected_cases_summary_sanitized.csv`

Four cases displayed in the qualitative figure. `role` records the selection
purpose, and metric/difference columns use the same definitions as the complete
case-fold table. The internal `case_dir` field was removed.

## `provenance/qualitative_selected_cases_provenance_sanitized.csv`

Path-free provenance for the four qualitative cases: case role, identifier,
fold, comparison, checkpoint basename, TTA status, prediction-set directory
names, Dice, and identification-rate values. Raw CT, mask, centroid, and server
paths are omitted.

## `data/calibration/residual_background_calibration_full.csv`

Eighteen rows: three empirical residual backgrounds by six injected effect
sizes (`delta`). `observed_mean_diff` and `observed_sd_diff` describe each
background. `mean_estimate` and the median confidence limits summarize the
simulation output. `detection_rate_ci_excludes_zero` is the fraction of
simulation runs whose interval excluded zero. The plotted x-axis is categorical.

## `data/pseudo_quality/d129_pseudo_quality_audit.csv`

One row per pseudo-labeled training case (70 rows). Columns include morphology-
based confidence components, historical and recomputed scores, binary Dice,
macro label Dice, label counts, and the indicator `kept_at_0p80`. These quality
metrics are distinct from the historical D134/D129 identification-rate result.

## Other tables

- `data/literature/literature_positioning_table_source.csv`: literature values,
  metric definitions, and comparability notes used for positioning only.
- `data/supplementary/`: source tables corresponding to Supplementary Tables
  S2 and S4-S8.
- `data/calibration/residual_background_calibration_main_text.csv`: compact
  three-row main-text summary.
- `data/calibration/figure_QA.json`: automated checks produced with the final
  calibration figure.

## Imported server supplement

- `data/paired_filtering/server_export/d129_d175_case_fold_eval_long.csv`:
  model-long input with 400 rows (two models, five folds, 40 cases).
- `data/paired_filtering/server_export/d129_d175_primary_paired_long.csv`:
  paired 200-row D129/D175 table used by the primary statistical script.
- `data/paired_filtering/server_export/d129_d175_primary_statistics.csv`:
  fold-level, case-averaged, and two-way case-fold bootstrap summaries for Dice
  and identification rate.
- `data/paired_filtering/server_export/d129_d175_primary_provenance_verified.json`:
  package-side verification provenance binding the archived input checksum,
  imported script checksum, compatible environment, and independent numerical
  verification.
- `data/pseudo_quality/server_export/confidence_scores_path_sanitized.csv`:
  frozen 70-case historical confidence output; only absolute mask paths were
  replaced with portable `pseudo_masks/<filename>` paths.
- `manifest/study/case_fold_role_manifest.csv`: 2,431 case-fold-role rows across
  the recorded datasets and folds.
- `manifest/study/pseudo_generation_72_to_70_manifest.csv`: candidate/input/
  output accounting for the 72-to-70 pseudo-label transition.
- `manifest/study/fixed_verse_external40_manifest.csv`: the fixed 40-case
  external evaluation set with portable project-root placeholders.

These files contain the final Fold 3/4 results used by the manuscript.
