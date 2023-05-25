import unittest

from parameterized import parameterized

from checkout.src.domain.entity.cpf import CPF


class CPFTest(unittest.TestCase):
    @parameterized.expand(
        [
            '406.302.170-27',
            '406302170',
            '406302170123456789',
            '406302170123456789',
            '111.111.111-11',
        ]
    )
    def test_must_invalid_cpf(self, _input: str) -> None:
        with self.assertRaises(ValueError) as context:
            CPF(_input)
        self.assertEqual(str(context.exception), 'Invalid cpf')

    @parameterized.expand(
        [
            '353.775.320-90',
            '253-737-010-41',
            '045.237.650.57',
            '790 103 150 61',
            '93682324070',
        ]
    )
    def test_must_valid_cpf(self, _input: str) -> None:
        cpf = CPF(_input)
        self.assertTrue(cpf.value)

    def test_must_format_cpf(self) -> None:
        cpf = CPF('93682324070')
        self.assertEqual(cpf.value, '936.823.240-70')


if __name__ == '__main__':
    unittest.main()
