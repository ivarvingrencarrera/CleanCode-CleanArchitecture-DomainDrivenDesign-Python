import unittest

from auth.src.domain.entity.email import Email


class EmailTest(unittest.TestCase):
    def test_must_create_a_valid_email(self) -> None:
        email = Email('ivar.carrera@gmail.com')
        self.assertEqual(email.get_value(), 'ivar.carrera@gmail.com')

    def test_must_not_create_a_valid_email(self) -> None:
        with self.assertRaises(ValueError) as context:
            Email('ivar.carrera@gmail')
        self.assertEqual(str(context.exception), 'Invalid email')
