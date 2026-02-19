# OGC Metadata Conversion Library
A metadata conversion library & CLI to convert ISO 19115-3 XML, UMM JSON & TrainingDML-AI JSON metadata to ISO 19115-4 JSON.

## Install
*Coming soon*

```bash
pip install ocl
```

## Usage
This package can be run either as a module in Python or as a CLI.

### Module
Example:

```python
from ocl.convert import convert

output = convert("data/test/test.json", "umm")
```

### CLI
The commands available to run via the CLI are:

```bash
ocl validate <file> -f iso3|umm|trainingDML|iso4
```

```bash
ocl convert <file> -f iso3|umm|trainingDML
```

## Mappings
Conversions are done by defining mappings in a Python dictionary that map properties between a source Pydantic model and a target Pydantic model using dot notation of keys:

e.g. `path.to.source.key` -> `target.key`

Nested arrays can also be targeted by using the `@` flag in the key path (the number of arrays must be the same):

e.g. `array@.obj.nested@.key` -> `target.key.array@.a.b.nested@.c`

Take a snippet of the UMM to ISO 19115-4 mapping for example:

```python
def process_provider_dates(value: list | None) -> dict | None:
    ...


umm_to_iso4_mapping: MappingDict = {
    "source_model": UMM,
    "target_model": ISO4,
    "mappings": [
        {
            "key": "GranuleUR",
            "to": "id",
        },
        {
            "key": "DataQuality",
            "to": "properties.dataQualityInfo",
        },
        {
            "key": "ProviderDates",
            "to": "properties.identificationInfo.citation",
            "to_func": lambda value, source: process_provider_dates(value)
        },
    ],
}
```

See the [mappings README](src/ocl/mappings/README.md) for more details.

## Developing
Install the project (requires [uv](https://docs.astral.sh/uv/)) by running:

```bash
uv sync
```
