# OGC Metadata Conversion
FastAPI API and Python library

## API
Available at - [ocl.dev.kurrawong.ai](https://ocl.dev.kurrawong.ai/)

There are two endpoints available (see the [OpenAPI docs](https://ocl.dev.kurrawong.ai/docs)):

- `/validate` - Validates a metadata file of a specified format (being one of `iso3`, `umm`, `trainingDML` or `iso4`) at a URL
  - GET - the `?file` URL must be URL-encoded
  - POST
- `/convert` - Converts a metadata file from a specified format (being one of `iso3`, `umm`, or `trainingDML`) at a URL to ISO 19115-4 JSON
  - GET
  - POST


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

### Taskfile
