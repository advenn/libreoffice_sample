import logging
import subprocess
from pathlib import Path
from typing import Optional
import pathlib

from .libreoffice_utils import get_libreoffice_command

logger = logging.getLogger("core")
RENDERED_FILES_DIR = pathlib.Path().parent / "pdf"
RENDERED_FILES_DIR.mkdir(parents=True, exist_ok=True)


def excel2pdf_via_libreoffice(
        excel_file: Path,
        output_dir: Path = RENDERED_FILES_DIR / "pdfs"
) -> Optional[Path]:
    """
    Convert an Excel file to PDF using LibreOffice.
    Ensures sheets fit into single pages.
    Returns path to PDF if successful, else None.
    """
    try:
        # Ensure output directory exists
        output_dir.mkdir(parents=True, exist_ok=True)

        # Build paths
        base_name = excel_file.stem
        pdf_file = output_dir / f"{base_name}.pdf"

        # Define the export filter as a raw string
        export_filter = 'pdf:calc_pdf_Export:{"SinglePageSheets":{"type":"boolean","value":"true"}}'

        # Get the LibreOffice command dynamically
        libreoffice_cmd = get_libreoffice_command()
        if not libreoffice_cmd:
            logger.error("No working LibreOffice command found")
            return None

        # Build command as list for better security and readability
        cmd = [
            libreoffice_cmd,
            "--convert-to", export_filter,
            "--outdir", str(output_dir),
            str(excel_file)
        ]

        # Run the command
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=False
        )

        # Log output for debugging
        print(f"Command: {' '.join(cmd)}")
        print("STDOUT:", result.stdout)
        print("STDERR:", result.stderr)

        # Return the expected PDF path if it was created
        if pdf_file.exists():
            return pdf_file
        else:
            logger.error(f"PDF file was not created: {pdf_file}")
            logger.error(f"LibreOffice stderr: {result.stderr}")
            return None

    except Exception as exc:
        logger.error(f"Error converting Excel to PDF: {exc}", exc_info=exc)
        return None
