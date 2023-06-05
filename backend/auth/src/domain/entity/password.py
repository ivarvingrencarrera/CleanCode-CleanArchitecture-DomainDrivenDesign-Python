import hashlib
import secrets


class Password:
    ITERATIONS = 100
    DERIVED_KEY_LENGTH = 64
    HASH_NAME = 'sha512'

    def __init__(self, value: str, salt: str) -> None:
        self.value = value
        self.salt = salt

    @classmethod
    async def create(cls, password: str, salt: str | None = None) -> 'Password':
        generated_salt = salt or secrets.token_hex(20)
        derived_key = hashlib.pbkdf2_hmac(
            cls.HASH_NAME, password.encode(), generated_salt.encode(), cls.ITERATIONS, cls.DERIVED_KEY_LENGTH
        ).hex()
        return Password(derived_key, generated_salt)

    async def validate(self, password: str) -> bool:
        value = hashlib.pbkdf2_hmac(
            self.HASH_NAME, password.encode(), self.salt.encode(), self.ITERATIONS, self.DERIVED_KEY_LENGTH
        ).hex()
        return self.value == value
