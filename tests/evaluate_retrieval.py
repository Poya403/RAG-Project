
import json
from pathlib import Path
import sys

from src.retrieval import retrieve

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))
DB_DIR = BASE_DIR / "data" / "vector_db"
QUESTIONS_FILE = BASE_DIR / "data" / "evaluation" / "evaluation_questions.json"

TOP_K = 5


def load_questions(input_file):
    with open(input_file, "r", encoding="utf-8") as file:
        questions = json.load(file)

    return questions


def calculate_metrics(results):
    total_recall = 0
    total_mrr = 0

    for result in results:
        relevant_ids = set(result["relevant_chunks"])
        retrieved_ids = result["retrieved_chunks"]

        # Calculate Recall@K
        relevant_retrieved = relevant_ids.intersection(retrieved_ids)

        recall = len(relevant_retrieved) / len(relevant_ids)
        total_recall += recall

        # Calculate Reciprocal Rank
        reciprocal_rank = 0

        for rank, chunk_id in enumerate(retrieved_ids, start=1):
            if chunk_id in relevant_ids:
                reciprocal_rank = 1 / rank
                break

        total_mrr += reciprocal_rank

    mean_recall = total_recall / len(results)
    mean_mrr = total_mrr / len(results)

    return mean_recall, mean_mrr


def evaluate_retrieval():
    questions = load_questions(QUESTIONS_FILE)

    results = []

    for item in questions:
        question = item["question"]
        relevant_ids = set(str(x) for x in item["relevant_chunks"])

        retrieved_chunks = retrieve(
            question,
            DB_DIR,
            top_k=TOP_K
        )

        retrieved_ids = [
            str(chunk["id"]) for chunk in retrieved_chunks
        ]

        results.append({
            "question": question,
            "relevant_chunks": relevant_ids,
            "retrieved_chunks": retrieved_ids
        })

        print("\nQuestion:", question)
        print("Relevant IDs:", sorted(relevant_ids))
        print("Retrieved IDs:", retrieved_ids)

    recall, mrr = calculate_metrics(results)

    print("\n" + "=" * 45)
    print("Retrieval Evaluation Results")
    print("=" * 45)

    print(f"Number of questions: {len(questions)}")
    print(f"Top K: {TOP_K}")
    print(f"Recall@{TOP_K}: {recall:.4f}")
    print(f"MRR: {mrr:.4f}")


evaluate_retrieval()