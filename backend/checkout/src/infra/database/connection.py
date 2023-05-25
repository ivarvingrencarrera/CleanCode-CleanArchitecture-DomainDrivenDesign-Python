from abc import ABC, abstractmethod


class Connection(ABC):
    @abstractmethod
    async def disconnect(self) -> None:
        pass

    @abstractmethod
    async def insert(self, query: str) -> None:
        pass

    @abstractmethod
    async def select_all(self, query: str, *params) -> list[list]:
        pass

    @abstractmethod
    async def select_one(self, query: str, *params) -> list:
        pass
