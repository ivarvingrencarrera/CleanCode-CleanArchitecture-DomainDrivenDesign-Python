from abc import ABC, abstractmethod
from datetime import datetime

from auth.src.domain.entity.user import User


class TokenGenerator(ABC):
    @abstractmethod
    def generate(self, user: User, expiration: int, issued_at: datetime) -> str:
        pass

    @abstractmethod
    def verify(self, token: str) -> dict:
        pass
