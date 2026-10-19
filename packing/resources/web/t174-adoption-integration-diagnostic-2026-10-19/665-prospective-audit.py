"""Review-only immutable data comparisons. No geometric or mathematical decider.

Read log, scope, invocation, and output are in 665-prospective-audit-README.md.
"""

import argparse
import ast
from fractions import Fraction
import gzip
import json
import lzma
from pathlib import Path
import subprocess

import yaml


COUNTS = [68, 84, 86, 103, 105, 108, 110, 127, 130, 131, 132, 155, 172,
          179, 180, 181, 182, 206, 208, 209, 210, 228, 238, 239, 240, 261,
          263, 268, 269, 270, 272, 273, 297, 305, 306, 307, 308]


def git(*args):
    return subprocess.check_output(["git", *args])


def blob(revision, path):
    return git("show", f"{revision}:{path}")


def structured(revision, path):
    data = blob(revision, path)
    if path.endswith(".gz"):
        data = gzip.decompress(data)
    elif path.endswith(".xz"):
        data = lzma.decompress(data)
    return yaml.safe_load(data)


def frontiers(revision):
    paths = [f"packing/frontier/n-{n:03d}.md" for n in range(1, 325)]
    raw = subprocess.check_output(["git", "cat-file", "--batch"],
                                  input="".join(f"{revision}:{p}\n" for p in paths).encode())
    offset = 0
    result = {}
    for n in range(1, 325):
        end = raw.index(b"\n", offset)
        header = raw[offset:end].decode()
        if header.endswith(" missing"):
            offset = end + 1
            continue
        size = int(header.split()[-1])
        data = raw[end + 1:end + 1 + size].decode()
        offset = end + size + 2
        result[n] = yaml.safe_load(data.split("---", 2)[1])["packing"]
    return result


def by_n(data):
    if isinstance(data, list):
        return {int(row["n"]): row for row in data if isinstance(row, dict) and "n" in row}
    for value in data.values():
        if isinstance(value, list) and value and isinstance(value[0], dict) and "n" in value[0]:
            return by_n(value)
        if isinstance(value, dict) and (found := by_n(value)):
            return found
    return {}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    for key in ("head", "base", "preintegration", "output"):
        parser.add_argument(f"--{key}", required=True)
    args = parser.parse_args()
    revs = {key: git("rev-parse", getattr(args, key)).decode().strip()
            for key in ("head", "base", "preintegration")}
    cases = {key: frontiers(rev) for key, rev in revs.items()}
    failures = []

    def check(label, condition):
        if not condition:
            failures.append(label)
        return condition

    check("case-roster", set(cases["head"]) == set(cases["base"]))
    rows = []
    for n in COUNTS:
        current, base, prior = (cases[k][n] for k in revs)
        row = {"n": n}
        for lane in ("reported_upper_bound", "verified_upper_bound"):
            row[f"{lane}_preintegration_equal"] = check(f"{n}:{lane}:prior", current[lane] == prior[lane])
            exact = Fraction(current[lane]["exact_form"])
            old_literal = base[lane].get("exact_form")
            basis = lane
            if old_literal is None:
                old_literal = base["verified_upper_bound"].get("exact_form")
                basis = "verified_upper_bound (reported lane has no exact form)"
            if old_literal is None:
                raise ValueError(f"n={n}: no exact baseline for {lane}")
            old = Fraction(old_literal)
            row[f"{lane}_comparison_basis"] = basis
            row[f"{lane}_strict_improvement"] = check(f"{n}:{lane}:strict", exact < old)
            row[f"{lane}_safe_display"] = check(f"{n}:{lane}:display", Fraction(current[lane]["value"]) >= exact)
        row["equal_exact_upper_lanes"] = check(f"{n}:upper-lane-agreement",
            Fraction(current["reported_upper_bound"]["exact_form"]) == Fraction(current["verified_upper_bound"]["exact_form"]))
        for lane in ("reported_lower_bound", "verified_lower_bound"):
            row[f"{lane}_base_equal"] = check(f"{n}:{lane}:base", current.get(lane) == base.get(lane))
        row["base_priority_retained"] = check(f"{n}:base-priority", all(item in current["priority_notes"] for item in base["priority_notes"]))
        row["prior_priority_retained"] = check(f"{n}:prior-priority", all(item in current["priority_notes"] for item in prior["priority_notes"]))
        row["base_evidence_retained"] = check(f"{n}:base-evidence", set(base["evidence"]) <= set(current["evidence"]))
        row["prior_evidence_retained"] = check(f"{n}:prior-evidence", set(prior["evidence"]) <= set(current["evidence"]))
        rows.append(row)
    all_lower_equal = check("all-case-lower-lanes", all(cases["head"][n].get(lane) == cases["base"][n].get(lane)
                            for n in cases["base"] for lane in ("reported_lower_bound", "verified_lower_bound")))
    other_cases = [n for n in cases["base"] if n not in COUNTS and cases["head"][n] != cases["base"][n]]
    check("nonadopted-case-metadata", not other_cases)

    result_sets = {k: {r["id"]: r for r in structured(rev, "packing/frontier/results.yaml")["results"]}
                   for k, rev in revs.items()}
    check("result-id-roster", set(result_sets["head"]) == set(result_sets["base"]))
    inherited_new = [f"T-{n:03d}" for n in range(200, 218)]
    inherited_changed = [rid for rid in inherited_new if result_sets["head"][rid] != result_sets["base"][rid]]
    check("671-new-records-unchanged", len(inherited_new) == 18 and not inherited_changed)
    check("existing-assurance-unchanged", all(
        row.get(key) == result_sets["base"][rid].get(key)
        for rid, row in result_sets["head"].items()
        for key in ("scope", "verification", "confirmation", "significance", "attribution", "reviews", "evidence", "artifacts", "controls")))
    changed_results = {}
    for rid, old in result_sets["base"].items():
        current = result_sets["head"][rid]
        keys = [key for key in sorted(set(old) | set(current)) if old.get(key) != current.get(key)]
        if keys:
            changed_results[rid] = {key: {"base": old.get(key), "head": current.get(key)} for key in keys}

    archive_path = "packing/devtools/house-adoption-prior-state-2026-10-17.json.xz"
    archives = {k: by_n(structured(rev, archive_path)["cases"]) for k, rev in revs.items()}
    archive_preserved = {key: check(f"archive:{key}", all(archives["head"].get(n) == record for n, record in archives[key].items()))
                         for key in ("base", "preintegration")}
    check("archive-exact-union", set(archives["head"]) == set(archives["base"]) | set(archives["preintegration"]))

    retained_files = {}
    for relative in ("packing/witnesses/known-best/n-{n:03d}.yaml", "packing/atlas/known-best/regularized/n-{n:03d}-regularized.yaml.gz"):
        bad = [n for n in COUNTS if blob(revs["head"], relative.format(n=n)) != blob(revs["preintegration"], relative.format(n=n))]
        retained_files[relative] = {"compared": len(COUNTS), "changed": bad}
        check(f"retained:{relative}", not bad)
    n29 = {"case_metadata_equal": check("n29:case", cases["head"][29] == cases["base"][29])}
    for path in ("packing/witnesses/known-best/n-029.yaml", "packing/atlas/known-best/regularized/n-029-regularized.yaml.gz",
                 "packing/atlas/known-best/rendering/n-029.svg", "packing/atlas/known-best/regularized/rendering/n-029.svg"):
        n29[path] = check(f"n29:{path}", blob(revs["head"], path) == blob(revs["base"], path))
    n29["reported_upper_bound"] = cases["head"][29]["reported_upper_bound"]

    indexes = {}
    for path in ("packing/atlas/known-best/regularized/index.json", "packing/atlas/known-best/manifest.json", "packing/atlas/known-best/bound-citations.json"):
        parsed = {k: structured(rev, path) for k, rev in revs.items()}
        index = {k: by_n(data) for k, data in parsed.items()}
        if index["head"]:
            changed = [n for n in COUNTS if index["head"].get(n) != index["preintegration"].get(n)]
            indexes[path] = {"keys": list(parsed["head"]), "count": len(index["head"]), "adopted_entry_changes_from_prior": changed,
                             "n29_equal_base": index["head"].get(29) == index["base"].get(29)}
            check(f"index:{path}:n29", indexes[path]["n29_equal_base"])

    defaults = {k: structured(rev, "packing/atlas/known-best/default-drawings.json") for k, rev in revs.items()}
    states = {k: by_n(data["states"]) for k, data in defaults.items()}
    check("adopted-regularization-states-unchanged", all(states["head"][n] == states["preintegration"][n] for n in COUNTS))
    check("n29-regularization-state", states["head"][29] == states["base"][29])
    check("no-pending-adopted-drawings", all(states["head"][n]["state"] != "pending" for n in COUNTS))
    drawings = {n: states["head"][n]["state"] for n in COUNTS}
    head_ast = ast.parse(blob(revs["head"], "packing/devtools/upper_bound_houses.py"))
    adopted = next(ast.literal_eval(node.value) for node in head_ast.body
                   if isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name) and node.target.id == "ADOPTED")
    check("adoption-map-37-T174", sorted(n for n, rid in adopted.items() if rid == "T-174") == COUNTS)
    check("adoption-map-n29-T195", adopted[29] == "T-195")
    check("adoption-history-exists", all(cases["head"][n]["priority_notes"] for n in adopted))

    identities = {}
    for path, comparison in (
        ("packing/frontier/evidence.yaml", "base"),
        ("packing/frontier/verifiers.yaml", "base"),
        ("packing/resources/web/pingyou-pr574-certificates-2026-10-13", "base"),
        ("packing/cases/regularized_drawings/think-3mry-2026-10-17", "preintegration"),
    ):
        identities[path] = check(f"retained-tree:{path}", git("rev-parse", f"{revs['head']}:{path}") == git("rev-parse", f"{revs[comparison]}:{path}"))

    receipt_path = "packing/devtools/house-custody-2026-10-11.json"
    receipts = {k: structured(rev, receipt_path) for k, rev in revs.items()}
    receipt = {k: {field: data.get(field) for field in ("outcome", "houses", "setup_seconds", "call_seconds", "snapshot_source_bytes", "fresh_geometric_deciders")} for k, data in receipts.items()}
    receipt["head_equals_preintegration"] = receipts["head"] == receipts["preintegration"]
    receipt["missing_current_adoptions"] = sorted(set(adopted) - {int(n) for n in receipts["head"]["houses"]})

    selected = {rid: {key: row.get(key) for key in ("headline", "scope", "verification", "confirmation", "significance", "attribution", "evidence", "reviews")} for rid, row in result_sets["head"].items()
                if rid in ("T-174", "T-195") or rid in inherited_new}
    data = {"classification": "Engineering diagnostic only: data preservation and exact rational comparison; no replay, no geometric decision, no rung change.",
            "revisions": revs, "failures": failures, "case_count": len(cases["head"]), "adoption_counts": COUNTS,
            "adoption_checks": rows, "all_lower_lanes_equal_base": all_lower_equal,
            "nonadopted_metadata_changes": other_cases, "result_counts": {k: len(v) for k, v in result_sets.items()},
            "new_671_ids": inherited_new, "new_671_changed": inherited_changed, "changed_results": changed_results,
            "archives": {"counts": {k: len(v) for k, v in archives.items()}, "parent_entries_preserved": archive_preserved},
            "retained_files": retained_files, "n29": n29, "indexes": indexes, "custody": receipt,
            "adopted_house_count": len(adopted), "drawing_states": drawings, "retained_tree_identity": identities,
            "selected_results": selected}
    Path(args.output).write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n")
    print(json.dumps({key: data[key] for key in ("classification", "revisions", "failures", "case_count", "all_lower_lanes_equal_base", "nonadopted_metadata_changes", "result_counts", "new_671_ids", "new_671_changed", "archives", "retained_files", "indexes")}, indent=2))
    print("Changed existing result fields:", {rid: list(fields) for rid, fields in changed_results.items()})
    print("Historical custody receipt unchanged:", receipt["head_equals_preintegration"])
    print("Current houses absent from historical custody:", receipt["missing_current_adoptions"])
    print("Drawing states:", drawings)
    print("Retained tree identities:", identities)
    raise SystemExit(bool(failures))


if __name__ == "__main__":
    main()
