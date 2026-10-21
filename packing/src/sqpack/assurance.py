"""Cross-record assurance rules that JSON Schema cannot express."""

from __future__ import annotations

import re
from collections.abc import Callable, Mapping, Sequence
from decimal import Decimal, InvalidOperation

NUMERICAL_METHODS = frozenset({"numerical-f64", "numerical-multiprecision"})
MACHINE_FORMAL_METHODS = frozenset(
    {"interval-certified", "exact-algebraic", "proof-assistant-checked"}
)
PROOF_METHODS = frozenset({"published-proof", "proof-audited"})

EXTERNAL_ORIGINS = frozenset({"external", "independently-external"})
"""Origins where the argument was made elsewhere, so reading it is a separate act."""
FORMAL_METHODS = MACHINE_FORMAL_METHODS | PROOF_METHODS
FORMAL_ORIGINS = frozenset(
    {"external", "independently-external", "replayed-here", "audited-here"}
)
DATE_PREFIX = re.compile(r"^\d{4}-\d{2}-\d{2}:\s+\S")


def _string_list(value: object) -> list[str]:
    if not isinstance(value, list):
        return []
    return [item for item in value if isinstance(item, str)]


def _dated_annotation(value: object) -> bool:
    return isinstance(value, str) and DATE_PREFIX.match(value) is not None


def _precision_is_recorded(value: object) -> bool:
    if not isinstance(value, Mapping):
        return False
    has_amount = isinstance(value.get("decimal_digits"), int) or isinstance(
        value.get("binary_bits"), int
    )
    return has_amount and isinstance(value.get("rounding"), str)


def _scope_contains(scope: object, n: int) -> bool:
    if not isinstance(scope, Mapping):
        return False
    values = scope.get("n_values")
    if isinstance(values, list):
        return n in values
    lower = scope.get("n_min")
    upper = scope.get("n_max")
    return isinstance(lower, int) and isinstance(upper, int) and lower <= n <= upper


#: The origins of execution beyond the producer, eligible for confirmation.
DISCHARGING_ORIGINS = frozenset({"replayed-here", "audited-here", "independently-external"})
#: Origins of a run made here, by this repository.
HERE_ORIGINS = frozenset({"replayed-here", "audited-here"})


def sampled(entry: Mapping[str, object]) -> bool:
    """Samples and malformed coverage cannot establish a whole claim."""
    raw = entry.get("independence")
    if "independence" in entry and not isinstance(raw, Mapping):
        return True
    if not isinstance(raw, Mapping) or "coverage" not in raw:
        return False
    coverage = raw["coverage"]
    return not isinstance(coverage, Mapping) or coverage.get("extent") != "full"


#: The actor each origin names: the producer's run is external, a retained third-party
#: run is independently-external, and a run here names the repository.
ORIGIN_ACTORS: Mapping[str, str] = {
    "external": "source-author",
    "independently-external": "independent-external",
    "replayed-here": "repository",
    "audited-here": "repository",
}


def formal_actor_origin_problems(evidence: Mapping[str, object]) -> list[str]:
    """A formal execution's actor must agree with its displayed origin.

    A proof-assistant build here is `replayed-here`. `audited-here` is refused for one:
    reading another party's build receipt is that entry's `external_review`, not a run
    here, and the label would otherwise let a receipt audit pass as a build here.
    """
    if evidence.get("method") != "proof-assistant-checked":
        return []
    if evidence.get("origin") == "audited-here":
        return [
            (
                "a proof-assistant build here is replayed-here; an audit of another "
                "party's build is a read on that build's own entry, not audited-here"
            )
        ]
    expected = ORIGIN_ACTORS.get(str(evidence.get("origin")))
    if expected is None or evidence.get("performed_by") != expected:
        return ["formal execution actor performed_by must agree with its origin"]
    return []


def confirming_execution(evidence: Mapping[str, object]) -> bool:
    """Execution beyond the producer, by the actor its origin names, for every method.

    An origin label cannot turn the producer's execution into confirmation, and a run
    whose actor is unidentified or disagrees with its origin confirms nothing.
    """
    origin = evidence.get("origin")
    return (
        isinstance(origin, str)
        and origin in DISCHARGING_ORIGINS
        and evidence.get("performed_by") == ORIGIN_ACTORS[origin]
    )


def verified_here(evidence: Mapping[str, object]) -> bool:
    """Whether verified evidence can carry a case's verified lane.

    A machine method's run counts only when this repository ran it, by the actor its
    origin names, and a formal build only as admitted. The producer's own build can
    earn V for the result it reports (epistemics.md, Reported Formal Proofs and Source
    Builds), and a third party's retained replay can confirm it, but "for a result by
    others, that is a complete replay here and a review of its mathematics"
    (frontier/README.md; epistemics.md's *Integrated* end point). Published and audited
    proofs are read, not run, and keep their own rules.
    """
    return evidence.get("method") not in MACHINE_FORMAL_METHODS or (
        confirming_execution(evidence)
        and evidence.get("origin") in HERE_ORIGINS
        and not external_formal_build_problems(evidence)
    )


#: The hypothesis a malformed `proof.conditional_on` stands for: one nothing discharges.
MALFORMED_PREMISE = "an unreadable proof.conditional_on"


def conditions(evidence: Mapping[str, object]) -> list[tuple[str, list[str]]]:
    """The hypotheses a proved theorem takes and does not prove (`proof.conditional_on`),
    each with the entries recorded as discharging it, in record order.

    Fails closed: a present `conditional_on` that is not a list, and each item that is
    not a mapping, is one hypothesis nothing discharges, so a malformed record never
    reads as unconditional. The schema refuses those shapes as well.
    """
    proof = evidence.get("proof")
    if not isinstance(proof, Mapping) or "conditional_on" not in proof:
        return []
    items = proof.get("conditional_on")
    if not isinstance(items, list):
        return [(MALFORMED_PREMISE, [])]
    return [
        (str(item.get("hypothesis")), _string_list(item.get("discharged_by")))
        if isinstance(item, Mapping)
        else (MALFORMED_PREMISE, [])
        for item in items
    ]


def discharges(evidence: Mapping[str, object] | None, *, confirming: bool = True) -> bool:
    """A complete machine execution can discharge a premise on the selected axis.

    Confirmation requires execution beyond the producer. Verification also accepts the
    producer's own formal build once it is admitted (`external_formal_build_problems`);
    a producer's exact or interval run has no admission rule and discharges nothing.
    Only machine executions discharge: a published or audited proof of a premise is
    read, not run (epistemics.md, Reported Formal Proofs and Source Builds). This checks
    one run, not its own premise closure.
    """
    return (
        evidence is not None
        and evidence.get("assurance") == "verified"
        and evidence.get("method") in MACHINE_FORMAL_METHODS
        and bool(evidence.get("certificate"))
        and bool(evidence.get("replay"))
        and evidence.get("replay_status") == "passed"
        and not sampled(evidence)
        and not external_formal_build_problems(evidence)
        and (
            confirming_execution(evidence)
            or (not confirming and formal_run_elsewhere(evidence))
        )
    )


#: Support already settled for an entry object within one closure, keyed by identity.
_Memo = dict[int, int]


def _hypothesis_support(
    evidence: Mapping[str, object],
    refs: list[str],
    evidence_by_id: Mapping[str, Mapping[str, object]],
    level: Callable[[Mapping[str, object]], int],
    *,
    confirming: bool,
    active: frozenset[str],
    memo: _Memo,
) -> tuple[int, bool]:
    """The strongest discharge of one hypothesis, and whether a cycle was cut below it."""
    best, cut = 0, False
    for ref in refs:
        other = evidence_by_id.get(ref)
        if (
            other is None
            or not discharges(other, confirming=confirming)
            or not _scope_covers(other.get("scope"), evidence.get("scope"))
        ):
            continue
        value, hit = _support(
            other, evidence_by_id, level, confirming=confirming, active=active, memo=memo
        )
        best, cut = max(best, value), cut or hit
    return best, cut


def _support(
    evidence: Mapping[str, object],
    evidence_by_id: Mapping[str, Mapping[str, object]],
    level: Callable[[Mapping[str, object]], int],
    *,
    confirming: bool,
    active: frozenset[str],
    memo: _Memo,
) -> tuple[int, bool]:
    """`claim_support_level`, with whether the answer depended on a cycle cut.

    An answer reached without cutting a cycle is the same from every path: if an entry
    on another path to it were reachable below it, that path and this subtree would form
    a cycle through it, which this evaluation would have cut. Such answers are
    memoized, so a shared sub-chain is settled once per closure.
    """
    key = str(evidence.get("id", ""))
    if key in active:
        return 0, True
    if (known := memo.get(id(evidence))) is not None:
        return known, False
    active = active | {key}
    result, cut = level(evidence), False
    for _, refs in conditions(evidence):
        value, hit = _hypothesis_support(
            evidence,
            refs,
            evidence_by_id,
            level,
            confirming=confirming,
            active=active,
            memo=memo,
        )
        result, cut = min(result, value), cut or hit
    if not cut:
        memo[id(evidence)] = result
    return result, cut


def claim_support_level(
    evidence: Mapping[str, object],
    evidence_by_id: Mapping[str, Mapping[str, object]],
    level: Callable[[Mapping[str, object]], int],
    *,
    confirming: bool,
    active: frozenset[str] = frozenset(),
) -> int:
    """The weakest support in an acyclic proof chain, using only supplied evidence.

    Each hypothesis needs one complete, scope-covering discharge. Alternative proofs
    take their maximum; serial premises take their minimum. The caller supplies the
    axis's rung for each atom, so an exact premise cannot silently earn formal rung 5.
    """
    return _support(
        evidence, evidence_by_id, level, confirming=confirming, active=active, memo={}
    )[0]


def undischarged(
    evidence: Mapping[str, object],
    evidence_by_id: Mapping[str, Mapping[str, object]],
    *,
    confirming: bool = True,
) -> list[str]:
    """The hypotheses of a conditional theorem that no recorded entry discharges: the
    entry is verified as an implication only, and nothing here has decided its premise."""
    memo: _Memo = {}
    return [
        hypothesis
        for hypothesis, refs in conditions(evidence)
        if not _hypothesis_support(
            evidence,
            refs,
            evidence_by_id,
            lambda _: 1,
            confirming=confirming,
            active=frozenset({str(evidence.get("id", ""))}),
            memo=memo,
        )[0]
    ]


def conditional_problems(evidence_by_id: Mapping[str, Mapping[str, object]]) -> list[str]:
    """What is wrong with the register's conditional theorems: a `discharged_by` entry
    that does not exist, does not discharge (`discharges`), or does not cover every case
    the theorem's entry covers."""
    errors: list[str] = []
    for evidence_id, evidence in evidence_by_id.items():
        for hypothesis, refs in conditions(evidence):
            if hypothesis == MALFORMED_PREMISE:
                errors.append(
                    f"{evidence_id}: proof.conditional_on is not a list of hypotheses"
                )
            for ref in refs:
                other = evidence_by_id.get(ref)
                if other is None:
                    errors.append(
                        f"{evidence_id}: {hypothesis} is discharged by unknown evidence {ref}"
                    )
                elif not discharges(other, confirming=False):
                    errors.append(
                        f"{evidence_id}: {hypothesis} is discharged by {ref}, which is not "
                        "a verified replay with a passing status and complete coverage"
                    )
                elif not _scope_covers(other.get("scope"), evidence.get("scope")):
                    errors.append(
                        f"{evidence_id}: {hypothesis} is discharged by {ref}, whose scope "
                        "does not cover this entry's"
                    )
                elif not claim_support_level(
                    other,
                    evidence_by_id,
                    lambda _: 1,
                    confirming=False,
                    active=frozenset({evidence_id}),
                ):
                    errors.append(
                        f"{evidence_id}: {hypothesis} is discharged by {ref}, whose "
                        "own premises are unresolved or circular"
                    )
    return errors


def _scope_covers(outer: object, inner: object) -> bool:
    if not isinstance(inner, Mapping):
        return False
    values = inner.get("n_values")
    if isinstance(values, list):
        return all(isinstance(n, int) and _scope_contains(outer, n) for n in values)
    lower, upper = inner.get("n_min"), inner.get("n_max")
    if not isinstance(lower, int) or not isinstance(upper, int):
        return False
    return all(_scope_contains(outer, n) for n in range(lower, upper + 1))


def formal_run_elsewhere(evidence: Mapping[str, object]) -> bool:
    """A proof-assistant execution this repository did not perform: the producer's own
    build, or a third party's build retained here. Its pass is known only from what it
    left behind, so both are held to the same retained-evidence rules; a stronger claim
    must not need less evidence than a weaker one. Only `replayed-here` is a build here
    (`formal_actor_origin_problems`)."""
    return evidence.get("method") == "proof-assistant-checked" and not (
        evidence.get("origin") == "replayed-here"
        and evidence.get("performed_by") == "repository"
    )


def external_formal_build_problems(evidence: Mapping[str, object]) -> list[str]:
    """Require inspected execution evidence before crediting a formal build run elsewhere.

    Source verification earns V independently of C. A credible announcement, a source
    tree or a partial build alone must not become a passing full-theorem execution, and
    a third party's build needs at least what the producer's does. Review owns receipt
    contents and statement fidelity; this checks their record.
    """
    if evidence.get("method") != "proof-assistant-checked":
        return []
    errors = formal_actor_origin_problems(evidence)
    if not formal_run_elsewhere(evidence):
        return errors
    errors.extend(
        f"a formal build run elsewhere requires retained {field}"
        for field in ("build_receipt", "axioms_receipt")
        if not evidence.get(field)
    )
    proof = evidence.get("proof")
    required = {"source", "theorem", "scope", "pinpoints", "assumptions", "audit_record"}
    if not isinstance(proof, Mapping) or not required.issubset(proof):
        errors.append("a formal build run elsewhere requires a scoped proof and audit_record")
    independence = evidence.get("independence")
    coverage = independence.get("coverage") if isinstance(independence, Mapping) else None
    if not isinstance(coverage, Mapping) or coverage.get("extent") != "full":
        errors.append("a formal build run elsewhere requires explicit full coverage")
    review = evidence.get("external_review")
    if (
        not isinstance(review, Mapping)
        or review.get("state") != "informally-verified"
        or not all(review.get(key) for key in ("date", "reviewed_by", "note"))
    ):
        errors.append(
            "a formal build run elsewhere requires a qualifying receipt and statement read"
        )
    if evidence.get("replay_status") != "passed":
        errors.append("a formal build run elsewhere must record its passing execution")
    return errors


#: The fields that name one execution's own record: its build and its axiom report.
RECEIPT_FIELDS = ("build_receipt", "axioms_receipt")


def shared_receipt_problems(evidence_by_id: Mapping[str, Mapping[str, object]]) -> list[str]:
    """A receipt records one execution, so every entry citing it names one actor.

    A confirming entry that carries the producer's `build_receipt` or `axioms_receipt`
    is the producer's run under another label; refusing the shared receipt keeps
    relabelling from turning the source's execution into a third party's or this
    repository's. A path is one receipt whichever of the two fields names it.
    Certificates are not compared: a replay here re-runs the source's certificate.
    """
    actors: dict[str, dict[tuple[str, str], list[str]]] = {}
    for evidence_id, evidence in evidence_by_id.items():
        actor = (str(evidence.get("origin")), str(evidence.get("performed_by")))
        for field in RECEIPT_FIELDS:
            receipt = evidence.get(field)
            if isinstance(receipt, str) and receipt:
                cited = actors.setdefault(receipt, {}).setdefault(actor, [])
                cited.append(f"{evidence_id} ({field})")
    return [
        f"{receipt}: one receipt is cited by entries of different actors ("
        + "; ".join(
            f"{', '.join(ids)} as {origin}/{performer}"
            for (origin, performer), ids in sorted(by_actor.items())
        )
        + ")"
        for receipt, by_actor in sorted(actors.items())
        if len(by_actor) > 1
    ]


def check_evidence_semantics(evidence: Mapping[str, object]) -> list[str]:
    """Return assurance-method violations for one evidence record."""
    errors: list[str] = []
    evidence_id = evidence.get("id", "<unknown evidence>")
    prefix = f"{evidence_id}: "
    errors.extend(prefix + problem for problem in external_formal_build_problems(evidence))
    assurance = evidence.get("assurance")
    method = evidence.get("method")

    if method in NUMERICAL_METHODS:
        if assurance != "numerically-checked":
            errors.append(
                prefix + "numerical method cannot support verified or reported assurance"
            )
        precision = evidence.get("precision")
        tolerance = evidence.get("tolerance")
        historical = (
            precision == "unrecorded-historical" or tolerance == "unrecorded-historical"
        )
        if historical:
            if not _dated_annotation(evidence.get("migration_annotation")):
                errors.append(
                    prefix + "unrecorded historical values require a dated migration annotation"
                )
        else:
            if not _precision_is_recorded(precision):
                errors.append(
                    prefix + "numerical evidence requires actual precision and rounding"
                )
            if not isinstance(tolerance, str) or not tolerance:
                errors.append(prefix + "numerical evidence requires a tolerance")
    elif method in FORMAL_METHODS:
        if assurance != "verified":
            errors.append(prefix + "formal method requires verified assurance")
        if evidence.get("origin") not in FORMAL_ORIGINS:
            errors.append(prefix + "verified evidence requires a displayed verification origin")
        if method in MACHINE_FORMAL_METHODS and (
            not evidence.get("certificate") or not evidence.get("replay")
        ):
            errors.append(prefix + f"{method} requires certificate and replay")
        if method in PROOF_METHODS:
            proof = evidence.get("proof")
            required = {"source", "theorem", "scope", "pinpoints", "assumptions"}
            if not isinstance(proof, Mapping) or not required.issubset(proof):
                errors.append(prefix + f"{method} requires a complete scoped proof record")
            elif method == "proof-audited" and not proof.get("audit_record"):
                errors.append(prefix + "proof-audited requires an independent audit record")
        if evidence.get("precision") is not None or evidence.get("tolerance") is not None:
            errors.append(
                prefix + "formal evidence must not use precision or tolerance as assurance"
            )
        # An argument this repository did not produce carries `verified` on the source's
        # authority, which is legitimate -- a published proof proves its claim whether or
        # not we read it. What is not legitimate is leaving a reader unable to tell which
        # of our verified claims anyone here has actually worked through. Six records were
        # in that state, each saying "not independently audited here" in prose that nothing
        # could query and nothing enforced, while `[Stromquist 2003]`'s n = 11 argument had
        # already needed a source-distinct repair. So the state is now stated or refused.
        if method in PROOF_METHODS and evidence.get("origin") in EXTERNAL_ORIGINS:
            review = evidence.get("external_review")
            if not isinstance(review, Mapping) or not review.get("state"):
                errors.append(
                    prefix + "an external proof must declare external_review.state: "
                    "whether anyone here has read the argument"
                )

    elif assurance == "reported":
        if method is not None:
            errors.append(prefix + "reported evidence uses reported_method, not method")
        if not isinstance(evidence.get("reported_method"), str):
            errors.append(prefix + "reported evidence requires reported_method")
    else:
        errors.append(prefix + f"unsupported assurance-method pair: {assurance!r}, {method!r}")

    if assurance == "verified" and method not in FORMAL_METHODS:
        errors.append(prefix + "verified requires a formal method")

    # Each novelty value carries its own documentary burden, so the two that can be
    # checked are checked here: attributing a result needs the source named, and
    # claiming one is new needs the dated review the claim was assessed against.
    novelty = evidence.get("novelty")
    if novelty == "previously-published" and not evidence.get("source_key"):
        errors.append(prefix + "previously-published evidence must name its source_key")
    # The vocabulary defines this label as "a statement about the search performed, never
    # an assertion of priority" -- and a date is not a statement about a search. All four
    # original claims carried one and none said what was looked for, so the label meant
    # whatever a reader assumed. A search is also only as good as the corpus it ran over,
    # which is why the basis names the corpus and its holes rather than just the terms.
    if novelty == "apparently-novel" and not evidence.get("novelty_basis"):
        errors.append(
            "apparently-novel requires novelty_basis: the corpus searched and what for"
        )
    if novelty == "apparently-novel" and not evidence.get("source_reviewed"):
        errors.append(prefix + "apparently-novel evidence requires a dated source_reviewed")
    return errors


def _bound_identity(bound: object) -> str | None:
    if not isinstance(bound, Mapping):
        return None
    exact_form = bound.get("exact_form")
    value = bound.get("value")
    if isinstance(exact_form, str) and exact_form:
        return exact_form
    return value if isinstance(value, str) and value else None


def _literal_exact_decimal(value: object) -> Decimal | None:
    """Return an exact decimal identity when the form is itself a decimal literal."""
    if not isinstance(value, str):
        return None
    try:
        decimal_value = Decimal(value)
    except InvalidOperation:
        return None
    return decimal_value if decimal_value.is_finite() else None


def bounds_agree_at_declared_precision(left: object, right: object) -> bool:
    """Decide whether two bound records represent one value at the printed precision.

    Conflicting exact identities never agree. Printed decimals must also agree: a value
    that omits digits from the other lane is accepted within half a unit of its last
    declared place, or one unit when both lanes name the same exact form and a source
    truncated rather than rounded its display. Evidence identity alone cannot excuse
    numerical drift. This is a display relation, not an exactness claim.
    """
    if not isinstance(left, Mapping) or not isinstance(right, Mapping):
        return False
    left_exact = left.get("exact_form")
    right_exact = right.get("exact_form")
    if left_exact and right_exact and left_exact != right_exact:
        return False
    try:
        left_value = Decimal(str(left["value"]))
        right_value = Decimal(str(right["value"]))
    except InvalidOperation, KeyError:
        return False
    left_exponent = left_value.as_tuple().exponent
    right_exponent = right_value.as_tuple().exponent
    left_unit = Decimal(1).scaleb(left_exponent) if isinstance(left_exponent, int) else None
    right_unit = Decimal(1).scaleb(right_exponent) if isinstance(right_exponent, int) else None
    left_reference = _literal_exact_decimal(left_exact)
    right_reference = _literal_exact_decimal(right_exact)
    if (left_reference is not None and left_value != left_reference) or (
        right_reference is not None and right_value != right_reference
    ):
        agrees = False
    elif left_unit is None or right_unit is None:
        agrees = left_value == right_value
    elif left_reference is not None:
        agrees = abs(right_value - left_reference) <= right_unit / 2
    elif right_reference is not None:
        agrees = abs(left_value - right_reference) <= left_unit / 2
    elif left_value == right_value:
        agrees = True
    else:
        if left_exact and right_exact:
            tolerance = max(left_unit, right_unit)
        else:
            tolerance = (left_unit + right_unit) / 2
        agrees = abs(left_value - right_value) <= tolerance
    return agrees


def _check_bound_evidence(
    *,
    label: str,
    bound: object,
    evidence_by_id: Mapping[str, Mapping[str, object]],
    n: int,
    verified: bool,
) -> list[str]:
    errors: list[str] = []
    if not isinstance(bound, Mapping):
        return [f"{label}: bound is missing or malformed"]
    refs = _string_list(bound.get("evidence"))
    if not refs:
        return [f"{label}: bound has no evidence"]
    expected_claim = "upper-bound" if "upper" in label else "lower-bound"
    for ref in refs:
        evidence = evidence_by_id.get(ref)
        if evidence is None:
            errors.append(f"{label}: unknown evidence {ref}")
            continue
        if not _scope_contains(evidence.get("scope"), n):
            errors.append(f"{label}: evidence {ref} does not cover n={n}")
        if verified:
            if evidence.get("assurance") != "verified":
                errors.append(f"{label}: evidence {ref} is not verified")
            elif not verified_here(evidence):
                errors.append(
                    f"{label}: evidence {ref} is a machine run not made here; the verified "
                    "lane takes another party's machine result only through a complete "
                    "replay here"
                )
            if evidence.get("claim") not in {expected_claim, "exact-value"}:
                errors.append(
                    f"{label}: evidence {ref} has claim {evidence.get('claim')!r}, "
                    f"expected {expected_claim!r}"
                )
            # A conditional theorem verifies an implication, so a verified bound cites
            # it only beside the run that decides each of its hypotheses: the lane then
            # shows everything the bound rests on.
            errors.extend(
                f"{label}: evidence {ref} is conditional on {hypothesis}, and the bound "
                "cites nothing that discharges it"
                for hypothesis, discharged in conditions(evidence)
                if not set(discharged) & set(refs)
            )
    return errors


def _check_rigidity_claim(
    rigidity: Mapping[str, object],
    cited: Sequence[Mapping[str, object]],
) -> list[str]:
    """Hold a case's rigidity block to the contract its evidence records are held to.

    `check_evidence_semantics` enforces the assurance-method pairing on `evidence.yaml`,
    and until this existed the case-level `rigidity` block was the one place a first-party
    claim escaped it. The schema requires only `[property, assurance, scope, evidence]`,
    leaves `method`, `certificate` and `replay` optional and nullable, and couples none of
    them -- so a block could read `verified` / `exact-algebraic` with nothing behind it, or
    outrank the evidence it rests on, and validation passed.

    The last of those is the one that matters. `n = 65`'s block cites evidence that is
    `numerically-checked` at `tolerance: 1e-8`; relabelling the block `verified` was
    accepted, which is a formal claim resting on a numerical one in the flattering
    direction. See `D-396`.

    Certificate and replay are satisfied by the block or by a cited verified record,
    because both conventions are in use: `n = 5`, `11` and `40` name the artifacts on the
    block, while the ten perfect squares leave them null and delegate to
    `E-perfect-square-tiling-rigid`, which carries them. Neither is wrong; what was wrong
    was that nothing required either.
    """
    errors: list[str] = []
    assurance = rigidity.get("assurance")
    method = rigidity.get("method")

    if method in NUMERICAL_METHODS:
        if assurance != "numerically-checked":
            errors.append("numerical method cannot support verified or reported assurance")
    elif method in FORMAL_METHODS:
        if assurance != "verified":
            errors.append("formal method requires verified assurance")
    else:
        # The catch-all `check_evidence_semantics` has and this did not. Without it a block
        # reading `reported` with no method, or no assurance and no method, produced no
        # error at all -- every branch below is keyed on a value it does not have, so the
        # least-specified claim was the least checked. `reported` in particular can never
        # be backed here: the block has no `reported_method` field to carry it, and the
        # register's own rule is that what a source says about rigidity belongs in
        # `reported_upper_bound.catalogue_rigid` and must not be restated in this block.
        errors.append(f"unsupported assurance-method pair: {assurance!r}, {method!r}")

    if assurance == "verified":
        if method not in FORMAL_METHODS:
            errors.append("verified requires a formal method")
        # A verified claim must rest on verified evidence. Without this the block's own
        # label is the whole of the argument, which is what the contract exists to refuse.
        # A machine run not made here, the producer's or a third party's, is not backing
        # either, as in the verified bound lanes (`verified_here`).
        backing = [
            record
            for record in cited
            if record.get("assurance") == "verified" and verified_here(record)
        ]
        if not backing:
            errors.append(
                "verified rigidity requires at least one verified evidence record "
                "that is a proof or a machine run made here"
            )
        # ...and on evidence about rigidity. Verified alone let a rigidity claim rest on a
        # record of the right n proving something else entirely -- an upper bound, say --
        # which is backing in name only. `_check_bound_evidence` already constrains claim
        # for bounds; this is the same rule one block over.
        elif not any(record.get("claim") == "derived-structure" for record in backing):
            errors.append(
                "verified rigidity requires verified evidence claiming derived-structure, "
                f"not {sorted({str(record.get('claim')) for record in backing})}"
            )
        if method in MACHINE_FORMAL_METHODS:
            backed = rigidity.get("certificate") and rigidity.get("replay")
            # A delegated certificate and replay come from a run made here, as backing
            # does: the producer's own run cannot supply the block's machine method.
            delegated = any(
                record.get("assurance") == "verified"
                and record.get("certificate")
                and record.get("replay")
                and verified_here(record)
                for record in cited
            )
            if not backed and not delegated:
                errors.append(
                    f"{method} requires certificate and replay, "
                    "on the block or on a cited verified record made here"
                )

    return errors


def check_case_semantics(
    case: Mapping[str, object],
    evidence_by_id: Mapping[str, Mapping[str, object]],
) -> list[str]:
    """Return cross-field and cross-record violations for one frontier case."""
    errors: list[str] = []
    n_value = case.get("n")
    if not isinstance(n_value, int):
        return ["case n is missing or malformed"]

    for ref in _string_list(case.get("evidence")):
        evidence = evidence_by_id.get(ref)
        if evidence is None:
            errors.append(f"n={n_value}: unknown evidence {ref}")
        elif not _scope_contains(evidence.get("scope"), n_value):
            errors.append(f"n={n_value}: evidence {ref} does not cover this case")

    for label, verified in (
        ("reported_upper_bound", False),
        ("verified_upper_bound", True),
        ("reported_lower_bound", False),
        ("verified_lower_bound", True),
    ):
        errors.extend(
            _check_bound_evidence(
                label=f"n={n_value} {label}",
                bound=case.get(label),
                evidence_by_id=evidence_by_id,
                n=n_value,
                verified=verified,
            )
        )

    # rigidity carries evidence refs like every other first-party claim, and until
    # this check existed they were the one kind nothing resolved: a block could cite
    # an id that does not exist, or one whose scope does not reach this n, and pass.
    rigidity = case.get("rigidity")
    if isinstance(rigidity, Mapping):
        cited: list[Mapping[str, object]] = []
        for ref in _string_list(rigidity.get("evidence")):
            evidence = evidence_by_id.get(ref)
            if evidence is None:
                errors.append(f"n={n_value} rigidity: unknown evidence {ref}")
            elif not _scope_contains(evidence.get("scope"), n_value):
                errors.append(f"n={n_value} rigidity: evidence {ref} does not cover this case")
            else:
                cited.append(evidence)
        errors.extend(
            f"n={n_value} rigidity: {error}" for error in _check_rigidity_claim(rigidity, cited)
        )

    upper = _bound_identity(case.get("verified_upper_bound"))
    lower = _bound_identity(case.get("verified_lower_bound"))
    status = case.get("status")
    if status == "proved" and (upper is None or lower is None or upper != lower):
        errors.append(f"n={n_value}: proved requires matching verified upper and lower bounds")
    if status == "open" and upper is not None and upper == lower:
        errors.append(f"n={n_value}: matching verified bounds require status proved")

    reported_upper = case.get("reported_upper_bound")
    reported_upper_refs = (
        set(_string_list(reported_upper.get("evidence")))
        if isinstance(reported_upper, Mapping)
        else set()
    )
    blockers = case.get("blockers")
    blocker_records = blockers if isinstance(blockers, list) else []
    upper_gap_blockers = [
        blocker
        for blocker in blocker_records
        if isinstance(blocker, Mapping)
        and bool(reported_upper_refs & set(_string_list(blocker.get("evidence"))))
    ]
    verified_upper = case.get("verified_upper_bound")
    errors.extend(_conjecture_errors(n_value, case.get("conjectured_optimum"), verified_upper))
    same_upper = bounds_agree_at_declared_precision(reported_upper, verified_upper)
    if same_upper and upper_gap_blockers:
        errors.append(f"n={n_value}: stale formal-upper-gap blocker")
    if not same_upper and not upper_gap_blockers:
        errors.append(f"n={n_value}: formal upper trails report without a blocker")
    return errors


def _conjecture_errors(n: int, conjecture: object, upper: object) -> list[str]:
    """A conjectured optimum written as a decimal may not exceed the verified ceiling.

    The decimal is a display, so it is allowed half a unit of its last place above the
    ceiling, and no more: a record whose certified ceiling lies below the side it
    conjectures optimal contradicts itself. On 2026-10-05 n = 126 kept the catalogue's
    conjectured `11.77473513240654` after an exact certificate put its ceiling 1.9e-11
    below it (T-098, review finding EX-1). The check is one-sided: it compares the
    conjecture with the verified ceiling only, not with the verified floor, and a
    conjecture or a ceiling that is not a decimal, such as `integer`, is not compared.
    """
    if not isinstance(conjecture, str) or not isinstance(upper, Mapping):
        return []
    try:
        stated = Decimal(conjecture)
        ceiling = Decimal(str(upper.get("value")))
    except InvalidOperation:
        return []
    exponent = stated.as_tuple().exponent
    if not isinstance(exponent, int) or not stated.is_finite() or not ceiling.is_finite():
        return []
    if stated - ceiling > Decimal(1).scaleb(exponent) / 2:
        return [
            f"n={n}: conjectured optimum {conjecture} exceeds the verified ceiling {ceiling}"
        ]
    return []


def check_experiment_semantics(experiment: Mapping[str, object]) -> list[str]:
    """Return assurance violations for one experiment payload."""
    errors: list[str] = []
    subject = experiment.get("subject")
    if not isinstance(subject, Mapping):
        return ["experiment subject is missing or malformed"]
    assurance = subject.get("assurance")
    method = subject.get("method")
    if method in NUMERICAL_METHODS:
        if assurance != "numerically-checked":
            errors.append("numerical experiment method requires numerically-checked assurance")
        historical = (
            subject.get("precision") == "unrecorded-historical"
            or subject.get("tolerance") == "unrecorded-historical"
        )
        if historical:
            if not _dated_annotation(subject.get("migration_annotation")):
                errors.append(
                    "unrecorded historical values require a dated migration annotation"
                )
        elif not _precision_is_recorded(subject.get("precision")) or not isinstance(
            subject.get("tolerance"), str
        ):
            errors.append(
                "numerical experiment requires actual precision, rounding, and tolerance"
            )
    elif method in FORMAL_METHODS:
        if assurance != "verified":
            errors.append("formal experiment method requires verified assurance")
        if subject.get("precision") is not None or subject.get("tolerance") is not None:
            errors.append("formal experiment must not use precision or tolerance as assurance")
        run_method = experiment.get("method")
        if not isinstance(run_method, Mapping) or any(
            not run_method.get(field) for field in ("entry_point", "command", "record")
        ):
            errors.append(
                "formal experiment requires an entry point, replay command, and record"
            )
    else:
        errors.append(f"unsupported experiment method {method!r}")

    results = experiment.get("results")
    if isinstance(results, Sequence) and not isinstance(results, (str, bytes)):
        for result in results:
            if not isinstance(result, Mapping):
                continue
            beat_record_flag = result.get("beat_record") is True
            beat_record_outcome = result.get("outcome") == "beat_record"
            claimed_record = beat_record_flag or beat_record_outcome
            if claimed_record and assurance != "verified":
                errors.append("beat_record requires verified assurance")
    return errors
