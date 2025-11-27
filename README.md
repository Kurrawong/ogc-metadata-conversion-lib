# OGC Metadata Conversion
FastAPI API and Python library

## API
Available at (a proper domain will be assigned soon) - https://ogc-converter-client.niceforest-128e6d31.australiaeast.azurecontainerapps.io/

The root endpoint / accepts:

- a ?file query parameter, which is a URL-encoded URL pointing to the metadata file to convert. 
- a ?format query parameter, which must be one of: `iso3`, `umm`, or `trainingDML`

## Library & CLI
The conversion library (currently called `ocl`, name TBD) can be used as a module in Python and as a CLI.

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

See the [library README](./packages/ocl/README.md) for more details.

## Developing
Install the project (requires uv) by running:

```bash
uv sync
```
