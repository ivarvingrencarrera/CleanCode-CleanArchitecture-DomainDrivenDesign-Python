from abc import ABC, abstractmethod


class HttpClient(ABC):
    @abstractmethod
    def get(self, url: str):
        pass

    @abstractmethod
    def post(self, url: str, body):
        pass
