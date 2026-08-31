#!/usr/bin/env python3
"""Grant or refuse the results register's declared rungs from recorded atoms.

`epistemics.md` at the repository root owns the vocabulary this enforces: every
`T-NNN` record in `frontier/results.yaml` declares a verification rung (V) and a
confirmation rung (C), and this checker re-derives both from the evidence
entries the record cites, failing the build when a declared rung is unsupported
-- or understated, since sandbagging distorts the record as surely as
inflation, unless a `composition` note claims the minimum over load-bearing
parts (the one legitimate reason a declared rung sits below what the strongest
cited atom supports).

The derivation, from `frontier/evidence.yaml`'s fields:

- an entry is *machine-proof shaped* (the C3 predicate, and V4's) when its
  method is exact-algebraic or interval-certified, it retains a certificate,
  and its replay is recorded and passing;
- it counts toward C only when this repository performed it
  (`origin: audited-here` or `replayed-here`);
- C4 needs at least two C3-shaped entries of ours with distinct methods;
- C2 is any passing replay of ours; C1 is a dated external review read
  (`informally-verified` or `defect-found`);
- V5 is a proof-assistant method, V4 any machine-proof-shaped entry by anyone,
  V3 a published proof carrying a `proof` block, V1 a numerical method with
  recorded precision; V0 and V2 are declared-not-derived and require a `notes`
  field saying why.

Beyond the rungs: ids are contiguous `T-001..`, evidence references resolve,
artifact and control paths exist, a C3-or-better rung names its adversarial
controls, a declared C5 names its review artifact, and every `T-NNN` mentioned
in the reader tier (`README.md`, `SYNOPSIS.md`) exists in the register.
The generated view is checked by `devtools.render_results --check`, registered
alongside this checker in the validation gate.

Usage, from `packing/`:
    uv run --frozen --all-extras --group dev python -m devtools.check_results
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

from sqpack.yamlio import safe_load

ROOT = Path(__file__).resolve().parent.parent
REPO = ROOT.parent
RESULTS = ROOT / "frontier" / "results.yaml"
EVIDENCE = ROOT / "frontier" / "evidence.yaml"
READER_TIER = (REPO / "README.md", REPO / "SYNOPSIS.md")

MACHINE_METHODS = {"exact-algebraic", "interval-certified"}
OURS_ORIGINS = {"audited-here", "replayed-here"}
DERIVED_NOT_DECLARED_V = {"V0", "V2"}


def _rank(rung: str) -> int:
    return int(rung[1])


def _machine_proof_shaped(entry: dict) -> bool:
    return (
        entry.get("method") in MACHINE_METHODS
        and bool(entry.get("certificate"))
        and bool(entry.get("replay"))
        and entry.get("replay_status") == "passed"
    )


def derive_confirmation(entries: list[dict]) -> str:
    ours = [entry for entry in entries if entry.get("origin") in OURS_ORIGINS]
    machine = [entry for entry in ours if _machine_proof_shaped(entry)]
    if len({entry.get("method") for entry in machine}) >= 2:
        return "C4"
    if machine:
        return "C3"
    if any(entry.get("replay_status") == "passed" for entry in ours):
        return "C2"
    if any(
        (entry.get("external_review") or {}).get("state")
        in {"informally-verified", "defect-found"}
        for entry in entries
    ):
        return "C1"
    return "C0"


def derive_verification(entries: list[dict]) -> str:
    if any(entry.get("method") == "proof-assistant-checked" for entry in entries):
        return "V5"
    if any(_machine_proof_shaped(entry) for entry in entries):
        return "V4"
    if any(
        entry.get("method") == "published-proof" and entry.get("proof") for entry in entries
    ):
        return "V3"
    if any(
        str(entry.get("method", "")).startswith("numerical") and entry.get("precision")
        for entry in entries
    ):
        return "V1"
    return "V0"


def main() -> int:
    problems: list[str] = []
    register = safe_load(RESULTS.read_text(encoding="utf-8"))
    evidence_index = {
        entry["id"]: entry
        for entry in safe_load(EVIDENCE.read_text(encoding="utf-8"))["evidence"]
    }
    results = register["results"]

    expected_ids = [f"T-{index:03d}" for index in range(1, len(results) + 1)]
    actual_ids = [record["id"] for record in results]
    if actual_ids != expected_ids:
        problems.append(f"register ids are not contiguous T-001..: {actual_ids}")

    for record in results:
        rid = record["id"]
        cited: list[dict] = []
        for ref in record["evidence"]:
            entry = evidence_index.get(ref)
            if entry is None:
                problems.append(f"{rid}: cites unknown evidence {ref}")
                continue
            cited.append(entry)

        for field in ("artifacts", "controls"):
            problems.extend(
                f"{rid}: {field} path does not exist: {path}"
                for path in record.get(field) or []
                if not (REPO / path).exists()
            )

        declared_c = record["confirmation"]
        derived_c = derive_confirmation(cited)
        has_composition = bool(record.get("composition"))
        if _rank(declared_c) > _rank(derived_c):
            problems.append(
                f"{rid}: declares {declared_c} but the cited atoms support only {derived_c}"
            )
        elif _rank(declared_c) < _rank(derived_c) and not has_composition:
            problems.append(
                f"{rid}: understates {derived_c} as {declared_c} with no "
                "composition note claiming the minimum over parts"
            )

        declared_v = record["verification"]
        if declared_v in DERIVED_NOT_DECLARED_V:
            if not record.get("notes"):
                problems.append(
                    f"{rid}: {declared_v} is declared-not-derived and needs a "
                    "notes field saying why"
                )
        else:
            derived_v = derive_verification(cited)
            if _rank(declared_v) > _rank(derived_v):
                problems.append(
                    f"{rid}: declares {declared_v} but the cited atoms support only {derived_v}"
                )
            elif _rank(declared_v) < _rank(derived_v) and not has_composition:
                problems.append(
                    f"{rid}: understates {derived_v} as {declared_v} with no "
                    "composition note claiming the minimum over parts"
                )

        if _rank(declared_c) >= 3 and not record.get("controls"):
            problems.append(f"{rid}: a {declared_c} rung names its adversarial controls")
        if declared_c == "C5":
            review = record.get("review_artifact")
            if not review:
                problems.append(f"{rid}: C5 requires review_artifact")
            elif not (REPO / review).exists():
                problems.append(f"{rid}: review_artifact does not exist: {review}")

    known = set(actual_ids)
    for path in READER_TIER:
        text = path.read_text(encoding="utf-8")
        problems.extend(
            f"{path.name}: mentions unknown result {mention}"
            for mention in sorted(set(re.findall(r"\bT-\d{3}\b", text)))
            if mention not in known
        )

    if problems:
        print(f"{len(problems)} results-register problems:")
        for line in problems:
            print(f"  {line}")
        return 1

    print(
        f"{len(results)} registered results: every declared rung is supported "
        "by its cited atoms, every path resolves, every reader-tier mention "
        "exists"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
