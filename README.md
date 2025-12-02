# OGC Metadata Conversion
FastAPI API and Python library

## API
Available at - [ocl.dev.kurrawong.ai](https://ocl.dev.kurrawong.ai/)

There are two endpoints available:

- `/validate`
  - Validates a metadata file specified at a URL-encoded URL by `?file` and of format `?format` (being one of `iso3`, `umm`, `trainingDML` or `iso4`)
- `/convert`
  - Converts a metadata file to ISO 19115-4 JSON specified at a URL-encoded URL by `?file` and of format `?format` (being one of `iso3`, `umm`, or `trainingDML`)


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
