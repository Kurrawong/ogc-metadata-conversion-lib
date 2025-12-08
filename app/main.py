import httpx
from fastapi import FastAPI, HTTPException
from starlette.responses import JSONResponse

from ocl.convert import convert as oclconvert
from ocl.utils import InputFormat, Format
from ocl.validate import validate as oclvalidate

# http://localhost:8000/validate?format=iso3&file=https%3A%2F%2Femc.spacebel.be%2Fcollections%2Fnovasar_l2ard_hh_hv%3FhttpAccept%3Dapplication%252Fvnd.iso.19115-3%252Bxml
# http://localhost:8000/convert?format=iso3&file=https%3A%2F%2Femc.spacebel.be%2Fcollections%2Fnovasar_l2ard_hh_hv%3FhttpAccept%3Dapplication%252Fvnd.iso.19115-3%252Bxml

app = FastAPI()


@app.get("/")
def index():
    return "home page"

@app.get("/validate", response_class=JSONResponse)
def validate(file: str | None = None, format: Format | None = None):
    """Validates a metadata file from a URL"""
    if not file and not format:
        return "Provide a URL containing metadata using ?format=<iso3|umm|trainingDML|iso4>&file=<url>"
    else:
        r = httpx.get(file)
        content = r.text
        try:
            return oclvalidate(content, format)
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))

@app.get("/convert", response_class=JSONResponse)
def convert(file: str | None = None, format: InputFormat | None = None):
    """Converts a metadata file from a URL to ISO 19115-4 JSON"""
    if not file and not format:
        return "Provide a URL containing metadata using ?format=<iso3|umm|trainingDML>&file=<url>"
    else:
        r = httpx.get(file)
        content = r.text
        try:
            return oclconvert(content, format)
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))
