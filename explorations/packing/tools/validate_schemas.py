#!/usr/bin/env python3
"""Validate every soft-schema artifact in frontier/ against its declared schema.

Two profiles are in use and they need different handling:

- `frontmatter-md` (the 100 `n-NNN.md` cases). The softschema CLI validates
  these directly: `uvx softschema@latest validate n-011.md`.
- `pure-yaml` (the four dataset files). The spec defines this profile, but
  softschema 0.6.1's CLI rejects any file without frontmatter
  ("missing --contract because the document has no YAML frontmatter"), so the
  CLI cannot enforce them today. Declaring `status: enforced` on a file nothing
  checks would be a claim-integrity defect of exactly the kind this project
  keeps finding in its sources, so this script validates them against the same
  compiled JSON Schema the CLI would use.

That makes the enforcement real for both profiles with no network access, which
is what `test.sh` needs. Run the CLI separately for an independent check of the
Markdown artifacts.
"""
from __future__ import annotations
import json, pathlib, sys, yaml
from jsonschema import Draft202012Validator

FRONTIER = pathlib.Path(__file__).resolve().parent.parent / "frontier"


def load_schema(name: str) -> dict:
    return yaml.safe_load((FRONTIER / name).read_text(encoding="utf-8"))


def payload_and_meta(path: pathlib.Path) -> tuple[dict, dict]:
    """Return (payload, softschema metadata) for either profile."""
    text = path.read_text(encoding="utf-8")
    if path.suffix == ".md":
        doc = yaml.safe_load(text.split("---\n")[1])
    else:
        doc = yaml.safe_load(text)
    meta = doc.get("softschema")
    if meta is None:
        raise ValueError("no softschema metadata block")
    env = meta.get("envelope")
    if env:
        return doc[env], meta
    # pure-yaml with no envelope: the whole root minus the metadata block
    return {k: v for k, v in doc.items() if k != "softschema"}, meta


def check(path: pathlib.Path) -> list[str]:
    errs: list[str] = []
    payload, meta = payload_and_meta(path)
    for key in ("contract", "schema", "status"):
        if not meta.get(key):
            errs.append(f"softschema.{key} missing")
    if errs:
        return errs
    if meta["status"] != "enforced":
        errs.append(f"status is {meta['status']!r}, expected 'enforced'")
    # A soft-schema document's `schema` is relative to the document, so resolve it
    # that way rather than against one fixed directory -- otherwise no artifact can
    # live outside frontier/, which the defect log does.
    schema_path = (path.parent / meta["schema"]).resolve()
    if not schema_path.exists():
        return errs + [f"declared schema not found: {meta['schema']}"]
    v = Draft202012Validator(yaml.safe_load(schema_path.read_text(encoding="utf-8")))
    for e in sorted(v.iter_errors(payload), key=lambda e: list(e.path)):
        loc = "/".join(str(x) for x in e.path) or "<root>"
        errs.append(f"{loc}: {e.message}")
    return errs


def cross_checks() -> list[str]:
    """Invariants a JSON Schema cannot express."""
    errs = []
    for kind in ("search", "proof"):
        d = yaml.safe_load((FRONTIER / f"{kind}-strategies.yaml").read_text(encoding="utf-8"))
        ss = d["strategies"]
        if d["count"] != len(ss):
            errs.append(f"{kind}-strategies: count {d['count']} != {len(ss)} entries")
        if [s["id"] for s in ss] != list(range(1, len(ss) + 1)):
            errs.append(f"{kind}-strategies: ids are not 1..{len(ss)}")
        unknown = {s["family"] for s in ss} - set(d["families"])
        if unknown:
            errs.append(f"{kind}-strategies: families not declared: {sorted(unknown)}")
    a = yaml.safe_load((FRONTIER / "asymptotic-waste-bounds.yaml").read_text(encoding="utf-8"))
    for b in a["lower_bounds"]:
        if b["confidence"] == "reconstructed" and not b.get("note"):
            errs.append(f"asymptotic: reconstructed bound {b['source_key']} carries no note")
    sa = yaml.safe_load((FRONTIER / "source-availability.yaml").read_text(encoding="utf-8"))
    keys = [s["key"] for s in sa["recovered"]] + [s["key"] for s in sa["unretrieved"]]
    dupes = {k for k in keys if keys.count(k) > 1}
    if dupes:
        errs.append(f"source-availability: key in both lists or duplicated: {sorted(dupes)}")
    return errs


def defect_checks() -> list[str]:
    """Whole-set invariants for the defect log that a JSON Schema cannot express."""
    errs = []
    path = FRONTIER.parent / "defects.yaml"
    if not path.exists():
        return ["defects.yaml is missing"]
    d = yaml.safe_load(path.read_text(encoding="utf-8"))
    ds = d["defects"]
    if d["count"] != len(ds):
        errs.append(f"defects: count {d['count']} != {len(ds)} entries")
    ids = [x["id"] for x in ds]
    if ids != [f"D-{i:03d}" for i in range(1, len(ids) + 1)]:
        errs.append("defects: ids are not contiguous from D-001")
    known = set(ids)
    for x in ds:
        # An open defect that nobody is tracking is a note, not a defect.
        if x["status"] in ("outstanding", "contained") and not x.get("bead"):
            errs.append(f"{x['id']}: {x['status']} without a bead")
        # The two classes where the direction of the error decides how bad it is.
        if x["class"] in ("soundness", "validity") and not x.get("direction"):
            errs.append(f"{x['id']}: {x['class']} without a direction")
        if x.get("recurrence_of") and x["recurrence_of"] not in known:
            errs.append(f"{x['id']}: recurrence_of unknown {x['recurrence_of']}")
        target = FRONTIER.parent / x["recorded_in"]
        if not target.exists():
            errs.append(f"{x['id']}: recorded_in does not exist: {x['recorded_in']}")
    return errs


def main() -> int:
    md = sorted(FRONTIER.glob("n-*.md"))
    datasets = sorted(p for p in FRONTIER.glob("*.yaml") if not p.name.endswith(".schema.yaml"))
    datasets += [FRONTIER.parent / "defects.yaml"]
    if not md or not datasets:
        print("frontier/ artifacts not found", file=sys.stderr)
        return 2
    failures = 0
    for p in md + datasets:
        errs = check(p)
        if errs:
            failures += 1
            print(f"FAIL {p.name}", file=sys.stderr)
            for e in errs[:6]:
                print(f"     {e}", file=sys.stderr)
    for e in cross_checks() + defect_checks():
        failures += 1
        print(f"FAIL cross-check: {e}", file=sys.stderr)
    if failures:
        return 1
    print(f"  {len(md)} frontmatter-md artifacts + {len(datasets)} pure-yaml datasets "
          f"validate against their declared schemas")
    print(f"  schemas in use: {sorted({yaml.safe_load(p.read_text())['softschema']['schema'] for p in datasets} | {'square-packing-case.schema.yaml'})}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
