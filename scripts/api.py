import os
import requests

GITLAB_TOKEN = os.getenv("GITLAB_TOKEN")
PROJECT_ID = 59536281
BASE_API = f"https://gitlab.com/api/v4/projects/{PROJECT_ID}"

def _headers():
    if not GITLAB_TOKEN:
        raise RuntimeError("GITLAB_TOKEN is not set")
    return {"PRIVATE-TOKEN": GITLAB_TOKEN}

def get(path, params=None):
    url = f"{BASE_API}{path}"
    r = requests.get(url, headers=_headers(), params=params)
    r.raise_for_status()
    return r.json()

def post(path, data=None):
    url = f"{BASE_API}{path}"
    r = requests.post(url, headers=_headers(), data=data)
    r.raise_for_status()
    return r.json()
