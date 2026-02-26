from pymongo import MongoClient
from bson.objectid import ObjectId
import os
import json
import uuid
from pymongo.errors import PyMongoError

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
DB_NAME = os.getenv("MONGO_DB", "chatbot_db")

client = MongoClient(MONGO_URI)
db = client[DB_NAME]
qa_coll = db.get_collection("qa")
USE_FILE_FALLBACK = False
FILE_STORE = os.path.join(os.path.dirname(__file__), "training_data.json")

# Probe MongoDB connection; if unavailable, enable file fallback
try:
    client.admin.command('ping')
except Exception:
    USE_FILE_FALLBACK = True

def _load_file_store():
    if not os.path.exists(FILE_STORE):
        data = {"training_data": []}
        with open(FILE_STORE, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)
        return data
    try:
        with open(FILE_STORE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception:
        return {"training_data": []}

def _save_file_store(data):
    with open(FILE_STORE, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)

def get_all_entries():
    if USE_FILE_FALLBACK:
        data = _load_file_store()
        out = []
        for entry in data.get("training_data", []):
            out.append({
                "id": entry.get("id"),
                "question": entry.get("question"),
                "answer": entry.get("answer"),
                "category": entry.get("category")
            })
        return out
    try:
        docs = list(qa_coll.find().sort("_id", 1))
        return [format_doc(d) for d in docs]
    except PyMongoError:
        return []

def get_first_n_questions(n=5):
    if USE_FILE_FALLBACK:
        data = _load_file_store()
        qs = [e.get('question') for e in data.get('training_data', []) if e.get('question')]
        return qs[:n]
    try:
        docs = list(qa_coll.find({}, {"question": 1}).limit(n))
        return [d.get("question") for d in docs if d.get("question")]
    except PyMongoError:
        return []

def find_answer_by_question(question):
    if not question:
        return None
    if USE_FILE_FALLBACK:
        data = _load_file_store()
        ql = question.lower()
        for e in data.get('training_data', []):
            if e.get('question', '').lower() == ql:
                return e.get('answer')
        return None
    try:
        doc = qa_coll.find_one({"question_lower": question.lower()})
        if doc:
            return doc.get("answer")
    except PyMongoError:
        return None
    return None

def add_entry(question, answer, category="general"):
    if not question or not answer:
        return None
    if USE_FILE_FALLBACK:
        data = _load_file_store()
        new_id = uuid.uuid4().hex
        entry = {"id": new_id, "question": question, "answer": answer, "category": category}
        data.setdefault('training_data', []).append(entry)
        _save_file_store(data)
        return new_id
    doc = {
        "question": question,
        "question_lower": question.lower(),
        "answer": answer,
        "category": category
    }
    try:
        res = qa_coll.insert_one(doc)
        return str(res.inserted_id)
    except PyMongoError:
        return None

def update_entry(entry_id, question=None, answer=None, category=None):
    if USE_FILE_FALLBACK:
        data = _load_file_store()
        changed = False
        for e in data.get('training_data', []):
            if e.get('id') == entry_id:
                if question is not None:
                    e['question'] = question
                if answer is not None:
                    e['answer'] = answer
                if category is not None:
                    e['category'] = category
                changed = True
                break
        if changed:
            _save_file_store(data)
        return changed
    try:
        oid = ObjectId(entry_id)
    except Exception:
        return False
    update = {}
    if question is not None:
        update["question"] = question
        update["question_lower"] = question.lower()
    if answer is not None:
        update["answer"] = answer
    if category is not None:
        update["category"] = category
    if not update:
        return False
    try:
        res = qa_coll.update_one({"_id": oid}, {"$set": update})
        return res.modified_count > 0
    except PyMongoError:
        return False

def format_doc(doc):
    return {
        "id": str(doc.get("_id")),
        "question": doc.get("question"),
        "answer": doc.get("answer"),
        "category": doc.get("category")
    }
