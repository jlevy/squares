"""Write the verifiable-claim documents and the proof card from the certificates.

Each claim document is one self-contained file per certificate: the claim, the theorem
and its proof, the finite form of Condition 5, how this repository decided the bytes, the
standard-library verifier `verify_claim.py` byte for byte, and the certificate it
decides, byte for byte as well, so a reader can paste that one file into a coding agent
or check it by hand without the rest of the repository. Both come from one template, so
the shared text cannot drift between them. The same renderer writes separate threshold
claim documents for T-025 and T-026 from one threshold template and one standard-library
verifier. The proof card states the T-018 bound on one page, from the same certificate
and the register, so its figures cannot drift from either. `--check` refuses a stale
copy; the test suite runs that check.

Run from `packing/`:

    uv run --frozen --group dev python -m devtools.render_verifiable_claim [--check]
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
from collections.abc import Sequence
from fractions import Fraction
from pathlib import Path
from typing import TypedDict, cast

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
THRESHOLD_TEMPLATE = TEMPLATES / "threshold_verifiable_claim.md"
CARD_TEMPLATE = TEMPLATES / "proof_card.md"
CARD = CASE / "t-018-proof-card.md"
RESULTS = PACKING / "frontier" / "results.yaml"
RESULT_ID = "T-018"
INTERVAL = PACKING / "src" / "sqpack" / "fractional" / "interval.py"
GATE = PACKING / "devtools" / "decide_certificate.py"
PINNED_VERIFIER = CASE / "minimal_verify.py"
FIGURE = CASE / "t-018-proof-visual.svg"
THRESHOLD_CASE = PACKING / "cases" / "n11_threshold_certificate"
THRESHOLD_VERIFIER = THRESHOLD_CASE / "verify_claim.py"
T025_CERTIFICATE = THRESHOLD_CASE / "certificate.json"
T026_CERTIFICATE = THRESHOLD_CASE / "certificate-191-50-net1440.json"
T026_LIMIT = THRESHOLD_CASE / "t-026-dilation-limit-corollary.json"
T025_CLAIM = THRESHOLD_CASE / "t-025-verifiable-claim-191-50.md"
T026_CLAIM = THRESHOLD_CASE / "t-026-verifiable-claim-dilation-limit.md"
T025_MINIMUM = Fraction("100000203/100000000")


class ThresholdFacts(TypedDict):
    """Typed values rendered from one retained threshold certificate."""

    n: int
    L: Fraction
    B: Fraction
    K: int
    D: Fraction
    point_atoms: int
    threshold_atoms: int
    point_mass: Fraction
    threshold_budget: Fraction
    total_budget: Fraction


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
    """Compare the two packaged certificate rungs, not the full result register."""
    if facts is headline:
        return "It is the tighter of the two certificate rungs packaged here."
    return "It is the looser of the two certificate rungs packaged here, with simpler numbers."


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
        "VERIFIER_URL": relative_link(VERIFIER_CLAIM, claim_path(facts)),
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
    stated in the template as the measurement it is. The claim verifier's time beside it
    comes from the table the claim document reads, so the card names both programs.
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
        "CLAIM_RUNTIME": runtime_phrase(facts),
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


def _record(path: Path) -> dict[str, object]:
    """One generated-claim input, parsed as JSON after its exact bytes stay available."""
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise SystemExit(f"{path.name}: expected one JSON object")
    return value


def _as_fraction(record: dict[str, object], name: str) -> Fraction:
    value = record[name]
    if not isinstance(value, str):
        raise SystemExit(f"{name} in the threshold certificate is not a rational string")
    return Fraction(value)


def _threshold_identity(path: Path) -> tuple[str, int]:
    raw = path.read_bytes()
    return hashlib.sha256(raw).hexdigest(), len(raw)


def _threshold_facts(certificate: dict[str, object]) -> ThresholdFacts:
    atoms = certificate["atoms"]
    threshold_atoms = certificate["threshold_atoms"]
    if not isinstance(atoms, list) or not isinstance(threshold_atoms, list):
        raise SystemExit("threshold certificate atom families must be arrays")
    if any(
        isinstance(atom, dict)
        and any(key in atom for key in ("variant", "multiplicities", "weighted_points"))
        for atom in threshold_atoms
    ):
        raise SystemExit("weighted threshold publication has not been admitted")
    steps = certificate["direction_steps"]
    if not isinstance(steps, int):
        raise SystemExit("threshold certificate direction_steps must be an integer")
    angle_limit = _as_fraction(certificate, "angle_limit")
    n = certificate["n"]
    if not isinstance(n, int) or isinstance(n, bool):
        raise SystemExit("threshold certificate n must be an integer")
    return {
        "n": n,
        "L": _as_fraction(certificate, "outer_side"),
        "B": _as_fraction(certificate, "square_side"),
        "K": steps,
        "D": angle_limit / steps,
        "point_atoms": len(atoms),
        "threshold_atoms": len(threshold_atoms),
        "point_mass": _as_fraction(certificate, "point_mass"),
        "threshold_budget": _as_fraction(certificate, "threshold_budget"),
        "total_budget": _as_fraction(certificate, "total_budget"),
    }


def _threshold_certificate_facts(
    facts: ThresholdFacts, *, minimum: Fraction, index: int
) -> str:
    side = facts["B"]
    gap = facts["D"]
    return f"""The embedded certificate has {facts["point_atoms"]} point atoms and
{facts["threshold_atoms"]} threshold atoms; every threshold atom is two-of-three. Its
container side is $L={facts["L"]}$, its core side is $B={side}$, and its net has
${int(facts["K"]) + 1}$ directions. The largest half-gap tangent is $D={gap}$, with

$$
B(1+D)={side * (1 + gap)}<1.
$$

The point mass is ${facts["point_mass"]}$, the threshold budget is
${facts["threshold_budget"]}$, and the total budget is
${facts["total_budget"]}<11$. The exact sweep finds minimum charge ${minimum}$ at
its first minimizing direction, index ${index}$. The verifier recomputes every displayed
mathematical value and reports that first minimizing direction."""


def _threshold_evidence(proof: Path, review: Path, certificate: Path) -> str:
    gate = PACKING / "devtools" / "decide_threshold_certificate.py"
    exact = PACKING / "src" / "sqpack" / "fractional" / "threshold.py"
    interval = PACKING / "src" / "sqpack" / "fractional" / "threshold_interval.py"
    return f"""The repository's [`{proof.name}`]({edition_file(proof)}) states the retained
proof and measurements. [`{review.name}`]({edition_file(review)}) reviews the theorem's
disjoint-trace budget, symmetry, net endpoint, event-cell boundaries, and
inclusion-exclusion reduction. The retention gate
[`{gate.name}`]({edition_file(gate)}) reads [`{certificate.name}`]({edition_file(certificate)})
once and requires agreement between the exact sweep in
[`threshold.py`]({edition_file(exact)}) and the directed-rounding interval decision in
[`threshold_interval.py`]({edition_file(interval)})."""


def render_threshold_claim(
    path: Path, certificate_path: Path, *, limit_path: Path | None
) -> str:
    certificate = _record(certificate_path)
    facts = _threshold_facts(certificate)
    cert_digest, cert_bytes = _threshold_identity(certificate_path)
    verifier_digest = sha256_of(THRESHOLD_VERIFIER)
    if limit_path is None:
        minimum, index = T025_MINIMUM, 69
        title = "T-025 Verifiable Claim: $s(11) \\geq 191/50$"
        opening = """The embedded threshold certificate directly proves

$$
s(11) \\geq \\frac{191}{50}=3.82.
$$

The certificate is instantiated at side $191/50$; this conclusion uses no limiting
argument."""
        derivation = """All five finite conditions hold for these bytes. Applying the
finite certificate theorem with $n=11$ and $L=191/50$ gives the displayed lower bound
directly."""
        proof = THRESHOLD_CASE / "t-025-threshold-certificate-proof.md"
        review = (
            REPO / "docs/project/reviews/review-2026-09-09-threshold-certificate-theorem.md"
        )
        evidence = _threshold_evidence(proof, review, certificate_path)
        scope = (
            "The registered headline records $s(11) \\geq 191/50$. Since the minimum is "
            "attained and this certificate excludes feasibility at $191/50$, the "
            "elementary compactness corollary is $s(11)>191/50$; it requires no "
            "additional computation. This claim does not bound the side from above or "
            "decide any different atom family, shrink, or direction net."
        )
        limit_sentence = "It has no separate limit record."
        limit_decision = ""
        limit_identity = ""
        limit_block = ""
    else:
        minimum, index = Fraction(1), 914
        limit = _record(limit_path)
        conclusion_value = limit["conclusion"]
        family_value = limit["strict_dilation_family"]
        sharpened_value = limit["sharpened_containment"]
        if not all(
            isinstance(value, dict)
            for value in (conclusion_value, family_value, sharpened_value)
        ):
            raise SystemExit(f"{limit_path.name}: malformed dilation sections")
        conclusion = cast(dict[str, object], conclusion_value)
        family = cast(dict[str, object], family_value)
        polynomial = str(conclusion["bounded_side_defining_polynomial"]).replace("*", r"\,")
        title = "T-026 Verifiable Claim: the Exact Dilation-Limit Bound"
        opening = r"""The embedded 1440-step threshold certificate and dilation record prove

$$
s(11) \geq C=
\frac{955000\sqrt{518400042893309449}}{179696714646249}
=3.8264474\ldots.
$$

This is an ordinary exact lower bound on $s(11)$."""
        derivation = rf"""The embedded certificate first satisfies all five conditions at
side $191/50$ from its own atoms and 1440-step sweep. Thus this document establishes
that source fact directly, without invoking T-025 as a theorem.

Now multiply the container side, core side, every point-atom coordinate, and every point
in every threshold atom by a positive rational $q$. Leave weights, thresholds, and the
direction net fixed. Inverse dilation preserves every point-membership trace, hence
every core charge and the total budget. Write $t=\tan d$ for the angular mismatch. If
$0\leq t\leq D<1$, then

$$
(1+D)^2(1+t^2)-(1+t)^2(1+D^2)=2(D-t)(1-Dt)\geq0.
$$

Together with $\cos d+\sin d=(1+t)/\sqrt{{1+t^2}}$, this gives strict core containment
whenever

$$
q^2B^2(1+D)^2<1+D^2.
$$

Define the positive numbers

$$
c=\frac{{\sqrt{{1+D^2}}}}{{B(1+D)}},\qquad C=\frac{{191}}{{50}}c.
$$

The record gives $B={facts["B"]}$ and $D={facts["D"]}$. The verifier re-derives

$$
c^2={family["factor_supremum_squared"]},\qquad
C^2={conclusion["bounded_side_squared"]},
$$

and checks that the displayed $C$ is the positive root of

$$
{polynomial}=0.
$$

Every positive rational $q<c$ satisfies the sharpened inequality. Using it in place of
the coarse Condition 4, the same core-selection and counting proof yields a finite
threshold certificate ruling out side $q(191/50)$. For any real $x<C$, rational density supplies
$x/(191/50)<q<c$. A packing at side $x$ would embed in the larger container of side
$q(191/50)$, contradicting that certificate. Hence no side below $C$ admits a packing,
so the infimum definition gives $s(11)\geq C$. At $q=c$ the uniform containment test
is an equality. The proof establishes the displayed `>=` theorem through the strict
rational family; it does not assert a certificate at the endpoint or a strict `>`
bound."""
        proof = THRESHOLD_CASE / "t-026-dilation-limit-proof.md"
        review = (
            REPO / "docs/project/reviews/review-2026-09-09-threshold-certificate-theorem.md"
        )
        evidence = _threshold_evidence(proof, review, certificate_path)
        corollary = PACKING / "devtools" / "dilation_corollary.py"
        dilation_review = REPO / "docs/project/reviews/review-2026-09-06-t022-dilation-limit.md"
        evidence += (
            f" The [`dilation_corollary.py`]({edition_file(corollary)}) replay checks the "
            "source declarations and re-derives the exact limit record. "
            f"[`{dilation_review.name}`]({edition_file(dilation_review)}) reviews the "
            "sharpened containment, density, and upward-embedding argument."
        )
        scope = (
            "The source sweep was measured at about 782 seconds on two workers, and the "
            "interval confirmation at about 154 seconds. They are exhaustive checks, "
            "outside the pull-request fast tier. This decision does not cover another "
            "atom family or direction net."
        )
        limit_digest, limit_bytes = _threshold_identity(limit_path)
        limit_sentence = "It also embeds the exact dilation-limit record."
        limit_decision = "It then re-derives the algebraic limit before accepting T-026."
        limit_identity = f"Limit Record SHA-256: `{limit_digest}`; bytes: `{limit_bytes}`."
        limit_block = f"""## Dilation Limit Record

The marked block is byte-for-byte [`{limit_path.name}`]({edition_file(limit_path)}).

<!-- BEGIN DILATION LIMIT RECORD -->
```json
{limit_path.read_text(encoding="utf-8").rstrip()}
```
<!-- END DILATION LIMIT RECORD -->"""

    values = {
        "TITLE": title,
        "OPENING_CLAIM": opening,
        "LIMIT_INPUT_SENTENCE": limit_sentence,
        "FILE_NAME": path.name,
        "LIMIT_DECISION_SENTENCE": limit_decision,
        "CERT_SHA256": cert_digest,
        "CERT_BYTES": str(cert_bytes),
        "LIMIT_IDENTITY_LINE": limit_identity,
        "CERTIFICATE_FACTS": _threshold_certificate_facts(facts, minimum=minimum, index=index),
        "CLAIM_DERIVATION": derivation,
        "EVIDENCE": evidence,
        "SCOPE": scope,
        "VERIFIER_URL": relative_link(THRESHOLD_VERIFIER, path),
        "VERIFIER_SHA256": verifier_digest,
        "VERIFIER_SOURCE": THRESHOLD_VERIFIER.read_text(encoding="utf-8").rstrip(),
        "CERT_NAME": certificate_path.name,
        "CERT_URL": edition_file(certificate_path),
        "CERTIFICATE_JSON": certificate_path.read_text(encoding="utf-8").rstrip(),
        "LIMIT_RECORD_BLOCK": limit_block,
    }
    sources = f"{THRESHOLD_TEMPLATE.name}, {THRESHOLD_VERIFIER.name}, {certificate_path.name}"
    if limit_path is not None:
        sources += f", and {limit_path.name}"
    banner = (
        "<!-- GENERATED by devtools.render_verifiable_claim from "
        f"devtools/templates/{sources}. Edit those, then regenerate. -->\n\n"
    )
    return banner + filled(THRESHOLD_TEMPLATE, values)


def documents() -> list[tuple[Path, str]]:
    """Every generated document with its fresh text: four claims, then the card."""
    facts = [derive(path) for path in WALKTHROUGH]
    if len(facts) != 2:
        raise SystemExit("each document names its one sibling; the walkthrough has to be two")
    headline = max(facts, key=lambda f: f.outer_side)
    claims = [
        (claim_path(f), render_claim(f, sibling, headline))
        for f, sibling in ((facts[0], facts[1]), (facts[1], facts[0]))
    ]
    threshold_claims = [
        (T025_CLAIM, render_threshold_claim(T025_CLAIM, T025_CERTIFICATE, limit_path=None)),
        (
            T026_CLAIM,
            render_threshold_claim(T026_CLAIM, T026_CERTIFICATE, limit_path=T026_LIMIT),
        ),
    ]
    return [*claims, *threshold_claims, (CARD, render_card(headline))]


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
