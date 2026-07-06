# AI Platform: AI Evaluation & Regression Testing

This document details benchmark testing against golden datasets.

## Verification Mappings

Every evaluation run validates completions output accuracy:
- **`Golden Dataset`**:Mappable inputs with keyword validation assertions and minimum score targets.
- **`AIEvaluator`**:
  - Compares raw text completions against keyword lists.
  - Scores outputs based on keyword presence.
  - Generates benchmark reports outlining average score percentages and pass status.
