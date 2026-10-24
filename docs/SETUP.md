# Configuration and deployment notes

[Back to the README](../README.md)

## Dependencies

The committed [requirements](../requirements.txt) pin Django 4.2.7, DRF 3.14.0, PyMuPDF 1.23.8, Pillow 10.1.0, and python-docx 1.1.0, among other packages.

Start with a Python 3.11 Windows virtual environment. The pinned `python-magic-bin` package targets Windows. On Linux/macOS, review the dependency list and install a platform-appropriate alternative if needed; the converter source itself does not import `magic`. Do not assume an unchanged install will work on every platform.

## Settings

Edit [xps_backend/settings.py](../xps_backend/settings.py). These values are Python settings; this project does not load a `.env` file.

| Setting | Purpose |
| --- | --- |
| `XPS_MAX_FILE_SIZE` | Serializer limit, currently 10 × 1024 × 1024 bytes |
| `XPS_MAX_PAGES` | Maximum source page count, currently 100 |
| `IMAGE_DPI` | Raster resolution, currently 150 |
| `IMAGE_QUALITY` | JPEG quality, currently 75 |
| `MEDIA_ROOT` | Local upload/output storage |
| `MEDIA_URL` | Development URL prefix, currently `/media/` |
| `XPS_CONVERSION_TIMEOUT` | Declared as 60 seconds, but not currently enforced |

Django's upload-memory settings are separate from the serializer's accepted file-size limit. Also configure request limits at the serving layer when deploying.

## Local verification

```bash
python manage.py check
python manage.py migrate
python manage.py runserver
```

Exercise each endpoint with a small, non-sensitive XPS document. Check page count, downloaded files, image quality, and extracted text. The existing `converter/tests.py` is scaffolding, not a conversion regression suite.

## Troubleshooting

| Symptom | What to inspect |
| --- | --- |
| Dependency installation fails | Python version, available wheels, and `python-magic-bin` platform support |
| No file accepted | Multipart field must be named `file` |
| File rejected | Extension and size limit |
| Parsing/conversion fails | XPS validity and page count |
| Output URL returns 404 locally | `DEBUG`, media URL routing, output file existence |
| DOCX is not editable text | The exposed DOCX route embeds rendered images by design |
| Empty extracted text | Source may contain images only; no OCR is performed |
| Disk usage keeps growing | Converted outputs have no scheduled cleanup |

## Before public deployment

Add authentication and throttling as appropriate, disable debug mode, restrict hosts, replace the development Django secret, and configure HTTPS and media serving. Use isolated conversion workers with enforced execution/resource limits for untrusted files. Set a retention policy and cleanup schedule for generated outputs.

Conversions currently run synchronously inside the request process. A cleanup helper exists, but no background job automatically removes old output directories.
