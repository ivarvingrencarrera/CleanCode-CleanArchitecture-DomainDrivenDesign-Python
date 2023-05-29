from collections.abc import Callable
from typing import Any

import uvicorn
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import ORJSONResponse

from freight.src.infra.http.http_server import HttpServer


class FastApiAdapter(HttpServer):
    def __init__(self) -> None:
        self.app = FastAPI(default_response_class=ORJSONResponse)

    def on(self, method: str, url: str, callback: Callable) -> None:
        async def route_handler(request: Request) -> Any:
            try:
                output = await callback(request.path_params, await request.json())
                return output
            except ValueError as e:
                raise HTTPException(status_code=422, detail=str(e)) from e

        self.app.add_api_route(url, route_handler, methods=[method.upper()])

    def listen(self, port: int) -> None:
        uvicorn.run(self.app, host='127.0.0.1', port=port)
