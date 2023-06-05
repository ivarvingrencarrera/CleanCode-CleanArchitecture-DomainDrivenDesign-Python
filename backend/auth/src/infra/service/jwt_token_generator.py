from datetime import datetime

import jwt
from jwt.exceptions import DecodeError, InvalidSignatureError

from auth.src.domain.entity.user import User
from auth.src.domain.service.token_generator import TokenGenerator


class JwtTokenGenerator(TokenGenerator):
    ALGORITHM = 'HS256'

    def __init__(self, key: str) -> None:
        self.key = key

    def generate(self, user: User, expiration: int, issued_at: datetime) -> str:
        payload = {
            'email': user.email.get_value(),
            'iat': int(issued_at.timestamp()),
            'exp': int(issued_at.timestamp() + expiration),
        }
        return jwt.encode(payload, self.key, self.ALGORITHM)

    async def verify(self, token: str) -> dict:
        try:
            return jwt.decode(token, self.key, algorithms=[self.ALGORITHM])
        except (DecodeError, InvalidSignatureError) as err:
            raise ValueError('Invalid token') from err
