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
    schema_path = FRONTIER / meta["schema"]
    if not schema_path.exists():
        return errs + [f"declared schema not found: {meta['schema']}"]
    v = Draft202012Validator(load_schema(meta["schema"]))
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


def main() -> int:
    md = sorted(FRONTIER.glob("n-*.md"))
    datasets = sorted(p for p in FRONTIER.glob("*.yaml") if not p.name.endswith(".schema.yaml"))
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
    for e in cross_checks():
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
