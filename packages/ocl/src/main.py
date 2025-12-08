# for running ocl as a Python library

from ocl.convert import convert
from ocl.validate import validate
from ocl.utils import Format

FORMAT: Format = "iso3"
CONVERT = True

def main():
    match FORMAT:
        case "iso3":
            file = "novasar_l2ard_hh_hv.xml"
            # file = "test/iso_xml.xml"
            # file = "test/mdb_example.xml"
            # file = "test/mdq_example.xml"
            with open(f"data/{file}", "r") as f:
                content = f.read()
        case "trainingDML":
            with open("data/TDML_example.json", "r") as f:
                content = f.read()
        case "umm":
            with open("data/umm-c-1.18.5-sample.json", "r") as f:
                content = f.read()
        case "iso4":
            with open("data/C1-19115-4-JSON-example.json", "r") as f:
                content = f.read()

    # print(content)

    if CONVERT:
        print(f"Converting {FORMAT}...")
        print(convert(content, FORMAT))
    else:
        print(f"Validating {FORMAT}...")
        print(validate(content, FORMAT))


if __name__ == "__main__":
    main()
