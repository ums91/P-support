"""
Main runner for scheduled or manual GitHub Actions workflow.
Detects parent issues by title prefix instead of label.
"""

import os
import sys
import json

# Ensure project root is in path
sys.path.append(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
)

from scripts.api import get
from scripts.processor import process_issue
from scripts.utils import load_processed, save_processed

CONFIG_PATH = os.path.join(
    os.path.dirname(__file__),
    "..",
    "config",
    "settings.json"
)

PARENT_PREFIX = "[Repo Mapping Update]"


def load_config():
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def main():
    config = load_config()
    processed = load_processed("processed.json")

    print(f"Loaded {len(processed)} processed issues")

    # Fetch all open issues (no label filtering)
    issues = get("/issues", params={
        "state": "open",
        "per_page": 100
    })

    # Filter by title prefix
    parent_issues = [
        i for i in issues
        if i["title"].startswith(PARENT_PREFIX)
    ]

    print(f"Found {len(parent_issues)} parent issues")

    new_count = 0

    for issue in parent_issues:
        number = int(issue["number"])

        if number in processed:
            continue

        print(f"Processing parent issue #{number}")

        results = process_issue(issue, config)

        if results:
            print(f"Created {len(results)} child tasks for #{number}")
        else:
            print(f"No action required for #{number}")

        processed.add(number)
        new_count += 1

    save_processed(processed, "processed.json")

    print(f"Completed run. Total processed this run: {new_count}")


if __name__ == "__main__":
    main()
