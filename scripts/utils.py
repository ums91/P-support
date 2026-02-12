import json
import os
from datetime import datetime

def load_processed(path="processed.json"):
    if not os.path.exists(path):
        return set()
    with open(path, "r", encoding="utf-8") as f:
        return set(json.load(f))

def save_processed(s, path="processed.json"):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(sorted(list(s)), f, indent=2)

def parse_iso_datetime(s):
    if s.endswith("Z"):
        s = s.replace("Z", "+00:00")
    return datetime.fromisoformat(s)

def extract_product_name(title):
    prefix = "[Repo Mapping Update]"
    cleaned = title.replace(prefix, "", 1).strip()
    if not cleaned:
        raise ValueError("Missing product name in issue title")
    return cleaned
