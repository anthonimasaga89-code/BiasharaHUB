from abc import ABC, abstractmethod


class PaymentProvider(ABC):
    @abstractmethod
    async def initiate(self, amount: float, phone: str | None, reference: str) -> dict:
        raise NotImplementedError

    @abstractmethod
    async def verify(self, reference: str) -> dict:
        raise NotImplementedError
