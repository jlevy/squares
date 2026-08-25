"""Behavioral checks for the derived current-research handoff."""

from __future__ import annotations

import pytest

from devtools.check_synopsis import (
    check_unprotected_fix_claims,
    select_handoff_cell,
)


def test_handoff_cell_is_selected_from_the_latest_session_action() -> None:
    items = [
        {"id": "BC-010", "bead": "think-old"},
        {"id": "BC-011", "bead": "think-next"},
    ]

    assert select_handoff_cell(items, "Resume BC-011 under think-next") == items[1]
    with pytest.raises(ValueError, match="exactly one agenda cell"):
        select_handoff_cell(items, "Compare BC-010 with BC-011")


def test_unprotected_fix_claims_rejects_stale_duplicate() -> None:
    current = "108 fixes left no regression check behind."
    stale_duplicate = f"{current} Ninety-eight fixes left no regression check behind."

    assert check_unprotected_fix_claims(current, 108) == []
    problems = check_unprotected_fix_claims(stale_duplicate, 108)
    assert len(problems) == 1
    assert "(108)" in problems[0]
