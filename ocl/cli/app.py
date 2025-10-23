from pathlib import Path
from typing import Annotated, Literal

import typer

# import ocl
from ocl.convert import ConvertFormats, convert as oclconvert
from ocl.validate import validate as oclvalidate
from ocl.cli.console import console

app = typer.Typer()


@app.command()
def validate(file: str):
    """Validates a metadata file"""
    console.print(f"validating {file}...")
    # ocl.validate.validate(file)
    oclvalidate(file)


@app.command()
def convert(file: str, format: Annotated[Literal["iso3", "umm", "trainingDML"], typer.Option(help="Input format")], output: str | None = None, dq: str | None = None):
    """Converts a metadata file to ISO 19115-4 JSON"""
    console.print(f"Converting {file}...")
    # ocl.convert.convert(file)
    console.print(oclconvert(file, format))


if __name__ == "__main__":
    app()
