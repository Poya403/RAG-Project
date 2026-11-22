from pathlib import Path

from flask import Flask, render_template, request, jsonify, Response
from src.chat_database import initialize_database
from src.web.response_utils import generate_answer

BASE_DIR = Path(__file__).resolve().parent
DB_DIR = BASE_DIR / "data" / "chat_history.db"
DB_VC_DIR = BASE_DIR / "data" / "vector_db"

# Initialize chat history database
initialize_database(DB_DIR)

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
        response_stream = generate_answer(
            question=question,
            db_vector_dir=DB_VC_DIR
        )

        return Response(
            response_stream,
            content_type="application/x-ndjson; charset=utf-8"
        )

    except Exception as error:
        return jsonify({"error": str(error)}), 500

if __name__ == "__main__":
    app.run(debug=True)
