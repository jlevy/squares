"""The root-name audit of the Lean kernel proof of Valid7 (#537, `devtools.audit_valid7_roots`).

The receipt in the evand-valid7-lean-2026-10-11 packet records that version 1's 9,800
certificate pickles and version 2's 9,800 generated root modules carry the names of the
k2m3 run V3's roots, R00000 to R09799; these tests re-derive what the retained files can,
the leaves file and the X-mode list, and hold the receipt to the digests the packets pin.
None needs the network or the release assets.
"""

from __future__ import annotations

import json

from devtools import audit_valid7_roots as audit


def test_the_receipt_re_derives_from_the_retained_files() -> None:
    assert audit.check() == []


def test_the_run_has_9800_roots_in_a_35_by_35_by_8_grid() -> None:
    grid = audit.leaves()
    assert (grid["roots"], grid["grid"]) == (9800, [35, 35, 8])


def test_both_versions_name_every_root_once() -> None:
    record = json.loads(audit.RECEIPT.read_text("utf-8"))
    assert record["version_1"]["pickles"] == record["version_1"]["listed"] == 9800
    assert record["version_1"]["every_pickle_matches_its_line"] is True
    assert record["version_2"]["root_modules"] == 9800
    assert record["version_2"]["lines"] == 62626
    assert record["version_2"]["others"] == ["Sqpack/V7/Main.lean"]
    assert record["xroots"]["roots"] == 2612
