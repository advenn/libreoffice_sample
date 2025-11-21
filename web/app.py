import tempfile
from pathlib import Path

from fastapi import FastAPI, UploadFile, File, HTTPException
from starlette.responses import FileResponse

from utils.convert_to_pdf import excel2pdf_via_libreoffice

app = FastAPI()


@app.post("/to_pdf")
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
