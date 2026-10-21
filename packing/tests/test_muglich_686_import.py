"""Issue #686's packet: its derived facts, claims record and complete exact replay receipts.

The facts are held to the attachment's manifest and to the issue's prints, the claims
record that the beyond-horizon rows are read against to its rebuild, and every count's
receipt to its fact: a positive accepted and both kernel controls refused by both routes.
A forged control, a receipt moved to another count and a side above its print are refused.
"""

from __future__ import annotations

import copy
import json
from dataclasses import replace
from fractions import Fraction
from functools import cache

from devtools import evand_arrangement_reports as kernel
from devtools import evand_exact_certificates as legacy
from devtools import muglich_686_import as imp


@cache
def certificates() -> dict[int, legacy.Certificate]:
    return imp.read_facts()


def admitted(record: object, n: int) -> None:
    kernel.validate_receipt(
        record, {n: certificates()[n]}, receipt_format=imp.RECEIPT_FORMAT, **imp.PROFILE
    )


def refused(record: object, n: int) -> bool:
    try:
        admitted(record, n)
    except ValueError:
        return True
    return False


def test_the_manifest_pins_the_attachment_and_names_every_member_and_fact() -> None:
    imp.check_manifest()
    record = json.loads(imp.SOURCES.read_text("utf-8"))
    assert record["archive"]["raw_asset_retained"] is False
    assert [row["n"] for row in record["members"]] == list(imp.COUNTS)


def test_every_fact_rounds_up_to_its_print_and_rebuilds_the_claims_record() -> None:
    stored = json.loads(imp.BEYOND.read_text("utf-8"))
    assert stored == imp.claims_record(certificates())
    assert all(row["n"] > stored["horizon"] for row in stored["results"])


def test_every_count_has_an_admitted_receipt_with_both_controls_refused() -> None:
    for n in imp.COUNTS:
        record = kernel.read_xz(imp.receipt_path(n))
        admitted(record, n)
        verdicts = {
            (row["control"], route): row[route]["verification_passed"]
            for row in record["cases"]
            for route in kernel.ROUTES
        }
        assert verdicts == {
            (control, route): control == "positive"
            for control in kernel.JOBS
            for route in kernel.ROUTES
        }


def test_a_control_forged_as_accepted_is_refused() -> None:
    record = kernel.read_xz(imp.receipt_path(328))
    forged = copy.deepcopy(record)
    control = forged["cases"][1]
    control["exact_verify"]["verification_passed"] = True
    control["exact_verify"]["failures"] = []
    assert refused(forged, 328)


def test_a_receipt_moved_to_another_count_is_refused() -> None:
    assert refused(kernel.read_xz(imp.receipt_path(330)), 328)


def test_a_side_above_its_print_is_refused() -> None:
    certificate = certificates()[810]
    printed = imp.printed_sides()[810]
    imp.admit(certificate, printed)
    raised = replace(certificate, side=Fraction(printed) + Fraction(1, 10**18))
    try:
        imp.admit(raised, printed)
    except imp.Muglich686Error:
        return
    raise AssertionError("a side above the issue's print was admitted")
