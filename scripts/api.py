import os
import requests

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
GITHUB_REPOSITORY = os.getenv("GITHUB_REPOSITORY")

if not GITHUB_TOKEN:
    raise RuntimeError("GITHUB_TOKEN is not set")

if not GITHUB_REPOSITORY:
    raise RuntimeError("GITHUB_REPOSITORY is not set")

BASE_API = f"https://api.github.com/repos/{GITHUB_REPOSITORY}"


def _headers():
    return {
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "Accept": "application/vnd.github+json"
    }


def get(path, params=None):
    url = f"{BASE_API}{path}"
    r = requests.get(url, headers=_headers(), params=params)
    r.raise_for_status()
    return r.json()


def post(path, data=None):
    url = f"{BASE_API}{path}"
    r = requests.post(url, headers=_headers(), json=data)
    r.raise_for_status()
    return r.json()


def patch(path, data=None):
    url = f"{BASE_API}{path}"
    r = requests.patch(url, headers=_headers(), json=data)
    r.raise_for_status()
    return r.json()
