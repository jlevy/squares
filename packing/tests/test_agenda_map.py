"""The agenda map is read from the agendas, not restated beside them.

The map exists because "where are we" was reconstructed by hand from seven agenda files
every time a session asked, and was reconstructed wrongly at least once: a throwaway
parser read `status:` where the field is `state:` and reported all eighty commitments as
unknown. These assertions pin the two things a hand parse got wrong -- the field name and
the state vocabulary -- plus the two derived claims the document makes in prose, so a
change to either the schema or the renderer fails here rather than in a stale table.
"""

from __future__ import annotations

from pathlib import Path

from devtools.render_agenda_map import (
    STATE_MEANING,
    STATE_ORDER,
    load,
    render,
    violations,
)
from sqpack.yamlio import safe_load

PROJECT_ROOT = Path(__file__).resolve().parents[1]
AGENDAS = PROJECT_ROOT / "campaign" / "agendas"
SCHEMA = PROJECT_ROOT / "campaign" / "schemas" / "agenda.schema.yaml"


def test_every_declared_state_is_ordered_and_explained() -> None:
    """The schema's enum is the vocabulary; the renderer must cover all of it.

    A state the schema allows but the renderer does not know would sort to the end as an
    unknown and carry no explanation, which is exactly the silent-omission failure the
    map is supposed to remove.
    """
    schema = safe_load(SCHEMA.read_text())
    declared = schema["properties"]["items"]["items"]["properties"]["state"]["enum"]
    assert set(declared) == set(STATE_ORDER)
    assert set(declared) == set(STATE_MEANING)


def test_commitments_are_loaded_from_every_agenda() -> None:
    """No agenda may be silently absent from the map."""
    files = sorted(AGENDAS.glob("agenda-*.md"))
    # Filenames are `agenda-NNN-slug.md` and ids are `agenda-NNN`, so the id is the
    # first two hyphen-separated fields. Matching on a slug fragment would pass while
    # silently dropping any agenda whose slug changed.
    assert {c.agenda for c in load()} == {"-".join(f.name.split("-")[:2]) for f in files}


def test_states_come_from_the_state_field_not_the_status_field() -> None:
    """`state` is the commitment; `status` is the agenda that contains it.

    Reading the wrong one is the specific mistake this tool was built after, and both
    fields exist in the same document, so nothing but an assertion separates them.
    """
    rows = load()
    assert {c.state for c in rows} <= set(STATE_ORDER)
    # Every commitment carries a state; none falls back to a placeholder.
    assert all(c.state for c in rows)
    # Agenda status is a different vocabulary and must not leak into the state column.
    assert {c.agenda_status for c in rows} <= {"active", "paused", "completed", "superseded"}


def test_a_blocked_cell_with_all_predecessors_complete_is_reported() -> None:
    """The map's whole reason for existing is catching a queue that has stalled.

    A cell whose blockers are discharged but whose state still reads `blocked` is
    takeable and invisible. The renderer must say so -- but only when nothing else
    blocks it. A cell whose edge cleared while its stated condition did not is still
    blocked, and calling it takeable would be the same class of wrong claim the map
    exists to remove. `BC-029` is exactly that case: `BC-027` is complete, and it still
    waits on an independent acceptance decision.
    """
    rows = load()
    done = {c.id for c in rows if c.state == "complete"}
    blocked = [c for c in rows if c.state == "blocked"]
    edge_cleared = [c for c in blocked if c.depends_on and set(c.depends_on) <= done]
    takeable = [c for c in edge_cleared if not c.blocked_on]
    text = render(rows)
    if takeable:
        assert "have every predecessor" in text
        for c in takeable:
            assert f"`{c.id}`" in text
    else:
        assert "have every predecessor" not in text
    # A cell whose edge cleared but which states another blocker must not be advertised.
    for c in edge_cleared:
        if c.blocked_on:
            assert f"and no other stated blocker, so `{c.id}`" not in text


def test_the_rendered_map_names_every_live_commitment() -> None:
    """A ready commitment absent from the live queue is worse than no map at all."""
    rows = load()
    text = render(rows)
    for c in rows:
        if c.state in ("ready", "tentative"):
            assert f"`{c.id}`" in text, f"{c.id} is takeable but missing from the map"


def test_no_commitment_is_offered_as_takeable_after_another_discharged_it() -> None:
    """The defect D-374 records, as an assertion rather than a one-time repair.

    Four agenda-005 commitments read `ready` after agenda-006 finished them, and OR-4
    sends a session to exactly that queue. Nothing but this stops it recurring.
    """
    assert [c.id for c in load() if c.discharged_by and c.state in ("ready", "tentative")] == []


def test_every_blocked_commitment_names_something_that_can_clear() -> None:
    """A blocker nobody can observe never clears.

    Either a predecessor commitment, or a stated condition. Four cells had neither and
    sat blocked on prose for as long as five agendas.
    """
    orphans = [
        c.id for c in load() if c.state == "blocked" and not c.depends_on and not c.blocked_on
    ]
    assert orphans == []


def test_the_renderer_refuses_a_queue_that_contradicts_itself() -> None:
    """The invariants are a refusal, not a report.

    `violations` is what makes `--check` fail; if it returned findings the renderer then
    ignored, the generated map would state the contradiction and call it current.
    """
    assert violations(load()) == []
