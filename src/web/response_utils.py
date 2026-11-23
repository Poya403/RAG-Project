import json
from src.rag_pipeline import answer_question
from src.chat_database import save_message

def generate_answer(question, db_vector_dir, db_chat_dir, conversation_id):
    answer_generator = answer_question(
        question=question,
        db_dir=db_vector_dir,
        top_k=2
    )

    full_answer = ""

    for event in answer_generator:
         # Collect answer tokens
        if event["type"] == "token":
            full_answer += event["content"]

        # Convert event to JSON
        json_data = json.dumps(
            event,
            ensure_ascii=False
        )

        yield json_data + "\n"

     # Save complete assistant answer
    if full_answer.strip():
        save_message(
            db_chat_dir,
            conversation_id,
            "assistant",
            full_answer
        )