from pathlib import Path
import json
import re

input_path = Path("data/processed/regulations_pypdf.txt")
articles_output = Path("data/processed/articles_cleaned.json")
appendix_output = Path("data/processed/appendix_definitions_raw.txt")

text = input_path.read_text(encoding="utf-8")
lines = text.splitlines()

page_pattern = re.compile(r"=+\s*صفحه\s+(\d+)\s*=+")
article_pattern = re.compile(
    r"^\s*ماده\s*([۰-۹0-9]+)\s*[.．]?\s*(.*)$"
)
appendix_pattern = re.compile(
    r"^\s*پیوست\s+شماره\s*[۰-۹0-9]+\s*شیوهنامه\s*$"
)
page_number_pattern = re.compile(r"^\s*[۰-۹0-9]+\s*$")

repeated_header = (
    "شیوهنامه اجرایی آییننامه یکپارچه مقررات آموزشی دوره کارشناسی"
)

articles = []
current_article = None
current_page = None
in_appendix = False
appendix_lines = []


def is_page_header_or_number(line):
    stripped = line.strip()
    return (
        stripped == repeated_header
        or bool(page_number_pattern.fullmatch(line))
    )


def save_current_article():
    global current_article

    if current_article is None:
        return

    current_article["text"] = "\n".join(
        current_article.pop("_lines")
    ).strip()

    articles.append(current_article)
    current_article = None


for line in lines:
    page_match = page_pattern.search(line)

    if page_match:
        current_page = int(page_match.group(1))
        continue

    # تشخیص شروع پیوست و پایان مواد
    if appendix_pattern.match(line):
        save_current_article()
        in_appendix = True
        appendix_lines.append(line.strip())
        continue

    if in_appendix:
        if not is_page_header_or_number(line):
            appendix_lines.append(line.rstrip())
        continue

    if is_page_header_or_number(line):
        continue

    # تشخیص شروع ماده جدید
    article_match = article_pattern.match(line)

    if article_match:
        save_current_article()

        extracted_number, title = article_match.groups()
        actual_number = len(articles) + 1

        current_article = {
            "number": actual_number,
            "extracted_number": extracted_number,
            "title": title.strip(),
            "page": current_page,
            "text": "",
            "text_verified": False,
            "numeric_values_verified": False,
            "_lines": [
                f"ماده {actual_number}. {title.strip()}"
            ]
        }

    elif current_article is not None:
        # حذف عنوان بخش از انتهای ماده قبلی
        if re.match(r"^\s*بخش\s+نخست\s*:", line):
            continue

        current_article["_lines"].append(line.rstrip())

# ذخیره آخرین ماده
save_current_article()

if len(articles) != 27:
    print(f"خطا: {len(articles)} ماده شناسایی شد؛ انتظار ۲۷ ماده بود.")
    print("فایل‌های خروجی ساخته نشدند.")

elif not in_appendix:
    print("خطا: عنوان پیوست پیدا نشد.")
    print("فایل‌های خروجی ساخته نشدند.")

else:
    articles_output.parent.mkdir(parents=True, exist_ok=True)

    articles_output.write_text(
        json.dumps(articles, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )

    appendix_output.write_text(
        "\n".join(appendix_lines).strip() + "\n",
        encoding="utf-8"
    )

    print(f"تعداد مواد: {len(articles)}")
    print(f"فایل مواد: {articles_output}")
    print(f"فایل پیوست: {appendix_output}")
    print(f"تعداد نویسه‌های پیوست: {len(chr(10).join(appendix_lines))}")

    print("\nانتهای ماده ۲۷:")
    print(articles[-1]["text"][-500:])

    print("\nابتدای فایل پیوست:")
    print("\n".join(appendix_lines[:8]))
