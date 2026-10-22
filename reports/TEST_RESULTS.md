# Test evidence

Executed locally on 2026-10-22 with Python 3.12, Streamlit 1.66.1, pandas 2.2.3 and pytest 9.1.1.

Command: `python -m pytest -q`

Result: **11 passed, 0 failed**.

Coverage includes domain calculations and edge cases, human-review gate validation, final-decision immutability, audit tamper detection, Streamlit startup and a project-specific UI interaction. Where optional local inference exists, its adapter is tested with a mock; no live-model performance is claimed.

`python -m portfolio.demo` completed successfully and regenerated JSON and SVG outputs. Initial UI tests exposed an entrypoint-path issue; it was corrected to resolve the app path relative to the test file before the passing run.

These are local test results. See the repository Actions tab for independently executed remote CI results; no remote pass is implied by this report.
