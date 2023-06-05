from auth.src.domain.service.token_generator import TokenGenerator


class GetSession:
    def __init__(self, token_generator: TokenGenerator) -> None:
        self.token_generator = token_generator

    def execute(self, token: str) -> dict:
        return self.token_generator.verify(token)
