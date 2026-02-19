# for running ocl as a CLI
from pathlib import Path
from typing import Annotated, Literal

import typer
from ocl.cli.console import console
from ocl.convert import convert as oclconvert
from ocl.validate import validate as oclvalidate

app = typer.Typer()


@app.command()
def validate(file: Path, format: Annotated[
    Literal["iso3", "umm", "trainingDML", "iso4"] | None, typer.Option("--format", "-f", help="Input format")] = None,
             output: str | None = None):
    """Validates a metadata file"""
    console.print(f"Validating {file}...")
    with open(file, "r") as f:
        content = f.read()
    console.print(oclvalidate(content, format))


@app.command()
def convert(file: Path, format: Annotated[
    Literal["iso3", "umm", "trainingDML"] | None, typer.Option("--format", "-f", help="Input format")] = None,
            output: str | None = None):
    """Converts a metadata file to ISO 19115-4 JSON"""
    console.print(f"Converting {file}...")
    with open(file, "r") as f:
        content = f.read()
    console.print(oclconvert(content, format))


if __name__ == "__main__":
    app()
