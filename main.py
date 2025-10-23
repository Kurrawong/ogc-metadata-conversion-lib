# for running ocl as a Python library

from ocl.convert import convert
from ocl.validate import validate

def main():
    # validate("data/test.json")
    o = convert("data/test.json", "umm")
    print(o)

if __name__ == "__main__":
    main()