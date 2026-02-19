import json
from pathlib import Path

import xmltodict
from ocl.models.iso3 import ISO3
from ocl.models.iso4 import ISO4
from ocl.models.trainingDML import TrainingDML
from ocl.models.umm import UMM
from ocl.utils import Format, guess_format, check_format
from pydantic import ValidationError

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
                doc = xmltodict.parse(content)
                if not doc.get("mdb:MD_Metadata"):
                    raise ValueError("Invalid XML content - expecting <mdb:MD_Metadata> in 19115-3 XML format")
                i = doc["mdb:MD_Metadata"]
                for k in list(i.keys()):
                    if k.startswith('@xmlns:'):
                        del i[k]
                ISO3.model_validate(i)
            case "trainingDML":
                TrainingDML.model_validate(json.loads(content))
            case "umm":
                UMM.model_validate(json.loads(content))
            case "iso4":
                ISO4.model_validate(json.loads(content))

        return {"valid": True}
    except ValidationError as e:
        return {"valid": False, "message": str(e)}
    except Exception as e:
        return {"valid": False, "message": e.message}
