"""A terminal session names what it cost, and the check that says so cannot go quiet.

Session-045 ran twenty-three phases without a resource rollup being written once, and
nothing noticed: no field was empty, no check failed, the session closed clean. The
omission was invisible because nothing joined a session to its usage data at all — rollups
are named by harness log id and sessions by their own sequence number.

The assertions that matter are the two that keep this from becoming decoration: that the
checker actually fails on a terminal session with no rollups, and that the grandfather
boundary is a boundary rather than a growing list of exemptions.
"""

from __future__ import annotations

import pathlib

import devtools.check_session_rollups as checker
from devtools.check_session_rollups import (
    GRANDFATHERED_BEFORE,
    REPO,
    TERMINAL,
    main,
    sessions,
)
from sqpack.yamlio import safe_load


def test_every_terminal_session_at_or_after_the_boundary_declares_rollups() -> None:
    for path, session in sessions():
        identifier = str(session.get("id", path.stem))
        if str(session.get("status")) not in TERMINAL:
            continue
        if identifier < GRANDFATHERED_BEFORE:
            continue
        declared = session.get("resource_rollups") or []
        assert declared, f"{path.name} is terminal and names no resource rollup"
        for relative in declared:
            assert (REPO / relative).is_file(), f"{path.name}: missing {relative}"


def test_the_declared_rollups_are_real_rollup_records() -> None:
    """A path that exists is not enough; it has to be the artifact it claims to be."""
    seen = 0
    for _path, session in sessions():
        for relative in session.get("resource_rollups") or []:
            payload = safe_load((REPO / relative).read_text(encoding="utf-8"))
            assert "softschema" in payload or "rollup" in payload, relative
            seen += 1
    assert seen >= 18, "session-045 alone declares eighteen"


def test_the_checker_fails_on_a_terminal_session_with_none(
    monkeypatch, tmp_path: pathlib.Path
) -> None:
    """The guard against this becoming decoration.

    Written as a real session record in a temporary tree rather than a stubbed return,
    because what is being tested is that the frontmatter path finds it.
    """
    record = tmp_path / "session-999-fabricated.md"
    record.write_text(
        "---\nsession:\n  id: session-999\n  status: completed\n---\n# fabricated\n",
        encoding="utf-8",
    )
    monkeypatch.setattr(checker, "SESSIONS", tmp_path)

    assert checker.main() == 1


def test_an_in_progress_session_is_not_required_to_have_them(
    monkeypatch, tmp_path: pathlib.Path
) -> None:
    """The rollup is written at the end; requiring it earlier would be wrong."""
    record = tmp_path / "session-999-fabricated.md"
    record.write_text(
        "---\nsession:\n  id: session-999\n  status: in_progress\n---\n# fabricated\n",
        encoding="utf-8",
    )
    monkeypatch.setattr(checker, "SESSIONS", tmp_path)

    assert checker.main() == 0


def test_the_checker_refuses_an_existing_file_with_an_unknown_contract(
    monkeypatch, tmp_path: pathlib.Path
) -> None:
    record = tmp_path / "session-999-fabricated.md"
    record.write_text(
        "---\nsession:\n  id: session-999\n  status: completed\n"
        "  resource_rollups: [usage.yaml]\n---\n# fabricated\n",
        encoding="utf-8",
    )
    (tmp_path / "usage.yaml").write_text(
        "softschema:\n  contract: invented/v1\n  envelope: rollup\n"
        "  status: enforced\nrollup: {}\n",
        encoding="utf-8",
    )
    monkeypatch.setattr(checker, "SESSIONS", tmp_path)
    monkeypatch.setattr(checker, "REPO", tmp_path)

    assert checker.main() == 1


def test_the_checker_accepts_an_enforced_codex_delta_contract(
    monkeypatch, tmp_path: pathlib.Path
) -> None:
    record = tmp_path / "session-999-fabricated.md"
    record.write_text(
        "---\nsession:\n  id: session-999\n  status: completed\n"
        "  resource_rollups: [usage.yaml]\n---\n# fabricated\n",
        encoding="utf-8",
    )
    (tmp_path / "usage.yaml").write_text(
        "softschema:\n"
        "  contract: packing.squares:CodexTaskTreeDelta/v1\n"
        "  envelope: rollup\n  status: enforced\nrollup: {}\n",
        encoding="utf-8",
    )
    monkeypatch.setattr(checker, "SESSIONS", tmp_path)
    monkeypatch.setattr(checker, "REPO", tmp_path)

    assert checker.main() == 0


def test_the_grandfather_boundary_is_a_boundary_not_a_list() -> None:
    """A new session is above it by construction, so the exemption cannot quietly grow."""
    assert GRANDFATHERED_BEFORE == "session-045"
    assert main() == 0
