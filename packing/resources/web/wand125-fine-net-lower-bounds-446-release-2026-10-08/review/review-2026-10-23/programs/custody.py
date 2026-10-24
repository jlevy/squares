"""Re-derive the release packet's custody records from its bytes (premises only).

For each of the four certificates this checks, with hashlib and the strict gzip reader:

- every retained release member against the retention record (acquisition/
  release-assets.json): a deterministic-gzip member by its decompressed bytes, an
  original-gzip or plain member by its stored bytes;
- the asset's size and SHA-256 against the source's ASSET.json and the 8 October packet's
  catalogue (or, for n = 27, its follow-up facts);
- the source's own inventory (files-sha256.json) against the retained members and
  documents (and, for documents pinned by digest only, the subtree manifest), listing
  the paths where they differ;
- the retained upstream documents against acquisition/upstream-subtree.sha256.

    python3 -I custody.py --packet PACKET --facts FACTS_PACKET --out outputs/custody.json
"""

from __future__ import annotations

import argparse
import json
import resource
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from t233lib import CERTS, loose_json, read_gzip_single, sha256  # noqa: E402


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--packet", type=Path, required=True)
    ap.add_argument("--facts", type=Path, required=True)
    ap.add_argument("--out", type=Path, required=True)
    args = ap.parse_args()
    pkt: Path = args.packet
    retention = loose_json((pkt / "acquisition" / "release-assets.json").read_bytes())
    catalogue = loose_json((args.facts / "reported-catalogue.json").read_bytes())
    followup = loose_json((args.facts / "reported-n27-followup.json").read_bytes())
    by_cert = {c["certificate"]: c for c in catalogue["claims"]}
    subtree = {}
    for line in (pkt / "acquisition" / "upstream-subtree.sha256").read_text().splitlines():
        if line.strip():
            digest, path = line.split(None, 1)
            subtree[path.strip().removeprefix("./")] = digest
    out: dict[str, object] = {"kind": "t233-review-custody/v1", "cases": {}}
    ok_all = True
    for _n, (name, _side) in CERTS.items():
        asset = next(a for a in retention["assets"] if a["certificate"] == name)
        problems: list[str] = []
        members = []
        for m in asset["members"]:
            if "stored" not in m:
                members.append({"path": m["path"], "pinned_only": True})
                continue
            stored = pkt / m["stored"]
            if m["form"] == "gzip":
                _s, raw = read_gzip_single(stored)
                good = sha256(raw) == m["sha256"] and len(raw) == m["bytes"]
            else:
                raw = stored.read_bytes()
                good = sha256(raw) == m["sha256"] and len(raw) == m["bytes"]
            members.append({"path": m["path"], "form": m["form"], "matches": good})
            if not good:
                problems.append(f"{m['path']} does not match the retention record")
        docdir = pkt / "square-packing" / "problems" / "square-lower-bounds" / "certificates" / name
        asset_json = loose_json((docdir / "ASSET.json").read_bytes())
        src_asset = asset_json["assets"][0]
        if (src_asset["size"], src_asset["sha256"]) != (asset["bytes"], asset["sha256"]):
            problems.append("asset size/digest differs from the source's ASSET.json")
        if name in by_cert:
            cat = by_cert[name]
            cat_pair = (cat["stored_bytes"], cat["stored_sha256"])
        else:
            cat_pair = (followup["archive_metadata"]["size"], followup["archive_metadata"]["sha256"])
        if cat_pair != (asset["bytes"], asset["sha256"]):
            problems.append("asset size/digest differs from the 8 October packet")
        inventory = loose_json((docdir / "files-sha256.json").read_bytes())
        member_sha = {m["path"].split(f"certificates/{name}/", 1)[1]: m["sha256"] for m in asset["members"]}
        differs = []
        for rel, digest in inventory.items():
            have = member_sha.get(rel)
            if have is None:
                local = docdir / rel
                if local.exists():
                    have = sha256(local.read_bytes())
                else:  # pinned by digest only: the subtree manifest holds its digest
                    have = subtree.get(f"problems/square-lower-bounds/certificates/{name}/{rel}")
            if have != digest:
                differs.append({"path": rel, "inventory": digest, "retained_or_member": have})
        docs = []
        for rel in ("README.md", "ASSET.json", "bundle.json", "files-sha256.json"):
            key = f"problems/square-lower-bounds/certificates/{name}/{rel}"
            got = sha256((docdir / rel).read_bytes())
            docs.append({"path": rel, "matches_subtree_manifest": subtree.get(key) == got})
            if subtree.get(key) != got:
                problems.append(f"{rel} differs from the subtree manifest")
        case_ok = not problems
        ok_all = ok_all and case_ok
        out["cases"][name] = {
            "asset": {"bytes": asset["bytes"], "sha256": asset["sha256"]},
            "members": members,
            "documents": docs,
            "source_inventory_differences": differs,
            "problems": problems,
            "verdict": "CUSTODY_HOLDS" if case_ok else "CUSTODY_FAILS",
        }
        print(name, out["cases"][name]["verdict"], "inventory differences:",
              [d["path"] for d in differs])
    usage = resource.getrusage(resource.RUSAGE_SELF)
    out["verdict"] = "ALL_CUSTODY_HOLDS" if ok_all else "CUSTODY_PROBLEM"
    out["cpu_seconds"] = round(usage.ru_utime + usage.ru_stime, 3)
    args.out.write_text(json.dumps(out, indent=1, sort_keys=True) + "\n")
    print(out["verdict"], "cpu", out["cpu_seconds"])
    return 0 if ok_all else 1


if __name__ == "__main__":
    raise SystemExit(main())
