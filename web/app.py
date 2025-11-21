import tempfile
from pathlib import Path

from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import FileResponse, HTMLResponse

from utils.convert_to_pdf import excel2pdf_via_libreoffice

app = FastAPI()


@app.get("/", response_class=HTMLResponse)
async def upload_form():
    """
    Return HTML form for file upload.
    """
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>PDF Converter</title>
        <style>
            body { font-family: Arial, sans-serif; max-width: 600px; margin: 50px auto; padding: 20px; }
            h1 { color: #333; }
            form { background: #f5f5f5; padding: 20px; border-radius: 8px; }
            input[type="file"] { margin: 10px 0; }
            button { background: #007bff; color: white; padding: 10px 20px; border: none; border-radius: 4px; cursor: pointer; }
            button:hover { background: #0056b3; }
            .info { color: #666; font-size: 14px; margin-top: 10px; }
        </style>
    </head>
    <body>
        <h1>PDF Converter</h1>
        <form action="/" method="post" enctype="multipart/form-data">
            <input type="file" name="file" accept=".xlsx,.xls,.doc,.docx,.txt,.odt,.ods,.ppt,.pptx,.csv" required>
            <br>
            <button type="submit">Convert to PDF</button>
            <p class="info">Supported formats: Excel, Word, PowerPoint, Text, OpenDocument, CSV</p>
        </form>
    </body>
    </html>
    """


@app.post("/")
async def to_pdf(file: UploadFile = File(...)):
    """
    Receive file from form body, convert it to PDF, and return the converted PDF file.
    """
    # Save uploaded file to a temporary location
    with tempfile.NamedTemporaryFile(delete=False, suffix=Path(file.filename).suffix) as tmp:
        content = await file.read()
        tmp.write(content)
        tmp_path = Path(tmp.name)

    # Convert to PDF
    pdf_path = excel2pdf_via_libreoffice(tmp_path)

    if pdf_path is None:
        raise HTTPException(status_code=500, detail="Failed to convert file to PDF")

    return FileResponse(pdf_path, filename=f"{tmp_path.stem}.pdf", media_type="application/pdf")
