from abc import ABC, abstractmethod
from collections.abc import Callable


class HttpServer(ABC):
    @abstractmethod
    def on(self, url: str, callback: Callable) -> None:
        pass

    @abstractmethod
    def listen(self, port: int) -> None:
        pass
