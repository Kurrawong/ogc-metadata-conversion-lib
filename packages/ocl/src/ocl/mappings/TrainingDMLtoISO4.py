from ocl.mapping import MappingDict
from ocl.models.trainingDML import TrainingDML
from ocl.models.iso4 import ISO4


def process_dq(data_quality: list | None) -> list | None:
    if data_quality is None:
        return None
    for dq in data_quality:
        del dq["type"]
    return data_quality


def geometry(obj: list | None) -> dict | None:
    if obj is None:
        return None

    coords = [[
        [obj[0], obj[1]],
        [obj[2], obj[1]],
        [obj[2], obj[3]],
        [obj[0], obj[3]],
        [obj[0], obj[1]],
    ]]

    return {
        "type": "Polygon",
        "coordinates": coords,
    }


def extent(obj: list | None) -> list | None:
    if obj is None or len(obj) == 0:
        return None

    extent_obj = {"geographicElement": [
        {
            "type": "EX_GeographicBoundingBox",
            "westBoundLongitude": obj[0],
            "eastBoundLongitude": obj[1],
            "southBoundLatitude": obj[2],
            "northBoundLatitude": obj[3],
        }
    ]}

    return [extent_obj]


trainingdml_to_iso4_mapping: MappingDict = {
    "source_model": TrainingDML,
    "target_model": ISO4,
    "mappings": [
        {
            "key": "id",
            "to": "id",
        },
        {
            "key": "id",
            "to": "properties.metadataIdentifier.code",
        },
        {
            "key": "quality",
            "to": "properties.dataQualityInfo",
            "to_func": lambda value, source: process_dq(value)
        },
        {
            "key": "extent",
            "to": "bbox",
        },
        {
            "key": "extent",
            "to": "geometry",
            "to_func": lambda value, source: geometry(value)
        },
        {
            "key": "extent",
            "to": "properties.identificationInfo.extent",
            "to_func": lambda value, source: extent(value)
        },
    ],
}