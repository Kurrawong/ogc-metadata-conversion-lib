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
from ocl.validate import validate

validate("data/test.json", "umm")
output = convert("data/test.json", "umm")
```

### CLI
The commands available to run via the CLI will be:

```bash
ocl validate [file]
```

and

```bash
ocl convert [file]
```

## Developing
Install the project by running (requires uv):

```bash
uv sync
```
