import unittest
from datetime import datetime, timezone

from auth.src.domain.entity.user import User
from auth.src.infra.service.jwt_token_generator import JwtTokenGenerator


class TokenGeneratorTest(unittest.IsolatedAsyncioTestCase):
    def setUp(self) -> None:
        self.email = 'ivar.carrera@gmail.com'
        self.password = 'abc123'
        self.private_key = 'key'
        self.token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6Iml2YXIuY2FycmVyYUBnbWFpbC5jb20iLCJpYXQiOjE2ODU5NTkyMDAsImV4cCI6MTY4Njk1OTIwMH0.CNjvMiIqhVK-LLL257kBRdLqqpak5SHF8u6TLO7BmQU'   # noqa E501
        self.invalid_token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6Iml2YXIuY2FycmVyYUBnbWFpbC6jb20iLCJpYXQiOjE2Nzk5MTEyMDAsImV4cCI6MTY4MDkxMTIwMH0.NgKEyXkX_WsK1vSrYkdyQM3rEZJ1IVm-JzIijh5SHbA'   # noqa E501

    async def test_must_generate_the_user_token(self) -> None:
        user = await User.create(self.email, self.password)
        expires_in = 1000000
        issued_at = datetime(2023, 6, 5, 10, 00, 00, tzinfo=timezone.utc)   # noqa UP017
        token_generator = JwtTokenGenerator(self.private_key)
        token = token_generator.generate(user, expires_in, issued_at)
        expected_token = self.token
        self.assertEqual(token, expected_token)

    async def test_deve_validar_o_token_do_usuario(self) -> None:
        token_generator = JwtTokenGenerator(self.private_key)
        output = await token_generator.verify(self.token)
        self.assertEqual(output['email'], self.email)
        print(output)

    async def test_deve_invalidar_o_token_do_usuario(self) -> None:
        token_generator = JwtTokenGenerator(self.private_key)
        with self.assertRaises(ValueError) as context:
            await token_generator.verify(self.invalid_token)
        self.assertEqual(str(context.exception), 'Invalid token')
