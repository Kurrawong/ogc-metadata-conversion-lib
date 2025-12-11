import json
from pathlib import Path

import xmltodict
from pydantic import ValidationError

from ocl.models.simple.iso3 import ISO3
from ocl.models.simple.iso4 import ISO4
from ocl.models.simple.trainingdml import TrainingDML
from ocl.models.simple.umm import UMM
from ocl.utils import Format, guess_format, check_format

ROOT_DIR = Path(__file__).parent.parent


def validate(content: str, format: Format | None = None):
    """Validates metadata of supported formats"""
    # schema = ""

    if format:
        check_format(content, format)
    else:
        format = guess_format(content)

    try:
        match format:
            case "iso3":
                # schema = ROOT_DIR.parent / "schemas" / "ISO19115-3" / "mdb.xsd"
                # xmlschema.validate(content, schema)
                doc = xmltodict.parse(content)
                if not doc.get("mdb:MD_Metadata"):
                    raise ValueError("Invalid XML content - expecting <mdb:MD_Metadata> in 19115-3 XML format")
                i = doc["mdb:MD_Metadata"]
                for k in list(i.keys()):
                    if k.startswith('@xmlns:'):
                        del i[k]
                ISO3.model_validate(i)
            case "trainingDML":
                # schema = ROOT_DIR.parent / "schemas" / "TDML/ai_eoTrainingData.json"
                # jsonschema.validate(json.loads(content), json.loads(open(schema, "r").read()))
                TrainingDML.model_validate(json.loads(content))
            case "umm":
                # schema = ROOT_DIR.parent / "schemas" / "umm/umm-c-json-schema.json"
                # jsonschema.validate(json.loads(content), json.loads(open(schema, "r").read()))
                UMM.model_validate(json.loads(content))
            case "iso4":
                # schema = ROOT_DIR.parent / "schemas" / "ISO19115-4/19115-4.json"
                # jsonschema.validate(json.loads(content), json.loads(open(schema, "r").read()))
                ISO4.model_validate(json.loads(content))

        return {"valid": True}
    except ValidationError as e:
        return {"valid": False, "message": str(e)}
    except Exception as e:
        return {"valid": False, "message": e.message}
