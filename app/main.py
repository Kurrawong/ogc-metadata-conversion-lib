import httpx
from fastapi import FastAPI, HTTPException
from ocl.convert import convert as oclconvert
from ocl.utils import InputFormat, Format
from ocl.validate import validate as oclvalidate
from pydantic import BaseModel, AnyUrl
from starlette.responses import JSONResponse

app = FastAPI()


@app.get("/")
def index():
    return "home page"


@app.get("/validate", response_class=JSONResponse)
def validate_get(file: str | None = None, format: Format | None = None):
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


class ValidateBody(BaseModel):
    file: AnyUrl
    format: Format


@app.post("/validate", response_class=JSONResponse)
def validate_post(body: ValidateBody):
    """Validates a metadata file from a URL"""
    body_dict = body.model_dump()
    try:
        r = httpx.get(str(body_dict["file"]))
    except httpx.ConnectError as e:
        raise HTTPException(status_code=404, detail=str(e))
    content = r.text
    try:
        return oclvalidate(content, body_dict["format"])
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/convert", response_class=JSONResponse)
def convert_get(file: str | None = None, format: InputFormat | None = None):
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


class ConvertBody(BaseModel):
    file: AnyUrl
    format: InputFormat


@app.post("/convert", response_class=JSONResponse)
def convert_post(body: ConvertBody):
    """Converts a metadata file from a URL to ISO 19115-4 JSON"""
    body_dict = body.model_dump()
    try:
        r = httpx.get(str(body_dict["file"]))
    except httpx.ConnectError as e:
        raise HTTPException(status_code=404, detail=str(e))
    content = r.text
    try:
        return oclconvert(content, body_dict["format"])
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
