from app.integrations.payments.base import PaymentProvider


class MockPaymentProvider(PaymentProvider):
    async def initiate(self, amount: float, phone: str | None, reference: str) -> dict:
        return {"status": "PENDING", "reference": reference, "amount": amount}

    async def verify(self, reference: str) -> dict:
        return {"status": "PENDING", "reference": reference}
