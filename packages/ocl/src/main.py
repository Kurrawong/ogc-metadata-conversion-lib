# for running ocl as a Python library

from ocl.convert import convert
from ocl.utils import Format
from ocl.validate import validate

FORMAT: Format = "trainingDML"
CONVERT = True
COLLECTION = False


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
        print(convert(content, FORMAT))
    else:
        print(f"Validating {FORMAT}...")
        print(validate(content, FORMAT))


if __name__ == "__main__":
    main()
