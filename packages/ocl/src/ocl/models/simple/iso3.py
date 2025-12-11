from typing import Annotated, Any

from pydantic import BaseModel, Field, AliasPath, BeforeValidator, model_validator


def dict_to_list(value: Any) -> list[dict]:
    if type(value) is dict:
        return [value]
    else:
        return value


def get_date_info(date_type_code: str, value: Any) -> str | None:
    if value["cit:dateType"]["cit:CI_DateTypeCode"]["#text"] == date_type_code:
        return value["cit:date"]["gco:DateTime"]
    else:
        return None


def get_creation_date(value: Any) -> str:
    return get_date_info("creation", value)


def get_revision_date(value: Any) -> str:
    return get_date_info("revision", value)


class DateInfo(BaseModel):
    creation: Annotated[str | None, BeforeValidator(get_creation_date)] = Field(validation_alias="cit:CI_Date",
                                                                                default=None)
    revision: Annotated[str | None, BeforeValidator(get_revision_date)] = Field(validation_alias="cit:CI_Date",
                                                                                default=None)

report_types = [
    "mdq:DQ_AbsolutePositionalAccuracy",
    "mdq:DQ_AccuracyOfATimeMeasurement",
    "mdq:DQ_Commission",
    "mdq:DQ_ConceptualConsistency",
    "mdq:DQ_Confidence",
    "mdq:DQ_DomainConsistency",
    "mdq:DQ_FormatConsistency",
    "mdq:DQ_GriddedDataPositionalAccuracy",
    "mdq:DQ_Homogeneity",
    "mdq:DQ_NonQuantitativeAttributeCorrectness",
    "mdq:DQ_Omission",
    "mdq:DQ_QuantitativeAttributeAccuracy",
    "mdq:DQ_RelativePositionalAccuracy",
    "mdq:DQ_Representativity",
    "mdq:DQ_TemporalConsistency",
    "mdq:DQ_TemporalValidity",
    "mdq:DQ_ThematicClassificationCorrectness",
    "mdq:DQ_TopologicalConsistency",
]

class Report(BaseModel):
    type: str
    # result
    # measure
    # evaluationMethod
    # derivedElement

    @model_validator(mode="before")
    def destructure(cls, data):
        for key in data.keys():
            if key in report_types:
                return {
                    "type": key.split("mdq:DQ_")[1],
                    **data[key]
                }
        return data


class Scope(BaseModel):
    level: str = Field(validation_alias=AliasPath("mcc:level", "mcc:MD_ScopeCode", "#text"))


class DataQualityInfo(BaseModel):
    scope: Scope = Field(validation_alias=AliasPath("mdq:scope", "mcc:MD_Scope"))
    report: Annotated[list[Report] | None, BeforeValidator(dict_to_list)] = Field(validation_alias="mdq:report", default=None)
    # evaluationReport: Optional[dict]


class ISO3(BaseModel):
    id: str | None = Field(
        validation_alias=AliasPath("mdb:metadataIdentifier", "mcc:MD_Identifier", "mcc:code", "gco:CharacterString"),
        default=None)
    # title: Optional[str] = None
    dateInfo: DateInfo | None = Field(validation_alias="mdb:dateInfo", default=None)
    dataQualityInfo: Annotated[list[DataQualityInfo] | None, BeforeValidator(dict_to_list)] = Field(
        validation_alias=AliasPath("mdb:dataQualityInfo", "mdq:DQ_DataQuality"), default=None)

    def model_dump_iso4(self):
        obj = self.model_dump(exclude_none=True)
        properties = {}
        if obj.get("id"):
            properties["metadataIdentifier"] = {
                "code": obj["id"]
            }
        if obj.get("dateInfo"):
            properties["dateInfo"] = obj["dateInfo"]
        if obj.get("dataQualityInfo"):
            properties["dataQualityInfo"] = obj["dataQualityInfo"]
        feature = {
            "type": "Feature",
            "conformsTo": [],
            "properties": properties
        }
        if obj.get("id"):
            feature["id"] = obj["id"]
        return feature