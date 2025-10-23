import json
from pathlib import Path
from typing import Literal

from ocl.cli.console import console
from ocl.models.iso3 import ISO3
from ocl.models.trainingdml import TrainingDML
from ocl.models.umm import UMM


type ConvertFormats = Literal["iso3", "umm", "trainingDML"]

def convert(file: str, format: ConvertFormats):
    """Converts JSON from various formats into ISO 19115-4 JSON"""
    with open(file, 'r') as f:
        content = f.read()
    
    match format:
        case "iso3":
            i = ISO3.model_validate_json(content)
            o = UMM.model_validate_json(i.model_dump_json())
        case "trainingDML":
            i = TrainingDML.model_validate_json(content)
            o = UMM.model_validate_json(i.model_dump_json())
        case "umm":
            o = UMM.model_validate_json(content)

    return o.model_dump_iso4_json()
