from typing import Literal


type ConvertFormats = Literal["iso3", "umm", "trainingDML"]


def convert(file: str, format: ConvertFormats | None = None):
    """Converts from various formats into ISO 19115-4 JSON"""
    return f"convert file={file}, format={format}"
