from ocl.mapping import MappingDict
from ocl.models.mapped.iso3 import ISO3
from ocl.models.mapped.iso4 import ISO4


def process_report(dq: list | dict | None, source: dict) -> list[dict] | None:
    if dq is None:
        return None
    # need to handle outer dataquality array due to bug in handling @. array selectors for now
    for d in dq:
        report = d.get("report")
        if report is None:
            continue
        if not isinstance(report, list):
            report = [report]

        report_arr = []

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

        for r in report:
            top_key = list(r.keys())[0]
            if not top_key in report_types:
                continue
            r_obj = {"type": top_key.replace("mdq:DQ_", "")}

            measure = r[top_key]["mdq:measure"]["mdq:DQ_MeasureReference"]

            measure_obj = {}

            if "mdq:measureIdentification" in measure:
                id = measure["mdq:measureIdentification"]["mcc:MD_Identifier"]
                id_obj = {"code": id["mcc:code"]["gco:CharacterString"]}

                if "mcc:authority" in id:
                    auth = id["mcc:authority"]["cit:CI_Citation"]
                    auth_obj = {"title": auth["cit:title"]["gco:CharacterString"]}

                    if "cit:alternateTitle" in auth:
                        auth_obj["alternateTitle"] = [name["gco:CharacterString"] for name in auth["cit:alternateTitle"]] if isinstance(auth["cit:alternateTitle"], list) else [auth["cit:alternateTitle"]["gco:CharacterString"]]

                    if auth.get("cit:date"):
                        auth_obj["date"] = process_dateinfo(auth["cit:date"], {})

                    # TODO: the rest of the authority object

                    id_obj["authority"] = auth_obj

                if "mcc:codeSpace" in id:
                    id_obj["codeSpace"] = id["mcc:codeSpace"]["gco:CharacterString"]

                if "mcc:version" in id:
                    id_obj["version"] = id["mcc:version"]["gco:CharacterString"]

                if "mcc:description" in id:
                    id_obj["description"] = id["mcc:description"]["gco:CharacterString"]

                measure_obj["measureIdentification"] = id_obj

            if "mdq:nameOfMeasure" in measure:
                measure_obj["nameOfMeasure"] = [name["gco:CharacterString"] for name in measure["mdq:nameOfMeasure"]] if isinstance(measure["mdq:nameOfMeasure"], list) else [measure["mdq:nameOfMeasure"]["gco:CharacterString"]]

            if "mdq:measureDescription" in measure:
                measure_obj["measureDescription"] = measure["mdq:measureDescription"]["gco:CharacterString"]

            r_obj["measure"] = measure_obj

            # result
            if r[top_key].get("mdq:result"):
                results = r[top_key]["mdq:result"] if isinstance(r[top_key]["mdq:result"], list) else [r[top_key]["mdq:result"]]
                result_types = [
                    "mdq:DQ_ConformanceResult",
                    "mdq:DQ_CoverageResult",
                    "mdq:DQ_DescriptiveResult",
                    "mdq:DQ_QuantitativeResult",
                ]

                results_array = []

                for result in results:
                    result_top_key = list(result.keys())[0]
                    print(result_top_key)
                    if not result_top_key in result_types:
                        continue
                    result_obj = {
                        "type": result_top_key.replace("mdq:DQ_", ""),
                        "pass": bool(result[result_top_key]["mdq:pass"]["gco:Boolean"])
                    }

                    # dateTime

                    # resultScope

                    # specification (required)


                    # explanation

                    results_array.append(result_obj)

                r_obj["result"] = results_array


            # derivedElement

            # evaluationMethod

            report_arr.append(r_obj)

        d["report"] = report_arr
    return dq


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
        {
            "key": "mdb:dataQualityInfo.mdq:DQ_DataQuality@.mdq:report",
            "to": "properties.dataQualityInfo@.report",
            "to_func": lambda value, source: process_report(value, source)
        },
        {
            "key": "mdb:dateInfo",
            "to": "properties.dateInfo",
            "to_func": lambda value, source: process_dateinfo(value, source)
        },
    ],
}