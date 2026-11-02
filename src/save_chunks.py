import json
from pathlib import Path

def save_chunks(chunks, file_path):
    file_path = Path(file_path)

    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(chunks, file, ensure_ascii=False, indent=4)