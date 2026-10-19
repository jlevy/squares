"""Kevin Fang's excess-theorem packet: custody, the inventory's arithmetic and the receipts."""

from __future__ import annotations

import json
from fractions import Fraction
from pathlib import Path

import pytest

from cases.asymptotic import fang_excess_inventory as inventory
from devtools import acquire_source
from devtools import upper_bound_reports as reports

NAME = "fang-excess-theorem-2026-10-13"


def test_the_packet_matches_its_acquisition_record() -> None:
    assert acquire_source.check(reports.packet_path(NAME), reports.REPO) == []


def test_the_inventory_receipt_rebuilds_and_every_check_holds() -> None:
    assert inventory.main(["--check"]) == 0


@pytest.mark.parametrize(
    ("n", "p", "q", "f"),
    [(15, 0, 0, 1), (30, 0, 0, 1), (31, 1, 0, 2), (36, 0, 1, 3), (47, 0, 1, 3), (64, 0, 2, 5)],
)
def test_f_and_its_maximiser_follow_the_definition_and_the_tie_break(
    n: int, p: int, q: int, f: int
) -> None:
    # At n = 47 both (2, 0) and (0, 1) reach p + 2q = 2; the README keeps the larger q.
    assert inventory.maximiser(n) == (p, q)
    assert inventory.excess(n) == f


def test_theorem_two_improves_every_published_deficiency_bound_from_15_to_72() -> None:
    receipt = inventory.build(
        {"read_at": "0" * 40, "below_grid": {"211": "14.9963367213363157"}}
    )
    rows = {row["k"]: row for row in receipt["deficiency"]}
    assert all(rows[k]["after_theorems"] < rows[k]["before"] for k in inventory.TABLE)
    assert (rows[65]["ryu"], rows[65]["theorem_2"]) == (63, 59)
    assert rows[15]["record_rows"] == 13
    assert receipt["crossover"]["ryu_below_theorem_2"][0] == [80, 85]


def test_a_certificate_header_with_one_square_too_many_is_refused(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    original = inventory.retained_text

    def altered(relative: str) -> str:
        text = original(relative)
        if relative == "theorem/n015_F1.cert":
            return text.replace("\n211 ", "\n212 ", 1)
        return text

    monkeypatch.setattr(inventory, "retained_text", altered)
    checks, _best = inventory.inventory_checks()
    assert not checks[0].holds
    assert "n=15: certificate header" in checks[0].value


def test_a_rectangle_squeezed_less_than_the_readme_states_is_refused(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setitem(inventory.STATED_SQUEEZE, "r17x16_n0257", Fraction(744, 10**6))
    (check,), _squeezes = inventory.rectangle_checks()
    assert not check.holds
    assert "r17x16_n0257: squeeze" in check.value


def test_a_frozen_row_the_retained_file_does_not_state_is_refused(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    stored = json.loads(inventory.HEADERS.read_text(encoding="utf-8"))
    stored["rows"][0]["side"] = "299998/20000"
    altered = tmp_path / "inventory-headers.json"
    altered.write_text(inventory.headers_text(stored), encoding="utf-8")
    monkeypatch.setattr(inventory, "HEADERS", altered)
    checks, _best = inventory.inventory_checks()
    assert not checks[0].holds
    assert "frozen list: theorem/n015_F1.cert states" in checks[0].value


def test_freezing_refuses_a_checkout_whose_bytes_are_not_the_pinned_ones(
    tmp_path: Path,
) -> None:
    first = inventory.inventory_files()[0]
    target = tmp_path / first
    target.parent.mkdir(parents=True)
    target.write_text(inventory.retained_text(first) + "\n", encoding="utf-8")
    with pytest.raises(ValueError, match="not the manifest's"):
        inventory.freeze_headers(tmp_path)


def test_freezing_refuses_a_certificate_above_the_byte_ceiling(tmp_path: Path) -> None:
    # One byte past MAX_CERTIFICATE_BYTES is refused before any digest or header is read.
    first = inventory.inventory_files()[0]
    target = tmp_path / first
    target.parent.mkdir(parents=True)
    target.write_bytes(b"0" * (inventory.MAX_CERTIFICATE_BYTES + 1))
    with pytest.raises(ValueError, match="larger than any inventory certificate"):
        inventory.freeze_headers(tmp_path)


def test_the_six_retained_certificates_are_the_frozen_list_s_rows() -> None:
    headers, problems = inventory.frozen_headers()
    assert problems == []
    retained = [
        relative
        for relative in inventory.inventory_files()
        if (inventory.SOURCE / relative).is_file()
    ]
    assert retained == [
        "theorem/n015_F1.cert",
        "theorem/n016_F1.cert",
        "theorem/n017_F1.cert",
        "theorem/n018_F1.cert",
        "theorem/n031_F2.cert",
        "theorem/best/n018_j2.cert",
    ]
    assert headers["theorem/n031_F2.cert"] == ["932", "619999/20000"]


def test_the_inventory_is_the_only_report_below_the_grid_at_thirty_counts() -> None:
    receipt = json.loads(inventory.RECEIPT.read_text(encoding="utf-8"))
    rows = inventory.inventory_map(receipt["record"])
    own = [row["count"] for row in rows if row["smallest"] == "inventory"]
    assert len(rows) == 76
    assert len(own) == 30
    assert (own[0], own[-1]) == (932, 4038)


def test_the_claim_record_rebuilds_with_932_the_one_beyond_horizon_claim() -> None:
    claims = reports.check_claims(reports.packet_path(NAME))
    assert [row["n"] for row in claims["results"]] == [211, 241, 273, 307, 308, 932]
    smallest = {row["n"]: row.get("smallest") for row in claims["results"]}
    assert [n for n, label in smallest.items() if label == reports.THIS] == [932]
    requested = reports.load_declaration(reports.packet_path(NAME))["requested"]
    assert [n for n in requested if n > reports.HORIZON] == [932]


def test_the_sample_receipt_admits_every_job_on_both_routes() -> None:
    packet = reports.packet_path(NAME)
    positives = reports.check_certification(packet)
    assert list(positives) == [211, 241, 273, 307, 308, 932]
    for margins in reports.margins(positives).values():
        assert Fraction(margins["exact_verify_best_pair_gap"]) > 0
        assert Fraction(margins["exact_verify_containment_clearance"]) > 0
