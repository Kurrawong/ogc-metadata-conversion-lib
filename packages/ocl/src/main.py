# for running ocl as a Python library
import xmltodict

from ocl.convert import convert
from ocl.utils import Format
from ocl.validate import validate
from ocl.mapping import SourceModel, TargetModel, convert_model, MappingDict

FORMAT: Format = "iso3"
CONVERT = True
COLLECTION = False

def test_mapping():
    input = SourceModel.model_validate({
        "source_nested_dict": {
            "b": {
                "c": "C"
            },
            "arr": [
                {
                    "d": {}
                },
                {
                    "d": {
                        "e": [
                            {
                                "f": {
                                    "g": {
                                        "h": [
                                            {}
                                        ]
                                    },
                                }
                            },
                            {
                                "f": {
                                    "g": {
                                        "h": [
                                            {"i": "J"}
                                        ]
                                    },
                                }
                            }
                        ]
                    }
                },
                {
                    "d": {
                        "e": [
                            {
                                "f": {
                                    "g": {
                                        "h": [
                                            {"i": "I1"},
                                            {"i": "I2"}
                                        ]
                                    },
                                }
                            },
                            {
                                "f": {
                                    "g": {
                                        "h": [
                                            {"i": "J1"},
                                            {"i": "J2"}
                                        ]
                                    },
                                }
                            }
                        ]
                    }
                },
            ],
        },
        "source_str": "some string"
    })
    mapping_dict: MappingDict = {
        "source_model": SourceModel,
        "target_model": TargetModel,
        "mappings": [
            {
                "key": "source_nested_dict.b",
                "to": "target_nested_dict.y.z",
                # "to_func": lambda value, source: None,
            },
            {
                "key": "source_nested_dict.b.c",
                "to": "target_str",
                "to_func": lambda value, source: value.lower() + source.source_str,
            },
            {
                "key": "source_str",
                "to": "target_nested_dict.a.b.c",
                # "to_func": lambda value, source: None,
            },
            {
                "key": "source_nested_dict.arr@.d.e@.f.g.h@.i",
                "to": "target_nested_dict.arr@.x@.y@.z",
                # "to_func": lambda value, source: None,
            },
        ],
    }
    output = convert_model(input, mapping_dict)
    print(output.model_dump())

def main():
    file = ""

    match FORMAT:
        case "iso3":
            file = "novasar_l2ard_hh_hv.xml"
            # file = "test/iso_xml.xml"
            # file = "test/mdb_example.xml"
            # file = "test/mdq_example.xml"
        case "trainingDML":
            if COLLECTION:
                file = "TDML_example.json"
            else:
                file = "TDML_data_example.json"

        case "umm":
            if COLLECTION:
                file = "umm-c-1.18.5-sample.json"
            else:
                file = "GranuleExample.json"
        case "iso4":
            if COLLECTION:
                file = "C1-19115-4-JSON-example.json"
            else:
                file = "novasar_l2ard_hh_hv_19115-4.json"

    with open(f"data/{file}", "r") as f:
        content = f.read()

    if CONVERT:
        print(f"Converting {FORMAT}...")
        output = convert(content, FORMAT)
        print("-----")
        print(output)
    else:
        print(f"Validating {FORMAT}...")
        output = validate(content, FORMAT)
        print("-----")
        print(output)


if __name__ == "__main__":
    main()
    # test_mapping()
