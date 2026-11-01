"""Issue #804's exact sides: the derived fact and its exact decisions (T-244).

Hyukdong Kim's attachment states five polynomials and the side each names. The
``hyukdongkim-exact-forms-2026-10-25`` packet keeps them as a derived fact, and the ledger's
``review/exact_forms.py sides`` decides them offline into ``exact-sides.json``. This holds the
receipt to a fresh decision, the fact to the digests the issue and triage state, and the
decisions T-244 and the requests record rest on: each polynomial irreducible on both routes,
the root each print names, the three sides that are T-193's, and the two below T-174.
"""

from __future__ import annotations

import gzip
import hashlib
import importlib.util
import json
from fractions import Fraction
from pathlib import Path
from types import ModuleType
from typing import Any

import pytest
import yaml

PACKING = Path(__file__).resolve().parents[1]
LEDGER = PACKING / "campaign/issue-intake/upper-bounds-issue804-20261025"
PROGRAM = LEDGER / "review/exact_forms.py"
PACKET = PACKING / "resources/web/hyukdongkim-exact-forms-2026-10-25"


def program() -> ModuleType:
    spec = importlib.util.spec_from_file_location("exact_forms_804", PROGRAM)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def receipt() -> dict[str, Any]:
    return json.loads((LEDGER / "exact-sides.json").read_text(encoding="utf-8"))


def rows() -> dict[int, dict[str, Any]]:
    return {int(row["n"]): row for row in receipt()["rows"]}


def test_the_receipt_is_a_fresh_decision() -> None:
    assert program().main(["sides", "--check"]) == 0


def test_the_fact_names_the_issue_attachment() -> None:
    fact = json.loads((PACKET / "facts/exact-forms.json").read_text(encoding="utf-8"))
    source = fact["source"]
    assert source["archive_sha256"] == (
        "c770f9c37dee6b248543f3e661318630a0f279bc6a8c7663cb2efc53e2814ee7"
    )
    assert source["member_sha256"] == (
        "531e7077b3242aa56e959031824fb435693deaf8d73f7e33016d49c9e1709202"
    )
    assert [form["n"] for form in fact["forms"]] == [88, 126, 172, 199, 263]
    sources = json.loads((PACKET / "acquisition/sources.json").read_text(encoding="utf-8"))
    assert sources["attachment"]["raw_asset_retained"] is False
    assert sources["attachment"]["licence"].startswith("CC0 1.0")
    public = sources["attachment"]["public_copy"]
    assert public["commit"] == "f480441e73824668fb18779151369e4d3ba6179a"
    assert len(sources["members"]) == 7
    assert all(member["retained"] for member in sources["members"])


def test_the_archive_files_are_kept_as_the_member_digests_name_them() -> None:
    """Since 1 November 2026 the packet keeps the seven files themselves (CC0 1.0, think-9vai):
    each is the member the triage measured, and the forms member is the fact's source."""
    sources = json.loads((PACKET / "acquisition/sources.json").read_text(encoding="utf-8"))
    kept = sorted(
        path.relative_to(PACKET / "source").as_posix()
        for path in (PACKET / "source").rglob("*")
        if path.is_file()
    )
    assert kept == sorted(member["path"] for member in sources["members"])
    for member in sources["members"]:
        data = (PACKET / member["retained_at"]).read_bytes()
        assert len(data) == member["bytes"]
        assert hashlib.sha256(data).hexdigest() == member["sha256"]
    forms = PACKET / "source/squares-exact-forms/exact_forms.json"
    assert hashlib.sha256(forms.read_bytes()).hexdigest() == (
        "531e7077b3242aa56e959031824fb435693deaf8d73f7e33016d49c9e1709202"
    )


def test_the_receipt_reads_the_retained_fact() -> None:
    digest = hashlib.sha256((PACKET / "facts/exact-forms.json").read_bytes()).hexdigest()
    assert receipt()["fact_sha256"] == digest


@pytest.mark.parametrize(
    ("n", "degree", "real_roots", "index"),
    [(88, 7, 5, 4), (126, 2, 2, 2), (172, 24, 4, 1), (199, 16, 2, 2), (263, 17, 1, 1)],
)
def test_each_polynomial_and_root(n: int, degree: int, real_roots: int, index: int) -> None:
    row = rows()[n]
    assert row["degree"] == degree
    assert row["primitive"] is True
    assert row["irreducible_sympy"] is True
    assert row["irreducible_sqpack_field"] is True
    assert row["real_roots"] == real_roots
    assert row["root_index_ascending"] == index


@pytest.mark.parametrize("n", [88, 126, 199])
def test_three_sides_are_t193s(n: int) -> None:
    daniel = rows()[n]["against_daniel_639"]
    assert daniel["same_polynomial"] is True
    assert daniel["relation"] == "equal"


@pytest.mark.parametrize(("n", "margin"), [(172, "3.898e-89"), (263, "2.126e-94")])
def test_two_sides_are_below_t174(n: int, margin: str) -> None:
    row = rows()[n]
    houses = row["against_case_bounds"]
    assert [house["member"] for house in houses] == ["record T-174"]
    assert houses[0]["relation"] == f"below by {margin} to {margin}"
    assert row["against_daniel_639"]["relation"] == "below"


def test_the_register_states_cuts_of_the_roots() -> None:
    """T-244's claim states each side cut at 100 places; it must start the root's cut."""
    register = yaml.safe_load((PACKING / "frontier/results.yaml").read_text(encoding="utf-8"))
    claim = next(result["claim"] for result in register["results"] if result["id"] == "T-244")
    for n in (172, 263):
        cut = str(rows()[n]["claim_cut"])
        assert f"s({n}) <= {cut}" in " ".join(claim.split())
        low, high = (Fraction(end) for end in rows()[n]["interval"])
        stated = Fraction(cut.rstrip("…"))
        assert stated <= low
        assert high < stated + Fraction(1, 10**100)


CONFIGURATIONS = PACKING / "resources/web/hyukdongkim-t244-configurations-2026-10-25"


@pytest.mark.parametrize(("n", "degree"), [(172, 24), (263, 17)])
def test_the_configuration_facts_name_the_comment_attachment(n: int, degree: int) -> None:
    """The author's configurations of 09:06:23Z are kept as derived facts, not bytes."""
    sources = json.loads((CONFIGURATIONS / "acquisition/sources.json").read_text("utf-8"))
    assert sources["attachment"]["sha256"] == (
        "16e6ad9d04f1def897478e59260880320bc7c06ae89e41fa83837c7dc29c9a2d"
    )
    assert sources["attachment"]["raw_asset_retained"] is False
    assert not any(member["retained"] for member in sources["members"])
    fact = json.loads(gzip.decompress((CONFIGURATIONS / f"facts/n{n}.json.gz").read_bytes()))
    member = f"t244-exact-configurations/n{n}.minpoly.json"
    assert fact["source"]["member"] == member
    measured = {item["path"]: item["sha256"] for item in sources["members"]}
    assert fact["source"]["member_sha256"] == measured[member]
    assert fact["field_degree"] == degree
    assert fact["squares"] == n == len(fact["configuration"]["squares"])
