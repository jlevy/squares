#!/usr/bin/env python3
"""Validate every enforced packing soft-schema artifact against its declared schema.

Two profiles are in use and they need different handling:

- `frontmatter-md` (the 100 `n-NNN.md` cases). The softschema CLI validates
  these directly: `uvx softschema@latest validate n-011.md`.
- `pure-yaml` (frontier datasets, defects, and witness interchange files). The spec
  defines this profile, but
  softschema 0.6.1's CLI rejects any file without frontmatter
  ("missing --contract because the document has no YAML frontmatter"), so the
  CLI cannot enforce them today. Declaring `status: enforced` on a file nothing
  checks would be a claim-integrity defect of exactly the kind this project
  keeps finding in its sources, so this script validates them against the same
  compiled JSON Schema the CLI would use.

That makes the enforcement real for both profiles with no network access, which
is what `packing-validate` needs. Run the CLI separately for an independent check of the
Markdown artifacts.
"""

from __future__ import annotations

import functools
import pathlib
import re
import sys

import yaml
from jsonschema_rs import Draft202012Validator

from devtools.check_basic_bounds import check_case_basic_bounds
from sqpack.assurance import check_case_semantics, check_evidence_semantics
from sqpack.yamlio import load_yaml, safe_load

FRONTIER = pathlib.Path(__file__).resolve().parent.parent / "frontier"
# The repository root. recorded_in paths, and the documents that cite defect ids, are
# repository-relative because the reader-facing tree now sits above packing/.
REPO = FRONTIER.parent.parent
WITNESSES = FRONTIER.parent / "witnesses"
RESOURCE_USAGE = FRONTIER.parent / "campaign" / "resource-usage"
DOCUMENT_MAP = FRONTIER.parent.parent / "docs" / "project" / "document-map.yaml"
COMPOSITE_FIGURE = FRONTIER.parent / "atlas" / "known-best" / "composite-figure.json"
TRANSLATION_ESCAPE_SCREEN = (
    FRONTIER.parent / "atlas" / "known-best" / "translation-escape-screen.json"
)
KNOWN_BEST_MANIFEST = FRONTIER.parent / "atlas" / "known-best" / "manifest.json"
CHUNK_PARTITION_ATLAS = FRONTIER.parent / "atlas" / "known-best" / "chunk-partitions.json"
CONTACT_ASSEMBLY_GRAMMAR = (
    FRONTIER.parent / "atlas" / "known-best" / "contact-assembly-grammar.yaml"
)
CONTACT_ENUMERATION_PRICING = (
    FRONTIER.parent / "atlas" / "known-best" / "contact-enumeration-pricing.json"
)
CONTACT_FULL_CELL_CONTROL = (
    FRONTIER.parent / "atlas" / "known-best" / "contact-full-cell-control.json"
)
CONTACT_OVERLAY_GALLERY = FRONTIER.parent / "atlas" / "known-best" / "contact-overlays.json"
CHUNK_EVIDENCE_PROFILE = (
    FRONTIER.parent / "atlas" / "known-best" / "chunk-evidence-profile.json"
)
PROSPECTIVE_SOURCE_AVAILABILITY = (
    FRONTIER.parent / "atlas" / "prospective" / "source-availability-101-324.json"
)
PROSPECTIVE_ATLAS_SEED = FRONTIER.parent / "atlas" / "prospective" / "manifest.json"
CONTACT_SCAFFOLD_ATLAS = (
    FRONTIER.parent / "atlas" / "enumerated" / "contact-scaffolds-size5.json"
)
CONTACT_STRUCTURES = FRONTIER.parent / "atlas" / "known-best" / "contact-structures.json"


def load_schema(name: str) -> dict:
    return load_yaml((FRONTIER / name).read_text(encoding="utf-8"))


def payload_and_meta(path: pathlib.Path) -> tuple[dict, dict]:
    """Return (payload, softschema metadata) for either profile."""
    text = path.read_text(encoding="utf-8")
    doc = load_yaml(text.split("---\n")[1]) if path.suffix == ".md" else load_yaml(text)
    meta = doc.get("softschema")
    if meta is None:
        raise ValueError("no softschema metadata block")
    env = meta.get("envelope")
    if env:
        return doc[env], meta
    # pure-yaml with no envelope: the whole root minus the metadata block
    return {k: v for k, v in doc.items() if k != "softschema"}, meta


@functools.cache
def _validator(schema_path: pathlib.Path) -> Draft202012Validator:
    """One compiled validator per schema, not per document.

    329 artifacts declare 23 distinct schemas, so building a validator at each call site
    re-read and re-compiled every schema fourteen times over (D-370).

    The validator is `jsonschema_rs`, not `jsonschema`: same drafts, same schemas, and
    two orders of magnitude faster over this corpus -- 7.1-7.8s against 55-88ms across
    339 artifacts, a ratio between 83x and 137x depending on container load, reproducible
    through `benchmarks/bench_schema_validation.py` (D-370).
    `tests/test_schema_validator_equivalence.py` is what makes that swap checkable rather
    than trusted -- it fails if the two disagree on any artifact or on any generated
    mutation of one.

    The two are equivalent in *verdict and location*, which is what this project reads.
    They are not equivalent in message text: `jsonschema` quotes with `'` and
    `jsonschema_rs` with `"`, so `'a' is a required property` becomes
    `"a" is a required property`. Nothing here parses that text, and the equivalence
    test normalises quoting rather than pretending the strings match.
    """
    return Draft202012Validator(load_yaml(schema_path.read_text(encoding="utf-8")))


def check(path: pathlib.Path) -> list[str]:
    errs: list[str] = []
    try:
        payload, meta = payload_and_meta(path)
    except (ValueError, yaml.YAMLError) as error:
        return [f"invalid or ambiguous YAML: {error}"]
    errs.extend(
        f"softschema.{key} missing"
        for key in ("contract", "schema", "status")
        if not meta.get(key)
    )
    if errs:
        return errs
    if meta["status"] != "enforced":
        errs.append(f"status is {meta['status']!r}, expected 'enforced'")
    # A soft-schema document's `schema` is relative to the document, so resolve it
    # that way rather than against one fixed directory -- otherwise no artifact can
    # live outside frontier/, which the defect log does.
    schema_path = (path.parent / meta["schema"]).resolve()
    if not schema_path.exists():
        return [*errs, f"declared schema not found: {meta['schema']}"]
    v = _validator(schema_path)
    for e in sorted(v.iter_errors(payload), key=lambda e: list(e.instance_path)):
        loc = "/".join(str(x) for x in e.instance_path) or "<root>"
        errs.append(f"{loc}: {e.message}")
    return errs


def cross_checks() -> list[str]:
    """Invariants a JSON Schema cannot express."""
    errs = []
    for kind in ("search", "proof"):
        d = safe_load((FRONTIER / f"{kind}-strategies.yaml").read_text(encoding="utf-8"))
        ss = d["strategies"]
        if d["count"] != len(ss):
            errs.append(f"{kind}-strategies: count {d['count']} != {len(ss)} entries")
        if [s["id"] for s in ss] != list(range(1, len(ss) + 1)):
            errs.append(f"{kind}-strategies: ids are not 1..{len(ss)}")
        # `outcome` is the machine-readable verdict; `note` is the prose the tables
        # actually render. Nothing compared them, so a strategy could be tagged
        # `produced_records` while its rendered cell says "No" -- the same silent
        # disagreement between a value and its display twin as defect D-022.
        # The two catalogues name this field differently: search records an `outcome`,
        # proof a `status`. Only the search side has a yes/no prose twin to compare.
        if kind == "search":
            for entry in ss:
                says_yes = entry["note"].lstrip().lower().startswith("yes")
                if says_yes != (entry["outcome"] == "produced_records"):
                    errs.append(
                        f"{kind}-strategies: entry {entry['id']} has outcome "
                        f"{entry['outcome']!r} but its note reads {entry['note'][:30]!r}"
                    )
        unknown = {s["family"] for s in ss} - set(d["families"])
        if unknown:
            errs.append(f"{kind}-strategies: families not declared: {sorted(unknown)}")
    a = safe_load((FRONTIER / "asymptotic-waste-bounds.yaml").read_text(encoding="utf-8"))
    errs.extend(
        f"asymptotic: reconstructed bound {b['source_key']} carries no note"
        for b in a["lower_bounds"]
        if b["confidence"] == "reconstructed" and not b.get("note")
    )
    evidence_document = safe_load((FRONTIER / "evidence.yaml").read_text(encoding="utf-8"))
    evidence_records = evidence_document["evidence"]
    evidence_ids = [record["id"] for record in evidence_records]
    duplicate_evidence = {item for item in evidence_ids if evidence_ids.count(item) > 1}
    if duplicate_evidence:
        errs.append(f"evidence: duplicate ids: {sorted(duplicate_evidence)}")
    evidence_by_id = {record["id"]: record for record in evidence_records}
    for record in evidence_records:
        errs.extend(check_evidence_semantics(record))

    case_numbers: list[int] = []
    for case in sorted(FRONTIER.glob("n-*.md")):
        doc = safe_load(case.read_text(encoding="utf-8").split("---\n")[1])
        packing = doc["packing"]
        case_numbers.append(packing["n"])
        errs.extend(
            f"{case.name}: {error}" for error in check_case_semantics(packing, evidence_by_id)
        )
        errs.extend(f"{case.name}: {error}" for error in check_case_basic_bounds(packing))
    if case_numbers != list(range(1, 101)):
        errs.append("frontier cases are not exactly n=1..100 in filename order")

    sa = safe_load((FRONTIER / "source-availability.yaml").read_text(encoding="utf-8"))
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
    d = safe_load(path.read_text(encoding="utf-8"))
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
        # A fixed label cannot coexist with an explicit statement that no fix exists.
        # D-145 arose when a broad edit changed D-039's status but not its evidence.
        fix = str(x.get("fix", "")).lstrip().lower()
        if x["status"] == "fixed" and fix.startswith("none yet"):
            errs.append(f"{x['id']}: fixed while fix still says none yet")
        # The two classes where the direction of the error decides how bad it is.
        if x["class"] in ("soundness", "validity") and not x.get("direction"):
            errs.append(f"{x['id']}: {x['class']} without a direction")
        if x.get("recurrence_of") and x["recurrence_of"] not in known:
            errs.append(f"{x['id']}: recurrence_of unknown {x['recurrence_of']}")
        target = REPO / x["recorded_in"]
        if not target.exists():
            errs.append(f"{x['id']}: recorded_in does not exist: {x['recorded_in']}")

    # Every defect id cited anywhere in the directory must exist in the log. D-024 was
    # cited in a schema comment and a commit message before its record was ever written,
    # and only the contiguity check noticed -- a reference to a defect nobody can look up
    # is the same dangling pointer the campaign's reserved-id rule exists to prevent.
    root = REPO
    # controls.yaml is a file of deliberate corruptions -- it cites a defect that does
    # not exist precisely to prove the recurrence check fires on one.
    skip = {"defects.yaml", "defects.md", "controls.yaml"}
    for path in sorted(root.rglob("*.yaml")) + sorted(root.rglob("*.md")):
        if path.name in skip or "resources" in path.parts or ".venv" in path.parts:
            continue
        # Dot-directories hold vendored agent skills and tooling caches, not our prose.
        parts = path.relative_to(root).parts
        if any(part.startswith(".") or part == "node_modules" for part in parts):
            continue
        cited = set(re.findall(r"\bD-[0-9]{3}\b", path.read_text(encoding="utf-8")))
        errs.extend(
            f"{path.relative_to(root)}: cites {missing}, not in defects.yaml"
            for missing in sorted(cited - known)
        )
    return errs


def corpus_paths() -> tuple[list[pathlib.Path], list[pathlib.Path]]:
    """Every enforced artifact, as (frontmatter-md, pure-yaml).

    Extracted from `main` so the equivalence test and the benchmark validate the same
    corpus this step does. A second enumeration would drift, and the first thing it
    would stop covering is whatever was added last.
    """
    md = sorted(FRONTIER.glob("n-*.md"))
    datasets = sorted(p for p in FRONTIER.glob("*.yaml") if not p.name.endswith(".schema.yaml"))
    datasets += [FRONTIER.parent / "defects.yaml"]
    datasets += sorted(
        path for path in WITNESSES.rglob("*.yaml") if not path.name.endswith(".schema.yaml")
    )
    datasets.append(DOCUMENT_MAP)
    datasets.append(KNOWN_BEST_MANIFEST)
    datasets.append(COMPOSITE_FIGURE)
    datasets.append(TRANSLATION_ESCAPE_SCREEN)
    datasets.append(CHUNK_PARTITION_ATLAS)
    datasets.append(CONTACT_ASSEMBLY_GRAMMAR)
    datasets.append(CONTACT_ENUMERATION_PRICING)
    datasets.append(CONTACT_FULL_CELL_CONTROL)
    datasets.append(CONTACT_OVERLAY_GALLERY)
    datasets.append(CHUNK_EVIDENCE_PROFILE)
    datasets.append(PROSPECTIVE_SOURCE_AVAILABILITY)
    datasets.append(PROSPECTIVE_ATLAS_SEED)
    datasets.append(CONTACT_SCAFFOLD_ATLAS)
    datasets.append(CONTACT_STRUCTURES)
    # One record per harness session log. The logs themselves are not retained, so
    # these are the durable artifact rather than a pointer to one and are enforced like
    # any other dataset.
    datasets += sorted(RESOURCE_USAGE.glob("*.yaml"))
    return md, datasets


def main() -> int:
    md, datasets = corpus_paths()
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
    print(
        f"  {len(md)} frontmatter-md artifacts + {len(datasets)} pure-yaml datasets "
        f"validate against their declared schemas"
    )
    declared = {
        safe_load(d.read_text(encoding="utf-8"))["softschema"]["schema"] for d in datasets
    }
    print(f"  schemas in use: {sorted(declared | {'square-packing-case.schema.yaml'})}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
