from pathlib import Path

def save_text(text, file_path):
    file_path = Path(file_path)

    with open(file_path, "w", encoding="utf-8") as file:
        file.write(text)