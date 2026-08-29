#!/usr/bin/env python3
"""Local feasibility and solve-cap controls for contact scaffolds."""

from __future__ import annotations

import numpy as np
import pytest
from scipy.optimize import OptimizeResult

import sqpack.contact_realization as realization
from sqpack.contact_assembly import (
    D4_TRANSFORMS,
    CanonicalScaffold,
    ContactEdge,
    ContactScaffold,
    canonicalize_scaffold,
    transform_scaffold,
)
from sqpack.contact_realization import (
    LocalRealizationError,
    check_local_contact_witness,
    realize_local_contact_scaffolds,
)


def _patch(*, delete_last: bool = False) -> ContactScaffold:
    edges = (
        ContactEdge(0, 1, "u", 1),
        ContactEdge(1, 2, "v", 1),
        ContactEdge(2, 3, "u", -1),
        ContactEdge(0, 3, "v", 1),
    )
    return ContactScaffold(
        ("angle-a",) * 4,
        edges[:-1] if delete_last else edges,
        ((),) * 4,
    )


def _infeasible_triangle() -> ContactScaffold:
    return ContactScaffold(
        ("angle-a",) * 3,
        (
            ContactEdge(0, 1, "u", 1),
            ContactEdge(1, 2, "u", 1),
            ContactEdge(0, 2, "u", 1),
        ),
        ((),) * 3,
    )


def test_patch_and_edge_deletion_share_a_witness_but_keep_distinct_labels() -> None:
    patch = _patch()
    deletion = _patch(delete_last=True)
    coordinates = ((0.0, 0.0), (1.0, 0.0), (1.0, 1.0), (0.0, 1.0))

    assert check_local_contact_witness(patch, coordinates, minimum_overlap=1.0).passed
    assert check_local_contact_witness(deletion, coordinates, minimum_overlap=1.0).passed
    patch_label = canonicalize_scaffold(patch)
    deletion_label = canonicalize_scaffold(deletion)
    assert isinstance(patch_label, CanonicalScaffold)
    assert isinstance(deletion_label, CanonicalScaffold)
    assert patch_label.canonical_label != deletion_label.canonical_label

    result = realize_local_contact_scaffolds(
        (patch, deletion), minimum_overlap=0.25, maximum_lp_solves=2
    )
    assert result.status == "completed"
    assert [receipt.outcome for receipt in result.receipts] == [
        "locally-feasible",
        "locally-feasible",
    ]


def test_positive_overlap_is_enforced_separately_from_normal_contact() -> None:
    edge = ContactScaffold(
        ("angle-a", "angle-a"),
        (ContactEdge(0, 1, "u", 1),),
        ((), ()),
    )
    coordinates = ((0.0, 0.0), (1.0, 0.75))

    passing = check_local_contact_witness(edge, coordinates, minimum_overlap=0.25)
    failing = check_local_contact_witness(edge, coordinates, minimum_overlap=0.3)

    assert passing.passed
    assert passing.minimum_realized_overlap == pytest.approx(0.25)
    assert not failing.passed
    assert failing.failed_edges == (0,)


def test_translation_gauge_and_d4_images_do_not_change_local_feasibility() -> None:
    patch = _patch()
    coordinates = ((0.0, 0.0), (1.0, 0.0), (1.0, 1.0), (0.0, 1.0))
    translated = tuple((u + 7.5, v - 3.25) for u, v in coordinates)
    assert check_local_contact_witness(patch, translated, minimum_overlap=0.5).passed

    image = transform_scaffold(
        patch,
        symmetry=D4_TRANSFORMS[6],
        old_to_new=(3, 1, 0, 2),
    )
    result = realize_local_contact_scaffolds(
        (patch, image), minimum_overlap=0.5, maximum_lp_solves=2
    )
    assert [receipt.outcome for receipt in result.receipts] == ["locally-feasible"]
    assert result.duplicate_candidates == 1
    assert result.receipts[0].coordinates is not None
    assert result.receipts[0].coordinates[0] == pytest.approx((0.0, 0.0))


def test_local_feasibility_does_not_imply_nonedge_separation() -> None:
    scaffold = ContactScaffold(
        ("angle-a",) * 3,
        (
            ContactEdge(0, 1, "u", 1),
            ContactEdge(0, 2, "v", 1),
        ),
        ((),) * 3,
    )
    coordinates = ((0.0, 0.0), (1.0, 0.9), (0.9, 1.0))
    check = check_local_contact_witness(scaffold, coordinates, minimum_overlap=0.1)

    assert check.passed
    assert abs(coordinates[1][0] - coordinates[2][0]) < 1
    assert abs(coordinates[1][1] - coordinates[2][1]) < 1


def test_infeasible_equalities_and_indeterminate_solver_status_stay_distinct(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    infeasible = realize_local_contact_scaffolds(
        (_infeasible_triangle(),), minimum_overlap=0.1, maximum_lp_solves=1
    )
    assert infeasible.receipts[0].outcome == "locally-infeasible"
    assert infeasible.receipts[0].solver_status == 2

    monkeypatch.setattr(
        realization,
        "linprog",
        lambda *_args, **_kwargs: OptimizeResult(success=False, status=4, x=None),
    )
    indeterminate = realize_local_contact_scaffolds(
        (_patch(),), minimum_overlap=0.1, maximum_lp_solves=1
    )
    assert indeterminate.receipts[0].outcome == "solver-indeterminate"
    assert indeterminate.receipts[0].solver_status == 4

    monkeypatch.setattr(
        realization,
        "linprog",
        lambda *_args, **_kwargs: OptimizeResult(success=True, status=0, x=np.zeros(8)),
    )
    invalid_success = realize_local_contact_scaffolds(
        (_patch(),), minimum_overlap=0.1, maximum_lp_solves=1
    )
    assert invalid_success.receipts[0].outcome == "solver-indeterminate"
    assert invalid_success.receipts[0].witness_check is not None
    assert not invalid_success.receipts[0].witness_check.passed


def test_lp_cap_and_canonical_deduplication_have_explicit_accounting() -> None:
    patch = _patch()
    image = transform_scaffold(
        patch,
        symmetry=D4_TRANSFORMS[1],
        old_to_new=(2, 0, 3, 1),
    )
    deduplicated = realize_local_contact_scaffolds(
        (patch, image), minimum_overlap=0.1, maximum_lp_solves=1
    )
    assert deduplicated.status == "completed"
    assert deduplicated.lp_solves == 1
    assert deduplicated.duplicate_candidates == 1
    assert deduplicated.encountered_candidates == 2

    limited = realize_local_contact_scaffolds(
        (patch, _patch(delete_last=True)),
        minimum_overlap=0.1,
        maximum_lp_solves=1,
    )
    assert limited.status == "limit"
    assert limited.limit_kind == "lp-solve-cap"
    assert limited.lp_solves == 1
    assert limited.encountered_candidates == 2
    assert limited.pending_canonical_label is not None

    zero = realize_local_contact_scaffolds((patch,), minimum_overlap=0.1, maximum_lp_solves=0)
    assert zero.status == "limit"
    assert zero.lp_solves == 0


def test_local_slice_rejects_constraints_it_does_not_own() -> None:
    with_walls = ContactScaffold(
        ("angle-a",),
        (),
        (("left",),),
    )
    with pytest.raises(LocalRealizationError, match="cannot enforce container walls"):
        realize_local_contact_scaffolds((with_walls,), minimum_overlap=0.1, maximum_lp_solves=1)
    with pytest.raises(LocalRealizationError, match="interval"):
        realize_local_contact_scaffolds((_patch(),), minimum_overlap=0.0, maximum_lp_solves=1)
    with pytest.raises(LocalRealizationError, match="interval"):
        realize_local_contact_scaffolds((), minimum_overlap=0.0, maximum_lp_solves=1)
    with pytest.raises(LocalRealizationError, match="nonnegative"):
        realize_local_contact_scaffolds((_patch(),), minimum_overlap=0.1, maximum_lp_solves=-1)
    with pytest.raises(LocalRealizationError, match="nonnegative"):
        realize_local_contact_scaffolds((), minimum_overlap=0.1, maximum_lp_solves=True)


def test_mixed_angle_classes_are_rejected_before_solving(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    mixed = ContactScaffold(
        ("angle-a", "angle-b"),
        (ContactEdge(0, 1, "u", 1),),
        ((), ()),
    )

    def fail_if_called(*_args: object, **_kwargs: object) -> OptimizeResult:
        raise AssertionError("mixed angle classes reached linprog")

    monkeypatch.setattr(realization, "linprog", fail_if_called)
    with pytest.raises(LocalRealizationError, match="one uniform vertex angle class") as error:
        realize_local_contact_scaffolds((mixed,), minimum_overlap=0.1, maximum_lp_solves=1)

    assert error.value.kind == "unsupported-angle-classes"
