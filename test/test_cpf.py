import unittest

from parameterized import parameterized

from src.cpf import CPF


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
        cpf = CPF(_input)
        self.assertFalse(cpf.is_valid())

    @parameterized.expand(
        [
            '08704506626',
            '353.775.320-90',
            '253-737-010-41',
            '045.237.650.57',
            '790 103 150 61',
            '93682324070',
        ]
    )
    def test_must_valid_cpf(self, _input: str) -> None:
        cpf = CPF(_input)
        self.assertTrue(cpf.is_valid())
