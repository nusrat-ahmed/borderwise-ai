from abc import ABC, abstractmethod
class PaymentProvider(ABC):
    @abstractmethod
    async def prepare_payment(self, payload: dict, idempotency_key: str) -> dict:
        raise NotImplementedError
