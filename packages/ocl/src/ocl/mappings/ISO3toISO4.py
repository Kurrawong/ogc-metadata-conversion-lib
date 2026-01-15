from ocl.mapping import MappingDict
from ocl.models.mapped.iso3 import ISO3
from ocl.models.mapped.iso4 import ISO4


def character_string(obj: dict) -> str | None:
    valid_keys = [
        "gco:CharacterString",
        "gcx:Anchor",
    ]
    for key in obj.keys():
        if key in valid_keys:
            return obj[key]
    return None


def md_identifier(obj: dict) -> dict:
    id_obj = {"code": character_string(obj["mcc:code"])}

    if "mcc:authority" in obj:
        id_obj["authority"] = ci_citation(obj["mcc:authority"]["cit:CI_Citation"])

    if "mcc:codeSpace" in obj:
        id_obj["codeSpace"] = character_string(obj["mcc:codeSpace"])

    if "mcc:version" in obj:
        id_obj["version"] = character_string(obj["mcc:version"])

    if "mcc:description" in obj:
        id_obj["description"] = character_string(obj["mcc:description"])

    return id_obj


def ci_citation(obj: dict) -> dict:
    cit_obj = {"title": character_string(obj["cit:title"])}

    if "cit:alternateTitle" in obj:
        cit_obj["alternateTitle"] = [character_string(name) for name in
                                     obj["cit:alternateTitle"]] if isinstance(obj["cit:alternateTitle"],
                                                                              list) else [
            character_string(obj["cit:alternateTitle"])]

    if obj.get("cit:date"):
        cit_obj["date"] = ci_date(obj["cit:date"])

    # edition

    # identifier

    # citedResponsibleParty

    # presentationForm

    # series

    # otherCitationDetails

    # ISBN

    # ISSN

    # onlineResource

    return cit_obj


def md_scope(obj: dict | None) -> dict | None:
    if obj is None:
        return None
    scope_obj = {"level": obj["mcc:level"]["mcc:MD_ScopeCode"]["#text"]}
    # extent
    # levelDescription
    return scope_obj


def process_report(report: list | dict | None) -> list[dict] | None:
    if report is None:
        return None

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
            measure_obj["measureIdentification"] = md_identifier(
                measure["mdq:measureIdentification"]["mcc:MD_Identifier"])

        if "mdq:nameOfMeasure" in measure:
            measure_obj["nameOfMeasure"] = [character_string(name) for name in
                                            measure["mdq:nameOfMeasure"]] if isinstance(measure["mdq:nameOfMeasure"],
                                                                                        list) else [
                character_string(measure["mdq:nameOfMeasure"])]

        if "mdq:measureDescription" in measure:
            measure_obj["measureDescription"] = character_string(measure["mdq:measureDescription"])

        r_obj["measure"] = measure_obj

        # result
        if r[top_key].get("mdq:result"):
            results = r[top_key]["mdq:result"] if isinstance(r[top_key]["mdq:result"], list) else [
                r[top_key]["mdq:result"]]
            result_types = [
                "mdq:DQ_ConformanceResult",
                "mdq:DQ_CoverageResult",
                "mdq:DQ_DescriptiveResult",
                "mdq:DQ_QuantitativeResult",
            ]

            results_array = []

            for result in results:
                result_top_key = list(result.keys())[0]
                if not result_top_key in result_types:
                    continue
                result_obj = {
                    "type": result_top_key.replace("mdq:DQ_", ""),
                    "pass": bool(result[result_top_key]["mdq:pass"]["gco:Boolean"])
                }

                # dateTime

                # resultScope

                # specification (required)
                result_obj["specification"] = ci_citation(
                    result[result_top_key]["mdq:specification"]["cit:CI_Citation"])

                # explanation

                results_array.append(result_obj)

            r_obj["result"] = results_array

        # derivedElement

        # evaluationMethod

        report_arr.append(r_obj)

    return report_arr


def process_data_quality(dq: list | dict | None) -> list[dict] | None:
    if dq is None:
        return None
    if not isinstance(dq, list):
        dq = [dq]
    d_arr = []
    for d in dq:
        d_obj = {"scope": md_scope(d["mdq:DQ_DataQuality"]["mdq:scope"]["mcc:MD_Scope"])}

        if d["mdq:DQ_DataQuality"].get("mdq:report"):
            d_obj["report"] = process_report(d["mdq:DQ_DataQuality"]["mdq:report"])

        # qualityEvaluationReport

        d_arr.append(d_obj)
    return d_arr


def ci_date(obj: list | dict | None) -> dict | None:
    if obj is None:
        return None
    if not isinstance(obj, list):
        obj = [obj]
    date_obj = {}
    for d in obj:
        date_obj[d["cit:CI_Date"]["cit:dateType"]["cit:CI_DateTypeCode"]["#text"]] = d["cit:CI_Date"]["cit:date"][
            "gco:DateTime"]
    return date_obj


iso3_to_iso4_mapping: MappingDict = {
    "source_model": ISO3,
    "target_model": ISO4,
    "mappings": [
        {
            "key": "mdb:metadataIdentifier.mcc:MD_Identifier.mcc:code",
            "to": "id",
            "to_func": lambda value, source: character_string(value)
        },
        {
            "key": "mdb:metadataIdentifier.mcc:MD_Identifier",
            "to": "properties.metadataIdentifier",
            "to_func": lambda value, source: md_identifier(value)
        },
        {
            "key": "mdb:dataQualityInfo",
            "to": "properties.dataQualityInfo",
            "to_func": lambda value, source: process_data_quality(value)
        },
        {
            "key": "mdb:dateInfo",
            "to": "properties.dateInfo",
            "to_func": lambda value, source: ci_date(value)
        },
    ],
}
