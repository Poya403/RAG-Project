
import json
from pathlib import Path

path = Path("data/processed/definitions.json")
definitions = json.loads(
    path.read_text(encoding="utf-8")
)

for item in definitions:
    print(f"{item['id']}. {item['term']}")
