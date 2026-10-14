# BorderWise AI — Development Roadmap

This document lists possible improvements. They are future work unless verified in the implementation.

## 1. Validate the Demo

- Start the application locally.
- Test transaction submission, validation messages, risk results, and history.
- Run the automated test suite.
- Record the actual output and date in `TEST-REPORT.md`.

## 2. Improve Engineering Quality

- Add clearer API error handling and structured logging.
- Expand tests for boundary cases.
- Add configuration through environment variables where appropriate.
- Keep secrets out of source control.
- Add continuous integration to run tests on each change.

## 3. Improve Risk Explainability

- Document each rule, rationale, and limitation.
- Show which rules contributed to a result.
- Evaluate false positives and false negatives with synthetic cases.
- Do not present a rule-based score as a validated prediction.

## 4. Security and Privacy

- Use synthetic data only.
- Design authentication, authorization, encryption, retention, and audit controls before deployment.
- Obtain legal and compliance review before using real financial data.
- Never connect to real banking or payment infrastructure without authorization and a security review.

## 5. Possible Future Research

- Compare transparent rules with a properly evaluated machine-learning baseline.
- Create a synthetic dataset with documented assumptions.
- Measure precision, recall, false-positive rate, and false-negative rate.
- Document fairness, explainability, data quality, and model-drift risks.

## Scope

The current project is a demonstration prototype. Roadmap items are not current features unless implemented and verified.
