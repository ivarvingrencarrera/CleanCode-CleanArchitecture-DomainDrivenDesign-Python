from abc import ABC, abstractmethod
from collections.abc import Callable


class CLIHandler(ABC):
    def __init__(self) -> None:
        self.commands = {}

    def on(self, command: str, callback: Callable):
        self.commands[command] = callback

    async def type(self, text: str):
        command, *params = text.split(' ')
        if command not in self.commands:
            return
        params = ' '.join(params).strip()

        await self.commands[command](params)

    @abstractmethod
    def write(self, text):
        pass
