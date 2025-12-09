from pathlib import Path

import xmlschema
from lxml import etree
import xmltodict

from ocl.utils import InputFormat, guess_format
# from ocl.models.simple.iso3xml import ISO3
from ocl.models.simple.iso3 import ISO3
from ocl.models.simple.umm import UMM
from ocl.models.simple.trainingdml import TrainingDML

ROOT_DIR = Path(__file__).parent.parent

def convert(content: str, format: InputFormat | None = None):
    """Converts from various formats into ISO 19115-4 JSON"""

    # if not format:
    #     format = guess_format(content)

    match format:
        case "iso3":
            # schema = xmlschema.XMLSchema(ROOT_DIR.parent / "schemas" / "ISO19115-3" / "mdb.xsd")
            # o = xmlschema.to_json(content, schema=schema)
            if content.startswith("{"):
                raise ValueError("Incorrect mediatype - detected JSON content when specifying iso3 format, expected XML content")
            doc = xmltodict.parse(content)
            if not doc.get("mdb:MD_Metadata"):
                raise ValueError("Invalid XML content - expecting <mdb:MD_Metadata> in 19115-3 XML format")
            i = doc["mdb:MD_Metadata"]
            for k in list(i.keys()):
                if k.startswith('@xmlns:'):
                    del i[k]
            # print(i)
            x = ISO3.model_validate(i)
            o = x.model_dump_iso4()
        case "trainingDML":
            if content.startswith("<"):
                raise ValueError("Incorrect mediatype - detected XML content when specifying trainingDML format, expected JSON content")
            o = TrainingDML.model_validate_json(content)
        case "umm":
            if content.startswith("<"):
                raise ValueError("Incorrect mediatype - detected XML content when specifying umm format, expected JSON content")
            o = UMM.model_validate_json(content)

    return o