# BorderWise AI

**An AI-assisted cross-border financial compliance and transaction risk-screening prototype.**

BorderWise AI is a competition prototype demonstrating transaction intake, explainable rule-based risk screening, and reviewable demo transaction history. It is designed to explore how AI-assisted financial workflows could support human review.

> **Disclaimer:** This is a simulation-only prototype. It is not a production banking, payment, or regulatory compliance system. No real money is transferred.

## Live Demo

- **Live Application:** [BorderWise AI](https://borderwise-ai.onrender.com)
- **API Documentation:** [Swagger UI](https://borderwise-ai.onrender.com/docs)
- **Source Code:** [GitHub Repository](https://github.com/nusrat-ahmed/borderwise-ai)

Replace `REPLACE_WITH_YOUR_RENDER_URL` with your actual Render service URL, such as `https://your-service-name.onrender.com`. Use the same base URL for all three links.

**Note:** The live links will work only after the application has been successfully deployed to Render.

## Features

- Browser-based demo transaction workflow.
- FastAPI backend for transaction validation and risk screening.
- Transparent, rule-based risk indicators.
- Local SQLite demo transaction history.
- API endpoints for transaction preparation, risk assessment, history, and audit records.
- Automated API tests.
- Swagger UI for interactive API exploration.

## Technology Stack

- **Backend:** Python, FastAPI
- **Frontend:** HTML, CSS, JavaScript
- **Database:** SQLite for local demo records
- **Testing:** Pytest
- **API Documentation:** OpenAPI / Swagger UI
- **Deployment:** Render (when configured and successfully deployed)

See `requirements.txt` for dependencies.

## Run Locally on Windows

1. Install Python 3.11 or newer.
2. Open the project folder in Visual Studio Code.
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

6. Start the application using the project startup script:

   ```powershell
   .\START-HERE.bat
   ```

7. Open the local application at:

   `http://127.0.0.1:8000`

If the startup script is not suitable for your environment, use the project's documented Uvicorn command.

## API Endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/` | Application homepage |
| GET | `/api/health` | Health check |
| GET | `/api/demo-info` | Demo information |
| POST | `/api/risk/assess` | Assess transaction risk |
| POST | `/api/transactions/prepare` | Prepare a simulated transaction |
| GET | `/api/transactions` | Retrieve demo transaction history |
| GET | `/api/audit` | Retrieve audit events |

For request fields and response schemas, see the Swagger UI link above after deployment.

## Run Automated Tests

Activate the virtual environment and run:

```powershell
python -m pytest -v
```

The current local test run reported **12 passed**. Rerun the tests after code changes and update this result if the test suite changes.

## Security and Limitations

- Risk screening uses illustrative rules; it is not a trained machine-learning model.
- The prototype does not connect to real banks, payment networks, sanctions providers, or live exchange-rate services.
- No real money is transferred.
- Local SQLite records are for demonstration and are not a tamper-proof audit log.
- The prototype does not provide production-grade authentication, authorization, or regulatory certification.
- Risk thresholds are illustrative and may not be comparable across currencies without verified currency normalization.
- Do not submit real financial or personal data through this demo.
- Never commit API keys, passwords, access tokens, private customer information, virtual environments, or local database files.

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

## Project Status

**Competition prototype — under development.**

Local automated tests have passed in the current development environment. Public deployment, API availability, and live demo functionality should be verified independently before submission.

Contributions and constructive feedback are welcome.
