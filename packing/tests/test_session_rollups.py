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

import copy
import json
import pathlib
import subprocess

import pytest
import yaml
from jsonschema_rs import Draft202012Validator

import devtools.check_session_gate as gate_checker
import devtools.check_session_rollups as checker
from devtools import validate_schemas
from devtools.check_session_rollups import (
    GRANDFATHERED_BEFORE,
    REPO,
    TERMINAL,
    main,
    sessions,
)
from sqpack.yamlio import safe_load

CODEX_RECEIPT = REPO / "packing/campaign/resource-usage/codex-task-tree-session-062.yaml"
SESSION_099 = REPO / "packing/campaign/agent-sessions/session-099-atlas-expansion-to-324.md"


def _unmeasured_record(
    directory: pathlib.Path,
    **overrides: str,
) -> None:
    status = overrides.get("status", "stopped")
    reason = overrides.get("reason", "native_harness_data_unavailable")
    detail = overrides.get("detail", "The native harness input is no longer available.")
    disposition = overrides.get("disposition", "think-ab12")
    stop_reason = overrides.get(
        "stop_reason", "Native resource evidence is unavailable; certification remains open."
    )
    rollups = overrides.get("rollups", "[]")
    handoff_role = overrides.get("handoff_role", "administrative_closeout")
    directory.mkdir(parents=True, exist_ok=True)
    (directory / "session-999-fabricated.md").write_text(
        "---\nsession:\n"
        "  id: session-999\n"
        f"  status: {status}\n"
        "  resource_usage_unmeasured:\n"
        f"    reason: {reason}\n"
        f"    detail: {detail}\n"
        f"    disposition_bead: {disposition}\n"
        f"    handoff_role: {handoff_role}\n"
        f"  resource_rollups: {rollups}\n"
        f"  stop_reason: {stop_reason}\n"
        "  next_action: Preserve the explicit unmeasured disposition.\n"
        "---\n# fabricated\n",
        encoding="utf-8",
    )


def test_every_terminal_session_at_or_after_the_boundary_declares_measurement() -> None:
    for path, session in sessions():
        identifier = str(session.get("id", path.stem))
        if str(session.get("status")) not in TERMINAL:
            continue
        if identifier < GRANDFATHERED_BEFORE:
            continue
        declared = session.get("resource_rollups") or []
        unmeasured = session.get("resource_usage_unmeasured")
        if unmeasured is not None:
            assert session.get("status") == "stopped", path.name
            assert declared == [], path.name
            assert checker.BEAD_REFERENCE.fullmatch(unmeasured["disposition_bead"]), path.name
            continue
        assert declared, f"{path.name} is terminal and names no resource measurement"
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


@pytest.mark.parametrize("status", ["completed", "stopped"])
def test_the_checker_fails_on_an_ordinary_terminal_session_with_none(
    monkeypatch, tmp_path: pathlib.Path, status: str
) -> None:
    """The guard against this becoming decoration.

    Written as a real session record in a temporary tree rather than a stubbed return,
    because what is being tested is that the frontmatter path finds it.
    """
    record = tmp_path / "session-999-fabricated.md"
    record.write_text(
        f"---\nsession:\n  id: session-999\n  status: {status}\n---\n# fabricated\n",
        encoding="utf-8",
    )
    monkeypatch.setattr(checker, "SESSIONS", tmp_path)

    assert checker.main() == 1


def test_the_checker_accepts_an_explicit_unmeasured_stopped_session(
    monkeypatch, tmp_path: pathlib.Path, capsys
) -> None:
    _unmeasured_record(tmp_path)
    monkeypatch.setattr(checker, "SESSIONS", tmp_path)
    monkeypatch.setattr(checker, "disposition_bead_presence", lambda _bead: "present")

    assert checker.main() == 0
    output = capsys.readouterr().out
    assert "explicitly record unavailable resource measurement" in output
    assert "session-999" in output


def test_the_checker_refuses_a_well_formed_missing_disposition_bead(
    monkeypatch, tmp_path: pathlib.Path, capsys
) -> None:
    _unmeasured_record(tmp_path)
    monkeypatch.setattr(checker, "SESSIONS", tmp_path)
    monkeypatch.setattr(checker, "disposition_bead_presence", lambda _bead: "missing")

    assert checker.main() == 1
    assert "does not resolve in the available tbd store" in capsys.readouterr().err


def test_disposition_bead_lookup_distinguishes_a_resolved_missing_bead(monkeypatch) -> None:
    checker.disposition_bead_presence.cache_clear()
    monkeypatch.setattr(checker.shutil, "which", lambda _command: "/synthetic/tbd")
    monkeypatch.setattr(
        checker.subprocess,
        "run",
        lambda *args, **_kwargs: subprocess.CompletedProcess(
            args[0],
            1,
            stdout=json.dumps({"error": "Issue not found", "type": "NotFoundError"}),
            stderr="",
        ),
    )

    assert checker.disposition_bead_presence("think-ab12") == "missing"
    checker.disposition_bead_presence.cache_clear()


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("status", "completed"),
        ("status", "in_progress"),
        ("reason", "operator_forgot_to_measure"),
        ("detail", "''"),
        ("handoff_role", "inferred_from_prose"),
        ("stop_reason", "''"),
        ("disposition", "not-a-bead"),
        (
            "rollups",
            "[packing/campaign/resource-usage/missing.yaml]",
        ),
    ],
)
def test_the_checker_refuses_every_broadened_unmeasured_shape(
    monkeypatch, tmp_path: pathlib.Path, field: str, value: str
) -> None:
    arguments = {field: value}
    _unmeasured_record(tmp_path, **arguments)
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


def test_a_passed_gate_can_clear_certification_while_usage_stays_unmeasured(
    monkeypatch, tmp_path: pathlib.Path
) -> None:
    """The two honest states remain independent throughout the terminal lifecycle."""
    _unmeasured_record(tmp_path)
    record = tmp_path / "session-999-fabricated.md"
    head = subprocess.run(
        ("git", "rev-parse", "HEAD"),
        cwd=REPO,
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()
    text = record.read_text(encoding="utf-8")
    record.write_text(
        text.replace(
            "  resource_usage_unmeasured:\n",
            f"  checks:\n  - 'full gate: fast at {head}: passed'\n"
            "  resource_usage_unmeasured:\n",
        ),
        encoding="utf-8",
    )
    monkeypatch.setattr(checker, "SESSIONS", tmp_path)
    monkeypatch.setattr(gate_checker, "SESSIONS", tmp_path)
    monkeypatch.setattr(gate_checker, "REPO", REPO)
    monkeypatch.setattr(checker, "disposition_bead_presence", lambda _bead: "present")

    assert checker.main() == 0
    assert gate_checker.main() == 0


def test_agent_session_schema_allows_that_post_certification_state() -> None:
    payload, _meta = validate_schemas.payload_and_meta(SESSION_099)
    candidate = copy.deepcopy(payload)
    candidate.pop("certification_pending", None)
    candidate["checks"].append("full gate: fast at 3a18a05a: passed")
    schema_path = REPO / "packing/campaign/schemas/agent-session.schema.yaml"
    validator = Draft202012Validator(safe_load(schema_path.read_text(encoding="utf-8")))

    assert list(validator.iter_errors(candidate)) == []


def test_the_checker_refuses_an_existing_file_with_an_unknown_contract(
    monkeypatch, tmp_path: pathlib.Path
) -> None:
    usage = tmp_path / "packing" / "campaign" / "resource-usage"
    usage.mkdir(parents=True)
    record = tmp_path / "session-999-fabricated.md"
    record.write_text(
        "---\nsession:\n  id: session-999\n  status: completed\n"
        "  resource_rollups: [packing/campaign/resource-usage/usage.yaml]\n"
        "---\n# fabricated\n",
        encoding="utf-8",
    )
    (usage / "usage.yaml").write_text(
        "softschema:\n  contract: invented/v1\n  envelope: rollup\n"
        "  status: enforced\nrollup: {}\n",
        encoding="utf-8",
    )
    monkeypatch.setattr(checker, "SESSIONS", tmp_path)
    monkeypatch.setattr(checker, "REPO", tmp_path)

    assert checker.main() == 1


def test_the_checker_refuses_noncanonical_or_absolute_receipt_paths(
    monkeypatch, tmp_path: pathlib.Path
) -> None:
    outside = tmp_path / "outside.yaml"
    outside.write_text(
        "softschema:\n  contract: packing.squares:ClaudeEfficiencyRollup/v1\n"
        "  envelope: rollup\n  status: enforced\nrollup: {}\n",
        encoding="utf-8",
    )
    (tmp_path / "session-998-traversal.md").write_text(
        "---\nsession:\n  id: session-998\n  status: completed\n"
        "  resource_rollups: "
        "[packing/campaign/resource-usage/../outside.yaml]\n---\n# fabricated\n",
        encoding="utf-8",
    )
    (tmp_path / "session-999-absolute.md").write_text(
        "---\nsession:\n  id: session-999\n  status: completed\n"
        f"  resource_rollups: [{outside}]\n---\n# fabricated\n",
        encoding="utf-8",
    )
    monkeypatch.setattr(checker, "SESSIONS", tmp_path)
    monkeypatch.setattr(checker, "REPO", tmp_path)

    assert checker.main() == 1


def test_the_checker_accepts_an_enforced_codex_delta_contract(
    monkeypatch, tmp_path: pathlib.Path
) -> None:
    usage = tmp_path / "packing" / "campaign" / "resource-usage"
    usage.mkdir(parents=True)
    record = tmp_path / "session-999-fabricated.md"
    record.write_text(
        "---\nsession:\n  id: session-999\n  status: completed\n"
        "  branch: codex/example\n"
        "  resource_rollups: [packing/campaign/resource-usage/usage.yaml]\n"
        "---\n# fabricated\n",
        encoding="utf-8",
    )
    (usage / "usage.yaml").write_text(
        CODEX_RECEIPT.read_text(encoding="utf-8"), encoding="utf-8"
    )
    monkeypatch.setattr(checker, "SESSIONS", tmp_path)
    monkeypatch.setattr(checker, "REPO", tmp_path)

    assert checker.main() == 0


def test_the_checker_requires_branch_attribution_for_a_terminal_codex_session(
    monkeypatch, tmp_path: pathlib.Path
) -> None:
    usage = tmp_path / "packing" / "campaign" / "resource-usage"
    usage.mkdir(parents=True)
    record = tmp_path / "session-999-fabricated.md"
    record.write_text(
        "---\nsession:\n  id: session-999\n  status: completed\n"
        "  resource_rollups: [packing/campaign/resource-usage/usage.yaml]\n"
        "---\n# fabricated\n",
        encoding="utf-8",
    )
    (usage / "usage.yaml").write_text(
        CODEX_RECEIPT.read_text(encoding="utf-8"), encoding="utf-8"
    )
    monkeypatch.setattr(checker, "SESSIONS", tmp_path)
    monkeypatch.setattr(checker, "REPO", tmp_path)

    assert checker.main() == 1


def test_the_checker_rejects_duplicate_rollup_declarations(
    monkeypatch, tmp_path: pathlib.Path
) -> None:
    usage = tmp_path / "packing" / "campaign" / "resource-usage"
    usage.mkdir(parents=True)
    reference = "packing/campaign/resource-usage/usage.yaml"
    (tmp_path / "session-999-fabricated.md").write_text(
        "---\nsession:\n  id: session-999\n  status: completed\n"
        "  branch: codex/example\n"
        f"  resource_rollups: [{reference}, {reference}]\n"
        "---\n# fabricated\n",
        encoding="utf-8",
    )
    (usage / "usage.yaml").write_text(
        CODEX_RECEIPT.read_text(encoding="utf-8"), encoding="utf-8"
    )
    monkeypatch.setattr(checker, "SESSIONS", tmp_path)
    monkeypatch.setattr(checker, "REPO", tmp_path)

    assert checker.main() == 1


def test_the_checker_rejects_cross_branch_codex_claims(
    monkeypatch, tmp_path: pathlib.Path
) -> None:
    usage = tmp_path / "packing" / "campaign" / "resource-usage"
    usage.mkdir(parents=True)
    reference = "packing/campaign/resource-usage/usage.yaml"
    for session_id, branch in (
        ("session-998", "codex/first"),
        ("session-999", "codex/second"),
    ):
        (tmp_path / f"{session_id}-fabricated.md").write_text(
            f"---\nsession:\n  id: {session_id}\n  status: completed\n"
            f"  branch: {branch}\n"
            f"  resource_rollups: [{reference}]\n"
            "---\n# fabricated\n",
            encoding="utf-8",
        )
    (usage / "usage.yaml").write_text(
        CODEX_RECEIPT.read_text(encoding="utf-8"), encoding="utf-8"
    )
    monkeypatch.setattr(checker, "SESSIONS", tmp_path)
    monkeypatch.setattr(checker, "REPO", tmp_path)

    assert checker.main() == 1


def test_the_checker_rejects_a_semantically_false_codex_delta(
    monkeypatch, tmp_path: pathlib.Path
) -> None:
    usage = tmp_path / "packing" / "campaign" / "resource-usage"
    usage.mkdir(parents=True)
    record = tmp_path / "session-999-fabricated.md"
    record.write_text(
        "---\nsession:\n  id: session-999\n  status: completed\n"
        "  branch: codex/example\n"
        "  resource_rollups: [packing/campaign/resource-usage/usage.yaml]\n"
        "---\n# fabricated\n",
        encoding="utf-8",
    )
    document = safe_load(CODEX_RECEIPT.read_text(encoding="utf-8"))
    document["rollup"]["delta"]["agent_active_seconds"] = 0.0
    (usage / "usage.yaml").write_text(
        yaml.safe_dump(document, sort_keys=False), encoding="utf-8"
    )
    monkeypatch.setattr(checker, "SESSIONS", tmp_path)
    monkeypatch.setattr(checker, "REPO", tmp_path)

    assert checker.main() == 1


def test_the_grandfather_boundary_is_a_boundary_not_a_list() -> None:
    """A new session is above it by construction, so the exemption cannot quietly grow."""
    assert GRANDFATHERED_BEFORE == "session-045"
    assert main() == 0


def test_agent_session_schema_requires_unique_resource_rollups() -> None:
    schema = safe_load(
        (REPO / "packing/campaign/schemas/agent-session.schema.yaml").read_text(
            encoding="utf-8"
        )
    )

    assert schema["properties"]["resource_rollups"]["uniqueItems"] is True


def test_session_099_unmeasured_terminal_state_satisfies_the_enforced_schema() -> None:
    assert validate_schemas.check(SESSION_099) == []
