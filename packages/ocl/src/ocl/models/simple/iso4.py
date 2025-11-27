from typing import List, Optional, Union, Literal

from pydantic import AnyUrl, BaseModel, Field

# class Properties(BaseModel):
#     dataQualityInfo: Optional[List[DataQuality]] = Field(None, unique_items=True)

class ISO4(BaseModel):
    # conformsTo: List[AnyUrl]
    type: Literal['Feature'] = Field(default="Feature")
    id: Optional[Union[float, str]] = None
    # properties: Properties
