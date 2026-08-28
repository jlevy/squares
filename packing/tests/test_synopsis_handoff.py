"""Behavioral checks for the derived current-research handoff."""

from __future__ import annotations

import pytest

from devtools.check_synopsis import (
    check_experiment_scope_claims,
    check_round_effort_claims,
    check_unprotected_fix_claims,
    load_agenda_items,
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


def test_handoff_cells_are_loaded_across_agendas(tmp_path) -> None:
    paths = []
    for number, cell_id in enumerate(("BC-010", "BC-019"), start=1):
        path = tmp_path / f"agenda-{number:03}.md"
        path.write_text(
            f"---\nagenda:\n  items:\n  - id: {cell_id}\n    bead: think-{number}\n---\n",
            encoding="utf-8",
        )
        paths.append(path)

    items = load_agenda_items(reversed(paths))

    assert [item["id"] for item in items] == ["BC-010", "BC-019"]
    assert select_handoff_cell(items, "Continue BC-019") == items[1]


def test_unprotected_fix_claims_rejects_stale_duplicate() -> None:
    current = "108 fixes left no regression check behind."
    stale_duplicate = f"{current} Ninety-eight fixes left no regression check behind."

    assert check_unprotected_fix_claims(current, 108) == []
    problems = check_unprotected_fix_claims(stale_duplicate, 108)
    assert len(problems) == 1
    assert "(108)" in problems[0]


def test_round_effort_claims_reject_stale_duplicate() -> None:
    current = (
        "There are 44 terminal rounds registered in `series-000`. "
        "They record 1061 agent-minutes and 30.7 wall-minutes."
    )
    stale_duplicate = (
        f"{current}\n\nThere are 39 terminal rounds registered in `series-000`. "
        "They record 933 agent-minutes and 28.3 wall-minutes."
    )

    assert check_round_effort_claims(current, "44", "1061", "30.7") == []
    assert check_round_effort_claims(stale_duplicate, "44", "1061", "30.7")


def test_experiment_scope_claims_preserve_h024_prerequisite() -> None:
    current = "Exp-012 leaves H-024 unresolved because its formal prerequisite is unmet."
    promoted = "Exp-012 numerically reconstructs the source and refutes H-024."

    assert check_experiment_scope_claims(current) == []
    assert check_experiment_scope_claims(promoted)
