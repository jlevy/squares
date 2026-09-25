"""The R052 loader maps the retained certificate onto native parent-core charges.

These tests check the reading and the exact premises only. The interval engine's
coverage decision is not run here; the last test pins that it refuses this
certificate at its static ceilings, which is a refusal and not a verdict.
"""

from __future__ import annotations

import copy
import gzip
import hashlib
import json
from collections.abc import Callable
from fractions import Fraction
from pathlib import Path
from typing import Any

import pytest

from devtools.verify_guzhou_r052_native import (
    PACKAGE,
    PILOT_ROWS,
    REVIEWED_SHA256,
    SOURCE,
    coverage_readiness,
    load_r052,
    parse_r052,
    physical_sites,
    run,
    source_counts,
)
from sqpack.fractional.parent_core import (
    ParentCoreCertificate,
    ParentCorePremises,
    validate_parent_core,
)

WEIGHT_UNITS = 10**12


@pytest.fixture(scope="module")
def loaded() -> tuple[ParentCoreCertificate, dict[str, Any]]:
    return load_r052()


@pytest.fixture(scope="module")
def premises(loaded: tuple[ParentCoreCertificate, dict[str, Any]]) -> ParentCorePremises:
    return validate_parent_core(loaded[0])


def test_retained_bytes_are_the_pinned_release() -> None:
    raw = gzip.decompress(SOURCE.read_bytes())
    pin = json.loads((PACKAGE / "SOURCE_PIN.json").read_text(encoding="utf-8"))
    assert hashlib.sha256(raw).hexdigest() == REVIEWED_SHA256 == pin["certificate_sha256"]


def test_counts_match_the_source_claims(
    loaded: tuple[ParentCoreCertificate, dict[str, Any]],
) -> None:
    assert source_counts(loaded[1]) == {
        "point_orbits": 2354,
        "threshold_orbits": 514,
        "generic_orbits": 54,
        "resource_columns": 2922,
        "physical_points": 18585,
        "physical_threshold_groups": 4504,
        "angular_rows": 15721,
    }


def test_exact_premises_hold_natively(
    loaded: tuple[ParentCoreCertificate, dict[str, Any]], premises: ParentCorePremises
) -> None:
    certificate = loaded[0]
    assert certificate.outer_side / certificate.parent_side == Fraction(231001, 50000)
    assert certificate.minimum_charge == Fraction(999426274093, WEIGHT_UNITS)
    assert premises.budget == Fraction(16990246659579, WEIGHT_UNITS)
    assert 17 * 999426274093 - 16990246659579 == 2
    assert (17 * certificate.minimum_charge - premises.budget) * WEIGHT_UNITS == 2
    assert premises.rows == 15721
    assert premises.minimum_containment_numerator > 0
    final = premises.final_half_tangent
    assert final == Fraction(207107, 500000)
    assert final * final + 2 * final - 1 == Fraction(309449, 250000000000)


def test_group_indices_name_d4_closed_orbits_in_source_order(
    loaded: tuple[ParentCoreCertificate, dict[str, Any]],
) -> None:
    """Every orbit, zero weight included, is the D4 image set of its first group.

    A site table in any other order would send some image outside the listed set.
    """
    raw = loaded[1]
    outer = 4613 * raw["coordinate_denominator"] // 1000
    sites, owners = physical_sites(raw, outer)
    assert len(sites) == len(owners) == 18585
    lookup = {site: index for index, site in enumerate(sites)}
    families = [(o["triples"]) for o in raw["threshold_orbits"]] + [
        o["groups"] for o in raw["generic_trigger_orbits"]
    ]
    for groups in families:
        images = set()
        for swap in (False, True):
            for flip_x in (False, True):
                for flip_y in (False, True):
                    image = []
                    for index in groups[0]:
                        x, y = sites[index]
                        if swap:
                            x, y = y, x
                        image.append(
                            lookup[(outer - x if flip_x else x, outer - y if flip_y else y)]
                        )
                    images.add(tuple(sorted(image)))
        assert {tuple(sorted(group)) for group in groups} == images


def _set(field: str, value: object) -> Callable[[dict[str, Any]], None]:
    return lambda raw: raw.__setitem__(field, value)


def _negative_point_weight(raw: dict[str, Any]) -> None:
    raw["point_orbits"] = [list(raw["point_orbits"][0]), *raw["point_orbits"][1:]]
    raw["point_orbits"][0][2] = -1


def _unknown_generic_kind(raw: dict[str, Any]) -> None:
    raw["generic_trigger_orbits"] = [
        dict(raw["generic_trigger_orbits"][0], kind="at_most"),
        *raw["generic_trigger_orbits"][1:],
    ]


def _invalid_site(raw: dict[str, Any]) -> None:
    orbit = copy.deepcopy(raw["threshold_orbits"][0])
    orbit["triples"][0][0] = 8 * len(raw["point_orbits"])
    raw["threshold_orbits"] = [orbit, *raw["threshold_orbits"][1:]]


def _asymmetric_group_orbit(raw: dict[str, Any]) -> None:
    positive = next(i for i, o in enumerate(raw["threshold_orbits"]) if o["weight"])
    orbit = copy.deepcopy(raw["threshold_orbits"][positive])
    orbit["triples"].pop()
    raw["threshold_orbits"] = list(raw["threshold_orbits"])
    raw["threshold_orbits"][positive] = orbit
    raw["budget_units"] -= orbit["weight"]


def _row(
    index: int, column: int, value: Callable[[list[str]], str]
) -> Callable[[dict[str, Any]], None]:
    def mutate(raw: dict[str, Any]) -> None:
        raw["entries"] = list(raw["entries"])
        row = list(raw["entries"][index])
        row[column] = value(row)
        raw["entries"][index] = row

    return mutate


def _truncate_cover(raw: dict[str, Any]) -> None:
    # Two rows keep the check fast; a cover ending anywhere short of tan(pi/8) fails alike.
    raw["entries"] = raw["entries"][:2]


@pytest.mark.parametrize(
    ("mutate", "message"),
    [
        (_set("L", "4614/1000"), "not the R052 container"),
        (_set("A", "230651/231001"), "not the R052 container"),
        (_set("budget_units", 16990246659580), "incorrect declared counting budget"),
        (_set("minimum_units", 999426274092), "no strict counting gap"),
        (_negative_point_weight, "nonnegative integer"),
        (_unknown_generic_kind, "unknown schema"),
        (_invalid_site, "invalid site"),
        (_asymmetric_group_orbit, "not D4 invariant"),
        (
            _row(1, 0, lambda r: str((Fraction(r[0]) + Fraction(r[1])) / 2)),
            "noncontiguous",
        ),
        (
            _row(0, 3, lambda _: str(Fraction(230650, 231001) - Fraction(1, 10**100))),
            "core reaches a parent boundary",
        ),
        (_truncate_cover, "does not reach pi/4"),
    ],
)
def test_mutations_are_refused(
    loaded: tuple[ParentCoreCertificate, dict[str, Any]],
    mutate: Callable[[dict[str, Any]], None],
    message: str,
) -> None:
    raw = dict(loaded[1])
    mutate(raw)
    with pytest.raises(ValueError, match=message):
        validate_parent_core(parse_r052(raw))


def test_wrong_bytes_and_duplicate_keys_are_refused(tmp_path: Path) -> None:
    raw = gzip.decompress(SOURCE.read_bytes())
    changed = tmp_path / "changed.json"
    changed.write_bytes(raw.replace(b'"L":"4613/1000"', b'"L":"4613/1000" ', 1))
    with pytest.raises(ValueError, match="differ from the reviewed"):
        load_r052(changed)
    duplicate = tmp_path / "duplicate.json"
    duplicate.write_bytes(b'{"L":"4613/1000","L":"4613/1000"}')
    with pytest.raises(ValueError, match="duplicate JSON key"):
        load_r052(duplicate, expected_sha256=None)


@pytest.mark.parametrize(("mode", "workers"), [("premises", 1), ("coverage", 2)])
def test_sizing_is_serial_coverage_only(mode: str, workers: int) -> None:
    with pytest.raises(ValueError, match="sizing run is serial coverage"):
        run(
            SOURCE,
            PILOT_ROWS,
            coverage=mode == "coverage",
            batch_size=1024,
            workers=workers,
            source_state=("0" * 40, True),
            sizing=True,
        )


def test_frozen_interval_engine_refuses_at_its_ceilings(
    loaded: tuple[ParentCoreCertificate, dict[str, Any]],
) -> None:
    report = coverage_readiness(loaded[0], 2048)
    assert report["admitted"] is False
    assert "8192" in report["refusal"]
    assert (report["point_atoms"], report["threshold_atoms"]) == (6901, 2036)
    assert (report["atom_rows"], report["distinct_sites"]) == (8937, 9261)
    assert (report["member_slots"], report["ragged_member_slots"]) == (44685, 13105)
    assert report["atom_rows"] > report["ceiling_atom_rows"]
    assert report["distinct_sites"] > report["ceiling_distinct_sites"]
    assert report["member_slots"] > report["ceiling_member_slots"]
