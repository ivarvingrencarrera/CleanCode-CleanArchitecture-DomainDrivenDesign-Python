from unittest.mock import MagicMock

import pytest

from auth.src.application.repository.user_repository import UserRepository
from auth.src.application.usecase.login import Login
from auth.src.application.usecase.sign_up import SignUp
from auth.src.domain.entity.user import User
from auth.src.infra.service.jwt_token_generator import JwtTokenGenerator

# def setUp(self) -> None:

#     async def save(user: User) -> None:

#     async def get(email: str) -> User:


# @pytest.fixture
# def user_repository():

#     class UserRepositoryImpl(UserRepository):
#         async def save(self, user: User) -> None:

#         async def get(self, email: str) -> User:


@pytest.fixture
def user_repository() -> UserRepository:
    users = {}

    class UserRepositoryImpl(UserRepository):
        async def save(self, user: User) -> None:
            users[user.email.get_value()] = user

        async def get(self, email: str) -> User:
            return users[email]

    return UserRepositoryImpl()


async def test_must_be_the_sign_up(user_repository: UserRepository) -> None:
    sign_up = SignUp(user_repository)
    input_ = {
        'email': 'joao@gmail.com',
        'password': 'abc123',
    }
    await sign_up.execute(input_)

    expected_token = '123456'
    mocked_token_generator = MagicMock(spec=JwtTokenGenerator)
    mocked_token_generator.generate.return_value = expected_token
    token_generator = mocked_token_generator

    login = Login(user_repository, token_generator)

    output = await login.execute(input_)
    assert output['token'] == expected_token
