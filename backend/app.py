from flask import Flask, request, jsonify
import pkgutil
import importlib.util

# Compatibility shim: Python 3.14+ may not expose pkgutil.get_loader
# Flask expects pkgutil.get_loader to exist; provide a lightweight shim
if not hasattr(pkgutil, "get_loader"):
    def _get_loader(name):
        try:
            spec = importlib.util.find_spec(name)
        except Exception:
            return None
        if spec is None:
            return None
        class LoaderShim:
            def get_filename(self, fullname):
                try:
                    if getattr(spec, "submodule_search_locations", None):
                        return spec.submodule_search_locations[0]
                except Exception:
                    pass
                return getattr(spec, "origin", None)
        return LoaderShim()
    pkgutil.get_loader = _get_loader
from flask_cors import CORS
import os
from dotenv import load_dotenv
import openai

from db import (
    get_first_n_questions,
    find_answer_by_question,
    get_all_entries,
    add_entry,
    update_entry,
)
import uuid
from datetime import datetime, timedelta

load_dotenv()

app = Flask(__name__)
CORS(app)

# Optional OpenAI key (kept for backward compatibility)
openai.api_key = os.getenv("OPENAI_API_KEY")

# Default responses dictionary
responses = {
    "admission": "For admission information, please visit our admissions office.",
    "fee": "Please check our fees page for detailed information.",
    "contact": "You can contact us at: support@college.edu"
}

@app.route("/chat", methods=["POST"])
def chat():
    user_msg = request.json.get("message", "")
    if not user_msg or not user_msg.strip():
        return jsonify({"reply": "Please enter a message."})

    text = user_msg.strip()

    # Check simple keyword-based default responses first
    for key, resp in responses.items():
        if key in text.lower():
            return jsonify({"reply": resp, "related_questions": []})

    # Check DB for exact question
    answer = find_answer_by_question(text)
    if answer:
        return jsonify({"reply": answer, "related_questions": []})

    # If not found, return the first five questions from DB
    first_five = get_first_n_questions(5)
    return jsonify({
        "reply": "I couldn't find a direct answer. Showing the first five suggested questions.",
        "action": "show_first_five",
        "first_five": first_five,
        "no_match": True
    })

@app.route("/get-answer", methods=["POST"])
def get_answer():
    """Get answer for a specific question"""
    try:
        question = request.json.get("question", "")

        if not question:
            return jsonify({"error": "Question is required"}), 400

        answer = find_answer_by_question(question)

        if answer:
            return jsonify({"question": question, "answer": answer, "success": True})
        else:
            return jsonify({"error": "Answer not found for this question", "success": False}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
# ...existing code...

@app.route("/get-training-data", methods=["GET"])
def get_training_data():
    """Get all training data"""
    try:
        entries = get_all_entries()
        return jsonify({"training_data": entries, "college_info": {}})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/add-training-data", methods=["POST"])
def add_training_data():
    """Add new training data"""
    try:
        data = request.json
        question = data.get("question", "")
        answer = data.get("answer", "")
        category = data.get("category", "general")

        if not question or not answer:
            return jsonify({"error": "Question and answer are required", "success": False}), 400

        new_id = add_entry(question, answer, category)
        if new_id:
            return jsonify({"success": True, "message": "Training data added", "id": new_id})
        return jsonify({"success": False, "error": "Could not add entry"}), 500
    except Exception as e:
        return jsonify({"error": str(e), "success": False}), 500


@app.route("/admin/login", methods=["POST"])
def admin_login():
    data = request.json or {}
    username = data.get("username")
    password = data.get("password")

    ADMIN_USER = os.getenv("ADMIN_USER", "admin")
    ADMIN_PASS = os.getenv("ADMIN_PASSWORD", "adminpass")

    if username == ADMIN_USER and password == ADMIN_PASS:
        # create token and store in-memory with expiry
        token = uuid.uuid4().hex
        expiry = datetime.utcnow() + timedelta(days=1)
        if not hasattr(app, 'admin_tokens'):
            app.admin_tokens = {}
        app.admin_tokens[token] = expiry
        return jsonify({"success": True, "token": token})
    return jsonify({"success": False, "error": "Invalid credentials"}), 401


@app.route("/admin/questions", methods=["GET"])
def admin_get_questions():
    # validate token from Authorization header
    auth = request.headers.get('Authorization', '')
    token = None
    if auth.startswith('Bearer '):
        token = auth.split(' ', 1)[1].strip()
    if not token or not getattr(app, 'admin_tokens', {}).get(token):
        return jsonify({"success": False, "error": "Unauthorized"}), 401
    if app.admin_tokens[token] < datetime.utcnow():
        del app.admin_tokens[token]
        return jsonify({"success": False, "error": "Token expired"}), 401
    try:
        entries = get_all_entries()
        return jsonify({"success": True, "questions": entries})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/admin/question", methods=["POST"])
def admin_add_question():
    # validate token
    auth = request.headers.get('Authorization', '')
    token = None
    if auth.startswith('Bearer '):
        token = auth.split(' ', 1)[1].strip()
    if not token or not getattr(app, 'admin_tokens', {}).get(token):
        return jsonify({"success": False, "error": "Unauthorized"}), 401
    if app.admin_tokens[token] < datetime.utcnow():
        del app.admin_tokens[token]
        return jsonify({"success": False, "error": "Token expired"}), 401
    try:
        data = request.json or {}
        q = data.get("question")
        a = data.get("answer")
        cat = data.get("category", "general")
        if not q or not a:
            return jsonify({"success": False, "error": "question and answer required"}), 400
        new_id = add_entry(q, a, cat)
        return jsonify({"success": True, "id": new_id})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/admin/question/<id>", methods=["PUT"])
def admin_update_question(id):
    # validate token
    auth = request.headers.get('Authorization', '')
    token = None
    if auth.startswith('Bearer '):
        token = auth.split(' ', 1)[1].strip()
    if not token or not getattr(app, 'admin_tokens', {}).get(token):
        return jsonify({"success": False, "error": "Unauthorized"}), 401
    if app.admin_tokens[token] < datetime.utcnow():
        del app.admin_tokens[token]
        return jsonify({"success": False, "error": "Token expired"}), 401
    try:
        data = request.json or {}
        q = data.get("question")
        a = data.get("answer")
        cat = data.get("category")
        ok = update_entry(id, question=q, answer=a, category=cat)
        if ok:
            return jsonify({"success": True})
        return jsonify({"success": False, "error": "not updated"}), 400
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route('/admin/logout', methods=['POST'])
def admin_logout():
    auth = request.headers.get('Authorization', '')
    token = None
    if auth.startswith('Bearer '):
        token = auth.split(' ', 1)[1].strip()
    if token and getattr(app, 'admin_tokens', {}).get(token):
        try:
            del app.admin_tokens[token]
        except Exception:
            pass
    return jsonify({"success": True})

@app.route("/health", methods=["GET"])
def health():
    """Check system health"""
    try:
        return jsonify({
            "status": "healthy",
            "openai": "connected" if openai.api_key else "not configured",
            "training_data_count": len(get_all_entries())
        })
    except Exception as e:
        return jsonify({"status": "error", "error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)