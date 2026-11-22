import json

from src.retrieval import retrieve
from src.generation import generate_answer

def answer_question(question, db_dir, top_k=5):
    # Retrieve relevant chunks
    retrieved_chunks = retrieve(
        question=question,
        db_dir=db_dir,
        top_k=top_k
    )

    # Check retrieved results
    if not retrieved_chunks:
        yield {
            "type": "token",
            "content": "اطلاعات کافی در آیین‌نامه وجود ندارد."
        }
        return

    # Extract retrieved texts
    sources = [
        chunk["text"] for chunk in retrieved_chunks
    ]

    # Send retrieved sources
    yield {
        "type": "sources",
        "sources": sources
    }

    # Combine retrieved texts into one context
    context = "\n\n".join(sources)

    # Generate the final answer
    for token in generate_answer(question, context):
        yield {
            "type": "token",
            "content": token
        }
