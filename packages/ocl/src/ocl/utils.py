import json
from typing import Literal, Union

import xmlschema

type InputFormat = Literal["iso3", "umm", "trainingDML"]
type OutputFormat = Literal["iso4"]
type Format = Union[InputFormat, OutputFormat]


def check_format(content: str, format: Format):
    """Checks the metadata format of a file is valid for use"""
    if format != "iso3":
        if not content.startswith("{"):
            raise ValueError(
                f"Incorrect mediatype - JSON content not detected when specifying {format} format, expected JSON content")
    else:
        if not content.startswith("<"):
            raise ValueError(
                f"Incorrect mediatype - XML content not detected when specifying {format} format, expected XML content")


def guess_format(content: str) -> Format:
    """Guesses the metadata format of a file"""
    if content.startswith("<"):
        return "iso3"
    else:
        try:
            obj = json.loads(content)
            if obj.get("type"):
                match obj["type"]:
                    case "Feature" | "FeatureCollection":
                        return "iso4"
                    case "AI_EOTrainingData" | "AI_EOTrainingDataset":
                        return "trainingDML"
                    case _:
                        raise ValueError("Invalid content - invalid value for 'type'")
            else:
                return "umm"
        except Exception as e:
            raise ValueError("Invalid content - not JSON format")


def _export_xml_schemas(url: str):
    # https://raw.githubusercontent.com/ISO-TC211/XML/refs/heads/master/schemas.isotc211.org/19157/-2/mdq/1.0/mdq.xsd
    # http://standards.iso.org/iso/19115/-3/mdb/1.0
    s = xmlschema.XMLSchema(url)
    s.export(target='my_schemas', save_remote=True)
