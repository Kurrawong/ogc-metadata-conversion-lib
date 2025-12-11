# for running ocl as a CLI

from typing import Annotated, Literal

import typer

from ocl.cli.console import console
from ocl.convert import convert as oclconvert
from ocl.validate import validate as oclvalidate

app = typer.Typer()


@app.command()
def validate(file: str, format: Annotated[
    Literal["iso3", "umm", "trainingDML", "iso4"] | None, typer.Option("--format", "-f", help="Input format")] = None,
             output: str | None = None):
    """Validates a metadata file"""
    console.print(f"Validating {file}...")
    console.print(oclvalidate(file, format))


@app.command()
def convert(file: str, format: Annotated[
    Literal["iso3", "umm", "trainingDML"] | None, typer.Option("--format", "-f", help="Input format")] = None,
            output: str | None = None):
    """Converts a metadata file to ISO 19115-4 JSON"""
    console.print(f"Converting {file}...")
    console.print(oclconvert(file, format))


if __name__ == "__main__":
    app()
