import json
from pathlib import Path
from sentence_transformers import SentenceTransformer

def create_embeddings(input_file, output_file):
    with open(input_file, "r", encoding="utf-8") as file:
        chunks = json.load(file)

    model = SentenceTransformer("intfloat/multilingual-e5-base")

    texts = []

    for chunk in chunks:
        texts.append("passage: " + chunk["text"])

    # Check the token limit
    for index, text in enumerate(texts, start=1):
        tokens = model.tokenizer(text, truncation=False)["input_ids"]

        if len(tokens) > model.max_seq_length:
            raise ValueError(f"Chunk {index} exceeds the token limit.")

    # Convert texts into embeddings
    embeddings = model.encode(
        texts,
        normalize_embeddings=True,
        show_progress_bar=True
    )

    # Prepare the final results
    results = []

    for index in range(len(chunks)):
        results.append({
            "id": index + 1,
            "text": chunks[index],
            "metadata": {
                "source": "regulations.docx"
            },
            "embedding": embeddings[index].tolist()
        })

    # Save embeddings to JSON file
    with open(output_file, "w", encoding="utf-8") as file:
        json.dump(results, file, ensure_ascii=False, indent=4)

    print("Embeddings created successfully!")
    
