import json
import chromadb

COLLECTION_NAME = "regulations"

def create_vector_db(embedding_file, db_dir):
    try:
        with open(embedding_file, "r", encoding="utf-8") as file:
            embeddings_data = json.load(file)

        if not isinstance(embeddings_data, list) or not embeddings_data:
            raise ValueError("Embedding data is empty or invalid.")

        ids = []
        documents = []
        metadatas = []
        vectors = []

        # Extract data from each embedding record
        for index, item in enumerate(embeddings_data):
            if not isinstance(item, dict):
                raise ValueError(f"Invalid record at index {index}.")

            if not all(key in item for key in ("id", "text", "embedding")):
                raise ValueError(f"Missing required fields at index {index}.")

            text_data = item["text"]

            if not isinstance(text_data, dict):
                raise ValueError(f"Invalid text structure at index {index}.")

            chunk_text = text_data.get("text")
            vector = item["embedding"]

            if not isinstance(chunk_text, str) or not chunk_text.strip():
                raise ValueError(f"Invalid chunk text at index {index}.")

            if not isinstance(vector, list) or not vector:
                raise ValueError(f"Invalid embedding at index {index}.")

            if not all(
                isinstance(value, (int, float)) and not isinstance(value, bool)
                for value in vector
            ):
                raise ValueError(f"Non-numeric embedding at index {index}.")

            # ChromaDB requires string IDs
            ids.append(str(item["id"]))
            documents.append(chunk_text)
            vectors.append(vector)

            metadata = item.get("metadata", {})
            metadatas.append(metadata)

        # Check embedding dimensions
        dimensions = {len(vector) for vector in vectors}

        if len(dimensions) != 1:
            raise ValueError("Embedding dimensions are inconsistent.")

        print("Vector Database :")
        print(f"Number of records: {len(ids)}")
        print(f"Embedding dimensions: {dimensions.pop()}")

        # Create persistent ChromaDB client
        client = chromadb.PersistentClient(path=str(db_dir))

        # Create or retrieve collection
        collection = client.get_or_create_collection(name=COLLECTION_NAME, metadata={"hnsw:space": "cosine"})

        # Store embeddings, documents and metadata
        collection.upsert(
            ids=ids,
            embeddings=vectors,
            documents=documents,
            metadatas=metadatas
        )

        print("\nPASS: Data stored successfully in ChromaDB.")
        print(f"Collection name: {COLLECTION_NAME}")
        print(f"Total records: {collection.count()}")

    except Exception as error:
        print(f"Vector database creation failed: {error}")