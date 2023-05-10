from abc import ABC, abstractmethod


class CurrencyGateway(ABC):
    @abstractmethod
    async def get_currencies(self) -> None:
        pass
