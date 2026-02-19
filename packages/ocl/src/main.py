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
            # file = "ISO19115-3XML/novasar_l2ard_hh_hv.xml"
            # file = "ISO19115-3XML/mdb_example.xml"
            # file = "ISO19115-3XML/mdq_example.xml"
            file = "ISO19115-3XML/KO2_OTPF_KO2_MSC_2F_20091121T032723_20091121T032723_017702_E096_N026.xml"
        case "trainingDML":
            if COLLECTION:
                file = "trainingDML/TDML_example.json"
            else:
                file = "trainingDML/TDML_data_example.json"
        case "umm":
            if COLLECTION:
                file = "UMM/umm-c-1.18.5-sample.json"
            else:
                file = "UMM/GranuleExample.json"
        case "iso4":
            if COLLECTION:
                file = "ISO19115-4JSON/C1-19115-4-JSON-example.json"
            else:
                file = "ISO19115-4JSON/novasar_l2ard_hh_hv_19115-4.json"

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
