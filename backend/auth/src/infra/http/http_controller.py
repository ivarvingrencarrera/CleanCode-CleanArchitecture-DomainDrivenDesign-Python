from auth.src.application.usecase.get_session import GetSession
from auth.src.application.usecase.login import Login
from auth.src.application.usecase.sign_up import SignUp
from auth.src.infra.http.http_server import HttpServer


class HttpController:
    def __init__(self, http_server: HttpServer, sign_up: SignUp, login: Login, get_session: GetSession) -> None:
        self.http_server = http_server
        self.sign_up = sign_up
        self.login = login
        self.get_session = get_session

        self.http_server.on('post', '/sign_up', self.sign_up_handler)
        self.http_server.on('post', '/login', self.login_handler)
        self.http_server.on('post', '/get_session', self.get_session_handler)

    async def sign_up_handler(self, _: dict, body: dict) -> None:
        return await self.sign_up.execute(body)

    async def login_handler(self, _: dict, body: dict) -> dict:
        return await self.login.execute(body)

    async def get_session_handler(self, _: dict, body: dict) -> dict:
        return await self.get_session.execute(body['token'])
