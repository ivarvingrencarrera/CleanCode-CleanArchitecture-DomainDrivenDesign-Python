import unittest

from auth.src.domain.entity.password import Password


class PasswordTest(unittest.IsolatedAsyncioTestCase):
    def setUp(self) -> None:
        self.password = 'abc123'
        self.salt = 'salt'
        self.derived_key = 'bd2615764cdf90d3f7467d0de0ca5e5cc87eaedf03471a462c354767e8ded32658a99116d16a2d45dca94a723d3535019125459b9dbaeb53960d8c11283289c2'   # noqa E501

    async def test_must_create_a_password(self) -> None:
        password = await Password.create(self.password, self.salt)
        self.assertEqual(password.value, self.derived_key)
        self.assertEqual(password.salt, self.salt)

    async def test_must_validate_a_password(self) -> None:
        password = Password(self.derived_key, self.salt)
        is_valid = await password.validate('abc123')
        self.assertTrue(is_valid)


if __name__ == '__main__':
    unittest.main()
