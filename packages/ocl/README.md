# OGC Metadata Conversion Library
A metadata conversion library & CLI to convert various geospatial metadata formats to ISO 19115-4 JSON.

## Install
TBD - This package will be available on PyPi

## Usage
This package will be available to use as a module in Python and as a CLI.

### Module
Example:

```python
from ocl.convert import convert

output = convert("data/test/test.json", "umm")
```

### CLI
The commands available to run via the CLI will be:

```bash
ocl convert [file] -f [format]
```

## Developing
Install the project (requires uv) by running:

```bash
uv sync
```
