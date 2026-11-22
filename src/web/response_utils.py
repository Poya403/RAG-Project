import json
from src.rag_pipeline import answer_question

def generate_answer(question, db_vector_dir):
    answer = answer_question(
        question=question,
        db_dir=db_vector_dir,
        top_k=2
    )
    
    for event in answer:
        # Convert event to JSON
        json_data = json.dumps(
            event,
            ensure_ascii=False
        )

        yield json_data + "\n"