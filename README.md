# LibreOffice PDF Converter

A Docker-based microservice for converting Excel files to PDF using LibreOffice, with support for fitting wide tables onto single pages.

## Purpose

This project demonstrates how to use LibreOffice's `SinglePageSheets` export option to convert wide Excel spreadsheets into readable single-page PDFs. It was created for presentation purposes to accompany the blog post:

**Blog Post:** [Converting Wide Excel Tables to Single-Page PDFs with LibreOffice](https://advenn.github.io/blog/posts/convert-to-pdf-with-libreoffice/)

## The Problem

When converting wide Excel files (15+ columns) to PDF using LibreOffice's default settings, columns get split across multiple pages, making the output unreadable.

## The Solution

Use the `SinglePageSheets` export filter:

```bash
libreoffice --headless --convert-to \
  'pdf:calc_pdf_Export:{"SinglePageSheets":{"type":"boolean","value":"true"}}' \
  --outdir /output input.xlsx
```

## Quick Start

### Using Docker

Build the image:

```bash
docker build -t libreoffice-pdf-converter .
```

Run the container:

```bash
docker run -p 8000:8000 libreoffice-pdf-converter
```

### Using Docker Compose

```bash
docker-compose up
```

### Access the Web Interface

Open your browser to [http://localhost:8000](http://localhost:8000)

1. Upload an Excel file (.xlsx, .xls, or other supported formats)
2. Check "Use single page conversion" to fit the sheet on one page
3. Click "Convert to PDF"
4. Download the converted PDF

## Supported Formats

- Excel (.xlsx, .xls)
- Word (.doc, .docx)
- PowerPoint (.ppt, .pptx)
- OpenDocument (.odt, .ods)
- CSV (.csv)
- Text (.txt)

## Project Structure

```
.
├── Dockerfile              # Container build instructions
├── docker-compose.yml      # Docker Compose configuration
├── requirements.txt        # Python dependencies
├── scripts/
│   ├── install_libre.sh    # LibreOffice installation script
│   └── start_app.sh        # Application startup script
├── utils/
│   ├── convert_to_pdf.py   # Core conversion logic
│   └── libreoffice_utils.py # LibreOffice command detection
└── web/
    └── app.py              # FastAPI web application
```

## License

MIT
