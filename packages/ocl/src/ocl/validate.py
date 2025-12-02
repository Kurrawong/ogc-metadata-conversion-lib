import json
from pathlib import Path

import jsonschema
import xmlschema

from ocl.utils import Format, guess_format

ROOT_DIR = Path(__file__).parent.parent


def validate(content: str, format: Format | None = None):
    """Validates metadata of supported formats"""
    is_json = True
    schema = ""

    # if not format:
    #     format = guess_format(content)

    match format:
        case "iso3":
            is_json = False
            # schema = "http://standards.iso.org/iso/19115/-3/mdb/1.0"
            schema = ROOT_DIR.parent / "schemas" / "ISO19115-3" / "mdb.xsd"
        case "trainingDML":
            schema = ROOT_DIR.parent / "schemas" / "TDML/ai_eoTrainingDataset.json"
        case "umm":
            schema = ROOT_DIR.parent / "schemas" / "umm/umm-c-json-schema.json"
        case "iso4":
            schema = ROOT_DIR.parent / "schemas" / "ISO19115-4/19115-4.json"

    try:
        if is_json:
            jsonschema.validate(content, json.loads(open(schema, "r").read()))
        else:
            xmlschema.validate(content, schema)
        return {"valid": True}
    except Exception as e:
        return {"valid": False, "message": e.message}
