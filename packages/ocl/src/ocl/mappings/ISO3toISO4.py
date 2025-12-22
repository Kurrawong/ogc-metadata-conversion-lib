from ocl.mapping import MappingDict
from ocl.models.mapped.iso3 import ISO3
from ocl.models.mapped.iso4 import ISO4


# def process_report(dq: list | dict | None, source: dict) -> list[dict] | None:
#     for d in dq:
#         # unfinished
#         if dq.get("report") is None:
#             return None
#         if not isinstance(report, list):
#             report = [report]
#         # print("report", report)
#         return report


def process_dateinfo(dateinfo: list | dict | None, source: dict) -> dict | None:
    if dateinfo is None:
        return None
    date = dateinfo.get("cit:CI_Date")
    if date is None:
        return None
    if not isinstance(date, list):
        date = [date]
    date_obj = {}
    for d in date:
        date_obj[d["cit:dateType"]["cit:CI_DateTypeCode"]["#text"]] = d["cit:date"]["gco:DateTime"]
    return date_obj


iso3_to_iso4_mapping: MappingDict = {
    "source_model": ISO3,
    "target_model": ISO4,
    "mappings": [
        {
            "key": "mdb:metadataIdentifier.mcc:MD_Identifier.mcc:code.gco:CharacterString",
            "to": "id",
        },
        {
            "key": "mdb:metadataIdentifier.mcc:MD_Identifier.mcc:code.gco:CharacterString",
            "to": "properties.metadataIdentifier.code",
        },
        {
            "key": "mdb:dataQualityInfo.mdq:DQ_DataQuality@.mdq:scope.mcc:MD_Scope.mcc:level.mcc:MD_ScopeCode.#text",
            "to": "properties.dataQualityInfo@.scope.level",
        },
        # {
        #     "key": "mdb:dataQualityInfo.mdq:DQ_DataQuality@.mdq:report",
        #     "to": "properties.dataQualityInfo@.report",
        #     "to_func": lambda value, source: process_report(value, source)
        # },
        {
            "key": "mdb:dateInfo",
            "to": "properties.dateInfo",
            "to_func": lambda value, source: process_dateinfo(value, source)
        },
    ],
}