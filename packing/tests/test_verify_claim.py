"""The unpinned standard-library verifier: accepted on the 19/5 rung, refused on the rest.

`cases/n11_fractional_certificate/verify_claim.py` is the verifier that
the `t-018-verifiable-claim-*.md` documents carry in full, each with its certificate, for a
reader outside the project. It imports
nothing from this project, so it is loaded from its path rather than imported, and it
is exercised through the same `load` and `decide` calls its command line makes: the
verdict is read back from the lines it prints.

Two tiers. The fast tier decides a two-atom-sized instance of the theorem (n = 2, one
atom of weight 1 at the center of a container of side 5/4) and one perturbation per
condition, in milliseconds, and checks the tight direction of the real 19/5 rung. The
`exhaustive_exact` tier runs the full 181-direction decision on the rung (about 36 s in
pure Python) and every row of `thirdparty/falsify.py`'s table, each a full decision.
"""

from __future__ import annotations

import json
import runpy
from fractions import Fraction
from pathlib import Path
from typing import Any

import pytest

from devtools.render_verifiable_claim import main as render_claims

CASE = Path(__file__).parents[1] / "cases/n11_fractional_certificate"
VERIFIER = CASE / "verify_claim.py"
RUNG_19_5 = CASE / "certificate-19-5.json"
RUNG_381_100 = CASE / "certificate.json"
#: The verifiable-claim documents, each carrying the verifier and its own certificate.
CLAIMS = {
    RUNG_19_5: CASE / "t-018-verifiable-claim-19-5.md",
    RUNG_381_100: CASE / "t-018-verifiable-claim-381-100.md",
}
THIRDPARTY = CASE / "thirdparty"

#: The smallest genuine instance: n = 2, L = 5/4, B = 7/10, one net step. Two B-squares
#: cannot sit side by side (2B > L), B(1 + D) = 4949749/5000000 < 1, and every admissible
#: placement at either net angle covers the center, so the least covered mass is exactly 1.
TINY = {
    "id": "tiny-n2",
    "n": 2,
    "claim": "s(2) >= 5/4",
    "outer_side": "5/4",
    "square_side": "7/10",
    "angle_limit": "207107/500000",
    "direction_steps": 1,
    "symmetry": "D4",
    "atoms": [["5/8", "5/8", "1"]],
}

#: The witness `thirdparty/verify.py` reports for the unperturbed rung, which
#: `falsify.perturbations` uses only to pick the atom it perturbs (atom 0 at (1/2, 29/30)).
WITNESS = (0, Fraction(0), Fraction(53, 100), Fraction(53, 100))

#: Every row of the falsification table, with the conditions the README records as
#: failing and the least covered mass it records, all from the reference verifier.
FALSIFICATIONS = [
    (0, "weight of that atom lowered by 1/10000", {1, 5}, Fraction(24999, 25000)),
    (1, "weights of its whole orbit lowered by 1/10000", {5}, Fraction(49993, 50000)),
    (2, "that atom dropped", {1, 5}, Fraction(49189, 50000)),
    (3, "its whole orbit dropped", {5}, Fraction(387, 400)),
    (4, "that atom shifted by +1/1000 in x", {1}, Fraction(50003, 50000)),
    (5, "container side 4, atoms unchanged", {1, 5}, Fraction(0)),
    (6, "container side 4, atoms translated by +1/10", {5}, Fraction(0)),
    (7, "weights scaled so the total is exactly n", {2}, Fraction(1100066, 1084775)),
    (8, "angle limit 41/100, short of tan(pi/8)", {3, 5}, Fraction(195849, 200000)),
    (9, "B raised to 1/(1 + D), so B(1 + D) = 1", {4}, Fraction(50003, 50000)),
]


@pytest.fixture(scope="module")
def minimal() -> dict[str, Any]:
    """The verifier's namespace, run from its path so nothing is imported from it."""
    return runpy.run_path(str(VERIFIER), run_name="verify_claim")


def decide(
    minimal: dict[str, Any], path: Path, capsys: pytest.CaptureFixture[str]
) -> tuple[int, set[int], str]:
    """Run the verifier's whole decision; return (exit status, failing conditions, stdout)."""
    status = minimal["decide"](*minimal["load"](str(path)))
    out = capsys.readouterr().out
    failing = {
        int(line.split()[1])
        for line in out.splitlines()
        if line.startswith("Condition ")
        if line.split()[2] == "fails:"
    }
    return status, failing, out


def write(record: dict[str, Any], path: Path) -> Path:
    path.write_text(json.dumps(record))
    return path


def test_the_smallest_instance_is_accepted(
    minimal: dict[str, Any], tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    status, failing, out = decide(minimal, write(TINY, tmp_path / "tiny.json"), capsys)
    assert status == 0
    assert failing == set()
    assert "least covered mass 1 at direction 0 (t = 0), center (5/8, 5/8)" in out
    assert out.endswith("VERIFIED: s(2) >= 5/4\n")


def perturbed(name: str) -> dict[str, Any]:
    """One perturbation of the smallest instance, breaking exactly the named condition."""
    record: dict[str, Any] = json.loads(json.dumps(TINY))
    if name == "atom shifted":
        record["atoms"][0][0] = "63/100"
    elif name == "mass reaching n":
        record["atoms"][0][2] = "2"
    elif name == "net short of pi/4":
        record["angle_limit"] = "41/100"
    elif name == "B raised to 1/(1 + D)":
        record["square_side"] = "500000/707107"
    elif name == "container enlarged, atom recentered":
        record["outer_side"] = "2"
        record["atoms"][0][:2] = ["1", "1"]
    elif name == "weight lowered":
        record["atoms"][0][2] = "9999/10000"
    return record


@pytest.mark.parametrize(
    ("name", "expected"),
    [
        ("atom shifted", {1}),
        ("mass reaching n", {2}),
        ("net short of pi/4", {3}),
        ("B raised to 1/(1 + D)", {4}),
        ("container enlarged, atom recentered", {5}),
        ("weight lowered", {5}),
    ],
)
def test_each_condition_refuses_its_own_perturbation(
    minimal: dict[str, Any],
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
    name: str,
    expected: set[int],
) -> None:
    status, failing, out = decide(minimal, write(perturbed(name), tmp_path / "p.json"), capsys)
    assert status == 1
    assert failing == expected
    assert out.endswith("REFUSED\n")


@pytest.mark.parametrize(
    "damage",
    [
        {"outer_side": 1.25},  # a JSON float is already rounded
        {"n": 0},
        {"direction_steps": 0},
        {"atoms": [["5/8", "5/8", "-1"]]},
        {"atoms": [["5/8", "5/8"]]},
        {"variant": "class"},  # a claim about a class of packings, not the one decided here
        {"variant": "conditional"},
    ],
)
def test_a_malformed_file_is_refused_before_any_condition(
    minimal: dict[str, Any], tmp_path: Path, damage: dict[str, Any]
) -> None:
    record = {**TINY, **damage}
    with pytest.raises((TypeError, ValueError)):
        minimal["load"](str(write(record, tmp_path / "bad.json")))


def test_the_tight_direction_of_the_rung_covers_50003_over_50000(
    minimal: dict[str, Any],
) -> None:
    """Direction 0 is where the rung's least covered mass is attained; one direction is fast."""
    n, side, shrunk, tangents, atoms = minimal["load"](str(RUNG_19_5))
    detail, holds = minimal["symmetric"](atoms, side)
    assert holds, detail
    assert sum(w for _, _, w in atoms) == Fraction(43391, 4000) < n
    scale = 200000
    assert all((w * scale).denominator == 1 for _, _, w in atoms)
    mass, center, cells = minimal["least_mass"](side, shrunk, tangents[0], atoms, scale)
    assert mass == Fraction(50003, 50000)
    assert center == (Fraction(53, 100), Fraction(53, 100))
    assert cells == 34969
    mass, _, cells = minimal["least_mass"](side, shrunk, tangents[-1], atoms, scale)
    assert mass >= 1
    assert cells == 499545


def fenced(text: str, language: str) -> str:
    """The body of a document's four-backtick block in that language, final newline kept."""
    start = text.index(f"````{language}\n") + len(f"````{language}\n")
    end = text.index("\n````\n", start)
    return text[start : end + 1]


@pytest.mark.parametrize("certificate", CLAIMS, ids=lambda p: p.stem)
def test_the_claim_document_carries_the_verifier_verbatim(certificate: Path) -> None:
    """The pasted source is the file, byte for byte."""
    assert fenced(CLAIMS[certificate].read_text(), "python") == VERIFIER.read_text()


@pytest.mark.parametrize("certificate", CLAIMS, ids=lambda p: p.stem)
def test_the_claim_document_carries_its_certificate_verbatim(certificate: Path) -> None:
    """The block is the file up to its final newline, which the fence supplies."""
    block = fenced(CLAIMS[certificate].read_text(), "json")
    assert block.rstrip("\n") == certificate.read_text().rstrip("\n")


@pytest.mark.parametrize("certificate", CLAIMS, ids=lambda p: p.stem)
def test_the_verifier_reads_the_certificate_out_of_the_claim_document(
    minimal: dict[str, Any], certificate: Path
) -> None:
    """One file travels: run on the document, the verifier decides the same certificate."""
    assert minimal["load"](str(CLAIMS[certificate])) == minimal["load"](str(certificate))


def test_a_document_without_a_certificate_is_refused(
    minimal: dict[str, Any], tmp_path: Path
) -> None:
    path = tmp_path / "claim.md"
    path.write_text("# A claim\n\nNo certificate here.\n")
    with pytest.raises(ValueError, match="fenced json block"):
        minimal["load"](str(path))


def test_the_claim_documents_are_current() -> None:
    """Regenerated from the template, the verifier and the certificates, nothing changes."""
    assert render_claims(["--check"]) == 0


@pytest.mark.exhaustive_exact
def test_the_19_5_rung_is_accepted_on_the_full_net(
    minimal: dict[str, Any], capsys: pytest.CaptureFixture[str]
) -> None:
    status, failing, out = decide(minimal, RUNG_19_5, capsys)
    assert status == 0
    assert failing == set()
    assert (
        "least covered mass 50003/50000 at direction 0 (t = 0), center (53/100, 53/100); "
        "90546593 cells over 181 directions"
    ) in out
    assert out.endswith("VERIFIED: s(11) >= 19/5\n")


@pytest.mark.exhaustive_exact
@pytest.mark.parametrize("case", FALSIFICATIONS, ids=[name for _, name, _, _ in FALSIFICATIONS])
def test_every_falsification_is_refused_on_the_expected_condition(
    minimal: dict[str, Any],
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
    case: tuple[int, str, set[int], Fraction],
) -> None:
    """`falsify.py`'s own perturbations, decided by the minimal verifier instead."""
    row, name, expected, least = case
    falsify = runpy.run_path(str(THIRDPARTY / "falsify.py"), run_name="falsify")
    record = json.loads((THIRDPARTY / "certificate.json").read_text())
    reference = falsify["verify"].load(str(THIRDPARTY / "certificate.json"))
    _, table = falsify["perturbations"](record, reference, WITNESS)
    perturbation = table[row][1]()
    status, failing, out = decide(minimal, write(perturbation, tmp_path / "p.json"), capsys)
    assert status == 1, name
    assert failing == expected, name
    assert f"least covered mass {least} at direction" in out, name
    assert out.endswith("REFUSED\n")
