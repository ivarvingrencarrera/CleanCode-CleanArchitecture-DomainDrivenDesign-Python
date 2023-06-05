from abc import ABC, abstractmethod


class AuthGateway(ABC):
    @abstractmethod
    async def verify(token: str) -> bool:
        pass
