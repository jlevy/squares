"""Francisco Couzo's in-corpus rows of issues #670, #672 and #675: the lane of 22 October.

Four certificates, retained as factual data from their pins with their per-count JSON and
read by the `evand-cert` adapter: s(204) of #670 (``23aff0c6``), s(227) and s(229) of
#672 (``af8cb795``) and s(204) of #675 (``c6da0fc7``). The general importer's checks run
on the packets through ``test_upper_bound_reports``; these hold what is particular to
them: each certificate's digest and exact side, each frozen comparison's order at its
count, the report order the 18 October ledger recorded, and the pose-by-pose measurement
behind T-227's regularization items and the notes of T-226 and T-228. Every test reads
the retained packets and the records only; none needs the network.
"""

from __future__ import annotations

import hashlib
import json
from fractions import Fraction
from pathlib import Path
from typing import Any

import yaml

from devtools import upper_bound_reports as reports

PACKETS = {
    "[Couzo issue 670 2026-10-17]": "couzo-issue670-2026-10-17",
    "[Couzo issue 672 2026-10-17]": "couzo-issue672-2026-10-17",
    "[Couzo issue 675 2026-10-18]": "couzo-issue675-2026-10-18",
}
#: Each certificate's path in its packet's source, the SHA-256 its per-count JSON names,
#: and the exact side its header states.
CERTIFICATES = {
    ("couzo-issue670-2026-10-17", 204): (
        "certificates/n204.cert",
        "f317d0c0b04b947b9199ed47c998ff221d05e4d01849b942545364a173bc73dc",
        Fraction(45044217780850246618141, 3041751595240000000000),
    ),
    ("couzo-issue672-2026-10-17", 227): (
        "certificates/n227.cert",
        "65b03df883e75f890eca985232252a6340b9b5da3437c41275c9201df03d8c17",
        Fraction(71427829379429597600111901507, 4589408083628500000000000000),
    ),
    ("couzo-issue672-2026-10-17", 229): (
        "certificates/n229.cert",
        "9ab667ec73e55b4570fdc427b9f9930831a3e3f07b6953a2e05c6aee0a07609f",
        Fraction(231170315041711399213831561, 14771101209934000000000000),
    ),
    ("couzo-issue675-2026-10-18", 204): (
        "certificates/best/n204.cert",
        "761af9ec961d812a313b9b119845af6f8d2befa79ca770d0d919a09673a97543",
        Fraction(101859759444979981360793459, 6878398651426000000000000),
    ),
}


def _packet(name: str) -> Path:
    return reports.packet_path(name)


def _json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _yaml(path: Path) -> Any:
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def test_each_certificate_has_its_digest_and_side_and_the_house_reader_rebuilds_it() -> None:
    for (name, n), (path, digest, side) in CERTIFICATES.items():
        packet = _packet(name)
        source = reports.REPO / reports.acquisition(packet)["archived_path"]
        assert hashlib.sha256((source / path).read_bytes()).hexdigest() == digest
        assert reports.read_facts(packet)[n].side == side
        key = next(key for key, packet_name in PACKETS.items() if packet_name == name)
        assert reports.house_side(key, n) == side
        metadata = _json(source / f"certificates/n{n}.json")
        assert metadata["certificate_sha256"] == digest
        assert Fraction(metadata["rational_side"]) == side


def test_the_frozen_comparisons_order_each_count_as_the_ledger_does() -> None:
    """At 204, #670 is below T-186 and above #675, T-223 and T-225; #675 is below #670
    and above T-223 and T-225. At 227, #672 is below the house T-196 and above T-225; at
    229 it is below T-196 and above the house T-199, T-198 and T-225."""
    expected = {
        ("couzo-issue670-2026-10-17", 204): (
            "above",
            {
                "T-225 (evand/square-packing@0075967)": "above",
                "#675": "above",
                "T-186": "below",
            },
        ),
        ("couzo-issue672-2026-10-17", 227): (
            "below",
            {"T-225 (evand/square-packing@0075967)": "above"},
        ),
        ("couzo-issue672-2026-10-17", 229): (
            "above",
            {
                "T-225 (evand/square-packing@0075967)": "above",
                "T-198 (#674)": "above",
                "T-196 (#668)": "below",
            },
        ),
        ("couzo-issue675-2026-10-18", 204): (
            "above",
            {
                "T-225 (evand/square-packing@0075967)": "above",
                "#670": "below",
                "T-186": "below",
            },
        ),
    }
    for name in sorted(set(PACKETS.values())):
        rows = {row["n"]: row for row in reports.check_claims(_packet(name))["results"]}
        for (packet, n), (case, pending) in expected.items():
            if packet != name:
                continue
            row = rows[n]
            assert row["case"]["relation"] == case, (name, n)
            assert {item["report"]: item["relation"] for item in row["pending"]} == pending
            assert row["smallest"] == "T-225 (evand/square-packing@0075967)"


def test_the_18_october_ledger_recorded_every_row_in_report_order() -> None:
    ledger = _json(reports.ROOT / "campaign/issue-intake/upper-bounds-20261018/ledger.json")
    counts = {row["n"]: row for row in ledger["counts"]}
    for n, report in ((204, "#670"), (204, "#675"), (227, "#672"), (229, "#672")):
        (step,) = (step for step in counts[n]["steps"] if step["report"] == report)
        assert step["verdict"] == "recorded", (n, report)


def test_the_measurement_behind_the_regularization_items_and_notes() -> None:
    """#672's 229 is one to one with de Winter's #668 witness (T-196), 57 squares beyond
    1e-3 and none beyond 1e-2; Evan Daniel's #674 opening and update pair with it under no
    symmetry, 77 and 79 squares beyond a tenth; #675's 204 is #670's under the identity, 5
    beyond a tenth, and T-223's is one to one with it, none beyond a tenth."""
    record = _json(_packet("couzo-issue672-2026-10-17") / "measure/identity.json")
    pairs = {(row["n"], row["view"], row["against"]): row for row in record}
    refines = pairs[229, "#672", "T-196 (#668)"]
    assert refines["nearest_centre"]["one_to_one"]
    assert refines["assignment"]["moved_beyond"]["1e-3"] == 57
    assert refines["assignment"]["moved_beyond"]["1e-2"] == 0
    for view, beyond in (("T-198 (#674 opening)", 77), ("T-199 (#674 update)", 79)):
        other = pairs[229, view, "#672"]
        assert not other["nearest_centre"]["one_to_one"]
        assert other["assignment"]["moved_beyond"]["1e-1"] == beyond
    sequence = pairs[204, "#675", "#670"]
    assert sequence["nearest_centre"]["one_to_one"]
    assert sequence["assignment"]["moved_beyond"]["1e-1"] == 5
    assert pairs[204, "T-223 (#678)", "#675"]["assignment"]["moved_beyond"]["1e-1"] == 0


def test_each_atom_says_which_positives_touch_the_box() -> None:
    """#670's and #675's positives touch the box at 204; #672's touches at 229 and clears
    every wall at 227 by exactly 1e-15, so its atom names the count that touches rather
    than saying every positive does (review A1 of #718)."""
    evidence = {
        row["id"]: row for row in _yaml(reports.ROOT / "frontier/evidence.yaml")["evidence"]
    }
    expected = {
        "couzo-issue670-2026-10-17": "In every positive squares touch the box",
        "couzo-issue672-2026-10-17": (
            "At 229 squares touch the box, a least wall clearance of exactly 0; at 227 every "
            "wall clears by at least 1.00e-15;"
        ),
        "couzo-issue675-2026-10-18": "In every positive squares touch the box",
    }
    for name, sentence in expected.items():
        planned = reports.register_plan(_packet(name))["evidence.yaml"]
        assert sentence in planned["limitations"], name
        recorded = evidence[planned["id"]]["limitations"]
        assert " ".join(recorded.split()) == " ".join(planned["limitations"].split()), name
