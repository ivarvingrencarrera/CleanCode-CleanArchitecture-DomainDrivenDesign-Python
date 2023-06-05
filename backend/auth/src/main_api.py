import sys
from pathlib import Path

projeto_dir = Path(__file__).resolve().parents[2]
sys.path.append(str(projeto_dir))


from auth.src.application.usecase.get_session import GetSession
from auth.src.application.usecase.login import Login
from auth.src.application.usecase.sign_up import SignUp
from auth.src.infra.database.asyncpg_adapter import AsyncPGAdapter
from auth.src.infra.http.fast_api_adapter import FastApiAdapter
from auth.src.infra.http.http_controller import HttpController
from auth.src.infra.repository.user_repository_database import UserRepositoryDatabase
from auth.src.infra.service.jwt_token_generator import JwtTokenGenerator


def main() -> None:
    # def user_repository():
    #     class UserRepositoryImpl(UserRepository):
    #         async def save(self, user: User) -> None:

    #         async def get(self, email: str) -> User:

    connection = AsyncPGAdapter()
    user_repository = UserRepositoryDatabase(connection)
    sign_up = SignUp(user_repository)
    token_generator = JwtTokenGenerator('key')
    login = Login(user_repository, token_generator)
    get_session = GetSession(token_generator)

    http_server = FastApiAdapter()
    HttpController(http_server, sign_up, login, get_session)
    http_server.listen(3005)


if __name__ == '__main__':
    main()
