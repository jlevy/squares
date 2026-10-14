"""Summarize OBLIGATIONS.json: id, kind, claim, depends_on, evidence file basenames (no hashes).

Usage: python3 -I summarize_obligations.py PATH_TO_OBLIGATIONS.json [kind-filter]
"""
import json
import sys
from collections import Counter

path = sys.argv[1]
kind_filter = sys.argv[2] if len(sys.argv) > 2 else None
with open(path, "r", encoding="utf-8") as fh:
    data = json.load(fh)

rows = data["rows"]
print("schema:", data.get("schema"))
print("scope:", data.get("scope"))
print("rows:", len(rows))
print("kinds:", Counter(r["kind"] for r in rows))
print("top-level keys:", sorted(data.keys()))
print("row keys:", sorted(set(k for r in rows for k in r.keys())))
print()
for r in rows:
    if kind_filter and r["kind"] != kind_filter:
        continue
    print("=" * 100)
    print(f"ID: {r['id']}   KIND: {r['kind']}   GRAPH: {r.get('graph_binding')}")
    print("CLAIM:", r["claim"])
    print("DEPENDS_ON:", r.get("depends_on"))
    ev = r.get("evidence", [])
    print("EVIDENCE (%d):" % len(ev))
    for e in ev:
        f = e.get("file")
        extra = {k: v for k, v in e.items() if k not in ("file", "sha256")}
        print("   -", f, extra if extra else "")
    other = {k: v for k, v in r.items() if k not in ("id", "kind", "claim", "depends_on", "evidence", "graph_binding")}
    if other:
        print("OTHER:", json.dumps(other)[:2000])
