
from pathlib import Path

from src.rag_pipeline import answer_question

# Define project paths
BASE_DIR = Path(__file__).resolve().parent.parent
DB_DIR = BASE_DIR / "data" / "vector_db"


# Define the question
question = "دانشجو در چه شرایطی مشروط می‌شود و چند نیمسال مشروطی باعث محرومیت از ادامه تحصیل خواهد شد؟"


# Generate the answer using RAG
answer = answer_question(
    question=question,
    db_dir=DB_DIR,
    top_k=2
)


# Display the result
print("Question:")
print(question)

print("\nRAG Answer:")
print(answer)