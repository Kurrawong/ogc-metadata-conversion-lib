from typing import Literal

from ocl.models.simple.iso3 import ISO3
from ocl.models.simple.umm import UMM
from ocl.models.simple.trainingdml import TrainingDML


type ConvertFormats = Literal["iso3", "umm", "trainingDML"]


def convert(file: str, format: ConvertFormats):
    """Converts JSON from various formats into ISO 19115-4 JSON"""
    with open(file, 'rb') as f:
        content = f.read()

    match format:
        case "iso3":
            o = ISO3.from_xml(source=content)
        case "trainingDML":
            o = TrainingDML.model_validate_json(content)
        case "umm":
            o = UMM.model_validate_json(content)

    return o.model_convert_iso4().model_dump_json()
