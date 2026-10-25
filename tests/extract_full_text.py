
from pathlib import Path
from pypdf import PdfReader

pdf_path = Path("data/raw/regulations.pdf")
output_path = Path("data/processed/regulations_pypdf.txt")

if not pdf_path.exists():
    raise FileNotFoundError(f"فایل PDF پیدا نشد: {pdf_path}")

reader = PdfReader(str(pdf_path))
pages = []

for page_number, page in enumerate(reader.pages, start=1):
    page_text = page.extract_text() or ""

    pages.append(
        f"========== صفحه {page_number} ==========\n"
        f"{page_text}"
    )

output_path.parent.mkdir(parents=True, exist_ok=True)
output_path.write_text(
    "\n\n".join(pages),
    encoding="utf-8"
)

print(f"تعداد صفحات PDF: {len(reader.pages)}")
print(f"فایل خروجی: {output_path}")
print(f"تعداد نویسه‌های استخراج‌شده: {sum(map(len, pages))}")
