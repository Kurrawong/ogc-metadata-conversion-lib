from typing import Literal, Optional

from pydantic import BaseModel, Field, AnyUrl


class ISO4(BaseModel):
    type: Literal["Feature"] = "Feature"
    conformsTo: list[AnyUrl] = []
    id: Optional[float | str]
    properties: dict
