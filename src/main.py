from pathlib import Path
import extract_full_text
import save_text

BASE_DIR = Path(__file__).resolve().parent.parent

def main():
    input_file = BASE_DIR / "data" / "raw" / "regulations.docx"
    output_file = BASE_DIR / "data" / "processed" / "regulations.txt"

    try:
        text = extract_full_text.extract_full_text(input_file)

        if text.strip():
                print("Text extraction was successful.")
                save_text.save_text(text, output_file)
        else:
            print("Warning: No text was extracted.")
    except Exception as error:
        print(f"Error: {error}")

if __name__ == "__main__":
    main()