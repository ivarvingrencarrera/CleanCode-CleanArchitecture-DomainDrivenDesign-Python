from auth.src.application.repository.user_repository import UserRepository
from auth.src.domain.entity.user import User
from auth.src.infra.database.connection import Connection


class UserRepositoryDatabase(UserRepository):
    users = None

    def __init__(self, connection: Connection) -> None:
        self.connection = connection

    async def save(self, user: User) -> None:
        self.users = user

    async def get(self, email: str) -> User:
        email = email
        return self.users
