from checkout.src.application.usecase.usecase import UseCase


class AuthDecorator(UseCase):
    def __init__(self, usecase: UseCase, auth_gateway):
        self.usecase = usecase
        self.auth_gateway = auth_gateway

    async def execute(self, input_data: dict) -> dict:
        return await self.usecase.execute(input_data)