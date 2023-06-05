import sys
from pathlib import Path

projeto_dir = Path(__file__).resolve().parents[2]
sys.path.append(str(projeto_dir))

from freight.src.application.repository.zip_code_repository import ZIPCodeRepository
from freight.src.application.usecase.calculate_freight import CalculateFreight
from freight.src.domain.entity.zip_code import ZIPCode
from freight.src.infra.http.fast_api_adapter import FastApiAdapter
from freight.src.infra.http.http_controller import HttpController


def main() -> None:
    zip_code_repository = ZIPCodeRepository()

    async def simulate_database(code):
        if code == '22060030':
            return ZIPCode('22060030', -27.5945, -48.5477)
        if code == '88015600':
            return ZIPCode('88015600', -22.9129, -43.2003)
        return None

    zip_code_repository.get = simulate_database
    calculate_freight = CalculateFreight(zip_code_repository)
    http_server = FastApiAdapter()
    HttpController(http_server, calculate_freight)
    http_server.listen(3002)


if __name__ == '__main__':
    main()
