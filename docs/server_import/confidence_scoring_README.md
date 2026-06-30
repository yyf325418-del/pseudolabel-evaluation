# Confidence scoring materials

`score_pseudo_case_confidence.py` is classified as the historical
score-generation script because its timestamp precedes the frozen
`confidence_scores.csv` output and its output schema matches the
70-case table.

The repository CSV preserves all numerical values. Only local absolute
mask paths were replaced by portable relative paths.

The threshold-based quality audit is a downstream analysis and should
not be described as part of the original score-generation command.
