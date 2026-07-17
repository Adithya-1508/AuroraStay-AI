# Release Tagging & Promotion Guides

This document guides developers through publishing container images and deploying stable charts.

## 1. Version Semantics

We use standard Semantic Versioning rules:
- Major releases for breaking changes.
- Minor releases for features additions.
- Patch releases for bug fixes and configurations.

## 2. Promotions Pipeline

1. **Local Validation**: Ensure formatting, lints, and tests pass:
   ```bash
   python scripts/lint_all.py
   python -m pytest
   ```
2. **Apply Tag**:
   ```bash
   git tag -a v1.0.0 -m "Release Version 1.0.0"
   git push origin v1.0.0
   ```
3. **Pipeline Action**: Github actions builds Docker images, runs Trivy security checks, packages the Helm charts, and publishes outputs.
