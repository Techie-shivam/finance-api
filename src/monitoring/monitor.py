import json
import os
from datetime import datetime

LOG_FILE = "data/predictions_log.jsonl"

def log_prediction(description: str, category: str):
    os.makedirs("data", exist_ok=True)
    entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "description": description,
        "category": category
    }
    with open(LOG_FILE, "a") as f:
        f.write(json.dumps(entry) + "\n")

def check_drift():
    if not os.path.exists(LOG_FILE):
        return
    categories = []
    with open(LOG_FILE) as f:
        for line in f:
            categories.append(json.loads(line)["category"])

    from collections import Counter
    dist = Counter(categories)
    print("Category distribution (last predictions):")
    for cat, count in dist.most_common():
        print(f"  {cat}: {count}")