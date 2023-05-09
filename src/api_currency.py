import random

from fastapi import FastAPI
from fastapi.responses import JSONResponse

app = FastAPI()


@app.get('/currencies')
async def read_currencies():
    return JSONResponse(content={'usd': 3})
