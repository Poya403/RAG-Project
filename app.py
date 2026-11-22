
import json
from pathlib import Path

from flask import Flask, render_template, request, jsonify, Response
from src.rag_pipeline import answer_question
from src.chat_database import initialize_database

# Define project paths
BASE_DIR = Path(__file__).resolve().parent
DB_DIR = BASE_DIR / "data" / "chat_history.db"

# Create Flask application
app = Flask(
    __name__,
    template_folder="Front-end/templates",
    static_folder="Front-end/static"
)

# Initialize chat history database
initialize_database(DB_DIR)

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

        answer_generator = answer_question(
            question=question,
            db_dir=DB_DIR,
            top_k=2
        )

        def stream_response():

            for event in answer_generator:

                # Convert event to JSON
                json_data = json.dumps(
                    event,
                    ensure_ascii=False
                )

                yield json_data + "\n"

        return Response(
            stream_response(),
            content_type="application/x-ndjson; charset=utf-8"
        )

    except Exception as error:
        return jsonify({"error": str(error)}), 500


if __name__ == "__main__":
    app.run(debug=True)
