from typing import Literal, Optional

from pydantic import BaseModel, Field, AnyUrl


class ISO4(BaseModel):
    type: Literal["Feature"] = "Feature"
    conformsTo: list[str] = [
        "https://standards.iso.org/iso/19115/-4/0.1/core",
        "https://standards.iso.org/iso/19115/-4/0.1/data-quality-core",
        "https://standards.iso.org/iso/19115/-4/0.1/no-ref"
    ]
    id: Optional[float | str]
    properties: dict
    bbox: Optional[list[float]]
    geometry: dict
