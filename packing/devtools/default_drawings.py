#!/usr/bin/env python3
"""Each count's default picture: its regularized view where the view improves on the
house drawing, else the house drawing, recorded and held to the data; and every count's
regularization state, gated.

Usage, from `packing/`, after
`uv run --frozen --all-extras --group dev python -m devtools.default_drawings`:

    --update [--workers K]
    --check [--workers K]
    --check-state

The owner decided on 13 October 2026 that the regularized drawing is the default picture,
with the house drawing kept as "as published", and that a regularization should be a
strict improvement (`docs/project/policies/regularization-policy.md`, section 12). For
every count the layer's index (`atlas/known-best/regularized/index.json`) draws, the
default picture is the view when all three hold:

1. **Exact.** Both maintained exact routes accept it, as its entry records.
2. **Side.** Its exact side is at most `U`, the case record's verified upper bound as
   `regularize_evand.verified_bound` holds it exactly, or the count is one of
   `ABOVE_U`, the views the policy's section 9, question 13 names above it.
3. **Improvement.** It improves on the house drawing under the policy's improvement rule
   (section 11), which `devtools.improvement_rule` reads from the policy and decides. Both
   drawings are measured as `devtools.regularize_select.today` measures a tree's drawing
   -- the house renderer's colouring by `census_drawing_regularity.regularity`, the house
   and stage totals by `regularize_evand.contact_partners` -- the two sides are compared
   exactly where the house witness is exact, and exactness is the view's gain where the
   house witness is only numerically checked.

Every other count is drawn from its house witness, including a view that ties its house
drawing on every goal: there the picture is the same, and the house is the record's.

`--update` writes `atlas/known-best/default-drawings.json`: one entry a drawn view, with
its default, the reason, both drawings' measures and the goals the view is better and
worse on. `--check` measures every view again and fails when the record is not what the
data gives, when a regularized default breaks the rule, or when the policy's goals or
their directions differ from the ones the code judges (`improvement_rule.problems`). It
lists, failing nothing, each count that keeps the house picture and why: "no gain",
"above U, not in the exceptions", a goal it is worse on, or an exact route's refusal.
It costs about 35 cpu-seconds: the views and their house drawings (about 20 for the 90
views of 13 October 2026) and the other 232 house drawings (14 on a loaded host,
15 October 2026), a few seconds of wall at four workers.

**The regularization state.** The owner, 15 October 2026: "The records should make it
evident which things are regularized, and if not, we should fix the record-keeping
process as well." n = 176 drew its raw house on the site for a day while the layer's
index said `regularized`, because adopting a new house lapsed the grid-slack view
`regularize_axis_components --update-atlas` had kept, and no record said so (think-gvke).
So the record's `states` gives every count n = 1..324 what is drawn, the drawn picture's
measures, the witness's SHA-256, the runs that decided that witness, and one state:

- `regularized`: a view of Evan Daniel's regularizer or the grid-slack generator is drawn
  (`STRONG_GENERATORS`);
- `regular-as-published`: the house drawing has no uneven and no near-axis square;
- `decided-no-better`: the strong generators ran on this very witness and drew nothing
  the improvement rule takes (`SETTLED`, by witness digest);
- `exempt`: the count is set aside with a reason and the bead that owns it (`SETTLED`);
- `pending`: none of these, as at a count whose strong view lapsed with its witness
  (the index's `lapsed`, which `--update-atlas` writes) or that only the axis tool's
  view, the reference and fallback, has drawn.

`--check-state` is the gate, reading digests and the record, measuring nothing: it fails
on a pending count `PENDING_ALLOWED` does not name, on a named count that is no longer
pending, on a record older than a witness, and on a `SETTLED` entry made on another
witness than the one the atlas holds or for a count that no longer needs it.


The site's drawings (`render_frontier_page`), the atlas tiles (`overview_sections`) and
the posters (`build_known_best_atlas`) read the record through `regularized_defaults`,
which refuses a record whose counts, views or generators are not the index's. Reading
it measures nothing: the measuring code is imported only to measure, so its readers stay
light.
"""

from __future__ import annotations

import argparse
import gzip
import json
import re
from collections.abc import Mapping, Sequence
from concurrent.futures import ProcessPoolExecutor
from fractions import Fraction
from functools import cache
from pathlib import Path
from typing import Any, NamedTuple

from strif import atomic_output_file

from devtools import improvement_rule
from devtools.improvement_rule import MEASURES
from devtools.regularize_axis_components import ABOVE_U, ALGORITHM, LAPSED, digest
from sqpack import retained_json
from sqpack.workers import worker_count
from sqpack.yamlio import load_yaml

ROOT = Path(__file__).resolve().parent.parent
REPO = ROOT.parent
INDEX = ROOT / "atlas/known-best/regularized/index.json"
RECORD = ROOT / "atlas/known-best/default-drawings.json"
RECORD_PATH = "packing/atlas/known-best/default-drawings.json"
CONTRACT = "packing.squares:DefaultDrawings/v2"
SCHEMA = "default-drawings.schema.yaml"
GENERATOR = "python -m devtools.default_drawings"
REGULARIZED = "regularized"
HOUSE = "house"
VIEW = "view"
#: How a refused count's reason reads, beside the improvement rule's own words.
ROUTE_REFUSED = "an exact route refused it"
UNKNOWN_U = "U is unknown"
ABOVE_BOUND = "above U, not in the exceptions"

#: The regularization states a count's drawing is in (the module's docstring).
REGULARIZED_STATE = "regularized"
REGULAR_AS_PUBLISHED = "regular-as-published"
DECIDED = "decided-no-better"
EXEMPT = "exempt"
PENDING = "pending"
STATES = (REGULARIZED_STATE, REGULAR_AS_PUBLISHED, DECIDED, EXEMPT, PENDING)
#: The generators whose drawn view makes a count `regularized`: Evan Daniel's regularizer
#: and the grid-slack port of his placement. The axis tool is the reference and fallback
#: (policy section 4); a drawing it alone made waits for these to decide its witness.
STRONG_GENERATORS = frozenset(
    {"evand-regularize", "regularize_grid_slack/0", "regularize_grid_slack/1"}
)
#: A bead id, which every `PENDING_ALLOWED` and `EXEMPT` entry names.
BEAD = re.compile(r"\bthink-[0-9a-z]{4}\b")


class Settled(NamedTuple):
    """A count the strong generators decided, or that is set aside, on one witness: its
    state (`DECIDED` or `EXEMPT`), that witness's SHA-256 as the index records it, the
    runs that decided it as (generator, run id), what they found, and where the record
    says so."""

    state: str
    witness_sha256: str
    runs: tuple[tuple[str, str], ...]
    outcome: str
    evidence: str


#: Both generators ran on the 42 witnesses jlevy/squares#518 adopted, on 12 October 2026.
_ADOPT518 = (
    ("evand-regularize", "evand-regularize-refreshed-adopt518-v2"),
    ("regularize_grid_slack/1", "grid-slack-on518"),
)
_README = "packing/atlas/known-best/README.md, the #518 paragraph"
_T146 = (
    "the house is Evan Daniel's own regularized list (T-146); neither generator drew "
    "better on it, and the axis tool's view does not improve on it"
)
_REFUSED_DECIMAL = (
    "a decimal Kingbird witness: the axis tool refuses it (its 36-digit rational pose "
    "overlaps at dilation 1), and no strong generator's outcome on it is recorded"
)

#: The counts whose drawing is not regularized and not regular as published, settled on
#: purpose: each named with the witness it was settled on, so a new witness makes the
#: count `pending` again. Written from the evidence the audit of 15 October 2026 found
#: (think-y1x3); the run receipts keep only aggregates, so `evidence` says where each
#: outcome is written down. The gate fails on an entry whose witness has changed or whose
#: count no longer needs it.
SETTLED: dict[int, Settled] = {
    39: Settled(
        EXEMPT,
        "4fa32e151c5b62af204cdd5d71f27259a4647cbf3447253af4ec79bdebdb1d94",
        (),
        _REFUSED_DECIMAL,
        "think-yk2h",
    ),
    55: Settled(
        EXEMPT,
        "4c395877784a7052f7e2eb2f039479731fc3cbfe4d94ea41b78dae270abb99ad",
        (),
        _REFUSED_DECIMAL,
        "think-yk2h",
    ),
    102: Settled(
        DECIDED,
        "a252f05aeef27f6e64cf3ff7272f17086cd89a0f2f2cc816276ca7de663e4902",
        _ADOPT518,
        _T146,
        _README,
    ),
    110: Settled(
        DECIDED,
        "2e6de0a4993519cd61f83b00ea1e45780625d31b39d5ef5fbe70bb4de6810210",
        (("evand-regularize", "evand-regularize-bound-1013"),),
        "Evan Daniel's exact view at U draws fewer shared sides (house 243 to 239), and "
        "the owner keeps the axis tool's view at the witness's side",
        "ABOVE_U; think-jnso",
    ),
    123: Settled(
        DECIDED,
        "93ea5694fddfeda898ce8183e9bcd197800126723beeffadcacac414930cd38d",
        _ADOPT518,
        "neither generator drew better than the axis tool's view",
        _README,
    ),
    155: Settled(
        DECIDED,
        "0663cee29900c268ce0bd0cfd6525a8c0e71581be836d8cf5f3f13b68a5c72af",
        _ADOPT518,
        "neither generator drew better than the axis tool's view",
        _README,
    ),
    179: Settled(
        DECIDED,
        "a7778adde5e8c169729e8bfc1cf59632669d9303e57196dc230d680af6e8da93",
        (("evand-regularize", "evand-regularize-full"),),
        "refused at row 7: a house or stage total of shared sides falls",
        "docs/project/research/research-2026-10-11-regularization-state-and-approach.md",
    ),
    180: Settled(
        DECIDED,
        "d453d21e11f0b2b1a035635df2a7c808ba3063b779234508820614677e1f89cf",
        (*_ADOPT518, ("evand-regularize", "evand-regularize-adopt518-v2-rerun-2026-10-13")),
        "Evan Daniel's view tied the axis tool's on all seven measures at the same side "
        "and was withdrawn (1d8f982ff)",
        _README,
    ),
    236: Settled(
        DECIDED,
        "77ef40d122d18d2de38b090e45f8e07cd4b8c8f8c825b7171bbe5c6a5532fe8c",
        _ADOPT518,
        "Evan Daniel's view drew one more angle class and was withdrawn (bd82e3a54); the "
        "axis tool's view does not improve on the house",
        _README,
    ),
    258: Settled(
        DECIDED,
        "da8920e0441dc0180b87fc8a78af5ab9c5704745cd0f4085eb150992d9c07669",
        _ADOPT518,
        _T146,
        _README,
    ),
    263: Settled(
        DECIDED,
        "e6e792983e2b1409179e8a1758c9138d0ee9885b8f6691c0d804df22c62e47c8",
        _ADOPT518,
        _T146,
        _README,
    ),
    269: Settled(
        DECIDED,
        "cce03481861340054989675f62d8f5f086392c51c5212b6762cd5961eeca2fc1",
        _ADOPT518,
        _T146,
        _README,
    ),
    290: Settled(
        EXEMPT,
        "f7328bab3dfa6b85db8c2ecdc01765e6a6fca9c7c45115502e5ee8496c2c78b9",
        (),
        _REFUSED_DECIMAL,
        "think-yk2h",
    ),
    291: Settled(
        EXEMPT,
        "7a002b02cb46b615fbef34dc6fcb6bdd6d2bb32298d6958e2955d04d173ed21d",
        (),
        _REFUSED_DECIMAL,
        "think-yk2h",
    ),
}

_LA7H = "think-la7h: re-housed by #614 (60aa1d39e)"
_KPM3 = "think-kpm3: re-housed by #614 (3b9fab84a)"
_3ZI3 = "think-3zi3: re-housed by #598 (8a4d26fea)"

#: The counts allowed to stay `pending`, each naming the bead whose runs will decide it.
#: Measured, not chosen, as `ABOVE_U` is: `--check-state` fails on a pending count not
#: named here and on a named count that is no longer pending, so a count leaves the list
#: as soon as it is decided, and joins it only by a reviewed change naming its bead (the
#: deferral an adoption makes when its runs must wait). Set on 15 October 2026
#: to the twenty counts the audit found drawn without a strong generator's decision on
#: their current witness (think-gvke, think-rz8c).
PENDING_ALLOWED: dict[int, str] = {
    105: f"{_LA7H}; its grid-slack view lapsed",
    129: f"{_LA7H}; its Evan Daniel view lapsed",
    146: f"{_LA7H}; its grid-slack view lapsed",
    153: f"{_KPM3}; its Evan Daniel view lapsed",
    154: "think-kpm3: re-housed by #598 (34e62125f) and #614 (3b9fab84a); never decided",
    156: f"{_LA7H}; its grid-slack view lapsed",
    175: f"{_3ZI3}; its grid-slack view lapsed",
    176: f"{_LA7H}; its grid-slack view lapsed, and the raw house is drawn",
    204: f"{_LA7H}; never decided",
    207: f"{_KPM3}; never decided",
    211: f"{_KPM3}; its grid-slack view lapsed",
    232: f"{_3ZI3}; never decided",
    237: f"{_KPM3}; its Evan Daniel view lapsed",
    241: f"{_KPM3}; its grid-slack view lapsed",
    264: f"{_3ZI3}; never decided",
    271: f"{_LA7H}; its grid-slack view lapsed",
    272: f"{_LA7H}; its Evan Daniel view lapsed earlier, in #553 (3e24adeb2)",
    302: f"{_KPM3}; its Evan Daniel view lapsed",
    303: f"{_LA7H}; never decided",
    304: f"{_KPM3}; its Evan Daniel view lapsed earlier, in #553 (3e24adeb2)",
}


def index_entries(index: Path = INDEX) -> dict[int, dict[str, Any]]:
    """Every entry of the layer's index, by count."""
    document = json.loads(index.read_text(encoding="utf-8"))
    return {int(entry["n"]): entry for entry in document["entries"]}


def drawn_views(index: Path = INDEX) -> dict[int, dict[str, Any]]:
    """The layer's entries that draw a view, by count."""
    return {
        n: entry for n, entry in index_entries(index).items() if entry["status"] == REGULARIZED
    }


def _view_witness(entry: Mapping[str, Any]) -> dict[str, Any]:
    text = gzip.decompress((REPO / entry["view"]["path"]).read_bytes()).decode("utf-8")
    return load_yaml(text)["witness"]


def drawn_above_bound(index: Path = INDEX) -> dict[int, float]:
    """Every drawn view whose exact side lies above `U`, by how far: each view's side read
    from its view file, exactly as both routes decide it, and held to `U` as the
    selection reads it."""
    from devtools import regularize_evand as drive  # noqa: PLC0415

    above: dict[int, float] = {}
    for n, entry in drawn_views(index).items():
        side, _placements, _corners = drive.view_geometry(_view_witness(entry))
        upper = drive.verified_bound(drive.case_facts(n))
        if upper is None:
            raise ValueError(f"n={n}: U is unknown")
        order = upper.compare(side)
        if order is None:
            raise ValueError(f"n={n}: U is not read exactly: {upper.unread}")
        if order > 0:
            above[n] = upper.difference(side)
    return above


def _routes(entry: Mapping[str, Any]) -> bool:
    """Whether both maintained exact routes accepted the view, as its entry records."""
    verdict = entry.get("exact_verification") or {}
    return bool(
        verdict.get("repository_verifier")
        and verdict.get("independent_checker")
        and verdict.get("passed")
    )


def _against(view: Fraction, house: Fraction | None) -> str | None:
    if house is None:
        return None
    return "smaller" if view < house else "larger" if view > house else "same"


def decide(unit: tuple[Path, int, Mapping[int, Mapping[str, Any]]]) -> dict[str, Any]:
    """One count's view against its house drawing, and the picture the rule draws."""
    from devtools import regularize_evand as drive  # noqa: PLC0415
    from devtools import regularize_select as select  # noqa: PLC0415

    tree, n, entries = unit
    entry = entries[n]
    view = select.today((tree, n, entries))
    house = select.today((tree, n, {}))
    if view["drawing"]["kind"] != "regularized-view" or house["drawing"]["kind"] != "witness":
        raise ValueError(f"n={n}: the view and the house drawing were not both measured")
    side = Fraction(str(view["side"]))
    house_side = None if house["side"] is None else Fraction(str(house["side"]))
    upper = drive.verified_bound(drive.case_facts(n))
    order = None if upper is None else upper.compare(side)
    gains, worse = improvement_rule.compare(view, house)
    against = _against(side, house_side)
    judgement = improvement_rule.judge(
        gains,
        worse,
        smaller=against == "smaller",
        larger=against == "larger",
        # Exactness is the gain of an exactly verified view over a numerically checked
        # witness, so a view an exact route refused gains none (review B2 of #591).
        exact_gain=not house["verified"] and _routes(entry),
    )
    if not _routes(entry):
        default, reason = HOUSE, ROUTE_REFUSED
    elif order is None:
        default, reason = HOUSE, UNKNOWN_U
    elif order > 0 and n not in ABOVE_U:
        default, reason = HOUSE, ABOVE_BOUND
    elif not judgement.improves:
        default, reason = HOUSE, judgement.reason
    else:
        default, reason = REGULARIZED, f"better on {', '.join(judgement.better)}"
    return {
        "n": n,
        "default": default,
        "reason": reason,
        "generator": entry.get("generator"),
        "view": entry["view"]["path"],
        "exact_routes": _routes(entry),
        "side": {
            "view_minus_U": None
            if upper is None or order is None
            else f"{upper.difference(side):.3e}",
            "named_above_U": n in ABOVE_U,
            "against_house": against,
        },
        "house_exact": bool(house["verified"]),
        "better": list(judgement.better),
        "worse": list(judgement.worse),
        "measures": {key: {"view": view[key], "house": house[key]} for key in MEASURES},
    }


def measure_house(unit: tuple[Path, int, Mapping[int, Mapping[str, Any]]]) -> dict[str, Any]:
    """One count's house drawing, measured as `decide` measures it, where the layer draws
    no view: the measures its regularization state is read from."""
    from devtools import regularize_select as select  # noqa: PLC0415

    tree, n, _entries = unit
    house = select.today((tree, n, {}))
    if house["drawing"]["kind"] != "witness":
        raise ValueError(f"n={n}: the house drawing was not measured")
    return {"n": n, "measures": {key: house[key] for key in MEASURES}}


def _measure(unit: tuple[Path, int, Mapping[int, Mapping[str, Any]]]) -> dict[str, Any]:
    _tree, n, entries = unit
    return decide(unit) if n in entries else measure_house(unit)


def _axis_record(entry: Mapping[str, Any]) -> Mapping[str, Any]:
    """The axis tool's own record of a count: the entry, or its `reference` where another
    generator's view is the entry."""
    return entry.get("reference") or entry


def _axis_outcome(record: Mapping[str, Any]) -> str:
    status = str(record["status"])
    if status == "refused":
        return f"refused: {record['refusal']['kind']}"
    return {"regularized": "view", "unchanged": "no change"}.get(status, status)


def run_decisions(
    entry: Mapping[str, Any], witness_sha256: str, settled: Settled | None
) -> list[dict[str, Any]]:
    """The tool runs that decided a count's witness, and what each found: the axis tool's
    record, the strong generator whose view the layer holds, and a `SETTLED` entry's runs
    where it was made on the witness the atlas holds now."""
    axis = _axis_record(entry)
    found: list[dict[str, Any]] = [
        {
            "generator": ALGORITHM,
            "run": None,
            "witness_sha256": axis["source"]["sha256"],
            "outcome": _axis_outcome(axis),
        }
    ]
    if entry.get("generator") != ALGORITHM:
        found.append(
            {
                "generator": entry["generator"],
                "run": str(entry["run"]["id"]),
                "witness_sha256": entry["source"]["sha256"],
                "outcome": "view",
            }
        )
    if settled is not None and settled.witness_sha256 == witness_sha256:
        found.extend(
            {
                "generator": generator,
                "run": run,
                "witness_sha256": settled.witness_sha256,
                "outcome": settled.outcome,
            }
            for generator, run in settled.runs
        )
    return found


def count_state(
    n: int,
    entry: Mapping[str, Any],
    decided: Mapping[str, Any],
    witness_sha256: str,
    *,
    settled: Mapping[int, Settled] | None = None,
    allowed: Mapping[int, str] | None = None,
) -> dict[str, Any]:
    """One count's regularization state, from its index entry, what `decide` or
    `measure_house` measured (`decided`), and its witness's digest now (the module's
    docstring)."""
    settled = SETTLED if settled is None else settled
    allowed = PENDING_ALLOWED if allowed is None else allowed
    viewed = decided.get("default") == REGULARIZED
    measures = decided["measures"]
    house = (
        {key: value[HOUSE] for key, value in measures.items()}
        if "default" in decided
        else dict(measures)
    )
    drawn = {key: value[VIEW] for key, value in measures.items()} if viewed else house
    generator = str(entry["generator"]) if viewed else None
    held = settled.get(n)
    current = held if held is not None and held.witness_sha256 == witness_sha256 else None
    lapse = entry.get(LAPSED) if entry.get("generator") == ALGORITHM else None
    strong_here = (
        entry.get("generator") in STRONG_GENERATORS
        and entry["source"]["sha256"] == witness_sha256
    )
    if generator in STRONG_GENERATORS:
        state = REGULARIZED_STATE
        why = f"the {generator} view of this witness is drawn (run {entry['run']['id']})"
    elif house["uneven_axis"] == 0 and house["near_axis"] == 0:
        state = REGULAR_AS_PUBLISHED
        why = "the house drawing has no uneven and no near-axis square"
    elif strong_here:
        # The layer holds a strong generator's view of this witness, and the improvement
        # rule does not draw it: that generator decided the witness, and drew no better.
        state = DECIDED
        why = (
            f"the {entry['generator']} view of this witness (run {entry['run']['id']}) is "
            f"not drawn: {decided['reason']}"
        )
    elif current is not None:
        state = current.state
        why = f"{current.outcome} ({current.evidence})"
    else:
        state = PENDING
        what = f"the {generator} view" if viewed else "the house drawing"
        why = f"no strong generator has decided this witness; {what} is drawn"
        if lapse:
            why += (
                f"; the {lapse['generator']} view of witness {lapse['witness_sha256'][:12]} "
                f"lapsed (run {lapse['run']})"
            )
        if n in allowed:
            why += f"; allowed pending: {allowed[n]}"
    return {
        "n": n,
        "state": state,
        "drawn": VIEW if viewed else HOUSE,
        "generator": generator,
        "witness_sha256": witness_sha256,
        "measures": drawn,
        "decisions": run_decisions(entry, witness_sha256, current),
        "lapsed": lapse,
        "why": why,
    }


def witness_digest(entry: Mapping[str, Any], tree: Path = REPO) -> str:
    """The SHA-256 of the witness file a count's index entry names, as it is now."""
    return digest((tree / entry["source"]["witness"]).read_bytes())


def document(*, workers: int = 1, tree: Path = REPO, index: Path = INDEX) -> dict[str, Any]:
    """The record the data gives: every drawn view's count decided, and every count's
    regularization state."""
    every = index_entries(index)
    entries = {n: entry for n, entry in every.items() if entry["status"] == REGULARIZED}
    units = [(tree, n, entries) for n in sorted(every, reverse=True)]
    if workers > 1 and len(units) > 1:
        with ProcessPoolExecutor(max_workers=workers) as pool:
            measured = list(pool.map(_measure, units))
    else:
        measured = [_measure(unit) for unit in units]
    by_n = {int(row["n"]): row for row in measured}
    rows = [by_n[n] for n in sorted(entries)]
    states = [
        count_state(n, every[n], by_n[n], witness_digest(every[n], tree)) for n in sorted(every)
    ]
    drawn = sum(1 for row in rows if row["default"] == REGULARIZED)
    return {
        "softschema": {"contract": CONTRACT, "schema": SCHEMA, "status": "enforced"},
        "contract": CONTRACT,
        "generated_by": f"{GENERATOR} --update",
        "policy_document": improvement_rule.POLICY_DOCUMENT,
        "rule": improvement_rule.SECTION,
        "measured_by": (
            "devtools.regularize_select.today on the view and on the house witness, "
            "judged by devtools.improvement_rule.judge"
        ),
        "measures": list(MEASURES),
        "totals": {
            "views": len(rows),
            REGULARIZED: drawn,
            HOUSE: len(rows) - drawn,
            "states": {
                state: sum(1 for row in states if row["state"] == state) for state in STATES
            },
        },
        "entries": rows,
        "states": states,
    }


def text(record: Mapping[str, Any]) -> str:
    return retained_json.dumps(record, ensure_ascii=False) + "\n"


@cache
def decisions(record: Path = RECORD, index: Path = INDEX) -> dict[int, dict[str, Any]]:
    """Every drawn view's decision, by count, from the retained record, refused where the
    record's counts, views or generators are not the index's: a stale record is refused
    rather than drawn from. Nothing is measured here; the records tier's check measures."""
    stale = f"{RECORD_PATH} is stale; run `{GENERATOR} --update`"
    found = json.loads(record.read_text(encoding="utf-8"))
    if found.get("contract") != CONTRACT:
        raise SystemExit(f"{RECORD_PATH} is not a {CONTRACT} record")
    drawn = drawn_views(index)
    rows = {int(row["n"]): row for row in found["entries"]}
    if sorted(rows) != sorted(drawn):
        raise SystemExit(f"{stale}: it decides other counts than the index draws")
    for n, row in rows.items():
        if row["view"] != drawn[n]["view"]["path"] or row["generator"] != drawn[n].get(
            "generator"
        ):
            raise SystemExit(f"{stale}: n={n} names another view than the index")
    return rows


@cache
def regularized_defaults(
    record: Path = RECORD, index: Path = INDEX
) -> dict[int, dict[str, Any]]:
    """The counts whose default picture is their regularized view (`decisions`)."""
    rows = decisions(record, index)
    return {n: row for n, row in rows.items() if row["default"] == REGULARIZED}


def held_reasons(record: Path = RECORD) -> dict[str, str]:
    """By view path, why each view the layer holds is not its count's default picture, in
    the words a case record's note gives it (review A4 of #591): the record's reason, or
    for a tie, that it ties the house drawing on every goal. Read from the retained record
    without measuring, and by the view's path, so a view the record does not name gets no
    reason here (`regularized_drawings.case_note`)."""
    found = json.loads(record.read_text(encoding="utf-8"))
    return {
        str(row["view"]): (
            "it ties the house drawing on every goal of the improvement rule"
            if row["reason"] == "no gain"
            else str(row["reason"])
        )
        for row in found.get("entries") or []
        if row["default"] == HOUSE
    }


@cache
def _generators(index: Path = INDEX) -> dict[str, Any]:
    return dict(json.loads(index.read_text(encoding="utf-8")).get("generators") or {})


def credit_line(n: int) -> str:
    """The credit line a drawing of count `n`'s regularized default carries: the
    generator's, as the policy's section 7 gives it (`regularized_drawings.
    generator_credit`)."""
    from devtools.regularized_drawings import generator_credit  # noqa: PLC0415

    row = regularized_defaults()[n]
    return generator_credit(str(row["generator"]), _generators())


def problems(expected: Mapping[str, Any], record: Path = RECORD) -> tuple[list[str], list[str]]:
    """What fails the check, and what it lists without failing: the counts that keep
    the house picture and why."""
    found = list(improvement_rule.problems())
    by_n = {int(row["n"]): row for row in expected["entries"]}
    if not record.is_file():
        found.append(f"{RECORD_PATH} is missing")
    else:
        retained = json.loads(record.read_text(encoding="utf-8"))
        for row in retained.get("entries", []):
            n = int(row["n"])
            if row.get("default") == REGULARIZED and by_n.get(n, {}).get("default") != (
                REGULARIZED
            ):
                why = by_n[n]["reason"] if n in by_n else "the index draws no view"
                found.append(
                    f"n={n} is drawn regularized by default, and the rule says not: {why}"
                )
        if record.read_text(encoding="utf-8") != text(expected):
            found.append(f"{RECORD_PATH} is not what the data gives")
    kept = [
        f"n={row['n']} keeps the house picture: {row['reason']}"
        for row in expected["entries"]
        if row["default"] == HOUSE
    ]
    return found, kept


def _summary(record: Mapping[str, Any]) -> str:
    totals = record["totals"]
    return (
        f"{totals[REGULARIZED]} of {totals['views']} drawn views are their counts' default "
        f"pictures, each improving on its house drawing; {totals[HOUSE]} keep the house"
    )


def _states_summary(rows: Sequence[Mapping[str, Any]]) -> str:
    counts = {state: sum(1 for row in rows if row["state"] == state) for state in STATES}
    return f"{len(rows)} counts: " + ", ".join(
        f"{counts[state]} {state.replace('-', ' ')}" for state in STATES
    )


def state_problems(
    record: Path = RECORD,
    index: Path = INDEX,
    tree: Path = REPO,
    *,
    settled: Mapping[int, Settled] | None = None,
    allowed: Mapping[int, str] | None = None,
) -> tuple[list[str], list[str]]:
    """What fails the regularization-state gate, and the pending counts it lists: digests
    and the retained record only, nothing measured (`--check` holds the record to the
    data)."""
    settled = SETTLED if settled is None else settled
    allowed = PENDING_ALLOWED if allowed is None else allowed
    found = json.loads(record.read_text(encoding="utf-8"))
    if found.get("contract") != CONTRACT:
        return [f"{RECORD_PATH} is not a {CONTRACT} record"], []
    stale = f"run `{GENERATOR} --update`"
    every = index_entries(index)
    rows = {int(row["n"]): row for row in found.get("states") or []}
    problems: list[str] = []
    if sorted(rows) != sorted(every) or len(rows) != len(found.get("states") or []):
        problems.append(
            f"{RECORD_PATH}'s states are not the index's counts, once each; {stale}"
        )
    for n in sorted(set(rows) & set(every)):
        row, entry = rows[n], every[n]
        now = witness_digest(entry, tree)
        if row["witness_sha256"] != now:
            problems.append(
                f"n={n}: the witness changed since its state was recorded "
                f"({row['witness_sha256'][:12]} to {now[:12]}); {stale}"
            )
        if row["state"] not in STATES:
            problems.append(f"n={n}: state {row['state']!r}")
        if row["drawn"] == VIEW and row["generator"] != entry.get("generator"):
            problems.append(
                f"n={n}: the record draws another view than the index holds; {stale}"
            )
        held = settled.get(n)
        if held is not None and held.witness_sha256 != now:
            problems.append(
                f"n={n}: SETTLED decided witness {held.witness_sha256[:12]}, and the atlas now "
                f"holds {now[:12]}; run the generators on it (regularization-process.md, "
                '"When a Witness Changes"), then settle it again or take it off SETTLED'
            )
        elif held is not None and row["state"] in (REGULARIZED_STATE, REGULAR_AS_PUBLISHED):
            problems.append(f"n={n}: SETTLED names it, but it is {row['state']}; take it off")
        if held is not None and held.state not in (DECIDED, EXEMPT):
            problems.append(f"n={n}: SETTLED gives state {held.state!r}")
        if held is not None and held.state == EXEMPT and not BEAD.search(held.evidence):
            problems.append(f"n={n}: an exemption names the bead that owns it")
    pending = {n for n, row in rows.items() if row["state"] == PENDING}
    problems.extend(
        f"n={n} is pending: {rows[n]['why']}. Run the strong generators on its witness "
        '(regularization-process.md, "When a Witness Changes"), or allow it in '
        "PENDING_ALLOWED with the bead that owns the run"
        for n in sorted(pending - set(allowed))
    )
    problems.extend(
        f"n={n}: PENDING_ALLOWED names it, but it is "
        f"{rows[n]['state'] if n in rows else 'not a count'}; take it off the list"
        for n in sorted(set(allowed) - pending)
    )
    problems.extend(
        f"n={n}: PENDING_ALLOWED names no bead: {allowed[n]!r}"
        for n in sorted(allowed)
        if not BEAD.match(allowed[n])
    )
    listed = [
        f"n={n} is pending, allowed: {allowed[n]}" for n in sorted(pending & set(allowed))
    ]
    summary = f"regularization states: {_states_summary(list(rows.values()))}"
    return problems, [*listed, summary]


def check_state() -> int:
    found, listed = state_problems()
    for line in listed:
        print(line)
    if found:
        for problem in found:
            print(f"regularization state: {problem}")
        return 1
    print(
        "regularization state check passed: every count is regularized, regular as "
        "published, decided or exempt, or pending on the shrink-only allowlist"
    )
    return 0


def update(*, workers: int = 1) -> int:
    expected = document(workers=workers)
    content = text(expected)
    if not RECORD.is_file() or RECORD.read_text(encoding="utf-8") != content:
        with atomic_output_file(RECORD) as temporary:
            temporary.write_text(content, encoding="utf-8")
    decisions.cache_clear()
    regularized_defaults.cache_clear()
    print(f"default drawings updated: {_summary(expected)}")
    print(f"regularization states: {_states_summary(expected['states'])}")
    return 0


def check(*, workers: int = 1) -> int:
    expected = document(workers=workers)
    found, kept = problems(expected)
    for line in kept:
        print(line)
    if found:
        for problem in found:
            print(f"default drawings drift: {problem}")
        print(f"run `{GENERATOR} --update`, or say why the rule has changed")
        return 1
    print(f"rule ({improvement_rule.SECTION}): {improvement_rule.statement()}")
    print(f"regularization states: {_states_summary(expected['states'])}")
    print(f"default drawings check passed: {_summary(expected)}")
    return 0


def parser() -> argparse.ArgumentParser:
    command = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    mode = command.add_mutually_exclusive_group(required=True)
    mode.add_argument("--update", action="store_true", help="write the record")
    mode.add_argument("--check", action="store_true", help="measure again and compare")
    mode.add_argument(
        "--check-state",
        action="store_true",
        help="the regularization-state gate: digests and the record, nothing measured",
    )
    command.add_argument(
        "--workers",
        type=int,
        default=None,
        help="processes to measure with (default: the gate's PACK_JOBS cap, or every core)",
    )
    return command


def main(argv: Sequence[str] | None = None) -> int:
    args = parser().parse_args(argv)
    if args.check_state:
        return check_state()
    workers = args.workers if args.workers is not None else worker_count(len(index_entries()))
    if args.update:
        return update(workers=workers)
    return check(workers=workers)


if __name__ == "__main__":
    raise SystemExit(main())
