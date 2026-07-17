# JIIM reviewer-refinement design

Date: 2026-07-17

## Objective

Produce a new, non-destructive JIIM submission package that applies the
verified wording, table, caption, and reproducibility refinements requested on
2026-07-17. Preserve all numerical results, estimands, figures, cohort counts,
and scientific boundaries from the consistency-fixed 2026-07-16 package.

## Output boundary

- Source package: `JIIM_Submission_20260716_ConsistencyFixed`
- New package: `JIIM_Submission_20260717_ReviewerRefined`
- The source package must remain unchanged.
- Rebuild the full manuscript, blinded manuscript, full and blinded online
  resources, cover letter, figures, PDFs, QA report, and file manifest.

## Verified decisions

### Article type

Retain the journal's official category and normalize its capitalization to:

`Article type: Hypothesis-driven research`

Do not replace it with `Original Article`. The current JIIM Instructions for
Authors list “Hypothesis-driven research” under Types of Papers:
https://link.springer.com/journal/10278/submission-guidelines

### Canonical terminology

| Concept | Canonical form |
|---|---|
| Article type | Hypothesis-driven research |
| Running title | Provenance audit of pseudo-label filtering |
| Primary comparison | D175 minus D129 |
| Model identifiers at first use | D129 and D175, internal identifiers |
| Teacher | supervised teacher checkpoint |
| Filter threshold | fixed morphology-score threshold of 0.80 |
| Tiny vertebral label | fewer than 400 voxels |
| Calibration background | observed D175-minus-D129 foreground-Dice residual background |

## Manuscript changes

1. Replace the running title with `Provenance audit of pseudo-label filtering`.
2. In the Abstract, replace the generic small-effect opening with the specific
   statement that small performance changes attributed to pseudo-label
   filtering can be confounded.
3. Replace `fully supervised teacher` with `supervised teacher checkpoint`.
4. In the Introduction, replace `used as shorthand for` with `used as a
   surrogate for`.
5. At first Methods use, identify D129 and D175 as internal identifiers.
6. Define tiny labels as vertebral labels containing fewer than 400 voxels.
7. Report the archived morphology-score weights: 0.15 coverage, 0.35 longest
   consecutive run, 0.20 continuity, 0.20 mean largest-component occupancy,
   and 0.10 size score. Keep the later D175 filtering threshold of 0.80
   distinct from the score-generation components.
8. Explain that fold resampling was included because the observed calibration
   design contained five fold-specific model estimates.
9. Replace `single reproducible` in the Fig. 4 caption with wording tied to the
   observed residual background.
10. Convert Table 5 endpoint display labels to consistent biomedical title
    case, including `Foreground Dice`, `Macro-label Dice`, and `Label-set
    Jaccard`.
11. Replace the overstrong statement that fold matching `removed` split
    confounding with the bounded statement that it `controlled this source of
    split variation`.
12. Begin the Fig. 5 caption with `Representative sagittal CT views`.
13. Preserve the final Conclusion sentence without shortening it.

## Repository changes

- Verify that the remote repository is publicly readable and that `main` and
  the release tag resolve.
- Verify active README results, licensing, and data/code availability.
- Remove the last active README reference containing the former journal
  acronym. Historical material may remain only in explicitly legacy paths and
  must not be presented as current evidence.
- If repository text changes, regenerate the canonical SHA-256 manifest, run
  the full repository test suite, commit, and push only after verification.

## Regression checks

The manuscript verifier must require the new article-type capitalization,
running title, Abstract language, teacher wording, fold-resampling rationale,
400-voxel definition, score weights, Fig. 4 wording, Table 5 display labels,
bounded Discussion wording, Fig. 5 sagittal-view wording, and D175 internal-ID
definition. It must prohibit the superseded phrases.

Existing checks remain mandatory: 150–250-word abstract, all 19 references
cited, Figs. 1–5 and Tables 1–5 cited in order, blinded identity isolation,
single-background calibration, no superseded package artifacts, and no blank
rendered pages.

## Visual acceptance criteria

- Inspect every page of the full manuscript, both online resources, and cover
  letter after Word/PDF export.
- No clipped text, overlapping objects, stranded table captions, missing
  repeated table headers, broken glyphs, or blank pages.
- Recheck Fig. 1, Fig. 4, Table 5, and the revised Fig. 5 caption at readable
  scale.

## Non-goals

- No new experiments, model inference, retraining, statistics, endpoints, or
  references.
- No invented ORCID or Zenodo DOI.
- No conversion to `Original Article` unless the live submission portal itself
  presents that category and the authors choose it there.
- No tracked-changes manuscript for this initial JIIM submission.
