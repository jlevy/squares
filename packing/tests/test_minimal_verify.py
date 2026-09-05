"""The standalone verifier decides the retained bytes, and refuses everything else.

`cases/n11_fractional_certificate/minimal_verify.py` is a second decision on
`certificate.json`: no numpy, no `sqpack`, nothing imported from this repository, and
its own SHA-256 pin on the bytes it will speak for. These tests run it the way a reader
does -- as a script, in a subprocess, on a path -- so what is asserted is the program's
printed verdict and its exit status, not the return value of an internal function.

Two refusals are worth separating, because they are different guarantees. A copy with
one weight lightened is still a well-formed certificate; it is refused because the atom
set is no longer D4-invariant, which is Condition 1. A copy with one byte changed is
refused before anything is parsed at all, because the digest is not the pinned one. The
first says the conditions are decided; the second says they are decided about *these*
bytes.
"""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
import sys
from fractions import Fraction
from pathlib import Path

import pytest

from devtools.check_rung_figures import decimal_matches
from sqpack.yamlio import safe_load

PACKING = Path(__file__).resolve().parents[1]
CASE = PACKING / "cases" / "n11_fractional_certificate"
VERIFIER = CASE / "minimal_verify.py"
CERTIFICATE = CASE / "certificate.json"
CARD = CASE / "PROOF-CARD.md"
RESULTS = PACKING / "frontier" / "results.yaml"

#: The verifier's own count of the cells it scores across the net. The exhaustive node
#: below re-derives it on every run and the card quotes it; this constant is what holds
#: those two together. Nothing else in the repository states it.
REACHABLE_CELLS = 567_131_843


def run(*arguments: str | Path) -> subprocess.CompletedProcess[str]:
    """Run the verifier as its own usage line says to: a script, given a path."""

    return subprocess.run(
        [sys.executable, str(VERIFIER), *(str(argument) for argument in arguments)],
        capture_output=True,
        text=True,
        check=False,
    )


def test_the_pinned_digest_is_the_retained_certificates_own_and_is_written_once() -> None:
    """One statement of the hash, in one file, and it is the artifact's."""

    source = VERIFIER.read_text(encoding="utf-8")
    digest = hashlib.sha256(CERTIFICATE.read_bytes()).hexdigest()
    pinned = re.findall(r'PINNED_SHA256 = "([0-9a-f]{64})"', source)

    assert pinned == [digest]
    assert source.count(digest) == 1


def test_a_single_lightened_weight_is_refused_by_condition_1(tmp_path: Path) -> None:
    """Halving one atom's weight leaves a well-formed file whose atoms are not D4."""

    record = json.loads(CERTIFICATE.read_text(encoding="utf-8"))
    x, y, weight = record["atoms"][0]
    record["atoms"][0] = [x, y, str(Fraction(weight) / 2)]
    lightened = tmp_path / "lightened.json"
    lightened.write_text(json.dumps(record), encoding="utf-8")

    result = run(lightened, "--unpinned")

    assert result.returncode == 1
    assert "REFUSED" in result.stdout
    assert "D4 image" in result.stdout
    assert "VERIFIED" not in result.stdout


def test_one_changed_byte_is_refused_by_the_pin(tmp_path: Path) -> None:
    """The digest is checked before the JSON is parsed, so nothing else is reached."""

    raw = CERTIFICATE.read_bytes()
    changed = raw.replace(b'"7/4000"', b'"7/4001"', 1)
    assert changed != raw
    assert len(changed) == len(raw)
    edited = tmp_path / "one-byte.json"
    edited.write_bytes(changed)

    result = run(edited)

    assert result.returncode == 1
    assert result.stdout.startswith("REFUSED  SHA-256")
    assert hashlib.sha256(changed).hexdigest() in result.stdout
    assert "Condition" not in result.stdout


def test_an_absent_certificate_is_refused_rather_than_crashing(tmp_path: Path) -> None:
    result = run(tmp_path / "not-here.json")

    assert result.returncode == 1
    assert "REFUSED" in result.stdout


@pytest.mark.exhaustive_exact
def test_the_retained_bytes_are_verified_on_the_full_net() -> None:
    """The whole decision, end to end.

    Measured 2026-09-05: 49.4 s for this node, of which 47.5 s is the verifier itself
    on CPython 3.14 and 47.3 s on the system's CPython 3.11. The marker registry in
    `test_module_boundaries.py` carries why that price belongs in this tier.
    """

    result = run(CERTIFICATE)

    assert result.returncode == 0, result.stdout
    assert "VERIFIED  s(11) >= 381/100" in result.stdout
    assert "Condition 1  PASS  1121 atoms" in result.stdout
    assert "Condition 2  PASS  total mass 434547/40000" in result.stdout
    assert "Condition 5  PASS  least covered mass 4001/4000" in result.stdout
    assert f"of 181, over {REACHABLE_CELLS} reachable cells" in result.stdout


def stated(pattern: str, text: str, label: str) -> str:
    """What the card says, where it says it, so the assertion can be against the artifact."""

    match = re.search(pattern, text)
    assert match is not None, f"the proof card no longer states {label}"
    return match.group(1)


def test_the_proof_card_states_the_certificates_own_figures() -> None:
    """Every parameter on the card, re-derived from the JSON the card is about.

    This is `D-439`'s shape at a new surface: prose quoting an artifact's figures, left
    behind when the artifact moves. `check_rung_figures.py` owns that rule for
    `results.yaml`, `evidence.yaml` and `defects.yaml`, and `check_case_prose.py` for
    the case bodies. The card is neither, and it is one document about one artifact
    sitting beside it, so the check lives here rather than in a third corpus-wide tool.
    """

    record = json.loads(CERTIFICATE.read_text(encoding="utf-8"))
    text = CARD.read_text(encoding="utf-8")
    total = sum((Fraction(weight) for _, _, weight in record["atoms"]), Fraction(0))
    limit, steps = Fraction(record["angle_limit"]), record["direction_steps"]
    tangents = [limit * step / steps for step in range(steps + 1)]
    gap = max(
        (tangents[k + 1] - tangents[k]) / (1 + tangents[k] * tangents[k + 1])
        for k in range(steps)
    )
    shrink = Fraction(record["square_side"])

    figures = {
        r"atoms\s+(\d+) nonnegative": (Fraction(len(record["atoms"])), "the atom count"),
        r"total weight\s+(\d+/\d+)": (total, "the total mass"),
        r"container side\s+L = (\d+/\d+)": (Fraction(record["outer_side"]), "the side"),
        r"shrink\s+B = (\d+/\d+)": (shrink, "the shrink"),
        r"net\s+(\d+) directions": (Fraction(steps + 1), "the direction count"),
        r"t_K\^2 \+ 2 t_K - 1 = (\d+/\d+)": (limit * limit + 2 * limit - 1, "the arc slack"),
        r"half-gap\s+D = (\d+/\d+)": (gap, "the largest half-gap tangent"),
        r"containment\s+B\(1 \+ D\) = (\d+/\d+)": (shrink * (1 + gap), "the containment"),
        r"least cover\s+(\d+/\d+)": (Fraction(record["least_cell_mass"]), "the least cover"),
        r"over (\d+) reachable event": (Fraction(REACHABLE_CELLS), "the reachable cells"),
    }
    for pattern, (value, label) in figures.items():
        assert Fraction(stated(pattern, text, label)) == value, label


def test_the_proof_card_quotes_the_digest_as_a_prefix_rather_than_pinning_it_again() -> None:
    """One pin, in `minimal_verify.py`; the card carries a prefix and where to get the rest."""

    digest = hashlib.sha256(CERTIFICATE.read_bytes()).hexdigest()
    text = CARD.read_text(encoding="utf-8")
    quoted = re.findall(r"sha256 ([0-9a-f]+)", text)

    assert quoted, "the card no longer quotes the certificate's digest at all"
    for prefix in quoted:
        assert len(prefix) >= 8
        assert digest.startswith(prefix)
    assert digest not in text
    assert "sha256sum certificate.json" in text


def test_every_fraction_equals_decimal_on_the_card_is_arithmetically_true() -> None:
    """The repository-wide rule applied to the card: `a/b = d.ddd` must be true as written.

    `decimal_matches` is imported rather than reimplemented, so this check and
    `check_rung_figures` can never disagree about what "true as written" means.
    """

    text = CARD.read_text(encoding="utf-8")
    pairs = re.findall(r"(?<![\w.])(\d+)/(\d+)\s*=\s*(-?\d+\.\d+)(?!\d)", text)

    assert pairs, "the card no longer states any fraction with its decimal"
    assert [
        f"{numerator}/{denominator} = {decimal}"
        for numerator, denominator, decimal in pairs
        if not decimal_matches(Fraction(int(numerator), int(denominator)), decimal)
    ] == []


def test_the_proof_card_reports_the_standing_the_register_holds() -> None:
    """The rung and the novelty label belong to `results.yaml`; the card only repeats them."""

    entry = next(
        result
        for result in safe_load(RESULTS.read_text(encoding="utf-8"))["results"]
        if result["id"] == "T-018"
    )
    text = CARD.read_text(encoding="utf-8")

    assert f"confirmation rung `{entry['confirmation']}`" in text
    assert f"`{entry['novelty']}`" in text
