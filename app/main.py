import httpx
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, AnyUrl
from starlette.responses import JSONResponse

from ocl.convert import convert as oclconvert
from ocl.utils import InputFormat, Format
from ocl.validate import validate as oclvalidate

# http://localhost:8000/validate?format=iso3&file=https%3A%2F%2Femc.spacebel.be%2Fcollections%2Fnovasar_l2ard_hh_hv%3FhttpAccept%3Dapplication%252Fvnd.iso.19115-3%252Bxml
# http://localhost:8000/convert?format=iso3&file=https%3A%2F%2Femc.spacebel.be%2Fcollections%2Fnovasar_l2ard_hh_hv%3FhttpAccept%3Dapplication%252Fvnd.iso.19115-3%252Bxml

# https://emc.spacebel.be/collections/novasar_l2ard_hh_hv?httpAccept=application%2Fvnd.iso.19115-3%2Bxml
# https://emc.spacebel.be/collections/376e342e-3fb8-4d98-bd1e-51a204e1268b/items/urn:eop:DLR:EOWEB:Water_Parameter_Baltic_Sea_MERIS_seasonal_maps:%40dims_nz_pl_dfd_XXXXB00000000000113941439%40dims_nz_pl_dfd_%40%40ENVISAT.MERIS.VA.L3.RWC_PCI?httpAccept=application/vnd.iso.19115-3%2Bxml

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
    # if not file and not format:
    #     return "Provide a URL containing metadata using ?format=<iso3|umm|trainingDML|iso4>&file=<url>"
    # else:
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
    # if not file and not format:
    #     return "Provide a URL containing metadata using ?format=<iso3|umm|trainingDML>&file=<url>"
    # else:
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
