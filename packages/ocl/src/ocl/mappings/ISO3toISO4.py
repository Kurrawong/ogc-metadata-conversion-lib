from typing import Any

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
            if isinstance(obj[key], dict):
                if "#text" in obj[key]:
                    return obj[key]["#text"]
                elif key == "gcx:Anchor" and "@xlink:href" in obj[key]:
                    return obj[key]["@xlink:href"]
                else:
                    return None
            return obj[key]
    return None


def code_list(obj: dict) -> str | None:
    if "#text" in obj:
        return obj["#text"]
    elif "@codeListValue" in obj:
        return obj["@codeListValue"]
    else:
        return None


def number(obj: dict) -> int | float | None:
    valid_keys = [
        "gco:Decimal",
        "gco:Integer",
    ]
    for key in obj.keys():
        if key in valid_keys:
            if key == "gco:Decimal":
                return float(obj[key])
            elif key == "gco:Integer":
                return int(obj[key])
            else:
                return obj[key]
    return None


def boolean(obj: dict) -> bool | None:
    valid_keys = [
        "gco:Boolean",
    ]
    for key in obj.keys():
        if key in valid_keys:
            return bool(obj[key])
    return None


def dict_to_list(obj: dict | list) -> list:
    return obj if isinstance(obj, list) else [obj]


def md_identifier(obj: dict) -> dict:
    id_obj = {"code": character_string(obj["mcc:code"])}

    if "mcc:authority" in obj:
        if obj["mcc:authority"].get("cit:CI_Citation"):
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

    if "cit:identifier" in obj:
        cit_obj["identifier"] = [md_identifier(id["mcc:MD_Identifier"]) for id in dict_to_list(obj["cit:identifier"])]

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
    scope_obj = {"level": code_list(obj["mcc:level"]["mcc:MD_ScopeCode"])}

    if "mri:extent" in obj:
        scope_obj["extent"] = [ex_extent(e["gex:EX_Extent"]) for e in dict_to_list(obj["mri:extent"])]

    # levelDescription

    return scope_obj


def record(obj: dict | None) -> Any | None:
    if obj is None:
        return None

    valid_keys = [
        "xsd:decimal",
    ]
    key = list(obj.keys())[0]
    if key in valid_keys:
        if key == "xsd:decimal":
            return float(obj[key])
        else:
            return obj[key]
    return obj[key]



def process_report(report: list | dict | None) -> list[dict] | None:
    if report is None:
        return None

    report_arr = []

    report_types = [
        "mdq:DQ_AbsoluteExternalPositionalAccuracy",
        "mdq:DQ_AbsolutePositionalAccuracy",
        "mdq:DQ_AccuracyOfATimeMeasurement",
        "mdq:DQ_Commission",
        "mdq:DQ_CompletenessCommission",
        "mdq:DQ_CompletenessOmission",
        "mdq:DQ_ConceptualConsistency",
        "mdq:DQ_Confidence",
        "mdq:DQ_DomainConsistency",
        "mdq:DQ_FormatConsistency",
        "mdq:DQ_GriddedDataPositionalAccuracy",
        "mdq:DQ_Homogeneity",
        "mdq:DQ_NonQuantitativeAttributeCorrectness",
        "mdq:DQ_Omission",
        "mdq:DQ_QuantitativeAttributeAccuracy",
        "mdq:DQ_RelativeInternalPositionalAccuracy",
        "mdq:DQ_RelativePositionalAccuracy",
        "mdq:DQ_Representativity",
        "mdq:DQ_TemporalConsistency",
        "mdq:DQ_TemporalValidity",
        "mdq:DQ_ThematicClassificationCorrectness",
        "mdq:DQ_TopologicalConsistency",
        "mdq:DQ_UsabilityElement",
    ]

    for r in dict_to_list(report):
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
            result_types = [
                "mdq:DQ_ConformanceResult",
                "mdq:DQ_CoverageResult",
                "mdq:DQ_DescriptiveResult",
                "mdq:DQ_QuantitativeResult",
            ]

            results_array = []

            for result in dict_to_list(r[top_key]["mdq:result"]):
                result_top_key = list(result.keys())[0]
                if not result_top_key in result_types:
                    continue
                result_obj = {
                    "type": result_top_key.replace("mdq:DQ_", ""),
                }

                if "mdq:resultScope" in result:
                    result_obj["resultScope"] = md_scope(result["mdq:resultScope"]["mcc:MD_Scope"])

                # dateTime

                # for ConformanceResult:
                if result_top_key == "mdq:DQ_ConformanceResult":
                    # pass (required)
                    if "mdq:pass" in result[result_top_key]:
                        result_obj["pass"] = bool(result[result_top_key]["mdq:pass"]["gco:Boolean"])

                    # specification (required)
                    if "mdq:specification" in result[result_top_key]:
                        result_obj["specification"] = ci_citation(result[result_top_key]["mdq:specification"]["cit:CI_Citation"])

                    # explanation

                # for CoverageResult:
                if result_top_key == "mdq:DQ_CoverageResult":
                    # spatialRepresentationType (required)
                    if "mdq:spatialRepresentationType" in result[result_top_key]:
                        result_obj["spatialRepresentationType"] = code_list(result[result_top_key]["mdq:spatialRepresentationType"]["MD_SpatialRepresentationTypeCode"])

                # for DescriptiveResult:
                if result_top_key == "mdq:DQ_DescriptiveResult":
                    # statement (required)
                    if "mdq:statement" in result[result_top_key]:
                        result_obj["statement"] = character_string(result[result_top_key]["mdq:statement"])

                # for QuantitativeResult:
                if result_top_key == "mdq:DQ_QuantitativeResult":
                    # value (required)
                    if "mdq:value" in result[result_top_key]:
                        result_obj["value"] = [record(val) for val in dict_to_list(result[result_top_key]["mdq:value"]["gco:Record"])]

                    # valueUnit

                    # valueRecordType
                    if "mdq:valueRecordType" in result[result_top_key]:
                        result_obj["valueRecordType"] = result[result_top_key]["mdq:valueRecordType"]["gco:RecordType"]

                results_array.append(result_obj)

            r_obj["result"] = results_array

        # derivedElement

        # evaluationMethod
        if "mdq:evaluationMethod" in r[top_key]:
            evaluation_method_types = [
                "mdq:DQ_AggregationDerivation",
                "mdq:DQ_FullInspection",
                "mdq:DQ_IndirectEvaluation",
                "mdq:DQ_SampleBasedInspection",
            ]

            method_array = []

            for method in dict_to_list(r[top_key]["mdq:evaluationMethod"]):
                method_top_key = list(method.keys())[0]
                if not method_top_key in evaluation_method_types:
                    continue
                method_obj = {
                    "type": method_top_key.replace("mdq:DQ_", ""),
                }

                # name

                # evaluationMethodDescription
                if "mdq:evaluationMethodDescription" in method[method_top_key]:
                    method_obj["evaluationMethodDescription"] = character_string(method[method_top_key]["mdq:evaluationMethodDescription"])

                # evaluationMethodType
                if "mdq:evaluationMethodType" in method[method_top_key]:
                    method_obj["evaluationMethodType"] = code_list(method[method_top_key]["mdq:evaluationMethodType"]["mdq:DQ_EvaluationMethodTypeCode"])

                # evaluationProcedure
                if "mdq:evaluationProcedure" in method[method_top_key]:
                    method_obj["evaluationProcedure"] = ci_citation(method[method_top_key]["mdq:evaluationProcedure"]["cit:CI_Citation"])

                # dateTime

                # referenceDoc
                if "mdq:referenceDoc" in method[method_top_key]:
                    method_obj["referenceDoc"] = [ci_citation(ref["cit:CI_Citation"]) for ref in dict_to_list(method[method_top_key]["mdq:referenceDoc"])]

                # deductiveSource

                # SampleBasedInspection only:

                # samplingSchema (required)

                # lotDescription (required)

                # samplingRation (required)

                method_array.append(method_obj)

            r_obj["evaluationMethod"] = method_array

        report_arr.append(r_obj)

    return report_arr


def process_data_quality(dq: list | dict | None) -> list[dict] | None:
    if dq is None:
        return None

    d_arr = []

    for d in dict_to_list(dq):
        d_obj = {"scope": md_scope(d["mdq:DQ_DataQuality"]["mdq:scope"]["mcc:MD_Scope"])}

        if "mdq:report" in d["mdq:DQ_DataQuality"]:
            d_obj["report"] = process_report(d["mdq:DQ_DataQuality"]["mdq:report"])

        if "mdq:qualityEvaluationReport" in d["mdq:DQ_DataQuality"]:
            pass

        d_arr.append(d_obj)
    return d_arr


def ci_date(obj: list | dict | None) -> dict | None:
    if obj is None:
        return None

    date_obj = {}

    for d in dict_to_list(obj):
        date_obj[code_list(d["cit:CI_Date"]["cit:dateType"]["cit:CI_DateTypeCode"])] = d["cit:CI_Date"]["cit:date"][
            "gco:DateTime"]
    return date_obj


def ex_extent(obj: dict | None) -> dict | None:
    if obj is None:
        return None
    if "gex:temporalElement" in obj:
        return None
    if "gex:geographicElement" in obj:
        extent_obj = {"geographicElement": []}

        for el in dict_to_list(obj["gex:geographicElement"]):
            element_types = [
                "gex:EX_GeographicBoundingBox",
                "gex:EX_GeographicDescription",
            ]
            element_top_key = list(el.keys())[0]
            if not element_top_key in element_types:
                continue
            element_obj = {"type": element_top_key.replace("gex:", "")}

            if element_top_key == "gex:EX_GeographicBoundingBox":
                element_obj = {
                    **element_obj,
                    "westBoundLongitude": number(el[element_top_key]["gex:westBoundLongitude"]),
                    "eastBoundLongitude": number(el[element_top_key]["gex:eastBoundLongitude"]),
                    "southBoundLatitude": number(el[element_top_key]["gex:southBoundLatitude"]),
                    "northBoundLatitude": number(el[element_top_key]["gex:northBoundLatitude"]),
                }


            elif element_top_key == "gex:EX_GeographicDescription":
                element_obj["geographicIdentifier"] = md_identifier(
                    el[element_top_key]["gex:geographicIdentifier"]["mcc:MD_Identifier"])

            if "gex:extentTypeCode" in el[element_top_key]:
                element_obj["extentTypeCode"] = boolean(el[element_top_key]["gex:extendTypeCode"])

            extent_obj["geographicElement"].append(element_obj)

        if "gex:description" in obj:
            extent_obj["description"] = character_string(obj["gex:description"])

        return extent_obj


def md_data_identification(obj: dict | None) -> dict | None:
    if obj is None:
        return None

    data_id_obj = {
        "citation": ci_citation(obj["mri:citation"]["cit:CI_Citation"]),
        "abstract": character_string(obj["mri:abstract"])
    }

    if "mri:pointOfContact" in obj:
        data_id_obj["pointOfContact"] = contact(obj["mri:pointOfContact"])

    if "mri:extent" in obj:
        data_id_obj["extent"] = [ex_extent(e["gex:EX_Extent"]) for e in dict_to_list(obj["mri:extent"])]

    if "mri:defaultLocale" in obj:
        data_id_obj["defaultLocale"] = pt_locale(obj["mri:defaultLocale"]["lan:PT_Locale"])

    if "mri:otherLocale" in obj:
        data_id_obj["otherLocale"] = other_locale(obj["mri:otherLocale"])

    return data_id_obj


def bbox(obj: dict | list | None) -> list[float] | None:
    if obj is None:
        return None

    for e in [ex_extent(e["gex:EX_Extent"]) for e in dict_to_list(obj)]:
        if e is None:
            continue
        if "geographicElement" in e:
            for element in e["geographicElement"]:
                if element["type"] == "EX_GeographicBoundingBox":
                    return [
                        element["westBoundLongitude"],
                        element["southBoundLatitude"],
                        element["eastBoundLongitude"],
                        element["northBoundLatitude"],
                    ]
    return None


def geometry(obj: dict | list | None) -> dict | None:
    box = bbox(obj)
    if box is None:
        return None

    coords = [[
        [box[0], box[1]],
        [box[2], box[1]],
        [box[2], box[3]],
        [box[0], box[3]],
        [box[0], box[1]],
    ]]

    return {
        "type": "Polygon",
        "coordinates": coords,
    }


def pt_locale(obj: dict | None) -> dict | None:
    if obj is None:
        return None

    locale_dict = {
        "language": code_list(obj["lan:language"]["lan:LanguageCode"]),
        # "characterEncoding": obj["lan:characterEncoding"],
        "characterEncoding": "UTF-8",
    }

    if "country" in obj:
        pass

    return locale_dict


def other_locale(obj: dict | list | None) -> list | None:
    if obj is None:
        return None

    return [pt_locale(l["lan:PT_Locale"]) for l in dict_to_list(obj)]


def md_metadata_scope(obj: dict | list | None) -> list | None:
    if obj is None:
        return None

    return [
        {
            "resourceScope": code_list(s["mdb:MD_MetadataScope"]["mdb:resourceScope"]["mcc:MD_ScopeCode"]),
            "name": code_list(s["mdb:MD_MetadataScope"]["mdb:resourceScope"]["mcc:MD_ScopeCode"])
        } for s in dict_to_list(obj)
    ]


def ci_contact(obj: dict | None) -> dict | None:
    if obj is None:
        return None

    contact_obj = {}

    # phone

    if "cit:address" in obj:
        addr_arr = []

        for addr in [a["cit:CI_Address"] for a in dict_to_list(obj["cit:address"])]:
            addr_obj = {}

            if "cit:deliveryPoint" in addr:
                addr_obj["deliveryPoint"] = [character_string(d) for d in dict_to_list(addr["cit:deliveryPoint"])]

            if "cit:city" in addr:
                addr_obj["city"] = character_string(addr["cit:city"])

            if "cit:administrativeArea" in addr:
                addr_obj["administrativeArea"] = character_string(addr["cit:administrativeArea"])

            if "cit:postalCode" in addr:
                addr_obj["postalCode"] = character_string(addr["cit:postalCode"])

            if "cit:country" in addr:
                addr_obj["country"] = character_string(addr["cit:country"])

            if "cit:electronicMailAddress" in addr:
                addr_obj["electronicMailAddress"] = [character_string(e) for e in
                                                     dict_to_list(addr["cit:electronicMailAddress"])]

            addr_arr.append(addr_obj)

        contact_obj["address"] = addr_arr

    # onlineResource

    # hoursOfService

    # contactInstructions

    # contactType

    return contact_obj


def contact(obj: dict | list | None) -> list | None:
    if obj is None:
        return None

    contact_arr = []

    # CI_Responsibility
    for r in [o["cit:CI_Responsibility"] for o in dict_to_list(obj)]:
        c = {
            "role": code_list(r["cit:role"]["cit:CI_RoleCode"]),
        }

        if "mri:extent" in r:
            c["extent"] = [ex_extent(e["gex:EX_Extent"]) for e in dict_to_list(r["mri:extent"])]

        if "cit:party" in r:
            parties = []

            for party in dict_to_list(r["cit:party"]):
                party_types = [
                    "cit:CI_Individual",
                    "cit:CI_Organisation",
                ]
                party_top_key = list(party.keys())[0]
                if not party_top_key in party_types:
                    continue
                party_obj = {"type": party_top_key.replace("cit:", "")}

                if "cit:name" in party[party_top_key]:
                    party_obj["name"] = character_string(party[party_top_key]["cit:name"])

                if "cit:contactInfo" in party[party_top_key]:
                    party_obj["contactInfo"] = [ci_contact(con["cit:CI_Contact"]) for con in
                                                dict_to_list(party[party_top_key]["cit:contactInfo"])]

                if "cit:partyIdentifier" in party[party_top_key]:
                    party_obj["partyIdentifier"] = [md_identifier(id) for id in
                                                    dict_to_list(party[party_top_key]["cit:partyIdentifier"])]

                # positionName

                parties.append(party_obj)

            c["party"] = parties

        contact_arr.append(c)

    return contact_arr


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
        {
            "key": "mdb:identificationInfo.mri:MD_DataIdentification",
            "to": "properties.identificationInfo",
            "to_func": lambda value, source: md_data_identification(value)
        },
        {
            "key": "mdb:identificationInfo.mri:MD_DataIdentification.mri:extent",
            "to": "bbox",
            "to_func": lambda value, source: bbox(value)
        },
        {
            "key": "mdb:identificationInfo.mri:MD_DataIdentification.mri:extent",
            "to": "geometry",
            "to_func": lambda value, source: geometry(value)
        },
        {
            "key": "mdb:defaultLocale.lan:PT_Locale",
            "to": "properties.defaultLocale",
            "to_func": lambda value, source: pt_locale(value)
        },
        {
            "key": "mdb:otherLocale",
            "to": "properties.otherLocale",
            "to_func": lambda value, source: other_locale(value)
        },
        {
            "key": "mdb:metadataScope",
            "to": "properties.metadataScope",
            "to_func": lambda value, source: md_metadata_scope(value)
        },
        {
            "key": "mdb:contact",
            "to": "properties.contact",
            "to_func": lambda value, source: contact(value)
        },
    ],
}
