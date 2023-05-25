import sys

from checkout.src.infra.cli.cli_handler import CLIHandler


class CLIHandlerPython(CLIHandler):
    def __init__(self) -> None:
        super().__init__()

    async def read_input(self):
        for line in sys.stdin:
            command = line.strip()
            await self.type(command)

    def write(self, text):
        print(text)
