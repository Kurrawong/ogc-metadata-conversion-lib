# OGC Metadata Converter
A library that converts ISO 19115-3 XML, UMM JSON & TrainingDML-AI JSON metadata to ISO 19115-4 JSON, available as a FastAPI API, a Python module and a CLI.

## API
Available at - [ocl.dev.kurrawong.ai](https://ocl.dev.kurrawong.ai/)

There are two endpoints available (see the [OpenAPI docs](https://ocl.dev.kurrawong.ai/docs)):

- `/validate` - Validates a metadata file of a specified format (being one of `iso3`, `umm`, `trainingDML` or `iso4`) at a URL
  - GET - the `?file` URL must be URL-encoded
  - POST - `file` & `format` POSTed in a JSON body
- `/convert` - Converts a metadata file from a specified format (being one of `iso3`, `umm`, or `trainingDML`) at a URL to ISO 19115-4 JSON
  - GET - the `?file` URL must be URL-encoded
  - POST - `file` & `format` POSTed in a JSON body


## Library & CLI
The conversion library (currently called `ocl`, name TBD) can be used as a module in Python and as a CLI.

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

See the [library README](./packages/ocl/README.md) for more details.

## Developing
Install the project (requires [uv](https://docs.astral.sh/uv/)) by running:

```bash
uv sync
```

### Taskfile
A number of commands are available in the [Taskfile](Taskfile.yaml), e.g.:

```bash
task run:lib
```
