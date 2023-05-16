import json
from abc import ABC, abstractmethod


class CurrencyGateway(ABC):
    @abstractmethod
    async def get_currencies(self) -> json:
        pass
