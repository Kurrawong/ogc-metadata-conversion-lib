from typing import Union

from fastapi import FastAPI

from ocl.convert import convert, ConvertFormats

app = FastAPI()


@app.get("/")
def index(file: str | None = None, format: ConvertFormats | None = None):
    return convert(file, format)
