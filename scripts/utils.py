import json, os
from datetime import datetime

def load_processed(path="processed.json"):
    if not os.path.exists(path): return set()
    return set(json.load(open(path)))

def save_processed(s, path="processed.json"):
    json.dump(sorted(list(s)), open(path, "w"), indent=2)

def parse_iso_datetime(s):
    if s.endswith("Z"): s=s.replace("Z","+00:00")
    return datetime.fromisoformat(s)

def extract_product_name(title):
    prefix="[Repo Mapping Update]"
    cleaned=title.replace(prefix,"",1).strip()
    if not cleaned: raise ValueError("Missing product")
    return cleaned
