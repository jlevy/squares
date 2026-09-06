"""Write the verifiable-claim documents and the proof card from the certificates.

Each claim document is one self-contained file per certificate: the claim, the theorem
and its proof, the finite form of Condition 5, how this repository decided the bytes, the
standard-library verifier `verify_claim.py` byte for byte, and the certificate it
decides, byte for byte as well, so a reader can paste that one file into a coding agent
or check it by hand without the rest of the repository. Both come from one template, so
the shared text cannot drift between them. The proof card states the headline bound on
one page, from the same certificate and the register, so its figures cannot drift from
either. `--check` refuses a stale copy of any of the three; the test suite runs that
check.

Run from `packing/`:

    uv run --frozen --group dev python -m devtools.render_verifiable_claim [--check]
"""

from __future__ import annotations

import argparse
import hashlib
import os
import re
import sys
from collections.abc import Sequence
from fractions import Fraction
from pathlib import Path

from strif import atomic_output_file

from devtools.render_explainer import (
    CASE,
    PACKING,
    REPO,
    TEMPLATES,
    THIRDPARTY,
    VERIFIER,
    VERIFIER_CLAIM,
    WALKTHROUGH,
    Facts,
    bound_substitutions,
    claim_path,
    decimal,
    derive,
    digits,
    edition_file,
    fill,
    runtime_phrase,
    slug,
)
from sqpack.fractional.certificate import d4_images
from sqpack.yamlio import safe_load

TEMPLATE = TEMPLATES / "verifiable_claim.md"
CARD_TEMPLATE = TEMPLATES / "proof_card.md"
CARD = CASE / "t-018-proof-card.md"
RESULTS = PACKING / "frontier" / "results.yaml"
RESULT_ID = "T-018"
INTERVAL = PACKING / "src" / "sqpack" / "fractional" / "interval.py"
GATE = PACKING / "devtools" / "decide_certificate.py"
PINNED_VERIFIER = CASE / "minimal_verify.py"
FIGURE = CASE / "t-018-proof-visual.svg"

#: The card quotes the certificate's digest by this many leading hex characters. The
#: whole digest is pinned once, in `minimal_verify.py`, and `sha256sum` gives a reader
#: the rest; a second full copy would be a second thing to keep in step.
DIGEST_PREFIX_CHARS = 12

#: Event cells the pinned verifier scores over every net direction, as it reports them.
#: Counting them is the full sweep, minutes of work the card should not pay for at every
#: render, so the count is recorded per certificate with the run that produced it
#: (`minimal_verify.py certificate.json`, 2026-09-05); a certificate without a recorded
#: count has no card. This is the one typed copy: `test_minimal_verify.py` imports it, and
#: its exhaustive node re-derives it from the verifier's own report.
REACHABLE_CELLS = {"381-100": 567_130_649}

#: How many decimal places the card carries for the two irrational-looking quantities it
#: cannot print exactly: the largest half-gap tangent and the containment product. Both
#: are rationals with long expansions, cut off rather than rounded.
HALF_GAP_PLACES = 10
CONTAINMENT_PLACES = 12


def frac(value: Fraction) -> str:
    return f"{value.numerator}/{value.denominator}"


def sha256_of(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def relative_link(target: Path, document: Path) -> str:
    """A link from `document` to `target`, relative, as the card writes its links."""
    return os.path.relpath(target, document.parent).replace(os.sep, "/")


def standing(facts: Facts, headline: Facts) -> str:
    """Where this bound stands among the project's, for a reader who has only this file."""
    if facts is headline:
        return "It is the tighter of the two bounds the project proves."
    return "It is the looser of the two bounds the project proves, with the simpler numbers."


def point(x: Fraction, y: Fraction) -> str:
    return f"({frac(x)}, {frac(y)})"


def perturbations(facts: Facts) -> dict[str, str]:
    """The perturbations “How to Check It” states, each computed from the certificate.

    The margin over Condition 5 is the least covered mass less 1, and the atom named is
    the first in the file that the witness placement covers. Lightening its whole orbit
    by more than the margin keeps Condition 1 and takes that placement below 1, so
    Condition 5 fails and the least the verifier reports is at most the old least less
    the lightening. Lightening the central atom, the one-point orbit, by the margin or
    less costs every placement at most the margin, so all five conditions still hold. The
    lightening is the coarsest power of ten above the margin, so that it reads as a
    number a reader would type.
    """
    side, half = facts.outer_side, facts.square_side / 2
    witness_x, witness_y = facts.witness
    margin = facts.least_mass - 1
    tight = next(
        a for a in facts.atoms if abs(a.x - witness_x) <= half and abs(a.y - witness_y) <= half
    )
    orbit = sorted(set(d4_images(tight.x, tight.y, side)))
    central = next((a for a in facts.atoms if (a.x, a.y) == (side / 2, side / 2)), None)
    places = 1
    while Fraction(1, 10 ** (places + 1)) > margin:
        places += 1
    lightening = Fraction(1, 10**places)
    if central is None or len(orbit) == 1 or tight.weight <= lightening:
        raise SystemExit(
            f"{facts.source.name}: the perturbations the claim document states need a "
            "central atom, a tight atom with an orbit of more than one site, and that "
            f"atom heavier than the lightening {lightening}"
        )
    return {
        "MARGIN_FRAC": frac(margin),
        "TIGHT_ATOM": point(tight.x, tight.y),
        "TIGHT_WEIGHT": frac(tight.weight),
        "TIGHT_ORBIT": str(len(orbit)),
        "TIGHT_ORBIT_SITES": ", ".join(point(x, y) for x, y in orbit),
        "LIGHTEN_FRAC": frac(lightening),
        "LIGHTENED_LEAST_FRAC": frac(facts.least_mass - lightening),
        "CENTER_ATOM": point(side / 2, side / 2),
        "CENTER_WEIGHT": frac(central.weight),
    }


def decided_here(facts: Facts, headline: Facts) -> str:
    """How the repository decided this certificate, beyond the verifier in the file.

    The two retention routes are the same for every certificate; the pinned verifier and
    the card exist for the headline bound, and the self-contained third-party package for
    the rung below it, so those sentences go with the certificate they are about.
    """
    sweep, interval, gate = edition_file(VERIFIER), edition_file(INTERVAL), edition_file(GATE)
    routes = (
        "Beyond the verifier in this file, the repository decides these bytes twice more, by "
        "two routes that share no code with it. With each other they share the "
        "`Certificate` representation, the loader that fills it from the file, and "
        "Conditions 2 to 4, decided once in closed form; what differs is how each decides "
        f"Condition 5. The exact event-cell sweep in [`certificate.py`]({sweep}) does at "
        "every net direction what “Why the Sweep Is Exact” describes and reports the least "
        f"covered mass ${frac(facts.least_mass)}$ at direction $0$. The interval branch and "
        "bound in "
        f"[`interval.py`]({interval}) works with directed rounding on the doubled net, the "
        "net directions and their reflections across the diagonal, so it never invokes "
        "Condition 1 and covers every orientation directly. The retention gate, "
        f"[`decide_certificate.py`]({gate}), builds the one `Certificate` both routes read, "
        "and accepts it only when both do and the interval route\u2019s enclosure of the "
        "least covered mass has width zero and equals the sweep\u2019s value exactly; both "
        "accepted this one. Two algorithms over one loaded object "
        "are not two independent implementations, nor two independent readings of the "
        "file, and the second and third decisions are worth exactly that much. "
        "The gate decides only unconditional certificates: a file declaring a `variant` "
        "other than `unconditional` is refused before either route runs, as it is by the "
        "verifier in this file, and these bytes declare none."
    )
    identity = (
        f"The certificate embedded below is the file `{facts.source.name}`, whose SHA-256 "
        f"is `{sha256_of(facts.source)}`."
    )
    if facts is headline:
        beside = (
            f"[`{PINNED_VERIFIER.name}`]({edition_file(PINNED_VERIFIER)}), beside this file in "
            "the repository, is another standard-library check, pinned to exactly these bytes "
            f"by that digest; [`{CARD.name}`]({edition_file(CARD)}) states the claim on one "
            f"page, and [`{FIGURE.name}`]({edition_file(FIGURE)}) draws the atoms, the tight "
            "Condition 5 witness and the shrink step."
        )
    else:
        beside = (
            f"The self-contained package under [`thirdparty/`]({edition_file(THIRDPARTY)}) "
            "decides this rung with nothing outside the standard library, and rebuilds "
            "Massaccesi\u2019s $n = 17$ certificate as a known-answer control beside it."
        )
    return f"{routes}\n\n{identity}\n\n{beside}"


def render_claim(facts: Facts, sibling: Facts, headline: Facts) -> str:
    """One document: the template filled with this certificate, its verifier and its file.

    The template names the least covered mass at direction 0; `derive` has already
    refused a certificate whose declared least is not the upright direction's, so what
    arrives here is described rightly. It also says that no direction's admissible
    centers degenerate to a point or to nothing, which holds because B < 1 (Condition 4,
    re-decided by `derive`) and L > 2, the one bound checked here.
    """
    if facts.outer_side <= 2:
        raise SystemExit(
            f"{facts.source.name}: L = {facts.outer_side} is not above 2, and the template "
            "says every direction admits a square of centers with interior"
        )
    values = {
        **perturbations(facts),
        "FILE_NAME": claim_path(facts).name,
        "CERT_NAME": facts.source.name,
        "CERT_URL": edition_file(facts.source),
        "L_FRAC": frac(facts.outer_side),
        "L_DEC": decimal(facts.outer_side),
        "N_ATOMS": str(len(facts.atoms)),
        "N_DIRECTIONS": str(facts.steps + 1),
        "LEAST_FRAC": frac(facts.least_mass),
        "WITNESS_CENTER": f"({frac(facts.witness[0])}, {frac(facts.witness[1])})",
        "RUNTIME": runtime_phrase(facts),
        "STANDING": standing(facts, headline),
        "DECIDED_HERE": decided_here(facts, headline),
        "OTHER_FILE_NAME": claim_path(sibling).name,
        "OTHER_CLAIM_URL": edition_file(claim_path(sibling)),
        "OTHER_L_FRAC": frac(sibling.outer_side),
        "VERIFIER_NAME": VERIFIER_CLAIM.name,
        "VERIFIER_URL": edition_file(VERIFIER_CLAIM),
        "VERIFIER_SOURCE": VERIFIER_CLAIM.read_text(encoding="utf-8").rstrip("\n"),
        "CERTIFICATE_JSON": facts.source.read_text(encoding="utf-8").rstrip("\n"),
        "BEST_PACKING_TEX": bound_substitutions()["BEST_PACKING_TEX"],
    }
    # The banner is prepended here rather than written in the template, so the
    # template itself is not mistaken for a generated view.
    banner = (
        f"<!-- GENERATED by devtools.render_verifiable_claim from "
        f"devtools/templates/{TEMPLATE.name}, {VERIFIER_CLAIM.name} and "
        f"{facts.source.name}. Edit those, then regenerate. -->\n\n"
    )
    return banner + filled(TEMPLATE, values)


def register_entry(result_id: str) -> dict[str, object]:
    """The result's row in the register: the card repeats its standing, never sets it."""
    for entry in safe_load(RESULTS.read_text(encoding="utf-8"))["results"]:
        if entry["id"] == result_id:
            return entry
    raise SystemExit(f"{RESULTS.name} has no result {result_id}")


def render_card(facts: Facts) -> str:
    """The proof card: the headline bound on one page, every figure from the certificate.

    The cell count and the pinned verifier's timing are the two figures the certificate
    does not carry; the count is recorded above with its provenance, and the timing is
    stated in the template as the measurement it is.
    """
    cells = REACHABLE_CELLS.get(slug(facts))
    if cells is None:
        raise SystemExit(
            f"{facts.source.name}: no recorded event-cell count; the card needs one"
        )
    entry = register_entry(RESULT_ID)
    review = REPO / str(entry.get("review_artifact", ""))
    if not entry.get("review_artifact") or not review.is_file():
        raise SystemExit(
            f"{RESULTS.name}: {RESULT_ID} names no review artifact on disk; the card "
            "states the rung beside the review it rests on"
        )
    containment = facts.square_side * (1 + facts.half_gap)
    limit = facts.angle_limit
    values = {
        "L_FRAC": frac(facts.outer_side),
        "L_DEC": decimal(facts.outer_side),
        "N_ATOMS": str(len(facts.atoms)),
        "TOTAL_FRAC": frac(facts.total_mass),
        "TOTAL_DEC": decimal(facts.total_mass),
        "B_FRAC": frac(facts.square_side),
        "B_DEC": decimal(facts.square_side),
        "N_DIRECTIONS": str(facts.steps + 1),
        "N_DIRECTIONS_MAX": str(facts.steps),
        "LIMIT_FRAC": frac(limit),
        "ARC_SLACK_FRAC": frac(limit * limit + 2 * limit - 1),
        "D_FRAC": frac(facts.half_gap),
        "D_APPROX": digits(facts.half_gap, HALF_GAP_PLACES),
        "CONTAINMENT_FRAC": frac(containment),
        "CONTAINMENT_APPROX": digits(containment, CONTAINMENT_PLACES),
        "LEAST_FRAC": frac(facts.least_mass),
        "LEAST_DEC": decimal(facts.least_mass),
        "CELLS": str(cells),
        "CERT_NAME": facts.source.name,
        "CERT_PATH": facts.source.resolve().relative_to(REPO).as_posix(),
        "CERT_URL": edition_file(facts.source),
        "DIGEST_PREFIX": sha256_of(facts.source)[:DIGEST_PREFIX_CHARS],
        "CLAIM_NAME": claim_path(facts).name,
        "CONFIRMATION": str(entry["confirmation"]),
        "REVIEW_ARTIFACT": relative_link(review, CARD),
        "NOVELTY": str(entry["novelty"]),
    }
    banner = (
        f"<!-- GENERATED by devtools.render_verifiable_claim from "
        f"devtools/templates/{CARD_TEMPLATE.name}, {facts.source.name} and "
        f"frontier/{RESULTS.name}. Edit those, then regenerate. -->\n\n"
    )
    return banner + filled(CARD_TEMPLATE, values)


def filled(template: Path, values: dict[str, str]) -> str:
    """The template with every placeholder substituted, refusing one a value carried in."""
    text = fill(template.read_text(encoding="utf-8"), values, where=template.name)
    left = {m.group(1) for m in re.finditer(r"\{\{([A-Z_]+)\}\}", text)}
    if left:
        raise SystemExit(f"{template.name}: a substituted value carried {sorted(left)} into it")
    return text


def documents() -> list[tuple[Path, str]]:
    """Every generated document with its fresh text: both claims, then the card."""
    facts = [derive(path) for path in WALKTHROUGH]
    if len(facts) != 2:
        raise SystemExit("each document names its one sibling; the walkthrough has to be two")
    headline = max(facts, key=lambda f: f.outer_side)
    claims = [
        (claim_path(f), render_claim(f, sibling, headline))
        for f, sibling in ((facts[0], facts[1]), (facts[1], facts[0]))
    ]
    return [*claims, (CARD, render_card(headline))]


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="exit non-zero if a committed document differs from a fresh render",
    )
    args = parser.parse_args(argv)

    stale = []
    for path, text in documents():
        if args.check:
            if not path.is_file() or path.read_bytes() != text.encode("utf-8"):
                stale.append(path)
            continue
        with atomic_output_file(path) as temporary:
            temporary.write_text(text, encoding="utf-8")
        print(f"wrote {path.relative_to(REPO)} ({len(text) / 1024:.0f} KB)")
    for path in stale:
        print(f"{path.relative_to(REPO)} is stale; rerender it", file=sys.stderr)
    if stale:
        return 1
    if args.check:
        print("the verifiable-claim documents and the proof card are current")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
