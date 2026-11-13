import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

CHUNK_FILE = BASE_DIR / "data" / "processed" / "chunks.json"
EMBEDDING_FILE = BASE_DIR / "data" / "processed" / "embeddings.json"


def validate_embeddings():

    try:
        with open(CHUNK_FILE, "r", encoding="utf-8") as file:
            chunks = json.load(file)

        with open(EMBEDDING_FILE, "r", encoding="utf-8") as file:
            embeddings = json.load(file)

        print("\nEmbedding Validation: ")
        print("------------------------")
        # Check the number of chunks and embeddings
        if len(chunks) != len(embeddings):
            print("ERROR: Number of chunks and embeddings do not match.")
            return

        print("PASS: Number of chunks and embeddings match.")

        dimensions = set()

        # Validate embeddings and their texts
        for chunk, item in zip(chunks, embeddings):

            vector = item.get("embedding")

            if not isinstance(vector, list) or not vector:
                print("ERROR: Invalid embedding vector.")
                return

            if not all(
                isinstance(value, (int, float)) and not isinstance(value, bool)
                for value in vector
            ):
                print("ERROR: Embedding contains non-numeric values.")
                return

            dimensions.add(len(vector))

            if chunk["text"] != item["text"]["text"]:
                print("ERROR: Chunk and embedding texts do not match.")
                return

        if len(dimensions) != 1:
            print("ERROR: Embedding dimensions are inconsistent.")
            return

        print("PASS: All embeddings contain valid numeric vectors.")
        print(f"Embedding dimensions: {dimensions.pop()}")
        print("PASS: All embeddings match their original chunks.")

        print("Embedding validation completed successfully!")

    except Exception as error:
        print(f"Validation failed: {error}")


if __name__ == "__main__":
    validate_embeddings()
