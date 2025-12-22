from ocl.mapping import MappingDict
from ocl.models.mapped.trainingDML import TrainingDML
from ocl.models.mapped.iso4 import ISO4


def process_dq(data_quality: list | None, source: dict) -> list | None:
    if data_quality is None:
        return None
    for dq in data_quality:
        del dq["type"]
    return data_quality


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
            "to_func": lambda value, source: process_dq(value, source)
        },
    ],
}