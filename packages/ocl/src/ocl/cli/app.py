from typing import Annotated, Literal

import typer

from ocl.convert import ConvertFormats, convert as oclconvert
from ocl.cli.console import console

app = typer.Typer()


@app.command()
def convert(file: str, format: Annotated[Literal["iso3", "umm", "trainingDML"] | None, typer.Option("--format", "-f", help="Input format")] = None, output: str | None = None):
    """Converts a metadata file to ISO 19115-4 JSON"""
    console.print(f"Converting {file}...")
    console.print(oclconvert(file, format))


if __name__ == "__main__":
    app()
