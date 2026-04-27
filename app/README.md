# OGC Metadata Converter API
A FastAPI Python API using the conversion library.

Available at - [ocl.dev.kurrawong.ai](https://ocl.dev.kurrawong.ai/)

There are two endpoints available (see the [OpenAPI docs](https://ocl.dev.kurrawong.ai/docs)) that will return with a JSON response:

- `/validate` - Validates a metadata file of a specified format (being one of `iso3`, `umm`, `trainingDML` or `iso4`) at a URL
  - GET - the `?file` URL must be URL-encoded
  - POST - `file` & `format` POSTed in a JSON body
- `/convert` - Converts a metadata file from a specified format (being one of `iso3`, `umm`, or `trainingDML`) at a URL to ISO 19115-4 JSON
  - GET - the `?file` URL must be URL-encoded
  - POST - `file` & `format` POSTed in a JSON body

## GET
> [!NOTE]  
> Note that `?file` URL must be URL-encoded.

```bash
curl "https://ocl.dev.kurrawong.ai/convert?file=<url_to_your_file_urlencoded>&format=<iso3|umm|trainingDML>"
```

## POST
JSON payload:

```json
{
  "file": "<url_to_your_file>",
  "format": "iso3" | "umm" | "trainingDML"
}
```

```bash
curl -X POST -H "Content-Type: application/json" -d <body> "https://ocl.dev.kurrawong.ai/convert"
```
