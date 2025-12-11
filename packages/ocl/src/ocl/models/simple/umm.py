from typing import Optional

from pydantic import BaseModel, Field, model_validator

class DataQualityInfo(BaseModel):
    scope: dict
    # report: Annotated[list[Report] | None, BeforeValidator(dict_to_list)] = Field(validation_alias="mdq:report", default=None)
    # evaluationReport: Optional[dict]

    @model_validator(mode="before")
    def destructure(cls, data):
        obj = {
            "scope": {
                "level": "dataset"
            }
        }

        if data.get("ParameterName"):
            obj["scope"]["levelDescription"] = [
                {
                    "attributes": [data["ParameterName"]]
                }
            ]
        return obj


class UMM(BaseModel):
    id: str = Field(validation_alias="GranuleUR")
    # title - ?
    # dateInfo - ?
    dataQualityInfo: Optional[list[DataQualityInfo]] = Field(validation_alias="MeasuredParameters")

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
