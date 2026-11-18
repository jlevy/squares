"""The source's pinned documents of mixed_n29_L582, read as data against the
asset and the exact values (review think-1lri).  Adapted from the n = 28 and
n = 30 review's program to this directory's eleven pinned documents.

Reads the eleven documents and the enclosing LICENSE fetched at the pinned
revision into a directory of their own, the release asset (in memory), the
packet's source-manifest.json and, by `git show`, this repository's crate at
e020eb1e2.  Nothing of the source is executed.

- every document's size, SHA-256 and Git blob against the manifest's pin;
- bundle.json's net block, digests and comparison against exact recomputation;
- ASSET.json's size and digest against the asset;
- the README: the files it names against the asset, the sealed bundle and the
  pinned directory; its stated digest, mass, count and seconds; the pinned edition
  against the sealed one;
- the shipped fine_net_check.sh: which receipt shape it writes, and its mutant and
  control-direction rules;
- SOUNDNESS.md and INDEPENDENCE.md: their Git blobs against this repository's
  editions, and what SOUNDNESS.md says of the net and of the fold;
- SPEC.md, REPRODUCE.md and the provenance note: the statements the review cites;
- the stated verifier commits (fe12e036c, UPSTREAM_COMMIT) against this clone.

Usage: python3 -I check_source_docs.py PACKET DOCS_DIR ASSET_DIR REPO [--out FILE]
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


def git(repo, *args):
    return subprocess.run(["git", "-C", str(repo), *args], capture_output=True)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("packet", type=Path)
    ap.add_argument("docs", type=Path)
    ap.add_argument("assets", type=Path)
    ap.add_argument("repo", type=Path)
    ap.add_argument("--out", type=Path)
    args = ap.parse_args()
    manifest = json.loads((args.packet / "source-manifest.json").read_text())
    problems = []
    prefix_git = "problems/square-lower-bounds/certificates/mixed_n29_L582/"
    cert = "mixed_n29_L582"
    out: dict = {"certificate": cert}

    # pins
    docs = {}
    pins = {}
    for d in manifest["source_documents"]:
        rel = d["path"][len(prefix_git):]
        b = (args.docs / rel).read_bytes()
        docs[rel] = b
        pins[rel] = len(b) == d["bytes"] and sha(b) == d["sha256"] and git_blob(b) == d["git_blob"]
    lic = (args.docs / "LICENSE").read_bytes()
    notice = manifest["license"]["project_notice"]
    pins["../../LICENSE"] = len(lic) == notice["bytes"] and git_blob(lic) == notice["git_blob"]
    out["documents_equal_pins"] = pins
    out["license_first_line"] = lic.decode().splitlines()[0]
    out["license_names"] = re.findall(r"Copyright \(c\) [^\n]+", lic.decode())
    for k, v in pins.items():
        if not v:
            problems.append(f"{k} differs from its pin")

    asset = (args.assets / manifest["release"]["asset"]).read_bytes()
    with tarfile.open(fileobj=io.BytesIO(asset), mode="r:gz") as tf:
        members = {m.name: tf.extractfile(m).read() for m in tf.getmembers() if m.isfile()}
    prefix = f"certificates/{cert}/"
    in_asset = {k[len(prefix):] for k in members}
    sealed_name = manifest["sealed_inner_bundle"]["name"]
    with tarfile.open(fileobj=io.BytesIO(members[prefix + sealed_name]), mode="r:gz") as st:
        sealed = {m.name.split("/", 1)[1]: st.extractfile(m).read() for m in st.getmembers() if m.isfile()}
    in_git_dir = set(docs)
    cand_bytes = members[prefix + "candidate.json"]
    cand = json.loads(cand_bytes)
    receipt = json.loads(members[prefix + "check2/receipt.json"])
    pre = json.loads(members[prefix + "verification/prepublication-receipt.json"])
    n, L, B = cand["n"], F(cand["L"]), F(cand["B"])
    D = F(cand["proof_net"]["step"])
    last = cand["proof_net"]["last"]
    t = last * D
    M = sum((F(r["mass"]) for r in cand["rectangles"]), F(0))

    b = json.loads(docs["bundle.json"])
    net = b["net"]
    out["bundle"] = {
        "n_L_B_net_mass": b["n"] == n and F(b["L"]) == L and F(b["B"]) == B and b["proof_net"] == cand["proof_net"]
        and b["angle_count"] == last + 1 and F(b["total_mass"]) == M and F(b["L_decimal"]) == L,
        "net_step_count": F(net["step"]) == D and net["count"] == last + 1,
        "endpoint": net["endpoint"], "endpoint_equals_t_max": F(net["endpoint"]) == t,
        "endpoint_check_equals_poly": F(net["endpoint_check"]) == t * t + 2 * t - 1,
        "rotated_side_upper_equals_B(1+D)": F(net["rotated_side_upper"]) == B * (1 + D),
        "side_margin_equals": F(net["side_margin"]) == 1 - B * (1 + D),
        "per_edge_margin_equals_half": F(net["per_edge_margin"]) == (1 - B * (1 + D)) / 2,
        "candidate_sha256_equals": b["candidate_sha256"] == sha(cand_bytes),
        "candidate_digest_equals_receipt": b["candidate_digest"] == receipt["candidate_digest"],
        "receipt_sha256_equals": b["receipt_sha256"] == sha(members[prefix + "check2/receipt.json"]),
        "verifier_sources_equal_sealed_members": all(
            ("check2/src/" + k) in sealed and sha(sealed["check2/src/" + k]) == v
            for k, v in b["verifier_source_sha256"].items() if k != "verifier_build_source_sha256"),
        "build_source": b["verifier_source_sha256"]["verifier_build_source_sha256"],
        "build_source_equals_receipt": b["verifier_source_sha256"]["verifier_build_source_sha256"]
        == receipt["receipt"]["verifier"]["source_sha256"],
        "compared_with": b["compared_with"], "improvement_lower": b["improvement_lower"],
        "improvement_exact": F(b["improvement_lower"]) == L - F(b["compared_with"]),
        "remaining_text": net["remaining"],
        "verification_text": b["verification"],
    }
    a = json.loads(docs["ASSET.json"])
    out["asset_json"] = {
        "size_sha_equal_asset": a["assets"][0]["size"] == len(asset) and a["assets"][0]["sha256"] == sha(asset),
        "source_commit": a["source"]["commit"],
        "published_after_is_the_pin's_parent": a["source"]["published_after"] in manifest["source_parent"],
        "documents_listed_are_pinned": all(p in [d["path"] for d in manifest["source_documents"]] for p in a["documents"]),
        "check": a["check"],
    }

    readme = docs["README.md"].decode()
    named = sorted(set(re.findall(r"`(check2/[^`]+|candidate\.json|bundle\.json|files-sha256\.json|verification/[^`]+|provenance/[^`]*)`", readme)))
    known = in_asset | set(sealed) | in_git_dir
    out["readme"] = {
        "files_named": named,
        "named_but_absent_everywhere": [p for p in named if p.rstrip("/") not in known and not any(x.startswith(p) for x in known)],
        "states_digest": receipt["candidate_digest"] in readme,
        "states_mass": f"{M.numerator}/{M.denominator}" in readme,
        "states_2073": "2073" in readme,
        "control_factor_stated": re.findall(r"x\s?0\.985", readme),
        "0.985_is_197/200": F("0.985") == F(197, 200),
        "seconds_stated": re.findall(r"VERIFIED in ([0-9.]+) s", readme),
        "stated_seconds_equal_prepublication_receipt": re.findall(r"VERIFIED in ([0-9.]+) s", readme) == [str(pre.get("seconds"))],
        "stated_seconds_equal_check2_run": re.findall(r"VERIFIED in ([0-9.]+) s", readme) == [str(receipt["receipt"]["seconds"])],
        "line_numbers": {
            "control_file_line": next((i + 1 for i, x in enumerate(readme.splitlines()) if "control.jsonl.gz" in x), None),
            "second_system_line": next((i + 1 for i, x in enumerate(readme.splitlines()) if "second-system" in x), None),
            "branch_commit_line": next((i + 1 for i, x in enumerate(readme.splitlines()) if "fe12e036c" in x), None),
            "prepublication_line": next((i + 1 for i, x in enumerate(readme.splitlines()) if "Pre-publication" in x or "fresh Ubuntu" in x), None),
        },
    }
    sealed_readme = sealed["README.md"].decode().splitlines()
    diff = list(difflib.unified_diff(sealed_readme, readme.splitlines(), lineterm="", n=0))
    added = [x[1:] for x in diff if x.startswith("+") and not x.startswith("+++")]
    removed = [x for x in diff if x.startswith("-") and not x.startswith("---")]
    out["readme"]["pinned_minus_sealed"] = {"lines_added": len(added), "lines_removed": len(removed),
                                            "headings_added": [x for x in added if x.startswith("#")]}
    for p in out["readme"]["named_but_absent_everywhere"]:
        problems.append(f"note: README names {p}, absent")  # recorded as a finding, not a failure

    script = docs["check2/src/fine_net_check.sh"].decode()
    out["shipped_script"] = {
        "sha256": sha(docs["check2/src/fine_net_check.sh"]),
        "writes_build_field": '"build": summary.get("build")' in script,
        "writes_schema_field": '"schema"' in script,
        "writes_tries": "tries" in script,
        "writes_integer_seconds": '"seconds": int(seconds)' in script,
        "control_kind_text": re.findall(r'"kind": "([^"]+)"', script),
        "mutant_rule": "F(985, 1000)" in script and 'json.dump(d, open(sys.argv[2], "w"))' in script,
        "control_directions_rule": "round(i*(c-1)/31)) for i in range(32)" in script,
        "pass_needs_one_exact_refusal_only": 'receipt["control"]["exact_below_threshold"] > 0' in script,
        "published_receipt_schema": receipt["receipt"].get("schema"),
        "published_receipt_has_build_field": "build" in receipt["receipt"],
        "prepublication_receipt_shape_is_the_script's": sorted(pre) == sorted(
            ["status", "exit", "n", "L", "B", "proof_net", "directions_expected", "directions_checked", "directions_verified",
             "candidate_digest", "file_sha256", "input_sha256", "build", "seconds", "control", "verdict"]),
    }

    snd = docs["check2/src/SOUNDNESS.md"]
    e020 = git(args.repo, "show", "e020eb1e2:packing/sqverify_fast/SOUNDNESS.md").stdout
    head = git(args.repo, "show", "HEAD:packing/sqverify_fast/SOUNDNESS.md").stdout
    ind = docs["check2/src/INDEPENDENCE.md"]
    e020_ind = git(args.repo, "show", "e020eb1e2:packing/sqverify_fast/INDEPENDENCE.md").stdout
    text = snd.decode()
    out["bundle_soundness"] = {
        "git_blob": git_blob(snd),
        "equals_e020eb1e2_edition": snd == e020,
        "mentions_proof_net": "proof_net" in text,
        "has_declared_nets_section": "## Declared Nets" in text,
        "claim_names_the_standard_net": "(here $83/40000$ and $201$)" in text,
        "N2_reflects_the_whole_configuration": "reflect the whole configuration" in text,
        "N2_names_t_200": "t_{200}" in text,
        "line_of_whole_configuration": next((i + 1 for i, x in enumerate(text.splitlines()) if "reflect the whole configuration" in x), None),
        "head_edition_folds_square_by_square": b"The fold is made square by square" in head,
        "head_has_declared_nets_section": b"## Declared Nets" in head,
    }
    out["bundle_independence"] = {"git_blob": git_blob(ind), "equals_e020eb1e2_edition": ind == e020_ind}
    spec = docs["check2/src/SPEC.md"].decode()
    out["spec"] = {
        "orientation_restriction_text": next((x.strip() for x in spec.splitlines() if "may be restricted" in x), None),
        "orientation_line": next((i + 1 for i, x in enumerate(spec.splitlines()) if "may be restricted" in x), None),
        "net_condition_text": next((x.strip() for x in spec.splitlines() if "(1 + last·step)² > 2" in x), None),
        "endpoint_form_equivalent": ((1 + t) ** 2 > 2) == (t * t + 2 * t - 1 > 0),
        "lists_t_max_le_half_in_section_3": "1/2" in spec.split("## 3.")[1].split("## 4.")[0],
        "lists_tangent_form_in_section_5": "B(1 + D/(1 − D²/4)) < 1" in spec,
    }
    rep = docs["check2/src/REPRODUCE.md"].decode()
    out["reproduce"] = {
        "timing_text": [x.strip() for x in rep.splitlines() if "832 directions" in x or "5.81" in x],
        "timing_lines": [i + 1 for i, x in enumerate(rep.splitlines()) if "832 directions" in x or "5.81" in x],
        "names_tools_commit_5fba675": "5fba675" in rep,
    }
    notes = docs["provenance/search-notes.md"].decode()
    out["search_notes"] = {"refers_to_itself": "see provenance/search-notes.md" in notes, "text": notes.strip().splitlines()[2:3]}
    up = docs["check2/src/UPSTREAM_COMMIT"].decode().strip()
    out["verifier_commits"] = {
        "upstream_commit_file": up,
        "upstream_commit_in_this_clone": git(args.repo, "cat-file", "-e", up + "^{commit}").returncode == 0,
        "fe12e036c_in_this_clone": git(args.repo, "rev-parse", "--verify", "--quiet", "fe12e036c^{commit}").returncode == 0,
        "clone_is_shallow": git(args.repo, "rev-parse", "--is-shallow-repository").stdout.decode().strip(),
    }
    out["problems"] = [p for p in problems if not p.startswith("note:")]
    out["notes"] = [p for p in problems if p.startswith("note:")]
    text_out = json.dumps(out, indent=1)
    if args.out:
        args.out.write_text(text_out + "\n")
    print(text_out)
    return 0 if not out["problems"] else 1


if __name__ == "__main__":
    sys.exit(main())
