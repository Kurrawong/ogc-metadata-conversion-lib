from typing import Literal, Optional

from pydantic import BaseModel, Field, RootModel


class Scope(RootModel):
    root: dict


class Report(RootModel):
    root: dict


class DataQualityInfo(BaseModel):
    type: Literal["DataQuality"] = Field(..., exclude=True)
    scope: Scope
    report: Optional[list[Report]] = Field(default=None)


class TrainingDML(BaseModel):
    type: Literal["AI_EOTrainingData"] = Field(..., exclude=True)
    id: str
    # title
    # created date
    dataQualityInfo: Optional[list[DataQualityInfo]] = Field(validation_alias="quality", default=None)

    def model_dump_iso4(self):
        obj = self.model_dump(exclude_none=True)
        properties = {
            "metadataIdentifier": {
                "code": obj["id"]
            }
        }
        if obj.get("dataQualityInfo"):
            properties["dataQualityInfo"] = obj["dataQualityInfo"]
        return {
            "type": "Feature",
            "id": obj["id"],
            "conformsTo": [],
            "properties": properties
        }
