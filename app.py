from pathlib import Path

from flask import Flask, render_template, request, jsonify, Response
from src.chat_database import *
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
    try:
        data = request.get_json()

        question = data.get("question", "").strip()
        conversation_id = data.get("conversation_id")

        if not question:
            return jsonify({"error": "Please enter a question."}), 400
    
        # Validate conversation ID
        if conversation_id is None:
            return jsonify({"error": "Conversation ID is required"}), 400
    
        # Save user question
        save_message(
            DATABASE_PATH=DB_DIR,
            conversation_id=conversation_id,
            role="user",
            content=question
        )
        
        response_stream = generate_answer(
            question=question,
            db_vector_dir=DB_VC_DIR,
            db_chat_dir=DB_DIR,
            conversation_id=conversation_id
        )

        return Response(
            response_stream,
            content_type="application/x-ndjson; charset=utf-8"
        )

    except Exception as error:
        return jsonify({"error": str(error)}), 500

@app.route("/conversations", methods=["GET"])
def getConversations():
    try:
        conversations = get_conversations(DB_DIR)

        return jsonify(conversations)
    
    except Exception as error:
        return jsonify({"error": str(error)}), 500

@app.route("/addConversation", methods=["POST"])
def addConversation():
    try:
        conversation_id = create_conversation(DB_DIR)

        return jsonify({
            "message": "Conversation was created successfully.",
            "conversation_id": conversation_id
        })
    
    except Exception as error:
        return jsonify({"error": str(error)}), 500

@app.route("/deleteConversation", methods=["DELETE"])
def deleteConversation():
    try:
        data = request.get_json()
        conversation_id = data.get("conversation_id")

        if not conversation_id:
            return jsonify({"error": "Conversation ID is required."}), 400

        deleted = delete_conversation(DB_DIR, conversation_id)

        if not deleted:
            return jsonify({"error": "Conversation not found."}), 404

        return jsonify({
            "message": "Conversation was deleted successfully.",
            "conversation_id": conversation_id
        })

    except Exception as error:
        return jsonify({"error": str(error)}), 500

@app.route("/renameConversation", methods=["PUT"])
def renameConversation():
    try:
        data = request.get_json()

        conversation_id = data.get("conversation_id")
        new_title = data.get("new_title", "").strip()

        if not conversation_id:
            return jsonify({"error": "Conversation ID is required."}), 400

        if not new_title:
            return jsonify({"error": "New title is required."}), 400

        renamed = rename_conversation(DB_DIR, conversation_id, new_title)

        if not renamed:
            return jsonify({"error": "Conversation not found."}), 404

        return jsonify({
            "message": "Conversation renamed successfully.",
            "conversation_id": conversation_id,
            "new_title": new_title
        })

    except Exception as error:
        return jsonify({"error": str(error)}), 500
        
if __name__ == "__main__":
    app.run(debug=True)
