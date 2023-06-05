import unittest

from auth.src.domain.entity.user import User


class UserTest(unittest.IsolatedAsyncioTestCase):
    def setUp(self) -> None:
        self.email = 'ivar.carrera@gmail.com'
        self.password = 'abc123'
        self.salt = 'salt'
        self.derived_key = 'bd2615764cdf90d3f7467d0de0ca5e5cc87eaedf03471a462c354767e8ded32658a99116d16a2d45dca94a723d3535019125459b9dbaeb53960d8c11283289c2'   # noqa: E501

    async def test_must_create_a_new_user(self) -> None:
        user = await User.create(self.email, self.password)
        is_valid_password = await user.validate_password(self.password)
        self.assertTrue(is_valid_password)

    async def test_deve_criar_um_usuario_a_partir_do_banco_de_dados(self) -> None:
        user = await User.build_existing_user(self.email, self.derived_key, self.salt)
        is_valid_password = await user.validate_password(self.password)
        self.assertTrue(is_valid_password)


if __name__ == '__main__':
    unittest.main()
