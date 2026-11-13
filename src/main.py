from pathlib import Path
import extract_full_text
import save_text
import chunk_text
import save_chunks

BASE_DIR = Path(__file__).resolve().parent.parent

def main():
    input_file = BASE_DIR / "data" / "raw" / "regulations.docx"
    output_file = BASE_DIR / "data" / "processed" / "regulations.txt"
    output_chunks = BASE_DIR / "data" / "processed" / "chunks.json"

    try:
        text = extract_full_text.extract_full_text(input_file)

        if text.strip():
            print("Text extraction was successful.")
            save_text.save_text(text, output_file)
            chunks = chunk_text.chunk_text(text)
            save_chunks.save_chunks(chunks, output_chunks, input_file.name)
        else:
            print("Warning: No text was extracted.")

    except Exception as error:
        print(f"Error: {error}")

if __name__ == "__main__":
    main()