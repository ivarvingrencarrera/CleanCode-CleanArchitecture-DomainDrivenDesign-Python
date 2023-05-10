import random

from fastapi import FastAPI
from fastapi.responses import JSONResponse

app = FastAPI()


@app.get('/currencies')
async def read_currencies():
    random_currency = 3 + random.random()
    return JSONResponse(content={'usd': random_currency})
