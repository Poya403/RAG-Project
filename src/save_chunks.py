
import json
from pathlib import Path

def save_chunks(chunks, file_path, source_file):
    file_path = Path(file_path)

    formatted_chunks = []

    for chunk_id, chunk in enumerate(chunks, start=1):
        formatted_chunks.append({
            "id": chunk_id,
            "text": chunk,
            "metadata": {
                "source": source_file
            }
        })

    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(formatted_chunks, file, ensure_ascii=False, indent=4)
