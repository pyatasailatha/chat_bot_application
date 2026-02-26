"""Seed MongoDB `qa` collection from training_data.json (idempotent upserts).

Usage:
  venv\Scripts\activate
  python seed_db.py
"""
import os
import json
from pymongo import MongoClient

MONGO_URI = os.getenv('MONGO_URI', 'mongodb://localhost:27017/')
DB_NAME = os.getenv('MONGO_DB', 'chatbot_db')

client = MongoClient(MONGO_URI)
db = client[DB_NAME]
qa = db.get_collection('qa')

DATA_FILE = os.path.join(os.path.dirname(__file__), 'training_data.json')

def load_file():
    if not os.path.exists(DATA_FILE):
        print('No training_data.json found to seed.')
        return []
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data.get('training_data', [])

def upsert_entries(entries):
    for e in entries:
        q = e.get('question')
        a = e.get('answer')
        cat = e.get('category', 'general')
        if not q or not a:
            continue
        qa.update_one({'question_lower': q.lower()}, {'$set': {
            'question': q,
            'question_lower': q.lower(),
            'answer': a,
            'category': cat
        }}, upsert=True)

if __name__ == '__main__':
    entries = load_file()
    if not entries:
        print('No entries to import.')
    else:
        print(f'Importing {len(entries)} entries into {DB_NAME}.qa')
        upsert_entries(entries)
        print('Done.')
