from pydantic import BaseModel

from auth.src.application.repository.user_repository import UserRepository
from auth.src.domain.entity.user import User


class Input(BaseModel):
    email: str
    password: str


class SignUp:
    def __init__(self, user_repository: UserRepository) -> None:
        self.user_repository = user_repository

    async def execute(self, input_data: dict) -> None:
        input_ = Input(**input_data)
        user = await User.create(input_.email, input_.password)
        await self.user_repository.save(user)
