"""The source's pinned documents of each certificate directory, read as data
against the asset and the exact values (review think-4ul6).

Reads, for each certificate, README.md, bundle.json, ASSET.json and
files-sha256.json fetched at the pinned revision (from raw.githubusercontent.com,
into a directory of their own), the release asset (in memory), and the packet's
source-manifest.json.  Nothing of the source is executed.

- every document's SHA-256 against the manifest's pin;
- bundle.json's net block, digests and comparisons against exact recomputation;
- ASSET.json's size and digest against the asset;
- the README: the files it names against the asset's members; its stated mass,
  digest, count and seconds against the candidate and receipts;
- the shipped check2/src/fine_net_check.sh: which receipt shape it writes, and its
  mutant and control-direction rules;
- the bundle's check2/src/SOUNDNESS.md: its Git blob, whether it is this
  repository's edition at e020eb1e2, and whether it states anything for a declared
  net (proof_net); the nested archive's own SOUNDNESS.md, likewise.

Usage: python3 -I check_source_docs.py PACKET DOCS_DIR ASSET_DIR REPO [--out FILE]
DOCS_DIR holds n28/ and n30/ with the four fetched documents each.
"""

from __future__ import annotations

import argparse
import difflib
import hashlib
import io
import json
import re
import subprocess
import sys
import tarfile
from fractions import Fraction as F
from pathlib import Path


def sha(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def git_blob(b: bytes) -> str:
    return hashlib.sha1(b"blob %d\0" % len(b) + b).hexdigest()


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("packet", type=Path)
    ap.add_argument("docs", type=Path)
    ap.add_argument("assets", type=Path)
    ap.add_argument("repo", type=Path)
    ap.add_argument("--out", type=Path)
    args = ap.parse_args()
    manifest = json.loads((args.packet / "source-manifest.json").read_text())
    e020 = subprocess.run(["git", "-C", str(args.repo), "show", "e020eb1e2:packing/sqverify_fast/SOUNDNESS.md"], capture_output=True).stdout
    out = {"certificates": []}
    problems = []
    for entry, short in zip(manifest["certificates"], ("n28", "n30")):
        cert = entry["certificate"]
        rec = {"certificate": cert}
        pins = {Path(d["path"]).name: d for d in entry["source_documents"] if Path(d["path"]).name in ("README.md", "bundle.json", "ASSET.json", "files-sha256.json")}
        docs = {k: (args.docs / short / k).read_bytes() for k in pins}
        rec["documents_equal_pins"] = {k: sha(v) == pins[k]["sha256"] and len(v) == pins[k]["bytes"] for k, v in docs.items()}
        asset = (args.assets / entry["release"]["asset"]).read_bytes()
        with tarfile.open(fileobj=io.BytesIO(asset), mode="r:gz") as tf:
            members = {m.name: tf.extractfile(m).read() for m in tf.getmembers() if m.isfile()}
        prefix = f"certificates/{cert}/"
        names = {k[len(prefix):] for k in members}
        # The sealed bundle holds every file of the directory (documents included).
        sealed_name = entry["sealed_inner_bundle"]["name"]
        with tarfile.open(fileobj=io.BytesIO(members[prefix + sealed_name]), mode="r:gz") as st:
            sealed = {m.name.split("/", 1)[1]: st.extractfile(m).read() for m in st.getmembers() if m.isfile()}
        names |= set(sealed)
        cand = json.loads(members[prefix + "candidate.json"])
        receipt = json.loads(members[prefix + "check2/receipt.json"])
        n, L, B = cand["n"], F(cand["L"]), F(cand["B"])
        D = F(cand["proof_net"]["step"])
        last = cand["proof_net"]["last"]
        t = last * D
        b = json.loads(docs["bundle.json"])
        net = b["net"]
        M = sum((F(r["mass"]) for r in cand["rectangles"]), F(0))
        rec["bundle"] = {
            "n_L_B_net_mass": b["n"] == n and F(b["L"]) == L and F(b["B"]) == B and b["proof_net"] == cand["proof_net"]
            and b["angle_count"] == last + 1 and F(b["total_mass"]) == M,
            "endpoint": net["endpoint"], "endpoint_equals_t_max": F(net["endpoint"]) == t,
            "endpoint_check_equals_poly": F(net["endpoint_check"]) == t * t + 2 * t - 1,
            "rotated_side_upper_equals_B(1+D)": F(net["rotated_side_upper"]) == B * (1 + D),
            "side_margin_equals": F(net["side_margin"]) == 1 - B * (1 + D),
            "per_edge_margin_equals_half": F(net["per_edge_margin"]) == (1 - B * (1 + D)) / 2,
            "candidate_sha256_equals": b["candidate_sha256"] == sha(members[prefix + "candidate.json"]),
            "candidate_digest_equals_receipt": b["candidate_digest"] == receipt["candidate_digest"],
            "receipt_sha256_equals": b["receipt_sha256"] == sha(members[prefix + "check2/receipt.json"]),
            "verifier_sources_equal_sealed_members": all(
                "check2/src/" + k in sealed and sha(sealed["check2/src/" + k]) == v
                for k, v in b["verifier_source_sha256"].items() if k != "verifier_build_source_sha256"
            ),
            "build_source": b["verifier_source_sha256"]["verifier_build_source_sha256"],
            "compared_with": b["compared_with"], "improvement_lower": b["improvement_lower"],
            "improvement_exact": F(b["improvement_lower"]) == L - F(b["compared_with"]),
            "verification_text": b["verification"],
        }
        a = json.loads(docs["ASSET.json"])
        rec["asset_json"] = {"size_sha_equal_asset": a["assets"][0]["size"] == len(asset) and a["assets"][0]["sha256"] == sha(asset),
                             "source_commit": a["source"]["commit"], "check": a["check"]}
        readme = docs["README.md"].decode()
        named = sorted(set(re.findall(r"`(check2/[^`]+|candidate\.json|bundle\.json|files-sha256\.json|verification/[^`]+)`", readme)))
        rec["readme"] = {
            "files_named": named,
            "named_but_absent": [p for p in named if p.rstrip("/") not in names and not any(x.startswith(p) for x in names)],
            "states_digest": receipt["candidate_digest"] in readme,
            "states_mass": f"{M.numerator}/{M.denominator}" in readme,
            "states_2073": "2073" in readme,
            "seconds_stated": re.findall(r"VERIFIED in ([0-9.]+) s", readme),
        }
        sealed_readme = sealed["README.md"].decode().splitlines()
        added = [x[1:] for x in difflib.unified_diff(sealed_readme, readme.splitlines(), lineterm="", n=0)
                 if x.startswith("+") and not x.startswith("+++")]
        removed = [x for x in difflib.unified_diff(sealed_readme, readme.splitlines(), lineterm="", n=0)
                   if x.startswith("-") and not x.startswith("---")]
        rec["readme"]["pinned_minus_sealed"] = {"lines_added": len(added), "lines_removed": len(removed),
                                                "headings_added": [x for x in added if x.startswith("#")]}
        script = sealed["check2/src/fine_net_check.sh"].decode()
        rec["shipped_script"] = {
            "sha256": sha(sealed["check2/src/fine_net_check.sh"]),
            "writes_build_field": '"build": summary.get("build")' in script,
            "writes_schema_field": "schema" in script,
            "writes_tries": "tries" in script,
            "control_kind_text": re.findall(r'"kind": "([^"]+)"', script),
            "mutant_rule": "F(985, 1000)" in script and "json.dump(d, open(sys.argv[2], \"w\"))" in script,
            "control_directions_rule": "round(i*(c-1)/31)) for i in range(32)" in script,
            "published_receipt_schema": receipt["receipt"].get("schema"),
            "published_receipt_has_build_field": "build" in receipt["receipt"],
        }
        snd = sealed["check2/src/SOUNDNESS.md"]
        rec["bundle_soundness"] = {
            "git_blob": git_blob(snd),
            "equals_e020eb1e2_edition": snd == e020,
            "mentions_proof_net": b"proof_net" in snd,
            "has_declared_nets_section": b"## Declared Nets" in snd,
        }
        arch = sealed["check2/src/sqverify-proof-net-fe12e036c.tar.gz"]
        with tarfile.open(fileobj=io.BytesIO(arch), mode="r:gz") as at:
            asnd = at.extractfile("sqverify_fast/SOUNDNESS.md").read()
        rec["archive_soundness"] = {"mentions_proof_net": b"proof_net" in asnd, "has_declared_nets_section": b"## Declared Nets" in asnd,
                                    "lines_more_than_bundle_copy": asnd.count(b"\n") - snd.count(b"\n")}
        for k, v in rec["documents_equal_pins"].items():
            if not v:
                problems.append(f"{cert} {k} differs from the pin")
        for k in ("n_L_B_net_mass", "endpoint_equals_t_max", "endpoint_check_equals_poly", "rotated_side_upper_equals_B(1+D)", "side_margin_equals",
                  "per_edge_margin_equals_half", "candidate_sha256_equals", "candidate_digest_equals_receipt", "receipt_sha256_equals", "improvement_exact"):
            if not rec["bundle"][k]:
                problems.append(f"{cert} bundle {k}")
        out["certificates"].append(rec)
    out["problems"] = problems
    text = json.dumps(out, indent=1)
    if args.out:
        args.out.write_text(text + "\n")
    print(text)
    return 0 if not problems else 1


if __name__ == "__main__":
    sys.exit(main())
