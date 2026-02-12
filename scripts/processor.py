from datetime import datetime
from .api import get, post
from .utils import parse_iso_datetime, extract_product_name


def child_issue_exists(parent_number, title):
    """
    Prevent duplicate child creation by checking open issues
    with matching title and parent reference.
    """
    issues = get("/issues", params={
        "state": "open",
        "per_page": 100
    })

    for issue in issues:
        if issue["title"] == title:
            body = issue.get("body", "")
            if f"Parent: #{parent_number}" in body:
                return True
    return False


def process_issue(issue, config):
    out = []

    title = issue["title"]
    number = issue["number"]
    created = parse_iso_datetime(issue["created_at"])

    cutoff = datetime.fromisoformat(
        config["cutoff_date"].replace("Z", "+00:00")
    )

    if created < cutoff:
        return out

    product = extract_product_name(title)

    labels = issue.get("labels", [])
    bu = next(
        (l["name"] for l in labels if l["name"].startswith("BU::")),
        None
    )

    # Base labels from config
    base_labels = list(config["default_labels"])

    # Add BU if present
    if bu:
        base_labels.append(bu)

    # Always enforce filter::ignore
    if "filter::ignore" not in base_labels:
        base_labels.append("filter::ignore")

    for task_name, secure_label in config["tasks"]:
        child_title = f"[{task_name}] {product}"

        if child_issue_exists(number, child_title):
            continue

        body = (
            f"Parent: #{number}\n\n"
            f"Auto-generated task for **{product}**.\n"
        )

        data = {
            "title": child_title,
            "body": body,
            "labels": base_labels + [secure_label]
        }

        child = post("/issues", data)

        out.append((child_title, child["number"]))

    return out
