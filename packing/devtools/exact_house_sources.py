"""Admit adopted finite identities through the maintained house and review readers."""

from __future__ import annotations

import argparse
import copy
import json
import lzma
from fractions import Fraction
from pathlib import Path
from typing import Any

from devtools import adopt_houses
from devtools import select_houses as selection
from devtools import upper_bound_houses as houses
from devtools import upper_bound_reports as reports
from devtools.retained_data import read_retained_text
from sqpack.exact_values import DERIVED_FROM_EXACT_FORM, algebraic_fields
from sqpack.kingbird_catalogue import normalized_polynomial
from sqpack.yamlio import safe_load

PRIOR = houses.ROOT / f"devtools/house-exact-prior-{houses.ADOPTED_ON}.json.xz"
PRIOR_FORMAT = "exact-house-prior-register-v1"


class ReadInputs:
    """Fully checked inputs shared within one invocation, never cached across public calls."""

    def __init__(self) -> None:
        self.archives: dict[Path, dict[str, Any]] = {}
        self.certificates: dict[tuple[str, str, Path, int], Any] = {}


def prior_path(day: str) -> Path:
    _require(day in adopt_houses.passes(), "unknown adoption pass")
    return houses.ROOT / f"devtools/house-exact-prior-{day}.json.xz"


def after_pass(day: str, n: int) -> dict[str, Any]:
    """The pass's selected state, preserved by the next move or the current case."""
    passes = adopt_houses.passes()
    _require(day in passes and n in adopt_houses.read_pass(day), "count outside adoption pass")
    for later in passes[passes.index(day) + 1 :]:
        following = adopt_houses.read_pass(later)
        if n in following:
            return safe_load(following[n].split("---", 2)[1])["packing"]
    text = (houses.ROOT / f"frontier/n-{n:03d}.md").read_text()
    return safe_load(text.split("---", 2)[1])["packing"]


def pass_source(day: str, n: int) -> houses.Source:
    state = after_pass(day, n)
    key = state["reported_upper_bound"]["source_key"]
    source = houses.sources().get(key)
    _require(source is not None, "pass transition has no maintained native source")
    assert source is not None
    _require(
        source.certificate(n).side
        == Fraction(state["reported_upper_bound"]["exact_form"])
        == Fraction(state["verified_upper_bound"]["exact_form"]),
        "pass transition native side",
    )
    return source


def scoped_certificate(source: houses.Source, n: int, *, inputs: ReadInputs | None = None):
    """Bind an old or current selection to its own accepted review and complete jobs."""
    checked = inputs or ReadInputs()
    identity = source.result, source.key, source.packet.resolve(), n
    if identity in checked.certificates:
        return checked.certificates[identity]
    entries = [row for row in selection.load_results() if row["id"] == source.result]
    _require(len(entries) == 1, "ambiguous registered adopted result")
    _require(
        (entries[0]["verification"], entries[0]["confirmation"]) == ("V3", "C3"),
        "source grade",
    )
    evidence = selection.load_evidence()
    candidates = selection.candidates(entries, evidence).get(n, [])
    _require(len(candidates) == 1, "adopted result lacks a unique accepted scoped review")
    candidate = candidates[0]
    certificate = source.certificate(n)
    _require(
        candidate.source_key == source.key and candidate.side == certificate.side, "review side"
    )
    for identifier in candidate.confirming_evidence:
        proof = evidence[identifier]
        _require(
            proof.get("source_key") == source.key and proof.get("method") == "exact-algebraic",
            "confirming evidence source/method",
        )
        _require(
            proof.get("replay") and proof.get("certificate"), "incomplete confirming evidence"
        )
        path = houses.REPO / str(proof["certificate"])
        reports.ensure_private(path)
        _require(
            path.resolve().is_relative_to(source.packet.resolve()), "evidence certificate path"
        )
    source.jobs(n, certificate)
    checked.certificates[identity] = certificate
    return certificate


def custody_for(source: houses.Source, n: int, adoption: str) -> dict[str, Any]:
    origin = source.origin(n)
    receipt = houses.receipt_for_source(source, n)
    reports.ensure_private(receipt)
    prefix = f"/blob/{origin.revision}/"
    _require(prefix in origin.url, "origin has no exact upstream certificate path")
    return {
        "result": source.result,
        "source_key": source.key,
        "revision": origin.revision,
        "facts": origin.path.relative_to(houses.REPO).as_posix(),
        "original_certificate": origin.url.split(prefix, 1)[1],
        "receipt": receipt.relative_to(houses.REPO).as_posix(),
        "verification": "V3",
        "confirmation": "C3",
        "algebraic_identity": "independently-checked",
        "geometry_replay": "native-replay-retained",
        "adoption": adoption,
        "global_optimality": "not-established",
    }


def validate_prior(document: dict[str, Any], *, inputs: ReadInputs | None = None) -> None:
    """Hold complete saved identities to the maintained native pre-adoption record."""
    checked = inputs or ReadInputs()
    _require(
        set(document) == {"format", "adopted_on", "current_entries", "selected_occurrences"},
        "prior register fields",
    )
    _require(
        document["format"] == PRIOR_FORMAT and document["adopted_on"] in adopt_houses.passes(),
        "prior register epoch",
    )
    day = document["adopted_on"]
    cases = adopt_houses.read_pass(day)
    current = {row["n"]: row for row in document["current_entries"]}
    selected = {row["n"]: row for row in document["selected_occurrences"]}
    roster = set(cases)
    _require(
        len(current) == len(document["current_entries"]) and set(current) == roster,
        "prior current roster",
    )
    _require(
        len(selected) == len(document["selected_occurrences"]) and set(selected) == roster,
        "prior selected roster",
    )
    for n in sorted(roster):
        prior = safe_load(cases[n].split("---", 2)[1])["packing"]
        row, occurrence = current[n], selected[n]
        _require(
            row["status"] == prior["status"]
            and row["side"]["value"] == str(prior["reported_upper_bound"]["value"]),
            "prior current side/status",
        )
        _require(
            row["lower"]["value"] == str(prior["verified_lower_bound"]["value"]),
            "prior current lower bound",
        )
        old_form = prior["reported_upper_bound"].get("exact_form")
        if old_form is None:
            native = reports.house_side(str(prior["reported_upper_bound"]["source_key"]), n)
            _require(
                str(native) == str(Fraction(prior["verified_upper_bound"]["exact_form"])),
                "prior native side differs from its complete retained source",
            )
            old_form = str(native)
        _require(
            algebraic_fields(old_form, None, None)["minimal_polynomial"]
            == row["polynomial"]["text"],
            "prior current polynomial",
        )
        _require(
            normalized_polynomial(row["polynomial"]["text"])
            == tuple(int(value) for value in row["polynomial"]["coefficients"]),
            "prior current coefficient vector",
        )
        _require(
            algebraic_fields(row["exact_form"], None, None)["minimal_polynomial"]
            == row["polynomial"]["text"],
            "prior current exact form",
        )
        previous = [
            earlier
            for earlier in adopt_houses.passes()
            if earlier < day and n in adopt_houses.read_pass(earlier)
        ]
        if previous:
            old_archive = read_prior(day=max(previous), inputs=checked)
            (old_selected,) = [
                old for old in old_archive["selected_occurrences"] if old["n"] == n
            ]
            old_custody = copy.deepcopy(old_selected["source_certificate"])
            old_custody["adoption"] = "adopted"
            _require(
                row.get("source_certificate") == old_custody, "prior adopted current custody"
            )
            _require(
                row.get("source_occurrences") == old_selected["sources"]
                and row.get("attribution") == old_selected["attribution"]
                and row.get("source_statuses")
                == [
                    "adopted-current" if flag == "pending-adoption" else flag
                    for flag in old_selected["source_statuses"]
                ],
                "prior adopted current occurrence/attribution",
            )
        source = pass_source(day, n)
        certificate = scoped_certificate(source, n, inputs=checked)
        custody = occurrence["source_certificate"]
        _require(
            custody == custody_for(source, n, "pending"), "prior selected complete custody"
        )
        _require(
            (custody["result"], custody["source_key"]) == (source.result, source.key),
            "prior selected custody",
        )
        _require(
            (custody["verification"], custody["confirmation"], custody["adoption"])
            == ("V3", "C3", "pending"),
            "prior source assurance",
        )
        _require(
            occurrence["kind"] == "unreconciled-source"
            and occurrence["sources"]
            and occurrence["attribution"]["source_text"],
            "prior source occurrence/attribution",
        )
        _require(
            Fraction(occurrence["exact_form"]) == certificate.side, "prior selected native side"
        )
        _require(
            occurrence["polynomial"]["coefficients"]
            == [str(certificate.side.denominator), str(-certificate.side.numerator)],
            "prior selected coefficients",
        )


def read_prior(
    path: Path | None = None,
    *,
    day: str | None = None,
    inputs: ReadInputs | None = None,
) -> dict[str, Any]:
    checked = inputs or ReadInputs()
    source = path or prior_path(day or houses.ADOPTED_ON)
    reports.ensure_private(source)
    identity = source.resolve()
    if identity in checked.archives:
        document = checked.archives[identity]
    else:
        document = houses.kernel.read_xz(source)
        validate_prior(document, inputs=checked)
        checked.archives[identity] = document
    if day is not None:
        _require(document["adopted_on"] == day, "archive differs from requested pass")
    return document


def prior_archives(
    *, inputs: ReadInputs | None = None
) -> tuple[tuple[Path, dict[str, Any]], ...]:
    checked = inputs or ReadInputs()
    return tuple(
        (prior_path(day), read_prior(day=day, inputs=checked)) for day in adopt_houses.passes()
    )


def retain_prior(
    register: Path,
    output: Path | None = None,
    *,
    day: str | None = None,
    collect_selected: bool = False,
) -> dict[str, Any]:
    """Retain one pass's full prior rows and complete scoped selected source occurrences."""
    day = day or houses.ADOPTED_ON
    destination = output or prior_path(day)
    roster = set(adopt_houses.read_pass(day))
    document = json.loads(read_retained_text(register))
    _require(
        document["softschema"]["contract"] == "packing.squares:ExactValues/v1",
        "input exact-register contract",
    )
    record = document["register"]
    occurrences = record["historical_entries"]
    if collect_selected:
        # The new pass's offers need not exist in the preceding exact register. This
        # maintained collector validates native custody, frozen claims and reviewed scope.
        from devtools import build_exact_values  # noqa: PLC0415

        occurrences = build_exact_values.declared_source_certificate_history(record["entries"])
    selected = {n: pass_source(day, n) for n in roster}
    retained = {
        "format": PRIOR_FORMAT,
        "adopted_on": day,
        "current_entries": [
            copy.deepcopy(row) for row in record["entries"] if row["n"] in roster
        ],
        "selected_occurrences": [
            copy.deepcopy(row)
            for row in occurrences
            if row["n"] in roster
            and row.get("source_certificate", {}).get("result") == selected[row["n"]].result
            and row.get("source_certificate", {}).get("source_key") == selected[row["n"]].key
        ],
    }
    validate_prior(retained)
    encoded = (json.dumps(retained, indent=2, ensure_ascii=False) + "\n").encode()
    compressed = lzma.compress(encoded)
    if destination.exists():
        _require(destination.read_bytes() == compressed, "existing prior register is immutable")
    else:
        with destination.open("xb") as stream:
            stream.write(compressed)
    return {
        "path": str(destination),
        "adopted_on": day,
        "selected_input": "maintained-native-collector"
        if collect_selected
        else "register-history",
        "current_entries": len(retained["current_entries"]),
        "selected_occurrences": len(retained["selected_occurrences"]),
        "decoded_bytes": len(encoded),
        "compressed_bytes": len(compressed),
    }


class HouseIdentityError(ValueError):
    """A current identity differs from its selected certificate, review or custody."""


def _require(condition: object, message: str) -> None:
    if not condition:
        raise HouseIdentityError(message)


class Inputs:
    """Retained source proofs reused within one exact-register build."""

    def __init__(self) -> None:
        self.checked: dict[int, tuple[Fraction, dict[str, Any]]] = {}
        self.priors: dict[str, dict[str, Any]] = {}
        self.read_inputs = ReadInputs()

    def admit(
        self, n: int, packing: dict[str, Any]
    ) -> tuple[dict[str, Any], dict[str, Any]] | None:
        reported = packing["reported_upper_bound"]
        key = reported.get("source_key")
        if n not in houses.ADOPTED:
            _require(key not in houses.source_keys(), "adopted source has no scoped count")
            return None
        source = houses.source_for(n)
        _require(key == source.key, "source/count is not the adopted house")
        _require(packing.get("n") == n and packing.get("status") == "open", "not an open case")
        if n not in self.checked:
            certificate = scoped_certificate(source, n, inputs=self.read_inputs)
            houses.check_houses([n])
            custody = custody_for(source, n, "adopted")
            day = houses.adopted_on(n)
            if day not in self.priors:
                self.priors[day] = read_prior(day=day, inputs=self.read_inputs)
            (occurrence,) = [
                row for row in self.priors[day]["selected_occurrences"] if row["n"] == n
            ]
            saved = occurrence["source_certificate"]
            _require(
                all(
                    saved[field] == value
                    for field, value in custody.items()
                    if field != "adoption"
                ),
                "adopted custody differs from complete prior source occurrence",
            )
            adopted_custody = copy.deepcopy(saved)
            adopted_custody["adoption"] = "adopted"
            self.checked[n] = (
                certificate.side,
                {
                    "source_certificate": adopted_custody,
                    "source_occurrences": copy.deepcopy(occurrence["sources"]),
                    "attribution": copy.deepcopy(occurrence["attribution"]),
                    "source_statuses": [
                        "adopted-current" if flag == "pending-adoption" else flag
                        for flag in occurrence["source_statuses"]
                    ],
                },
            )
        side, provenance = self.checked[n]
        verified = packing.get("verified_upper_bound", {})
        _require(
            type(reported.get("algebraic_degree")) is int and reported["algebraic_degree"] == 1,
            "native side degree",
        )
        _require(
            reported.get("algebraic_source") in {None, DERIVED_FROM_EXACT_FORM},
            "native algebraic origin",
        )
        _require(
            Fraction(str(reported.get("exact_form")))
            == side
            == Fraction(str(verified.get("exact_form"))),
            "native exact form",
        )
        ceiling = selection.ceiling(side)
        _require(str(verified.get("value")) == ceiling, "verified upward ceiling")
        _require(
            Fraction(str(reported.get("value"))) in {side, Fraction(ceiling)},
            "reported native side or upward ceiling",
        )
        entries = [row for row in selection.load_results() if row["id"] == source.result]
        proof = selection.confirming(entries[0], selection.load_evidence(), n)
        _require(
            proof and set(proof) <= set(verified.get("evidence", [])),
            "current confirming evidence",
        )
        reporting = selection.reporting(entries[0], selection.load_evidence(), key)
        _require(
            reporting and set(reporting) <= set(reported.get("evidence", [])),
            "current reporting evidence",
        )
        fields = algebraic_fields(str(side), None, None)
        supplied = reported.get("minimal_polynomial")
        _require(
            supplied is None
            or normalized_polynomial(str(supplied)) == (side.denominator, -side.numerator),
            "supplied polynomial is not the native side",
        )
        return {**reported, **fields}, copy.deepcopy(provenance)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--retain-prior-register", type=Path, required=True)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--pass-date", default=houses.ADOPTED_ON, choices=adopt_houses.passes())
    parser.add_argument("--collect-selected", action="store_true")
    arguments = parser.parse_args()
    print(
        json.dumps(
            retain_prior(
                arguments.retain_prior_register,
                arguments.output,
                day=arguments.pass_date,
                collect_selected=arguments.collect_selected,
            ),
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
