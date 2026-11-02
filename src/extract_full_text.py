
from docx import Document
from pathlib import Path

def extract_full_text(file_path):
    file_path = Path(file_path)

    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    if file_path.suffix.lower() != ".docx":
        raise ValueError("The file format must be .docx.")

    document = Document(file_path)

    extracted_text = []

    for paragraph in document.paragraphs:
        text = paragraph.text.strip()

        if text:
            extracted_text.append(text)

    for table in document.tables:
        for row in table.rows:
            row_text = []

            for cell in row.cells:
                cell_text = cell.text.strip()

                if cell_text:
                    row_text.append(cell_text)

            if row_text:
                extracted_text.append(" | ".join(row_text))

    return "\n".join(extracted_text)
