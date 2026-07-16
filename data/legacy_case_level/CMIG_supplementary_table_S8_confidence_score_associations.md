# Supplementary Table S8. Confidence-score associations with pseudo-label quality measures

Moved from the main text to reduce table density. The main text retains the key qualitative conclusion from this audit.

| Audit metric | Pearson r (p) | Spearman rho (p) | Below-threshold mean | Retained mean | Group p | Interpretation |
| --- | --- | --- | --- | --- | --- | --- |
| Binary foreground Dice | -0.135 (0.2646) | -0.064 (0.5998) | 0.9739 | 0.9586 | 0.0065 | Below-threshold cases were not lower quality by binary Dice. |
| Macro label Dice | +0.162 (0.1791) | +0.386 (0.0010) | 0.8639 | 0.8388 | 0.5702 | Threshold status did not identify lower macro-Dice cases. |
| Label-count error | +0.148 (0.2224) | +0.007 (0.9563) | 0.57 | 1.44 | 0.0260 | Below-threshold cases had fewer count errors in this audit. |
| Label-set Jaccard | +0.225 (0.0609) | +0.448 (0.0001) | 0.8881 | 0.8797 | 0.9921 | Threshold status did not identify lower label-set agreement. |
| Label-set recall | -0.023 (0.8471) | +0.074 (0.5400) | 1.0000 | 0.9992 | 0.7751 | Recall was near one in both groups. |
