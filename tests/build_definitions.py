
from pathlib import Path
import json
import re

input_path = Path("data/processed/appendix_definitions_raw.txt")
output_path = Path("data/processed/definitions.json")

if not input_path.exists():
    raise FileNotFoundError(
        f"ابتدا فایل پیوست را بساز: {input_path}"
    )

text = input_path.read_text(encoding="utf-8")
lines = text.splitlines()

definitions = []
current_definition = None

skip_lines = {
    "پیوست شماره 2 شیوهنامه",
    "(تعاریف)",
}

definition_pattern = re.compile(r"^\s*([^:：]+?)\s*[:：]\s*(.*)$")


def save_current_definition():
    if current_definition is None:
        return

    definition_text = " ".join(
        current_definition["parts"]
    ).strip()

    definitions.append({
        "id": len(definitions) + 1,
        "term": current_definition["term"],
        "definition": definition_text,
        "text_verified": False,
        "numeric_values_verified": False,
    })


for line in lines:
    line = line.strip()

    if not line or line in skip_lines:
        continue

    match = definition_pattern.match(line)

    if match:
        term, first_part = match.groups()

        if len(term) > 80:
            if current_definition is not None:
                current_definition["parts"].append(line)
            continue

        save_current_definition()

        current_definition = {
            "term": term.strip(),
            "parts": [first_part.strip()] if first_part.strip() else [],
        }

    elif current_definition is not None:
        current_definition["parts"].append(line)

save_current_definition()

output_path.parent.mkdir(parents=True, exist_ok=True)
output_path.write_text(
    json.dumps(definitions, ensure_ascii=False, indent=2),
    encoding="utf-8",
)

print("تعداد تعریف‌های استخراج‌شده:", len(definitions))
print("فایل خروجی:", output_path)

print("\nپنج تعریف اول:")
for item in definitions[:5]:
    print(f"\n{item['id']}. {item['term']}:")
    print(item["definition"])
