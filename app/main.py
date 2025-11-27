import httpx
from fastapi import FastAPI

from ocl.convert import convert, ConvertFormats

app = FastAPI()


@app.get("/")
def index(file: str | None = None, format: ConvertFormats | None = None):
    if not file and not format:
        return "Provide a URL containing metadata using ?file=<url>&format=<iso3|umm|trainingDML>"
    else:
        r = httpx.get(file)
        content = r.content
        return convert(content, format)
