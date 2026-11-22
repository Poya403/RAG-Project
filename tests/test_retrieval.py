from pathlib import Path
from src.retrieval import retrieve


BASE_DIR = Path(__file__).resolve().parent.parent
DB_DIR = BASE_DIR / "data" / "vector_db"

question = "شرایط دانش‌آموختگی دانشجوی دوره کارشناسی چیست؟"

results = retrieve(
    question=question,
    db_dir=DB_DIR,
    top_k=10
)

print("\nQuestion:", question)
print("\nRetrieved Chunks:")

for index, chunk in enumerate(results, start=1):
    print("\n" + "=" * 60)
    print(f"Rank: {index}")
    print(f"Chunk ID: {chunk['id']}")
    print(f"Distance: {chunk['distance']:.4f}")
    print(f"Text:\n{chunk['text']}")

