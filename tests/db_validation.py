import json
from pathlib import Path
import chromadb
import math

BASE_DIR = Path(__file__).resolve().parent.parent

EMBEDDING_FILE = BASE_DIR / "data" / "processed" / "embeddings.json"
VECTOR_DB_DIR = BASE_DIR / "data" / "vector_db"

COLLECTION_NAME = "regulations"


def test_embedding():
    with open(EMBEDDING_FILE, "r", encoding="utf-8") as file:
        data = json.load(file)

    # Connect to ChromaDB
    client = chromadb.PersistentClient(path=str(VECTOR_DB_DIR))
    collection = client.get_collection(name=COLLECTION_NAME)

    # Retrieve stored records
    stored = collection.get(include=["documents", "embeddings"])

    print("\nVector DataBase Validation: ")
    print("------------------------")

    # Test 1: Number of records
    assert collection.count() == len(data), "Record count mismatch!"
    print("PASS: Record count is correct.")

    # Test 2: Document consistency
    assert stored["documents"] == [item["text"]["text"] for item in data], "Document mismatch!"
    print("PASS: Documents are correctly stored.")

    # Test 3: Embedding dimensions
    assert all(len(vector) == 768 for vector in stored["embeddings"]), "Invalid embedding dimensions!"
    print("PASS: All embeddings have 768 dimensions.")

    # Test 4: Embedding values
    assert all(
        all(isinstance(v, (int, float)) and
            not isinstance(v, bool) and math.isfinite(v)
            for v in vector)
        for vector in stored["embeddings"]
    ), "Invalid embedding values!"
    print("PASS: All embedding values are valid.")

    print("\nVector DataBase validation completed successfully!")


if __name__ == "__main__":
    test_embedding()
