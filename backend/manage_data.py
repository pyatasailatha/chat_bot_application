"""
Data management script for training the college chatbot
This allows you to easily add, update, and manage training data
"""

import json
import os

class TrainingDataManager:
    def __init__(self, filepath="training_data.json"):
        self.filepath = filepath
        self.data = self.load_data()
    
    def load_data(self):
        """Load training data from file"""
        if os.path.exists(self.filepath):
            with open(self.filepath, "r") as f:
                return json.load(f)
        return {"college_info": {}, "training_data": []}
    
    def save_data(self):
        """Save training data to file"""
        with open(self.filepath, "w") as f:
            json.dump(self.data, f, indent=2)
    
    def add_training_entry(self, question, answer, category="general"):
        """Add a new Q&A pair"""
        entry = {
            "question": question,
            "answer": answer,
            "category": category
        }
        self.data["training_data"].append(entry)
        self.save_data()
        print(f"✓ Added: {question}")
    
    def add_multiple_entries(self, entries):
        """Add multiple Q&A pairs at once"""
        for question, answer, category in entries:
            self.add_training_entry(question, answer, category)
    
    def update_college_info(self, info_dict):
        """Update college information"""
        self.data["college_info"].update(info_dict)
        self.save_data()
        print("✓ College info updated")
    
    def list_all_training_data(self):
        """List all training data"""
        print(f"\n{'='*60}")
        print(f"COLLEGE INFO: {json.dumps(self.data['college_info'], indent=2)}")
        print(f"\n{'='*60}")
        print(f"TRAINING DATA ({len(self.data['training_data'])} entries):")
        print(f"{'='*60}\n")
        
        for idx, entry in enumerate(self.data["training_data"], 1):
            print(f"{idx}. [{entry['category'].upper()}]")
            print(f"   Q: {entry['question']}")
            print(f"   A: {entry['answer']}\n")
    
    def get_category_count(self):
        """Get count of entries by category"""
        categories = {}
        for entry in self.data["training_data"]:
            cat = entry.get("category", "general")
            categories[cat] = categories.get(cat, 0) + 1
        return categories


if __name__ == "__main__":
    manager = TrainingDataManager()
    
    # Example: Add new training data
    new_entries = [
        ("What is the college website?", "Visit www.college.edu for more information.", "general"),
        ("How do I apply for scholarship?", "Apply through the student portal after admission.", "admissions"),
        ("What are the lab timings?", "Labs are open from 9:00 AM to 5:00 PM.", "timings"),
    ]
    
    print("Adding sample training data...")
    manager.add_multiple_entries(new_entries)
    
    # Update college info
    college_info = {
        "phone": "+91-44-XXXXXXXX",
        "email": "info@college.edu",
        "website": "www.college.edu"
    }
    manager.update_college_info(college_info)
    
    # Display all data
    manager.list_all_training_data()
    
    # Show statistics
    print(f"\n{'='*60}")
    print("CATEGORY STATISTICS:")
    print(f"{'='*60}")
    for category, count in manager.get_category_count().items():
        print(f"{category.upper()}: {count} entries")
