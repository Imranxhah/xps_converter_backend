# Conversion API

[Back to the README](../README.md)

All routes accept `POST` with a multipart file field named **file**. Do not manually set a multipart boundary; let your HTTP client generate it. Examples use `curl`; use `curl.exe` on Windows PowerShell.

## PDF

```bash
curl -X POST "http://127.0.0.1:8000/api/convert/to-pdf/" -F "file=@sample.xps"
```

Illustrative success response (IDs, filename, and page count vary):

```json
{
  "success": true,
  "message": "XPS converted to PDF successfully",
  "total_pages": 2,
  "pdf_url": "http://127.0.0.1:8000/media/converted/<uuid>/sample.pdf"
}
```

The endpoint returns JSON, not the PDF bytes. Download the file from `pdf_url`.

## Images

```bash
curl -X POST "http://127.0.0.1:8000/api/convert/to-images/" -F "file=@sample.xps"
```

The response includes `success`, `message`, `total_pages`, and an `images` array of absolute JPEG URLs. Images use names such as `page_1.jpg`.

## Word document

```bash
curl -X POST "http://127.0.0.1:8000/api/convert/to-docx/" -F "file=@sample.xps"
```

The response includes `docx_url` and `total_pages`. The file is named using the source stem plus `_image_based.docx`. It embeds rendered images; text is not reconstructed as editable Word paragraphs. The reported page count refers to the source, not a measured Word pagination result.

A text-only DOCX utility exists in the source, but no API route exposes it.

## Text

```bash
curl -X POST "http://127.0.0.1:8000/api/convert/read-text/" -F "file=@sample.xps"
```

Illustrative response:

```json
{
  "success": true,
  "message": "Text extracted successfully",
  "total_pages": 1,
  "text_content": [
    {"page": 1, "text": "Example document text"}
  ]
}
```

Image-only documents may yield little or no text; OCR is not implemented.

## Errors

Serializer validation and caught conversion errors return HTTP 400. Upload validation responses use `details` as an object of field errors, for example:

```json
{
  "success": false,
  "error": "Invalid file upload",
  "details": {
    "file": ["Only XPS files are allowed"]
  }
}
```

Caught conversion failures return `success: false` with an `error` string. Other HTTP-layer failures may have a different response shape. Clients should check status and fields before dereferencing a download URL.

## Limits and storage

Uploads must have an `.xps` extension and fit the configured size limit. A matching extension is not content authentication; PyMuPDF must still parse the file. Page-count validation is performed during conversion.

Output URLs are built from the incoming request's origin. Configure host/proxy behavior and file serving before deployment. Output files are retained on disk; the request cleanup removes only the temporary upload.
