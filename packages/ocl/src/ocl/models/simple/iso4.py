from typing import List, Optional, Union, Literal

from pydantic import AnyUrl, BaseModel, Field


# class DataQualityInfo(BaseModel):
#     scope: Scope
#     report: Optional[list[Report]] = Field(default=None)
    # evaluationReport: Optional[dict]


class Properties(BaseModel):
    dataQualityInfo: Optional[List[dict]] = Field(default=None)


class ISO4(BaseModel):
    type: Literal['Feature'] = Field(default="Feature")
    id: Optional[Union[float, str]] = None
    conformsTo: List[AnyUrl]
    properties: Properties
    # geometry
    # bbox
