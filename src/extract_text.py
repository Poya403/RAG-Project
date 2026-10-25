# import pymupdf
# import os

# pdf_path = "data/raw/regulations.pdf"
# output_path = "data/processed/regulations.txt"

# pdf = pymupdf.open(pdf_path)

# text = ""

# for page_number, page in enumerate(pdf, start=1):
#     text += f"\n--- Page {page_number} ---\n"
#     text += page.get_text()
#     text += "\n"

# pdf.close()

# os.makedirs("data/processed", exist_ok=True)

# with open(output_path, "w", encoding="utf-8") as file:
#     file.write(text)

# print("Text extracted successfully!")
# print("Total pages:", page_number)
# print("Number of characters:", len(text))


from pathlib import Path
from pypdf import PdfReader

pdf_path = Path("data/raw/regulations.pdf")
output_path = Path("data/processed/regulations_pypdf.txt")

reader = PdfReader(str(pdf_path))
pages = []

for page_number, page in enumerate(reader.pages, start=1):
    text = page.extract_text() or ""

    pages.append(
        f"\n{'=' * 20} صفحه {page_number} {'=' * 20}\n\n{text}"
    )

output_path.write_text("\n".join(pages), encoding="utf-8")

print(f"تعداد صفحات پردازش‌شده: {len(pages)}")
print(f"فایل متن کامل ساخته شد: {output_path}")
