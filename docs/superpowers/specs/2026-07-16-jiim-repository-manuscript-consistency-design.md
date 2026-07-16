# JIIM Manuscript–Repository Consistency Design

Date: 2026-07-16

## Objective

Produce a submission package and public reproducibility repository in which the manuscript, README, executable analyses, machine-readable outputs, figure source data, and release metadata report the same subject-equal results. The work preserves the audited July 2026 estimand: D175 minus D129, five folds averaged within scan, repeated scans averaged within subject, and 37 internal subjects receiving equal weight.

## Source of truth

The July server audit is authoritative for the manuscript's primary numbers. The required inputs are the archived `mean_estimand_statistics.py`, its tests, the 40-case-to-37-subject mapping, fold-specific D129/D175 effects, and the verified subject-level statistics. The June GitHub case-level/two-way-case-fold analysis remains available only as a clearly labelled legacy sensitivity analysis and is not called primary.

The following locked internal results must agree everywhere:

- Foreground Dice mean difference: -0.0014706567567567468; 95% CI [-0.0038258230405405227, 0.00041474628378378447]; paired sign-flip permutation p = 0.20034979965020036.
- Identification-rate mean difference: -0.005542535135135135; 95% CI [-0.019014789594594593, 0.005811671486486485]; paired sign-flip permutation p = 0.43985156014843985.
- Internal cohort: 40 scans, 37 subjects, 5 folds.

## Repository design

The public repository will be updated in place and versioned as release `v1.0.0` after verification.

### Primary analysis

Create a dedicated subject-equal analysis entry point under `scripts/analysis/`. It will read path-free CSV inputs committed under `data/internal37/`, reproduce the two locked endpoint rows, and write primary statistics and subject-level effects under `data/internal37/outputs/`. The script will use 100,000 subject bootstrap replicates, 1,000,000 paired sign-flip permutations, and the archived seeds. Tests will verify subject counts, aggregation order, exact point estimates, confidence intervals within the archived numerical tolerance, and deterministic p values.

The old `paired_two_way_case_fold_bootstrap.py` and its outputs will move to a `legacy_case_level/` namespace. README text will explain that these analyses weight scans or case-fold observations rather than independent subjects and are retained only for historical traceability.

### Reproducible small-effect calibration

Figure 4(a) will be replaced by one fully reproducible calibration curve based only on the primary D175-D129 foreground-Dice residual background. Unsupported D162-D119 and D129-D119 curves will be removed because their raw subject-by-fold inputs are not present in the final audit archive.

The calibration script will:

1. Construct a 37-subject by 5-fold D175-minus-D129 foreground-Dice matrix from the archived subject-fold table, after repeated scans have been averaged within subject for each fold.
2. Center the empirical matrix by subtracting its grand mean.
3. Inject systematic shifts of 0, 0.001, 0.003, 0.005, 0.010, and 0.020 Dice.
4. For each shift, generate 300 pseudo-experiments by resampling 37 subject rows and five fold columns with replacement.
5. For each pseudo-experiment, calculate a two-level percentile 95% confidence interval from 2,000 independent subject-and-fold bootstrap resamples.
6. Define detection as a confidence interval that excludes zero.
7. Use seed 20260716 and write every setting, estimate, interval, and detection indicator to a long-form CSV, plus a six-row summary CSV.

The calibration is explicitly design-specific, ancillary, and not an equivalence test or a universal power analysis. Tests will verify deterministic output, 300 runs per effect, empirical centering, output schema, and exact figure-to-CSV agreement.

### Metadata and licensing

- `LICENSE-CODE`: MIT License for original software.
- `LICENSE-DATA`: CC BY 4.0 notice and official licence link for author-generated tables, figure source data, manifests, and documentation.
- `LICENSE`: dual-licensing map that excludes third-party datasets, images, annotations, checkpoints, and masks.
- Replace `CITATION.cff.template` with a valid `CITATION.cff` using the supplied four authors, current manuscript title, repository URL, and version 1.0.0.
- Replace `zenodo_metadata.json.template` with `.zenodo.json` containing complete creator, title, description, keyword, licence-map, and related-dataset metadata, but no invented DOI.
- Retain `THIRD_PARTY_DATA_LICENSES.md` and make its exclusions explicit.
- Regenerate the repository SHA-256 manifest after all renames and outputs.

### Repository language and naming

The README title will exactly match the manuscript title: `Provenance-Audited Evaluation of Morphology-Based Pseudo-Label Filtering in CT Vertebra Segmentation: A Split-Controlled Case Study`.

README lead results will be the two locked subject-equal estimates. `CMIG_BOOTSTRAP_OUTPUT`, `CMIG_` filenames, “Gains” framing, pre-release promises, and obsolete 40-case external statements will be removed or moved into explicitly historical documentation. Environment variables will use the `PSEUDOLABEL_` prefix.

## Manuscript design

Work in a new package, `JIIM_Submission_20260716_ConsistencyFixed`, preserving the previous package unchanged.

### Methods and Figure 4

Insert `2.7 Design-specific small-effect calibration` immediately after statistical analysis and renumber the generative-AI section to 2.8. The new subsection will state the residual construction, centering, injected shifts, 300 pseudo-experiments per shift, 2,000 nested bootstrap replicates, subject/fold resampling, detection definition, seed, and design-specific interpretation boundary.

Redraw Figure 4(a) from the generated primary calibration summary CSV. Figure 4(b) will continue to show the four documented missing-label penalty schemes. The caption will identify panel (a) as the D175-D129 subject-by-fold calibration and will not imply support from unarchived residual backgrounds.

### Citations and cross-references

- Cite references [3]-[7] in the Introduction paragraph describing vertebra localisation, identification, segmentation, transformers, anatomical consistency, and compact 3D U-Net approaches.
- Cite RIDGE [8] in the Introduction and Discussion, mapping the repository audit to reproducibility, integrity, dependability, generalisability, and efficiency without claiming complete RIDGE compliance.
- Add narrative, consecutive citations for Tables 1-5 and Figs. 1-5. A citation occurring only inside another figure caption does not satisfy this requirement.
- Keep the existing reference numbering and bibliography entries.

### Declarations and article type

- Use `Article type: Hypothesis-driven Research`.
- Add `Consent to participate: Not applicable.` and `Consent for publication: Not applicable.` to the title-page declarations.
- Retain the existing ethics explanation for secondary analysis of public de-identified datasets.
- State the actual disclosed tools as OpenAI ChatGPT and Codex only; no other tool will be invented.
- Do not invent ORCID identifiers. The title page will omit ORCID until authors provide verified identifiers.

### Availability wording

The Data and Code Availability statements will name the versioned GitHub repository and enumerate the available subject mapping, subject-level effects, primary statistics, calibration run table, penalty sensitivity, figure source data, and scripts. They will not claim a Zenodo DOI until one has been minted. The release tag is an interim stable version; Zenodo deposition remains an author-account action after the public release is pushed.

## Validation gates

The work is complete only if all gates pass:

1. A clean checkout reproduces the two internal primary rows within locked tolerance.
2. README, manuscript abstract, Results, Table 4, repository primary CSV, and generated verification report contain identical signs and rounded values.
3. The calibration script regenerates its run-level CSV, summary CSV, and Figure 4(a) deterministically.
4. No `CMIG_BOOTSTRAP_OUTPUT`, stale manuscript title, “Small Pseudo-Label Gains”, pre-release promise, or unsupported three-background calibration claim remains in active repository documentation.
5. References [1]-[19] are all cited in the manuscript body, including [3]-[8].
6. Tables 1-5 and Figs. 1-5 are each cited in narrative text in consecutive order.
7. Consent statements, exact article type, accurate AI disclosure, title-page declarations, anonymous-version checks, and 150-250-word abstract checks pass.
8. Full and blinded Word files, supplements, cover letter, figures, PDFs, and contact sheets render without blank pages, overlap, clipping, or identity leakage.
9. Repository licences, `CITATION.cff`, `.zenodo.json`, third-party exclusions, checksums, and release version validate.
10. Git changes are committed only after repository tests and document QA pass; push occurs only through authenticated GitHub access.

## Scope boundary

This work does not invent ORCID identifiers, mint a Zenodo DOI without the author's Zenodo account, upload third-party CT data or annotations, retrain models, or alter the locked experimental results. It repairs reproducibility, reporting, release metadata, and submission formatting around the completed analyses.
