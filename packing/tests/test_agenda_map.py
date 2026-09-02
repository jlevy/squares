"""The agenda map is read from the agendas, not restated beside them.

The map exists because "where are we" was reconstructed by hand from seven agenda files
every time a session asked, and was reconstructed wrongly at least once: a throwaway
parser read `status:` where the field is `state:` and reported all eighty commitments as
unknown. These assertions pin the two things a hand parse got wrong -- the field name and
the state vocabulary -- plus the two derived claims the document makes in prose, so a
change to either the schema or the renderer fails here rather than in a stale table.
"""

from __future__ import annotations

from dataclasses import replace
from pathlib import Path

from devtools.render_agenda_map import (
    STATE_MEANING,
    STATE_ORDER,
    Commitment,
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


def test_current_autonomous_w6_rows_name_registered_hypotheses() -> None:
    """Agenda-012/013 may not route scientific W6 results only through AgentSessions."""
    for name in (
        "agenda-012-weighted-proof-precision-bridge-and-cross-scale-controls.md",
        "agenda-013-nine-hour-autonomous-run.md",
    ):
        text = (AGENDAS / name).read_text(encoding="utf-8")
        document = safe_load(text.split("---\n")[1])
        for item in document["agenda"]["items"]:
            if "research-loop" in (item.get("workflows") or []):
                assert item.get("hypotheses"), (
                    f"{item['id']} claims research-loop/W6 without a registered hypothesis"
                )


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

    Asserting against real data only ever exercises whichever branch the queue happens to
    be in, and deleting the reporting block entirely would leave that green. So the
    positive branch is driven by a synthetic queue, and both branches are checked against
    the same renderer.

    This docstring used to add that no real cell was in that state. It was true when
    written and false within the day: `BC-025`'s predecessors both completed, and it sat
    advertised as takeable while genuinely blocked on two unrecorded things. The claim
    could not fail, because the assertions below run against the synthetic queue -- a
    statement about real data, in a test that never reads it. `D-401` records the whole
    of it; the state is now a refusal rather than a report, so the real queue is checked
    by `violations` instead of by a sentence here.
    """
    done = Commitment(
        agenda="agenda-001",
        agenda_status="active",
        doc="agenda-001-x.md",
        id="BC-001",
        state="complete",
        priority=0,
        purpose="research",
        owner_focus="insight",
        question="a finished predecessor",
        bead="think-aaaa",
        depends_on=(),
        blocked_on="",
        discharged_by="",
    )
    stalled = replace(
        done,
        id="BC-002",
        state="blocked",
        question="a cell whose only blocker is discharged",
        bead="think-bbbb",
        depends_on=("BC-001",),
    )
    text = render([done, stalled])
    # "has" for one, "have" for several: the noun was already pluralised conditionally
    # and the verb was not, so a single stalled cell read "1 blocked commitment have".
    assert "has every predecessor" in text
    assert "`BC-002`" in text

    # The same cell, now stating a second blocker, must not be advertised as takeable.
    # Its hybrid manual gate must appear in the summary even though it also has a
    # dependency edge; otherwise a coordinator could mistake predecessor completion for
    # authorization.
    still_blocked = replace(stalled, blocked_on="an acceptance decision nobody has made")
    quiet = render([done, still_blocked])
    assert "have every predecessor" not in quiet
    assert "**1 blocked commitment carries a manual condition** (`BC-002`)" in quiet
    assert "Dependency edges alone cannot make this ready" in quiet
    assert "an acceptance decision nobody has made" in quiet


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


def test_a_blocked_cell_whose_edges_all_cleared_must_say_why() -> None:
    """Reporting the stall was never enough; it is a refusal now.

    `BC-025` sat blocked with both predecessors complete and no `blocked_on`, so the map
    advertised it as takeable. It was genuinely blocked -- `H-047`'s regularizer does not
    exist, and five of its seven instances retain no pose -- but neither reason was written
    anywhere, and nothing refused that. The asymmetry this closes is the point: `ledger.py`
    already refuses a `ready` cell with incomplete dependencies, so the queue was guarded
    against over-claiming readiness and not at all against under-claiming it.
    """
    done = Commitment(
        agenda="agenda-001",
        agenda_status="active",
        doc="agenda-001-x.md",
        id="BC-001",
        state="complete",
        priority=0,
        purpose="research",
        owner_focus="insight",
        question="a finished predecessor",
        bead="think-aaaa",
        depends_on=(),
        blocked_on="",
        discharged_by="",
    )
    stalled = replace(
        done,
        id="BC-002",
        state="blocked",
        question="blocked, edges clear, silent about why",
        bead="think-bbbb",
        depends_on=("BC-001",),
    )
    assert any("no blocked_on says why" in problem for problem in violations([done, stalled]))

    speaking = replace(stalled, blocked_on="A review decision nobody has taken.")
    assert violations([done, speaking]) == []
