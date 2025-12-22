from ocl.mapping import MappingDict
from ocl.models.mapped.umm import UMM
from ocl.models.mapped.iso4 import ISO4


def process_dq(data_quality: list | None, source: dict) -> list | None:
    if data_quality is None:
        return None
    dq_value = []
    for dq in data_quality:
        obj = {
            "scope": {
                "level": "dataset"
            }
        }

        if dq.get("ParameterName"):
            obj["scope"]["levelDescription"] = [
                {
                    "attributes": [dq["ParameterName"]]
                }
            ]

        dq_value.append(obj)
    return dq_value


def process_provider_dates(provider_dates: list, source: dict) -> dict | None:
    obj = {}
    for date in provider_dates:
        match (date["Type"]):
            case "Create":
                obj["creation"] = date["Date"]
            case "Insert":
                obj["insertion"] = date["Date"]
            case "Update":
                obj["revision"] = date["Date"]
            case "Delete":
                obj["deletion"] = date["Date"]
    if len(obj.keys()) == 0:
        return None
    return obj

umm_to_iso4_mapping: MappingDict = {
    "source_model": UMM,
    "target_model": ISO4,
    "mappings": [
        {
            "key": "GranuleUR",
            "to": "id",
        },
        {
            "key": "GranuleUR",
            "to": "properties.metadataIdentifier.code",
        },
        {
            "key": "MeasuredParameters",
            "to": "properties.dataQualityInfo",
            "to_func": lambda value, source: process_dq(value, source)
        },
        # {
        #     "key": "MeasuredParameters@.ParameterName",
        #     "to": "properties.dataQualityInfo@.scope.levelDescription",
        #     # "to_func": lambda value, source: [{"attributes": [value]}]
        # },
        {
            "key": "ProviderDates",
            "to": "properties.identificationInfo.citation",
            "to_func": lambda value, source: process_provider_dates(value, source)
        },
    ],
}