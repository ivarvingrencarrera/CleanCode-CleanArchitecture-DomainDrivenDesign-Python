from datetime import datetime

from pydantic import BaseModel

from auth.src.application.repository.user_repository import UserRepository
from auth.src.domain.service.token_generator import TokenGenerator


class Input(BaseModel):
    email: str
    password: str


class Output(BaseModel):
    token: str


class Login:
    def __init__(self, user_repository: UserRepository, token_generator: TokenGenerator):
        self.user_repository = user_repository
        self.token_generator = token_generator

    async def execute(self, input_data: dict) -> dict:
        input_ = Input(**input_data)
        user = await self.user_repository.get(input_.email)
        is_password_valid = await user.validate_password(input_.password)
        if not is_password_valid:
            raise ValueError('Authentication failed')
        token = self.token_generator.generate(user, 1000000, datetime.now())
        return Output(token=token).dict()
