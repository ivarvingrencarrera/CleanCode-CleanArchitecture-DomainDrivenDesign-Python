from auth.src.domain.entity.email import Email
from auth.src.domain.entity.password import Password


class User:
    def __init__(self, email: Email, password: Password) -> None:
        self.email = email
        self.password = password

    @classmethod
    async def create(cls, email: str, password: str) -> 'User':
        return User(Email(email), await Password.create(password))

    @classmethod
    async def build_existing_user(cls, email: str, hash_: str, salt: str) -> 'User':
        return User(Email(email), Password(hash_, salt))

    async def validate_password(self, password: str) -> bool:
        return await self.password.validate(password)
