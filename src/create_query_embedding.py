from sentence_transformers import SentenceTransformer

def create_query_embedding(question):
    model = SentenceTransformer("intfloat/multilingual-e5-base")

    query = "query: " + question

    # Check the token limit
    tokens = model.tokenizer(query, truncation=False)["input_ids"]

    if len(tokens) > model.max_seq_length:
        raise ValueError("The query exceeds the token limit.")

    # Convert the query into an embedding
    embedding = model.encode(
        query,
        normalize_embeddings=True
    )

    return embedding.tolist()