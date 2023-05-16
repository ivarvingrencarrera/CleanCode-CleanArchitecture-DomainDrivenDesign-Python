from fastapi import FastAPI
from fastapi.responses import JSONResponse

app = FastAPI()


@app.get('/currencies')
async def read_currencies():
    return JSONResponse(
        content={'currency': 'USD', 'symbol': '$', 'name': 'United States dollar', 'rates': 3},
    )
