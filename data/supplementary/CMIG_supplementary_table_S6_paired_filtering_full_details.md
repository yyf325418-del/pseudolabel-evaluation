# Supplementary Table S6. Full paired filtering details

Consolidated from the legacy component tables. The main manuscript now reports a compact cluster-aware summary.

# S6a. Fold-wise Dice effect

| Fold | Cases | Student-8+PL70 Dice | Filtered Student-8+PL Dice | Delta Dice |
| --- | --- | --- | --- | --- |
| 0 | 40 | 0.9260 | 0.9247 | -0.0013 |
| 1 | 40 | 0.9259 | 0.9259 | +0.0000 |
| 2 | 40 | 0.9231 | 0.9205 | -0.0026 |
| 3 | 40 | 0.9250 | 0.9254 | +0.0003 |
| 4 | 40 | 0.9273 | 0.9263 | -0.0011 |
| Mean +/- SD | - | 0.9255 +/- 0.0016 | 0.9245 +/- 0.0024 | -0.0009 +/- 0.0012 |

# S6b. Fold-wise identification-rate effect

| Fold | Cases | Student-8+PL70 ID rate | Filtered Student-8+PL ID rate | Delta ID |
| --- | --- | --- | --- | --- |
| 0 | 40 | 0.9435 | 0.9503 | +0.0068 |
| 1 | 40 | 0.9597 | 0.9564 | -0.0033 |
| 2 | 40 | 0.9472 | 0.9371 | -0.0101 |
| 3 | 40 | 0.9226 | 0.9371 | +0.0144 |
| 4 | 40 | 0.9571 | 0.9576 | +0.0005 |
| Mean +/- SD | - | 0.9460 +/- 0.0147 | 0.9477 +/- 0.0101 | +0.0017 +/- 0.0094 |

# S6c. Cluster-aware sensitivity analyses

| Analysis scale | Metric | Unit / n | Mean diff. (D175-D129) | Wilcoxon p | Paired t p | Bootstrap 95% CI |
| --- | --- | --- | --- | --- | --- | --- |
| Fold-level paired means | Dice | 5 folds | -0.000934 | 0.3125 | 0.1472 | Descriptive only (n = 5 folds) |
| Case-averaged paired differences | Dice | 40 cases | -0.000934 | 0.1744 | 0.1854 | -0.002363 to +0.000305 |
| Two-way case-fold bootstrap | Dice | 200 case-fold observations | -0.000934 | Not estimated | Not estimated | -0.002966 to +0.000985 |
| Fold-level paired means | Identification rate | 5 folds | +0.001666 | 0.8125 | 0.7123 | Descriptive only (n = 5 folds) |
| Case-averaged paired differences | Identification rate | 40 cases | +0.001666 | 0.9811 | 0.7726 | -0.008973 to +0.013187 |
| Two-way case-fold bootstrap | Identification rate | 200 case-fold observations | +0.001666 | Not estimated | Not estimated | -0.012857 to +0.019653 |
