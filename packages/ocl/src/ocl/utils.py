from typing import Literal, Union

type InputFormat = Literal["iso3", "umm", "trainingDML"]
type OutputFormat = Literal["iso4"]
type Format = Union[InputFormat, OutputFormat]

def guess_format(content: str) -> Format:
    """Guesses the metadata format of a file"""
    pass
