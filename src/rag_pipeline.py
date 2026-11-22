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
        yield "اطلاعات کافی در آیین‌نامه وجود ندارد."
        return

    # Combine retrieved texts into one context
    context = "\n\n".join(
        chunk["text"] for chunk in retrieved_chunks
    )

    # Generate the final answer
    yield from generate_answer(question, context)
