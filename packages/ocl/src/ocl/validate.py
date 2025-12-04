import json
from pathlib import Path

import jsonschema
import xmlschema
import xmltodict

from ocl.utils import Format, guess_format
from ocl.models.simple.iso3 import ISO3

ROOT_DIR = Path(__file__).parent.parent


def validate(content: str, format: Format | None = None):
    """Validates metadata of supported formats"""
    is_json = True
    schema = ""

    # if not format:
    #     format = guess_format(content)

    match format:
        case "iso3":
            # s = xmlschema.XMLSchema("https://raw.githubusercontent.com/ISO-TC211/XML/refs/heads/master/schemas.isotc211.org/19157/-2/mdq/1.0/mdq.xsd")
            # s.export(target='my_schemas', save_remote=True)
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
            # xmlschema.validate(content, schema)
            i = xmltodict.parse(content)["mdb:MD_Metadata"]
            for k in list(i.keys()):
                if k.startswith('@xmlns:'):
                    del i[k]
            ISO3.model_validate(i)
        return {"valid": True}

    except Exception as e:
        return {"valid": False, "message": e.message}
