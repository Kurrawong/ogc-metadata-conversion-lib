# for running ocl as a Python library

from ocl.convert import convert

def main():
    # o = convert("data/test/test.json", "umm")

    with open("data/test/iso_xml.xml", 'rb') as f:
        content = f.read()

    o = convert(content, "iso3")
    # o = convert("data/umm-c-1.18.5-sample.json", "umm")
    # o = convert("data/TDML_example.json", "trainingDML")

    print(o)


if __name__ == "__main__":
    main()
