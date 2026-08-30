"""Cross-record assurance rules that JSON Schema cannot express."""

from __future__ import annotations

import re
from collections.abc import Mapping, Sequence
from decimal import Decimal, InvalidOperation

NUMERICAL_METHODS = frozenset({"numerical-f64", "numerical-multiprecision"})
MACHINE_FORMAL_METHODS = frozenset(
    {"interval-certified", "exact-algebraic", "proof-assistant-checked"}
)
PROOF_METHODS = frozenset({"published-proof", "proof-audited"})
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


def check_evidence_semantics(evidence: Mapping[str, object]) -> list[str]:
    """Return assurance-method violations for one evidence record."""
    errors: list[str] = []
    evidence_id = evidence.get("id", "<unknown evidence>")
    prefix = f"{evidence_id}: "
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
            if evidence.get("claim") not in {expected_claim, "exact-value"}:
                errors.append(
                    f"{label}: evidence {ref} has claim {evidence.get('claim')!r}, "
                    f"expected {expected_claim!r}"
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
        backing = [record for record in cited if record.get("assurance") == "verified"]
        if not backing:
            errors.append("verified rigidity requires at least one verified evidence record")
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
            delegated = any(
                record.get("assurance") == "verified"
                and record.get("certificate")
                and record.get("replay")
                for record in cited
            )
            if not backed and not delegated:
                errors.append(
                    f"{method} requires certificate and replay, "
                    "on the block or on a cited verified record"
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
    same_upper = bounds_agree_at_declared_precision(reported_upper, verified_upper)
    if same_upper and upper_gap_blockers:
        errors.append(f"n={n_value}: stale formal-upper-gap blocker")
    if not same_upper and not upper_gap_blockers:
        errors.append(f"n={n_value}: formal upper trails report without a blocker")
    return errors


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
