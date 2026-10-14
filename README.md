# BorderWise AI

**An AI-assisted cross-border financial compliance and transaction risk-screening prototype.**

BorderWise AI demonstrates a workflow combining transaction intake, rule-based risk screening, and a reviewable demo history. It is an early-stage competition prototype, not a production banking or compliance system.

## Features

- Browser-based demo transaction workflow.
- Backend API for transaction validation and risk screening.
- Transparent, rule-based risk indicators.
- Local demo transaction history.
- Automated API tests.

## Technology

- Python backend with FastAPI
- HTML, CSS, and JavaScript frontend
- SQLite for local demo records
- Pytest for automated tests

See `requirements.txt` for dependencies.

## Run Locally on Windows

1. Install Python (Python 3.11 or newer is recommended).
2. Open this folder in Visual Studio Code.
3. Select **Terminal → New Terminal**.
4. Create and activate a virtual environment:

   ```powershell
   py -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

5. Install dependencies:

   ```powershell
   python -m pip install -r requirements.txt
   ```

6. Start the application:

   ```powershell
   .\START-HERE.bat
   ```

7. Open `http://127.0.0.1:8000` in your browser.

If PowerShell blocks activation, use Command Prompt or follow your local PowerShell policy. Do not change system-wide execution policy for this project.

## Run Tests

With the virtual environment activated and dependencies installed:

```powershell
python -m pytest -q
```

The automated tests are in `tests/`. Rerun the tests after changes before reporting results.

## Limitations

- Risk screening is rule-based; it is not a trained machine-learning model.
- The demo does not connect to a real bank, payment network, sanctions provider, or live exchange-rate service.
- No real money is transferred.
- Local SQLite records are for demonstration and are not a tamper-proof audit log.
- The prototype does not provide production-grade authentication, authorization, or regulatory certification.
- Thresholds are illustrative and may not be comparable across currencies unless currency normalization is implemented and verified.

## Security

- Never commit API keys, passwords, access tokens, private customer information, virtual environments, or local database files.
- Review `.gitignore` before pushing to a public repository.
- Use synthetic data only.
- Any real-world integration would require authorization, security and privacy controls, reliable data sources, and regulatory review.

## Project Structure

```text
.
├── backend/
├── frontend/
├── tests/
├── requirements.txt
├── START-HERE.bat
├── README.md
├── SECURITY-AND-BANK-INTEGRATION.md
└── TEST-REPORT.md
```

## Status

This is a competition prototype. Verify current features and test results against the code before submission.
