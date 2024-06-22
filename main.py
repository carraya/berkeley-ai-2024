from typing import Optional, Union
from fastapi import FastAPI
from models import Suspect, CallInfo

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/info/")

@app.post("/info/")
async def case_info(call_info: CallInfo):
    return call_info
