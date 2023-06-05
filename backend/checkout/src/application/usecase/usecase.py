from abc import ABC, abstractmethod


class UseCase(ABC):
    @abstractmethod
    async def execute(self, input_data: dict) -> dict:
        pass