import sys
from pathlib import Path

projeto_dir = Path(__file__).resolve().parents[2]
sys.path.append(str(projeto_dir))

from freight.src.application.usecase.calculate_freight import CalculateFreight
from freight.src.infra.http.fast_api_adapter import FastApiAdapter
from freight.src.infra.http.http_controller import HttpController


def main() -> None:
    calculate_freight = CalculateFreight()
    http_server = FastApiAdapter()
    HttpController(http_server, calculate_freight)
    http_server.listen(3002)


if __name__ == '__main__':
    main()
