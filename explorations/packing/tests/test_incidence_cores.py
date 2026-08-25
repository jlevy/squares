"""Fast structural checks for the retained Trump incidence-core case."""

from __future__ import annotations

from cases.trump11 import incidence_cores


def test_branch_zero_structure_and_unresolved_terminal_path() -> None:
    field, groups, branch_group, representative = incidence_cores.derive_branch(0)

    assert len(representative) == 14
    checks = incidence_cores.structural_checks(field, groups, branch_group)
    assert checks
    assert all(checks.values())
