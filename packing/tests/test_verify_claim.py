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

from devtools.render_explainer import derive
from devtools.render_verifiable_claim import main as render_claims
from devtools.render_verifiable_claim import perturbations

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
    "total_mass": "1",
    "least_cell_mass": "1",
    "symmetry": "D4",
    "atoms": [["5/8", "5/8", "1"]],
}

#: The adversarial review's degenerate instance (Finding 3): n = 2, L = B = 1/2, net
#: (0, 1/2), one atom of weight 1 at the center. Upright, the B-square fits with no room
#: to move, so (1/4, 1/4) is the one admissible center; at t = 1/2 its bounding box is
#: 7/10 wide and nothing fits, so Condition 5 quantifies over nothing there. Every
#: hypothesis holds, B(1 + D) = 3/4, and the bound s(2) >= 1/2 follows.
REVIEWER = {
    "id": "reviewer-n2",
    "n": 2,
    "claim": "s(2) >= 1/2",
    "outer_side": "1/2",
    "square_side": "1/2",
    "angle_limit": "1/2",
    "direction_steps": 1,
    "total_mass": "1",
    "least_cell_mass": "1",
    "symmetry": "D4",
    "atoms": [["1/4", "1/4", "1"]],
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
    assert (
        "Declarations hold: claim 's(2) >= 5/4', total_mass 1, least_cell_mass 1, as computed"
    ) in out
    assert out.endswith("VERIFIED: s(2) >= 5/4\n")


def test_forged_declarations_are_refused_after_every_condition_holds(
    minimal: dict[str, Any], tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    """Finding 4 of the adversarial review: the file's own figures are compared, not carried."""
    record = {**TINY, "claim": "s(2) >= 100", "total_mass": "-100", "least_cell_mass": "500"}
    status, failing, out = decide(minimal, write(record, tmp_path / "forged.json"), capsys)
    assert status == 1
    assert failing == set()
    assert (
        "Declarations fail: claim declared 's(2) >= 100', computed 's(2) >= 5/4'; "
        "total_mass declared -100, computed 1; least_cell_mass declared 500, computed 1"
    ) in out
    assert out.endswith("REFUSED\n")


def test_a_certificate_missing_a_declaration_is_refused_before_any_condition(
    minimal: dict[str, Any], tmp_path: Path
) -> None:
    for field in ("claim", "total_mass", "least_cell_mass"):
        record = {key: value for key, value in TINY.items() if key != field}
        with pytest.raises(KeyError, match=field):
            minimal["load"](str(write(record, tmp_path / "bad.json")))


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


def test_a_failed_condition_skips_the_sweep(
    minimal: dict[str, Any], tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    """Finding 9b: the sweep is the expensive step, and it is not paid for a refused file."""
    status, failing, out = decide(
        minimal, write(perturbed("mass reaching n"), tmp_path / "p.json"), capsys
    )
    assert status == 1
    assert failing == {2}
    assert (
        "Condition 5 not evaluated: Condition 2 fails, and the sweep runs only when "
        "Conditions 1 to 4 hold"
    ) in out
    assert (
        "Declarations fail: total_mass declared 1, computed 2; least_cell_mass not compared"
    ) in out
    record = {**perturbed("mass reaching n"), "angle_limit": "41/100"}
    _, failing, out = decide(minimal, write(record, tmp_path / "q.json"), capsys)
    assert failing == {2, 3}
    assert "Condition 5 not evaluated: Conditions 2, 3 fail, and the sweep" in out


def test_a_certificate_above_the_ceiling_is_refused_before_any_condition(
    minimal: dict[str, Any], tmp_path: Path
) -> None:
    """Both standalone parser bounds accept the ceiling and refuse the next value.

    The declared-bound checker cannot resolve the runpy namespace, so name its keys:
    cases/n11_fractional_certificate/verify_claim.py::MAX_ATOMS
    cases/n11_fractional_certificate/verify_claim.py::MAX_DIRECTIONS
    """
    atoms = [["5/8", "5/8", "1"]] * (minimal["MAX_ATOMS"] + 1)
    with pytest.raises(ValueError, match="this verifier decides at most"):
        minimal["load"](str(write({**TINY, "atoms": atoms}, tmp_path / "wide.json")))
    minimal["load"](str(write({**TINY, "atoms": atoms[:-1]}, tmp_path / "at-ceiling.json")))
    steps = {**TINY, "direction_steps": minimal["MAX_DIRECTIONS"]}
    with pytest.raises(ValueError, match="this verifier decides at most"):
        minimal["load"](str(write(steps, tmp_path / "long.json")))
    within = {**TINY, "direction_steps": minimal["MAX_DIRECTIONS"] - 1}
    assert (
        len(minimal["load"](str(write(within, tmp_path / "fine.json")))[3])
        == (minimal["MAX_DIRECTIONS"])
    )


@pytest.mark.parametrize(
    "damage",
    [
        {"outer_side": 1.25},  # a JSON float is already rounded
        {"total_mass": 1.0},
        {"claim": 5},
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


def test_a_direction_where_no_square_fits_decides_nothing(minimal: dict[str, Any]) -> None:
    side = shrunk = Fraction(1, 2)
    atoms = [(Fraction(1, 4), Fraction(1, 4), Fraction(1))]
    assert minimal["least_mass"](side, shrunk, Fraction(1, 2), atoms, 1) == (None, None, 0)


def test_a_direction_with_one_admissible_center_is_scored_directly(
    minimal: dict[str, Any],
) -> None:
    side, center = Fraction(1, 2), (Fraction(1, 4), Fraction(1, 4))
    atoms = [(*center, Fraction(1))]
    # Upright with B = L, the one placement is the container itself.
    assert minimal["least_mass"](side, side, Fraction(0), atoms, 1) == (1, center, 1)
    # At t = 1/2 a B-square's bounding box is 7B/5 wide, so B = 5L/7 fits exactly once.
    rotated = minimal["least_mass"](side, Fraction(5, 14), Fraction(1, 2), atoms, 1)
    assert rotated == (1, center, 1)
    light = [(*center, Fraction(1, 2))]
    half = minimal["least_mass"](side, side, Fraction(0), light, 2)
    assert half == (Fraction(1, 2), center, 1)


def test_the_reviewers_degenerate_instance_is_accepted(
    minimal: dict[str, Any], tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    status, failing, out = decide(minimal, write(REVIEWER, tmp_path / "r.json"), capsys)
    assert status == 0
    assert failing == set()
    assert (
        "least covered mass 1 at direction 0 (t = 0), center (1/4, 1/4); 1 cells over "
        "2 directions, 1 of them admitting no placement"
    ) in out
    assert out.endswith("VERIFIED: s(2) >= 1/2\n")


def test_a_single_placement_short_of_mass_fails_condition_5(
    minimal: dict[str, Any], tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    record = {**REVIEWER, "atoms": [["1/4", "1/4", "1/2"]]}
    record.update(total_mass="1/2", least_cell_mass="1/2")
    status, failing, out = decide(minimal, write(record, tmp_path / "r.json"), capsys)
    assert status == 1
    assert failing == {5}
    assert "least covered mass 1/2 at direction 0 (t = 0), center (1/4, 1/4)" in out


def test_no_placement_at_any_direction_holds_vacuously(
    minimal: dict[str, Any], tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    """B = 3/5 > L: bounding boxes 3/5 and 21/25 wide, and B(1 + D) = 9/10 still."""
    record = {**REVIEWER, "square_side": "3/5"}
    status, failing, out = decide(minimal, write(record, tmp_path / "r.json"), capsys)
    assert status == 0
    assert failing == set()
    assert (
        "Condition 5 holds: no placement at any of the 2 directions, so nothing was decided"
    ) in out
    assert out.endswith("VERIFIED: s(2) >= 1/2\n")


def test_the_tight_direction_of_the_rung_covers_50003_over_50000(
    minimal: dict[str, Any],
) -> None:
    """Direction 0 is where the rung's least covered mass is attained; one direction is fast."""
    n, side, shrunk, tangents, atoms, declared = minimal["load"](str(RUNG_19_5))
    assert declared == {
        "claim": "s(11) >= 19/5",
        "total_mass": Fraction(43391, 4000),
        "least_cell_mass": Fraction(50003, 50000),
    }
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


def test_the_documents_state_these_perturbations() -> None:
    """The figures “How to Check It” prints, pinned so that a change in how they are chosen
    is noticed; the exhaustive tier below runs the 19/5 ones through the verifier."""
    stated = perturbations(derive(RUNG_19_5))
    assert stated["MARGIN_FRAC"] == "3/50000"
    assert stated["TIGHT_ATOM"] == "(1/2, 29/30)"
    assert stated["TIGHT_ORBIT"] == "8"
    assert stated["LIGHTEN_FRAC"] == "1/10000"
    assert stated["LIGHTENED_LEAST_FRAC"] == "24999/25000"
    assert stated["CENTER_ATOM"] == "(19/10, 19/10)"
    stated = perturbations(derive(RUNG_381_100))
    assert stated["MARGIN_FRAC"] == "1/4000"
    assert stated["TIGHT_ATOM"] == "(43/100, 99/100)"
    assert stated["LIGHTEN_FRAC"] == "1/1000"
    assert stated["LIGHTENED_LEAST_FRAC"] == "3997/4000"
    assert stated["CENTER_ATOM"] == "(381/200, 381/200)"


def lightened(certificate: Path, sites: str, by: str) -> dict[str, Any]:
    """The certificate with every atom at one of the sites, as the document lists them,
    lightened by the stated amount; the declarations are left as they were."""
    record: dict[str, Any] = json.loads(certificate.read_text())
    targets = {
        tuple(Fraction(c) for c in site.split(", ")) for site in sites[1:-1].split("), (")
    }
    for atom in record["atoms"]:
        if (Fraction(atom[0]), Fraction(atom[1])) in targets:
            atom[2] = str(Fraction(atom[2]) - Fraction(by))
    return record


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
    assert (
        "Declarations hold: claim 's(11) >= 19/5', total_mass 43391/4000, "
        "least_cell_mass 50003/50000, as computed"
    ) in out
    assert out.endswith("VERIFIED: s(11) >= 19/5\n")


@pytest.mark.exhaustive_exact
def test_the_stated_orbit_lightening_fails_condition_5_alone(
    minimal: dict[str, Any], tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    """The document's first perturbation of the 19/5 rung, with the outcome it states."""
    stated = perturbations(derive(RUNG_19_5))
    record = lightened(RUNG_19_5, stated["TIGHT_ORBIT_SITES"], stated["LIGHTEN_FRAC"])
    status, failing, out = decide(minimal, write(record, tmp_path / "orbit.json"), capsys)
    assert status == 1
    assert failing == {5}
    least = Fraction(out.split("least covered mass ")[1].split(" ")[0])
    assert least <= Fraction(stated["LIGHTENED_LEAST_FRAC"])
    assert "Declarations fail: total_mass declared 43391/4000" in out
    assert "least_cell_mass declared 50003/50000" in out


@pytest.mark.exhaustive_exact
def test_the_stated_benign_lightening_keeps_every_condition(
    minimal: dict[str, Any], tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    """The document's benign perturbation of the 19/5 rung: only the declarations refuse."""
    stated = perturbations(derive(RUNG_19_5))
    record = lightened(RUNG_19_5, stated["CENTER_ATOM"], stated["MARGIN_FRAC"])
    status, failing, out = decide(minimal, write(record, tmp_path / "center.json"), capsys)
    assert status == 1
    assert failing == set()
    assert out.count(" holds: ") == 5
    assert "Declarations fail: total_mass declared 43391/4000, computed 1084769/100000" in out
    assert out.endswith("REFUSED\n")


@pytest.mark.exhaustive_exact
@pytest.mark.parametrize("case", FALSIFICATIONS, ids=[name for _, name, _, _ in FALSIFICATIONS])
def test_every_falsification_is_refused_on_the_expected_condition(
    minimal: dict[str, Any],
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
    case: tuple[int, str, set[int], Fraction],
) -> None:
    """`falsify.py`'s own perturbations, decided by the minimal verifier instead.

    `falsify.py` never short-circuits, so its table records a Condition 5 minimum for
    every row; this verifier sweeps only once Conditions 1 to 4 hold, so a row failing
    among them is expected to report Condition 5 as not evaluated, and only a row that
    fails Condition 5 alone reproduces the recorded least covered mass.
    """
    row, name, expected, least = case
    falsify = runpy.run_path(str(THIRDPARTY / "falsify.py"), run_name="falsify")
    record = json.loads((THIRDPARTY / "certificate.json").read_text())
    reference = falsify["verify"].load(str(THIRDPARTY / "certificate.json"))
    _, table = falsify["perturbations"](record, reference, WITNESS)
    perturbation = table[row][1]()
    status, failing, out = decide(minimal, write(perturbation, tmp_path / "p.json"), capsys)
    assert status == 1, name
    before_sweep = expected - {5}
    assert failing == (before_sweep or expected), name
    if expected <= {5}:
        assert f"least covered mass {least} at direction" in out, name
    else:
        assert "Condition 5 not evaluated" in out, name
    assert out.endswith("REFUSED\n")
