from pathlib import Path

import xmltodict

from ocl.mapping import convert_model
from ocl.mappings.UMMtoISO4 import umm_to_iso4_mapping
from ocl.mappings.TrainingDMLtoISO4 import trainingdml_to_iso4_mapping
from ocl.mappings.ISO3toISO4 import iso3_to_iso4_mapping
from ocl.models.mapped.iso3 import ISO3
from ocl.models.mapped.trainingDML import TrainingDML
from ocl.models.mapped.umm import UMM
# from ocl.models.mapped.iso4 import ISO4
from ocl.utils import InputFormat, guess_format, check_format

ROOT_DIR = Path(__file__).parent.parent


def convert(content: str, format: InputFormat | None = None):
    """Converts from various formats into ISO 19115-4 JSON"""

    if format:
        check_format(content, format)
    else:
        format = guess_format(content)

    match format:
        case "iso3":
            # schema = xmlschema.XMLSchema(ROOT_DIR.parent / "schemas" / "ISO19115-3" / "mdb.xsd")
            # o = xmlschema.to_json(content, schema=schema)
            if content.startswith("{"):
                raise ValueError(
                    "Incorrect mediatype - detected JSON content when specifying iso3 format, expected XML content")
            doc = xmltodict.parse(content)
            if not doc.get("mdb:MD_Metadata"):
                raise ValueError("Invalid XML content - expecting <mdb:MD_Metadata> in 19115-3 XML format")
            i = doc["mdb:MD_Metadata"]
            for k in list(i.keys()):
                if k.startswith('@xmlns:'):
                    del i[k]
            input = ISO3.model_validate(i)
            output = convert_model(input, iso3_to_iso4_mapping)
            o = output.model_dump()
        case "trainingDML":
            if content.startswith("<"):
                raise ValueError(
                    "Incorrect mediatype - detected XML content when specifying trainingDML format, expected JSON content")
            input = TrainingDML.model_validate_json(content)
            output = convert_model(input, trainingdml_to_iso4_mapping)
            o = output.model_dump()
        case "umm":
            if content.startswith("<"):
                raise ValueError(
                    "Incorrect mediatype - detected XML content when specifying umm format, expected JSON content")
            input = UMM.model_validate_json(content)
            output = convert_model(input, umm_to_iso4_mapping)
            o = output.model_dump()

    return o
