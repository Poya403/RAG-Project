import chromadb

from src.create_query_embedding import create_query_embedding
from src.create_vector_db import COLLECTION_NAME


def retrieve(question, db_dir, top_k=5):
    # Check top_k value
    if top_k < 1:
        raise ValueError("top_k must be greater than zero.")
    
    # Create query embedding
    query_embedding = create_query_embedding(question)

    # Connect to ChromaDB
    client = chromadb.PersistentClient(path=str(db_dir))

    # Get the existing collection
    collection = client.get_collection(name=COLLECTION_NAME)

    # Check the number of records
    collection_count = collection.count()

    # Check the number of records
    if collection_count == 0:
        raise ValueError("The collection is empty.")

    # Search for the most similar chunks
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=min(top_k, collection_count),
        include=["documents", "metadatas", "distances"]
    )

    # Prepare the final results
    retrieved_chunks = []

    for index in range(len(results["ids"][0])):
        retrieved_chunks.append({
            "id": results["ids"][0][index],
            "text": results["documents"][0][index],
            "metadata": results["metadatas"][0][index],
            "distance": results["distances"][0][index]
        })

    return retrieved_chunks
