import re


class Email:
    def __init__(self, email: str) -> None:
        if not self.is_valid(email):
            raise ValueError('Invalid email')
        self.__value = email

    def get_value(self) -> str:
        return self.__value

    @staticmethod
    def is_valid(email: str) -> bool:
        regex = r"^(([^<>()[\]\\.,;:\s@\"']+(\.[^<>()[\]\\.,;:\s@\"']+)*)|(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$"   # noqa E501
        return bool(re.match(regex, email))
