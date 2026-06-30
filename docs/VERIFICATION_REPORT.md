# Server supplement verification report

Verification performed on 2026-06-30 before merging the server supplement into
the reproducibility package.

## Import integrity

- All 21 entries in the supplied `SHA256SUMS.txt` matched their source files.
- Twenty-two source files were imported; the additional file is the supplied
  checksum list itself.
- `manifest/server_supplement_import.csv` maps every original relative path to
  its package destination and records the original SHA-256 digest.
- No raw CT, NIfTI, DICOM, checkpoint, or model-weight files were present.
- No machine-specific absolute filesystem paths were found in imported text
  files. Portable `<PROJECT_ROOT>` placeholders were retained.

## Primary bootstrap reproduction

The imported `paired_two_way_case_fold_bootstrap.py` was independently executed
against
`data/paired_filtering/server_export/d129_d175_case_fold_eval_long.csv` using:

- Python 3.10.19
- NumPy 2.2.6
- pandas 2.3.3
- SciPy 1.15.3
- 100,000 bootstrap repetitions
- seed 20260629

The verification execution passed the script's regression checks. All four CSV
outputs were row-for-row and numerically equivalent to the imported server
outputs within `1e-12`. Byte hashes differed because the local pandas version
serialized equivalent floating-point values with different text precision.

The repository verification record
`d129_d175_primary_provenance_verified.json` binds the archived CSV, imported
script, environment, and successful numerical verification.
