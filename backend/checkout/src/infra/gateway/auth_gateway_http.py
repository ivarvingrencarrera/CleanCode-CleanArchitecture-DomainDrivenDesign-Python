
from checkout.src.application.gateway.auth_gateway import AuthGateway
from fastapi.encoders import jsonable_encoder

from checkout.src.infra.http.http_client import HttpClient


class AuthGatewayHttp(AuthGateway):
    def __init__(self, http_client: HttpClient) -> None:
        self.http_client = http_client

    async def verify(self, token: str) -> bool:    
        url = 'http://localhost:3005/get_session/'
        return await self.http_client.get(url, jsonable_encoder(token))
