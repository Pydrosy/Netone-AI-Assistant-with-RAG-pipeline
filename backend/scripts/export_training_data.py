#!/usr/bin/env python3
"""
Export training data for model improvement
"""

import sys
import os
import csv
import json
from datetime import datetime

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.models.database import SessionLocal, TrainingData, Message
from sqlalchemy import and_

def export_training_data():
    """Export training data to CSV and JSON formats"""
    
    db = SessionLocal()
    
    # Get all training data with positive feedback (helpful responses)
    training_data = db.query(TrainingData).filter(
        TrainingData.was_helpful == True
    ).all()
    
    print(f"Found {len(training_data)} helpful training examples")
    
    # Export to CSV for fine-tuning
    csv_file = f"training_data_{datetime.now().strftime('%Y%m%d')}.csv"
    with open(csv_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['user_question', 'assistant_response', 'sources', 'rating'])
        
        for data in training_data:
            writer.writerow([
                data.user_question,
                data.assistant_response,
                json.dumps(data.sources_used),
                data.user_rating or ''
            ])
    
    print(f"✅ Exported to {csv_file}")
    
    # Export to JSONL format (for fine-tuning)
    jsonl_file = f"training_data_{datetime.now().strftime('%Y%m%d')}.jsonl"
    with open(jsonl_file, 'w', encoding='utf-8') as f:
        for data in training_data:
            record = {
                "messages": [
                    {"role": "user", "content": data.user_question},
                    {"role": "assistant", "content": data.assistant_response}
                ],
                "metadata": {
                    "sources": data.sources_used,
                    "rating": data.user_rating
                }
            }
            f.write(json.dumps(record) + '\n')
    
    print(f"✅ Exported to {jsonl_file}")
    
    # Summary
    print("\n📊 Training Data Summary:")
    print(f"Total helpful examples: {len(training_data)}")
    
    db.close()
    
    return len(training_data)

if __name__ == "__main__":
    count = export_training_data()
    print(f"\n🎉 Export complete! {count} records exported.")