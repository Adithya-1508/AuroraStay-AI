# Data Platform: Data Quality Framework

This document details the quantitative quality indicators calculated for ingested datasets.

## Quality Indicators

1. **Completeness**:
   - Assesses the proportion of non-null attributes inside key fields (e.g. email, phone, dates).
   - Target: $\ge 98\%$ completeness score.
2. **Uniqueness**:
   - Assesses uniqueness constraint rates on email profiles and booking primary codes.
   - Target: $100\%$ uniqueness score.
3. **Validity**:
   - Assesses check rates against logical constraints (costs $\ge 0$, score $\in [1, 5]$, date chronological correctness).
   - Target: $100\%$ validity score.
4. **Overall Score**:
   - Represents the aggregate weighted average score of completeness, uniqueness, and validity metrics.
