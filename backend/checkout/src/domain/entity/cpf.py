import re


class CPF:
    CPF_LENGTH = 11

    def __init__(self, cpf: str) -> None:
        self.cpf = re.sub('[^0-9]', '', cpf)
        self._sum = self._sum_digits()
        if not self.is_valid():
            raise ValueError('Invalid cpf')
        self.value = self._format()

    def is_valid(self) -> bool:
        return self._is_valid_length() and not self._is_same_digit() and self._check_sum_digits()

    def _is_valid_length(self) -> bool:
        return len(self.cpf) == self.CPF_LENGTH

    def _sum_digits(self) -> int:
        return sum(int(digit) for digit in self.cpf)

    def _is_same_digit(self) -> bool:
        return len(set(self.cpf)) == 1

    def _check_sum_digits(self) -> bool:
        first_digit = str(self._sum)[0]
        second_digit = str(self._sum)[1]
        return first_digit == second_digit

    def _format(self) -> str:
        return f'{self.cpf[:3]}.{self.cpf[3:6]}.{self.cpf[6:9]}-{self.cpf[9:]}'
