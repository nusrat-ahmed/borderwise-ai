from .base import PaymentProvider
class DemoPaymentProvider(PaymentProvider):
    async def prepare_payment(self, payload: dict, idempotency_key: str) -> dict:
        return {"provider":"demo-simulator","provider_reference":"DEMO-"+idempotency_key[:12],
                "status":"simulated_pending_authorization","real_money_moved":False,
                "message":"Simulation only. No bank/payment network contacted."}
