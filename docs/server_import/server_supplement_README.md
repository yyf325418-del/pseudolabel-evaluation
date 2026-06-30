# CMIG server supplement

This package supplements the existing manuscript reproducibility
archive with split manifests, the primary paired bootstrap analysis,
and the historical confidence-scoring implementation.

## Split-manifest generator

```bash
export VERSE_PROJECT_ROOT=/path/to/verse-main
export NNUNET_PREPROCESSED_ROOTS=/optional/root1:/optional/root2
export CMIG_MANIFEST_OUTPUT=/path/to/output/manifests
python scripts/posthoc/build_case_role_manifest.py
```

## Primary paired bootstrap

```bash
export VERSE_PROJECT_ROOT="$(pwd)"
export D129_D175_LONG_CSV="$(pwd)/data/derived/d129_d175_case_fold_eval_long.csv"
export CMIG_BOOTSTRAP_OUTPUT="$(pwd)/repository_outputs/derived_statistics"
python scripts/posthoc/paired_two_way_case_fold_bootstrap.py
```

## Confidence scoring

`score_pseudo_case_confidence.py` is the historical score-generation
script. The repository CSV preserves numerical values while replacing
local absolute mask paths with portable relative paths.

No CT, NIfTI mask, checkpoint, DICOM, or other image data are included.
