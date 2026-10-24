"""Kevin Fang's excess-theorem packet: custody, the inventory's arithmetic and the receipts."""

from __future__ import annotations

import hashlib
import json
import re
import shlex
from fractions import Fraction
from pathlib import Path, PurePosixPath

import pytest

from cases.asymptotic import fang_excess_inventory as inventory
from devtools import acquire_source, check_results
from devtools import upper_bound_reports as reports
from sqpack.assurance import (
    claim_support_level,
    conditional_problems,
    conditions,
    undischarged,
)
from sqpack.yamlio import safe_load

NAME = "fang-excess-theorem-2026-10-13"
#: The 14 October review's checker run on the 18 pieces of Propositions 4 and 5, which
#: E-fang-excess-pieces-exact-replay records and the note's proof takes as its premise.
PIECES_RECEIPT = reports.packet_path(NAME) / "receipts" / "pieces-exact-check.log"
#: The Lean packet's copies of the author's pieces, whose bytes PIECES.md's digests name.
LEAN_CERTS = inventory.ROOT / "resources/web/fang-excess-lean-2026-10-18/source/certs/ours"
NOTE_PROOF = "E-fang-excess-note-proof"
PIECES_REPLAY = "E-fang-excess-pieces-exact-replay"


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


def lean_jexc(n: int) -> int:
    """`jExc` of Fang's Sqlean/Theorem2.lean at 947bdae, in natural-number division."""
    return max((n + 1) // 16, 1 + 2 * ((n - 15) // 21))


def test_the_lean_excess_is_f_or_one_short_wherever_mixing_the_steps_gains() -> None:
    # The records say where Fang's Lean theorem2 falls short of Theorem 2 (review A2 of
    # PR 781): not at n = 52 to 56 alone, but wherever k = n - 15 >= 37 leaves 16 to 20
    # on division by 21, by one and never more, and never above F(n).
    counts = range(15, 5001)
    excess = {n: inventory.excess(n) for n in counts}
    assert all(excess[n] - 1 <= lean_jexc(n) <= excess[n] for n in counts)
    short = {n for n in counts if lean_jexc(n) < excess[n]}
    assert short == {n for n in counts if n - 15 >= 37 and (n - 15) % 21 >= 16}
    assert (min(short), len(short), len(counts)) == (52, 1180, 4986)
    below_100 = [*range(52, 57), *range(73, 78), *range(94, 99)]
    assert sorted(n for n in short if n < 100) == below_100


def theorem_piece_digests() -> dict[str, str]:
    """The certificate file of each piece theorem/PIECES.md gives the role `theorem`, with
    the SHA-256 its table lists."""
    digests: dict[str, str] = {}
    for line in inventory.retained_text("theorem/PIECES.md").splitlines():
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if len(cells) == 10 and cells[7] == "theorem":
            path = cells[1].strip("`")
            fetched = f"{cells[0]}.cert"  # n-211 is fetched, and its row names no path
            name = PurePosixPath(path).name if path.endswith(".cert") else fetched
            digests[name] = cells[9].strip("`")
    return digests


def theorem_pieces() -> set[str]:
    """The certificate file of each piece theorem/PIECES.md gives the role `theorem`."""
    return set(theorem_piece_digests())


def data_lines(path: Path) -> list[str]:
    """A certificate's lines without its comment lines, which copies of one packing vary in."""
    lines = path.read_text(encoding="utf-8").splitlines()
    return [line for line in lines if not line.startswith("#")]


def piece_bindings(named: list[str]) -> dict[str, str]:
    """How each replayed certificate is the piece theorem/PIECES.md lists (review B1 of
    PR 781): by the table's SHA-256 itself, or, where the table's digest is of another
    copy (the 14 October review's MR-1), by data lines identical to the Lean packet's
    copy, whose bytes have that digest. Raises if a file binds neither way."""
    digests = theorem_piece_digests()
    bindings: dict[str, str] = {}
    for relative in named:
        path = inventory.ROOT / relative
        listed = digests[path.name]
        if hashlib.sha256(path.read_bytes()).hexdigest() == listed:
            bindings[path.name] = "digest"
            continue
        twin = LEAN_CERTS / path.name
        assert hashlib.sha256(twin.read_bytes()).hexdigest() == listed, path.name
        assert data_lines(path) == data_lines(twin), path.name
        bindings[path.name] = "data lines"
    return bindings


def receipt_verdicts(text: str) -> dict[str, tuple[Fraction, str]]:
    """Each certificate rectangle_check.py printed, with its exact squeeze and verdict."""
    found: dict[str, tuple[Fraction, str]] = {}
    name, squeeze = "", Fraction(0)
    for line in text.splitlines():
        if re.match(r"\S+\.cert: n = \d+", line):
            name = line.split(":", 1)[0]
        elif line.startswith("  squeeze "):
            squeeze = Fraction(line.split(" = ", 1)[1].split()[0])
        elif line.startswith("  verdict: "):
            found[name] = (squeeze, line.removeprefix("  verdict: "))
    return found


def test_the_pieces_receipt_decides_the_eighteen_theorem_pieces_above_the_squeeze() -> None:
    text = PIECES_RECEIPT.read_text(encoding="utf-8")
    command = shlex.split(text.splitlines()[0].removeprefix("# command: "))
    named = [argument for argument in command if argument.endswith(".cert")]
    assert command[3].endswith("review/programs/rectangle_check.py")
    assert all((inventory.ROOT / path).is_file() for path in named)
    assert {PurePosixPath(path).name for path in named} == theorem_pieces()
    verdicts = receipt_verdicts(text)
    assert set(verdicts) == theorem_pieces()
    assert len(verdicts) == 18
    assert {verdict for _squeeze, verdict in verdicts.values()} == {"STRICT_VALID"}
    assert all(squeeze > inventory.D0 for squeeze, _verdict in verdicts.values())
    assert min(verdicts, key=lambda name: verdicts[name][0]) == "n0308.cert"
    for stem, stated in inventory.STATED_SQUEEZE.items():
        assert verdicts[f"{stem}.cert"][0] >= stated
    assert "18 of 18 as required" in text
    assert "; exit 0; " in text.splitlines()[-1]
    # The bytes decided are the pieces the note's table names: Daniel's seven by the
    # table's digest, the author's eleven by their data lines.
    bindings = piece_bindings(named)
    assert sorted(name for name, how in bindings.items() if how == "digest") == [
        f"n-{n}.cert" for n in (110, 132, 156, 182, 211, 241, 273)
    ]
    assert len(bindings) == 18


def test_the_note_s_finite_premise_is_discharged_by_the_pieces_replay() -> None:
    by_id = {
        entry["id"]: entry
        for entry in safe_load(check_results.EVIDENCE.read_text(encoding="utf-8"))["evidence"]
    }
    note = by_id[NOTE_PROOF]
    assert [refs for _hypothesis, refs in conditions(note)] == [[PIECES_REPLAY]]
    assert undischarged(note, by_id, confirming=False) == []
    problems = conditional_problems({key: by_id[key] for key in (NOTE_PROOF, PIECES_REPLAY)})
    assert problems == []
    # The published proof carries its V3 to the theorem only through the replay: without
    # it the premise is open and the note supports the implication alone. T-163's derived
    # V3 does not depend on the note, since each count's pool takes the inventory's
    # two-route replay, so the theorem part's V3 is held here and in its composition.
    level = check_results.verification_level
    assert level(note) == 3
    assert level(by_id[PIECES_REPLAY]) == 3
    assert claim_support_level(note, by_id, level, confirming=False) == 3
    assert claim_support_level(note, {NOTE_PROOF: note}, level, confirming=False) == 0
    assert check_results.derive_verification([note]) == "V0"
