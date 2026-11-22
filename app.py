
from pathlib import Path
from flask import Flask, render_template, request, jsonify
from src.rag_pipeline import answer_question

# Define project paths
BASE_DIR = Path(__file__).resolve().parent
DB_DIR = BASE_DIR / "data" / "vector_db"

# Create Flask application
app = Flask(
    __name__,
    template_folder="Front-end/templates",
    static_folder="Front-end/static"
)


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/ask", methods=["POST"])
def ask():
    data = request.get_json()

    question = data.get("question", "").strip()

    if not question:
        return jsonify({"error": "Please enter a question."}), 400

    try:
        answer = answer_question(
            question=question,
            db_dir=DB_DIR,
            top_k=2
        )

        return jsonify({"answer": answer})

    except Exception as error:
        return jsonify({"error": str(error)}), 500

if __name__ == "__main__":
    app.run(debug=True)
