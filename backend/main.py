from __future__ import annotations

import json
import os
import sqlite3
from contextlib import asynccontextmanager
from datetime import datetime, timezone
from pathlib import Path
from uuid import uuid4

from fastapi import FastAPI, Header, HTTPException, Request
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from .providers.demo import DemoPaymentProvider
from .schemas import PaymentRequest

ROOT = Path(__file__).resolve().parent.parent
DB = Path(os.getenv("BORDERWISE_DB_PATH", ROOT / "borderwise_demo.sqlite3"))
provider = DemoPaymentProvider()


def db() -> sqlite3.Connection:
    connection = sqlite3.connect(DB, timeout=10)
    connection.row_factory = sqlite3.Row
    return connection


def init_db() -> None:
    DB.parent.mkdir(parents=True, exist_ok=True)
    with db() as connection:
        connection.execute(
            """CREATE TABLE IF NOT EXISTS transactions(
                id TEXT PRIMARY KEY,
                idem TEXT UNIQUE,
                created TEXT,
                payload TEXT,
                risk TEXT,
                provider TEXT,
                status TEXT
            )"""
        )
        connection.execute(
            """CREATE TABLE IF NOT EXISTS audit(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                created TEXT,
                correlation TEXT,
                event TEXT,
                txid TEXT,
                details TEXT
            )"""
        )


@asynccontextmanager
async def lifespan(_: FastAPI):
    init_db()
    yield


app = FastAPI(
    title="BorderWise AI API",
    version="1.1.0-demo",
    description="Explainable student-finance prototype; simulation only.",
    lifespan=lifespan,
)


@app.middleware("http")
async def security_headers(request: Request, call_next):
    correlation_id = request.headers.get("X-Correlation-ID") or str(uuid4())
    response = await call_next(request)
    response.headers.update(
        {
            "X-Correlation-ID": correlation_id,
            "X-Content-Type-Options": "nosniff",
            "X-Frame-Options": "DENY",
            "Referrer-Policy": "no-referrer",
            "Cache-Control": "no-store",
            "Content-Security-Policy": "default-src 'self'; style-src 'self' 'unsafe-inline'; script-src 'self'; connect-src 'self'",
        }
    )
    return response


app.mount("/static", StaticFiles(directory=str(ROOT / "frontend")), name="static")


@app.get("/")
def home():
    return FileResponse(ROOT / "frontend" / "index.html")


def audit(correlation_id: str, event: str, transaction_id: str | None, details: dict) -> None:
    with db() as connection:
        connection.execute(
            "INSERT INTO audit(created,correlation,event,txid,details) VALUES(?,?,?,?,?)",
            (
                datetime.now(timezone.utc).isoformat(),
                correlation_id,
                event,
                transaction_id,
                json.dumps(details, ensure_ascii=False),
            ),
        )


def assess_risk(payment: PaymentRequest) -> dict:
    """Transparent demo rules. This is not a trained AI or production fraud model."""
    score = 0
    reasons: list[str] = []
    amount = payment.amount
    recipient = payment.recipient_name.casefold().strip()
    purpose = payment.purpose.casefold().strip()

    if amount >= 5000:
        score += 35
        reasons.append("Amount is high under the demo policy (AUD-equivalent threshold).")
    elif amount >= 1500:
        score += 15
        reasons.append("Amount exceeds the demo review threshold.")

    if recipient in {"unknown", "test mismatch", "unverified recipient"}:
        score += 45
        reasons.append("Recipient matches a demo unverified-recipient marker.")

    if purpose not in {"tuition", "university fee", "education"}:
        score += 10
        reasons.append("Purpose is outside the configured education-payment examples.")

    if not reasons:
        reasons.append("No configured demo rule was triggered.")

    score = min(score, 100)
    decision = "block_demo" if score >= 70 else "review" if score >= 30 else "allow_demo"
    return {
        "decision": decision,
        "score": score,
        "reasons": reasons,
        "disclaimer": "Transparent demo rules only; not a real or trained fraud model.",
    }


def transaction_to_dict(row: sqlite3.Row) -> dict:
    return {
        "id": row["id"],
        "status": row["status"],
        "created_at": row["created"],
        "payload": json.loads(row["payload"]),
        "risk": json.loads(row["risk"]),
        "provider": json.loads(row["provider"]),
    }


@app.get("/api/health")
def health():
    return {"status": "ok", "mode": "simulation", "real_money_moved": False}


@app.get("/api/demo-info")
def demo_info():
    return {
        "mode": "simulation",
        "provider": "demo-simulator",
        "live_banking_enabled": False,
        "risk_engine": "explainable-rule-based-demo",
        "real_money_moved": False,
    }


@app.post("/api/risk/assess")
def risk_assess(payment: PaymentRequest):
    """Evaluate a sample payment without saving a transaction or calling a provider."""
    return {"mode": "simulation", "risk": assess_risk(payment), "real_money_moved": False}


@app.post("/api/transactions/prepare", status_code=201)
async def prepare(
    payment: PaymentRequest,
    request: Request,
    idempotency_key: str = Header(..., alias="Idempotency-Key", min_length=8, max_length=100),
):
    payload_json = payment.model_dump_json()
    with db() as connection:
        old = connection.execute("SELECT * FROM transactions WHERE idem=?", (idempotency_key,)).fetchone()
    if old:
        if json.loads(old["payload"]) != payment.model_dump():
            raise HTTPException(
                status_code=409,
                detail="This Idempotency-Key was already used with a different payload. Use a new key for a new request.",
            )
        return transaction_to_dict(old)

    risk = assess_risk(payment)
    transaction_id = "BW-" + uuid4().hex[:16].upper()
    provider_result = await provider.prepare_payment(payment.model_dump(), idempotency_key)
    status = "prepared_demo" if risk["decision"] == "allow_demo" else "needs_review"
    created = datetime.now(timezone.utc).isoformat()

    try:
        with db() as connection:
            connection.execute(
                "INSERT INTO transactions VALUES(?,?,?,?,?,?,?)",
                (
                    transaction_id,
                    idempotency_key,
                    created,
                    payload_json,
                    json.dumps(risk, ensure_ascii=False),
                    json.dumps(provider_result),
                    status,
                ),
            )
    except sqlite3.IntegrityError:
        # A concurrent request may have claimed this idempotency key first.
        with db() as connection:
            old = connection.execute("SELECT * FROM transactions WHERE idem=?", (idempotency_key,)).fetchone()
        if old and json.loads(old["payload"]) == payment.model_dump():
            return transaction_to_dict(old)
        raise HTTPException(status_code=409, detail="Idempotency-Key conflict. Retry with a new key.")

    audit(
        request.headers.get("X-Correlation-ID", "not-provided"),
        "TRANSACTION_PREPARED_DEMO",
        transaction_id,
        {"risk_decision": risk["decision"], "risk_score": risk["score"], "status": status},
    )
    return {
        "id": transaction_id,
        "status": status,
        "created_at": created,
        "payload": payment.model_dump(),
        "risk": risk,
        "provider": provider_result,
    }


@app.get("/api/transactions")
def transactions():
    with db() as connection:
        rows = connection.execute("SELECT * FROM transactions ORDER BY created DESC LIMIT 100").fetchall()
    return {"items": [transaction_to_dict(row) for row in rows], "mode": "simulation"}


@app.get("/api/audit")
def get_audit():
    with db() as connection:
        rows = connection.execute("SELECT * FROM audit ORDER BY id DESC LIMIT 100").fetchall()
    return {
        "items": [
            {
                "id": row["id"],
                "created_at": row["created"],
                "correlation_id": row["correlation"],
                "event_type": row["event"],
                "transaction_id": row["txid"],
                "details": json.loads(row["details"]),
            }
            for row in rows
        ],
        "mode": "simulation",
    }
