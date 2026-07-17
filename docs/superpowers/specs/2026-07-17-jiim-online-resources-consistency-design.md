# JIIM Online Resources and Cross-Artifact Consistency Design

## Objective

Prepare a submission-ready JIIM package in which the manuscript, supplementary
PDF, source-data archive, cover letter, repository outputs, and submission
instructions use the same provenance scope and statistical values.

## Approved packaging

The submission will use two supplementary files:

1. `Online_Resource_1.pdf`: the publication-ready textual supplement. It will
   be generated from the full, non-blinded supplement because supplementary
   files are intended for publication as submitted. The retained DOCX may stay
   in the working package for regeneration, but the submission instructions
   will identify the PDF as the file to upload.
2. `Online_Resource_2.zip`: a machine-readable reproducibility archive
   containing source-data CSV/JSON/Markdown files, the server audit archive and
   checksum, evidence ledger, figure contracts, builder/verifier scripts, and a
   concise archive README. The ZIP must not contain another redundant copy of
   itself.

The manuscript will cite both resources in the Methods. The captions supplied
to the submission system will be recorded in `README_SUBMISSION.md`.

## Manuscript changes

- Add to the end of Section 2.2: “Full checkpoint manifests and secondary
  endpoint, ROI, and missing-label penalty analyses are provided in Online
  Resource 1. Machine-readable source data and the server audit archive are
  provided in Online Resource 2.”
- Preserve the existing article type, title, endpoint hierarchy, conclusions,
  and removal of the generative-AI statement.
- Report the current primary-ROI penalized-HD95 permutation result using the
  primary mean-estimand analysis: full precision `0.9925290074709925`, displayed
  as `p=0.993`.

## Online Resource 1 changes

- Expand Supplementary Table S1 from the 15 D119/D129/D175 rows to all 27
  selected checkpoints in the audited manifest.
- Use human-readable model labels such as `D119 full-supervised`, `D129
  unfiltered`, and `D175 paired filtering` while preserving fold, train/validation
  counts, checkpoint type, and SHA-256 prefix.
- Replace program-like cohort and penalty labels with publication-facing text.
- In Table S4, rename the final column to `Direction reversed vs conditional
  result`, display `Yes`/`No`, and define `Yes` in a table note.
- In Table S4, use the primary-analysis penalized-HD95 permutation value for the
  current 1.0x ROI-diagonal row so that it matches the manuscript and source of
  record.
- In Table S5, use columns `Penalty family`, `Evaluated penalty`, `Break-even`,
  and `Difference at evaluated penalty`; distinguish `1.0x ROI diagonal` from
  `100 mm`.
- Replace references to an unspecified `source_data directory` or `server
  archive` with explicit references to Online Resource 2.

## Cover letter changes

- Replace “The revised analysis does not overstate a computational advance”
  with the approved contribution paragraph beginning “The principal
  contribution is an auditable evaluation pattern rather than a new filtering
  algorithm.”
- Remove the footer page number while keeping the one-page layout.

## Statistical source-of-record rule

The discrepancy arose because two scripts performed one-million-draw sign-flip
Monte Carlo tests with different seeds. The primary mean-estimand output is the
source of record for the primary endpoint table. Its penalized-HD95 value is
`0.9925290074709925`, displayed as `0.993`.

To prevent future drift:

- the repository and submission-package primary statistics CSV retain full
  precision;
- the current-penalty row used in the supplementary display is resolved to that
  primary value;
- README prose, manuscript tables, supplement tables, and figure source data
  must use the same rounded display;
- verification must fail if either `0.992` is displayed for this primary result
  or the full-precision source-of-record value is absent.

## Verification and acceptance criteria

- Main full and blinded manuscripts explicitly cite Online Resources 1 and 2.
- Online Resource 1 is a readable PDF with no clipping, broken tables, orphaned
  table notes, or single-character wrapping artifacts.
- Supplementary Table S1 contains exactly 27 checkpoint rows and covers every
  audited `paper_role`.
- The manuscript and supplement display penalized-HD95 permutation `p=0.993`;
  machine-readable source data retain `0.9925290074709925`.
- `Online_Resource_2.zip` opens successfully, contains a README and checksum
  evidence, and excludes patient images, annotations, model checkpoints, and
  prediction masks.
- The cover letter contains no “revised analysis” phrase and no footer page
  number.
- Full and blinded DOCX files pass structural checks; all generated PDFs have no
  blank pages and pass page-by-page visual inspection.
- The existing no-AI-disclosure requirement remains enforced.

## Out of scope

- No model retraining, new inference, or recomputation of clinical endpoints.
- No change to the manuscript's scientific conclusions or endpoint hierarchy.
- No upload to the JIIM portal; the package will only be prepared locally.
