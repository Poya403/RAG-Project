from pathlib import Path
import extract_full_text
import save_text
import chunk_text
import save_chunks
import create_embeddings
import create_vector_db

BASE_DIR = Path(__file__).resolve().parent.parent

def main():
    input_file = BASE_DIR / "data" / "raw" / "regulations.docx"
    output_file = BASE_DIR / "data" / "processed" / "regulations.txt"
    output_chunks = BASE_DIR / "data" / "processed" / "chunks.json"
    output_embeddings = BASE_DIR / "data" / "processed" / "embeddings.json"
    vector_db_dir = BASE_DIR / "data" / "vector_db"

    try:
        # Check if embeddings already exist
        if output_embeddings.exists():
            print("Embeddings already exist. Skipping processing.")
            return

        text = extract_full_text.extract_full_text(input_file)

        if text.strip():
            save_text.save_text(text, output_file)
            print("Text extraction was successful.")

            chunks = chunk_text.chunk_text(text)
            save_chunks.save_chunks(chunks, output_chunks, input_file.name)
            print("The chunk production phase was successfull.")

            create_embeddings.create_embeddings(output_chunks, output_embeddings)
            print("The embedding production phase was successfull.")

            create_vector_db.create_vector_db(output_embeddings, vector_db_dir)
            print("The information was stored in the vector database.")
        else:
            print("Warning: No text was extracted.")

    except Exception as error:
        print(f"Error: {error}")

if __name__ == "__main__":
    main()
