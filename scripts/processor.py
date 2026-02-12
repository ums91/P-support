from datetime import datetime
from .api import get, post
from .utils import parse_iso_datetime, extract_product_name

def child_issue_exists(parent_iid, title):
    for l in get(f"/issues/{parent_iid}/links"):
        if l.get("title")==title: return True
    return False

def process_issue(issue, config):
    out=[]
    title=issue["title"]
    iid=issue["iid"]
    created=parse_iso_datetime(issue["created_at"])
    cutoff=datetime.fromisoformat(config["cutoff_date"].replace("Z","+00:00"))
    if created<cutoff: return out

    product=extract_product_name(title)
    labels=[l["title"] for l in issue["labels"]]
    bu=next((l for l in labels if l.startswith("BU::")), None)

    base=list(config["default_labels"])
    if bu: base.append(bu)

    for name, sec in config["tasks"]:
        ctitle=f"[{name}] {product}"
        if child_issue_exists(iid, ctitle): continue
        data={"title":ctitle,"description":"","labels":",".join(base+[sec])}
        child=post("/issues", data)
        post(f"/issues/{iid}/links", {"target_issue_iid": child["iid"]})
        out.append((ctitle, child["iid"]))
    return out
