"""Main runner for scheduled pipelines."""
import os, sys, json

# Ensure project root is in Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scripts.api import get
from scripts.processor import process_issue
from scripts.utils import load_processed, save_processed

CONFIG_PATH = os.path.join(os.path.dirname(__file__), "..", "config", "settings.json")

def load_config():
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def main():
    config = load_config()
    processed = load_processed("processed.json")

    print(f"Loaded {len(processed)} processed IIDs")

    issues = get("/issues", params={"labels": "Repo Mapping Update", "per_page": 100})

    new_count = 0
    for issue in issues:
        iid = int(issue["iid"])
        if iid in processed:
            continue

        results = process_issue(issue, config)
        if results:
            print(f"Processed IID={iid}, created {len(results)} child tasks.")
        else:
            print(f"No action needed for IID={iid}")

        processed.add(iid)
        new_count += 1

    save_processed(processed, "processed.json")
    print(f"Completed run. Total new issues processed: {new_count}")

if __name__ == "__main__":
    main()
