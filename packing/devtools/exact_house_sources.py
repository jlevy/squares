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


def validate_prior(document: dict[str, Any]) -> None:
    """Hold complete saved identities to the maintained native pre-adoption record."""
    _require(
        set(document) == {"format", "adopted_on", "current_entries", "selected_occurrences"},
        "prior register fields",
    )
    _require(
        document["format"] == PRIOR_FORMAT and document["adopted_on"] == houses.ADOPTED_ON,
        "prior register epoch",
    )
    cases = adopt_houses.read_history()
    current = {row["n"]: row for row in document["current_entries"]}
    selected = {row["n"]: row for row in document["selected_occurrences"]}
    roster = set(houses.NUMBERS)
    _require(
        len(current) == len(document["current_entries"]) and set(current) == roster,
        "prior current roster",
    )
    _require(
        len(selected) == len(document["selected_occurrences"]) and set(selected) == roster,
        "prior selected roster",
    )
    for n in houses.NUMBERS:
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
        source = houses.source_for(n)
        custody = occurrence["source_certificate"]
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
            Fraction(occurrence["exact_form"]) == houses.side(n), "prior selected native side"
        )
        _require(
            occurrence["polynomial"]["coefficients"]
            == [str(houses.side(n).denominator), str(-houses.side(n).numerator)],
            "prior selected coefficients",
        )


def read_prior(path: Path | None = None) -> dict[str, Any]:
    source = path or PRIOR
    reports.ensure_private(source)
    document = houses.kernel.read_xz(source)
    validate_prior(document)
    return document


def retain_prior(register: Path, output: Path | None = None) -> dict[str, Any]:
    """Capture only the 42 full current rows and 42 selected source rows before regeneration."""
    destination = output or PRIOR
    document = json.loads(read_retained_text(register))
    _require(
        document["softschema"]["contract"] == "packing.squares:ExactValues/v1",
        "input exact-register contract",
    )
    record = document["register"]
    retained = {
        "format": PRIOR_FORMAT,
        "adopted_on": houses.ADOPTED_ON,
        "current_entries": [
            copy.deepcopy(row) for row in record["entries"] if row["n"] in houses.ADOPTED
        ],
        "selected_occurrences": [
            copy.deepcopy(row)
            for row in record["historical_entries"]
            if row["n"] in houses.ADOPTED
            and row.get("source_certificate", {}).get("result") == houses.ADOPTED[row["n"]]
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
        self.prior: dict[str, Any] | None = None

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
            entries = [row for row in selection.load_results() if row["id"] == source.result]
            _require(len(entries) == 1, "ambiguous registered adopted result")
            result = entries[0]
            _require(
                (result["verification"], result["confirmation"]) == ("V3", "C3"), "source grade"
            )
            evidence = selection.load_evidence()
            candidates = selection.candidates(entries, evidence).get(n, [])
            _require(
                len(candidates) == 1, "adopted result lacks a unique accepted scoped review"
            )
            candidate = candidates[0]
            certificate = source.certificate(n)
            _require(
                candidate.source_key == key and candidate.side == certificate.side,
                "review side",
            )
            for identifier in candidate.confirming_evidence:
                proof = evidence[identifier]
                _require(
                    proof.get("source_key") == key and proof.get("method") == "exact-algebraic",
                    "confirming evidence source/method",
                )
                _require(
                    proof.get("replay") and proof.get("certificate"),
                    "incomplete confirming evidence",
                )
                path = houses.REPO / str(proof["certificate"])
                reports.ensure_private(path)
                _require(
                    path.resolve().is_relative_to(source.packet.resolve()),
                    "evidence certificate path",
                )
            source.jobs(n, certificate)
            houses.check_houses([n])
            origin = source.origin(n)
            receipt = houses.receipt_of(n)
            reports.ensure_private(receipt)
            prefix = f"/blob/{origin.revision}/"
            _require(prefix in origin.url, "origin has no exact upstream certificate path")
            original = origin.url.split(prefix, 1)[1]
            custody = {
                "result": source.result,
                "source_key": source.key,
                "revision": origin.revision,
                "facts": origin.path.relative_to(houses.REPO).as_posix(),
                "original_certificate": original,
                "receipt": receipt.relative_to(houses.REPO).as_posix(),
                "verification": "V3",
                "confirmation": "C3",
                "algebraic_identity": "independently-checked",
                "geometry_replay": "native-replay-retained",
                "adoption": "adopted",
                "global_optimality": "not-established",
            }
            if self.prior is None:
                self.prior = read_prior()
            (occurrence,) = [row for row in self.prior["selected_occurrences"] if row["n"] == n]
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
    parser.add_argument("--output", type=Path, default=PRIOR)
    arguments = parser.parse_args()
    print(json.dumps(retain_prior(arguments.retain_prior_register, arguments.output), indent=2))


if __name__ == "__main__":
    main()
