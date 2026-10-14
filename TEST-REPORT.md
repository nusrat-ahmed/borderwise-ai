# Test Report

## Test Scope

The automated tests in `tests/test_api.py` exercise selected API behavior and validation paths for the local competition prototype.

## Run the Tests

Activate the project's virtual environment, install dependencies from `requirements.txt`, and run:

```powershell
python -m pytest -q
```

## Reporting Results

Record the actual output from the current code version. Do not reuse an earlier test count after changing code without rerunning the suite.

Passing tests provide evidence only for the cases covered. They do not establish production readiness, regulatory compliance, security certification, or correctness for every possible input.

## Manual Checks

Before presenting the demo, verify:
- The application starts without errors.
- The home page and static assets load.
- A synthetic transaction can be submitted.
- Validation and risk-screening results are displayed clearly.
- Demo history behaves as expected.
- Invalid inputs produce understandable responses.
- No real personal or financial information is used.

## Scope Limits

This report does not represent a penetration test, independent security audit, or validation against live banking systems.
