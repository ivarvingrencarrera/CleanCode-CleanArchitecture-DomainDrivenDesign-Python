from abc import abstractmethod

from auth.src.domain.entity.user import User


class UserRepository:
    @abstractmethod
    async def save(self, user: User) -> None:
        pass

    @abstractmethod
    async def get(self, email: str) -> User:
        pass
