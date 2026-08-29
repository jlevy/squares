"""Contracts for the agent-log rollup readers."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from devtools.logrollup import REGISTRY, ClaudeCodeReader, build_registry
from devtools.logrollup.claude import Shape, executable_of, traits_of
from devtools.logrollup.model import Elapsed, SessionRollup, SourceLog, Span


def test_shell_shapes_put_one_off_code_ahead_of_incidental_structure() -> None:
    # OR-1 is about heredocs and `python -c`, so a Python heredoc that also pipes has to
    # classify as one; the piping is incidental and must not win.
    assert Shape.of("python3 - <<'PY'\nprint(1)\nPY | wc -l") is Shape.python_heredoc
    assert Shape.of("uv run python -c 'print(1)'") is Shape.python_inline
    assert Shape.of("cat > f <<'EOF'\nx\nEOF") is Shape.heredoc
    assert Shape.of("make format && git commit") is Shape.compound
    assert Shape.of("grep -n x f | head") is Shape.pipeline
    assert Shape.of("ls -la") is Shape.simple
    assert Shape.of("   ") is Shape.empty
    assert Shape.python_heredoc.is_one_off_code
    assert not Shape.compound.is_one_off_code


def test_command_identity_never_carries_content() -> None:
    assert executable_of("VAR=1 /usr/bin/git status") == "git"
    assert executable_of("'unclosed") == "(unlexable)"
    assert executable_of("") is None
    assert set(traits_of("a | b > c $(d) &")) == {
        "pipes",
        "redirects_output",
        "substitutes",
        "backgrounded",
    }


def test_elapsed_reports_nothing_it_did_not_measure() -> None:
    empty = Elapsed.of([])
    assert empty.count == 0
    assert "median_seconds" not in empty.payload()
    assert Elapsed.of([1.0, 3.0]).payload()["median_seconds"] == 2.0


def _log(tmp_path: Path) -> Path:
    """One minimal but well-formed Claude Code transcript."""
    turn = {
        "type": "assistant",
        "uuid": "a1",
        "parentUuid": "u0",
        "sessionId": "s-1",
        "version": "2.1.251",
        "gitBranch": "main",
        "effort": "max",
        "timestamp": "2026-08-29T00:00:10.000Z",
        "message": {
            "model": "claude-opus-5",
            "usage": {"input_tokens": 5, "output_tokens": 7},
            "content": [
                {"type": "tool_use", "id": "t1", "name": "Bash", "input": {"command": "ls"}}
            ],
        },
    }
    records = [
        {
            "type": "user",
            "uuid": "u0",
            "sessionId": "s-1",
            "timestamp": "2026-08-29T00:00:00.000Z",
        },
        turn,
        {
            "type": "user",
            "uuid": "u1",
            "sessionId": "s-1",
            "timestamp": "2026-08-29T00:00:14.000Z",
            "message": {"content": [{"type": "tool_result", "tool_use_id": "t1"}]},
        },
    ]
    path = tmp_path / "session.jsonl"
    path.write_text("\n".join(json.dumps(r) for r in records) + "\n", encoding="utf-8")
    return path


def test_a_claude_log_reads_end_to_end(tmp_path: Path) -> None:
    path = _log(tmp_path)
    reader = REGISTRY.for_path(path)
    assert reader.harness == "claude-code"

    payload = reader.read(path).payload()
    rollup = payload["rollup"]
    assert payload["softschema"]["contract"].endswith("ClaudeEfficiencyRollup/v1")
    assert rollup["source"]["records"] == 3
    assert rollup["span"]["wall_seconds"] == 14.0
    assert rollup["turns"]["by_model_and_thinking_level"] == {"claude-opus-5 @ max": 1}
    assert rollup["tokens"] == {"input_tokens": 5, "output_tokens": 7}
    assert rollup["tokens_by_thinking_level"]["max"]["output_tokens"] == 7
    assert rollup["tool_calls"]["by_shell_shape"]["simple"]["count"] == 1
    assert rollup["tool_calls"]["by_thinking_level"]["max"]["count"] == 1
    # The turn is 10s after its parent and the result 4s after the turn: latency and tool
    # time are different measurements and must not be conflated.
    assert rollup["turns"]["latency"]["total_seconds"] == 10.0
    assert rollup["tool_calls"]["total_seconds"] == 4.0


def test_a_rollup_must_state_its_semantics(tmp_path: Path) -> None:
    records = [{"type": "user", "sessionId": "s", "timestamp": "2026-08-29T00:00:00.000Z"}]
    path = tmp_path / "empty.jsonl"
    path.write_text(json.dumps(records[0]) + "\n", encoding="utf-8")
    silent = SessionRollup(
        contract="x/v1",
        schema="s.yaml",
        source=SourceLog.of(path, harness="x", records=records),
        span=Span.of(records),
        semantics={},
    )
    with pytest.raises(ValueError, match="semantics"):
        silent.payload()


def test_an_unrecognised_log_is_refused_rather_than_guessed(tmp_path: Path) -> None:
    path = tmp_path / "other.jsonl"
    path.write_text('{"type": "something-else"}\n', encoding="utf-8")
    with pytest.raises(LookupError, match="no reader recognises"):
        REGISTRY.for_path(path)


def test_the_registry_refuses_two_readers_for_one_harness() -> None:
    with pytest.raises(ValueError, match="duplicate harness"):
        build_registry([ClaudeCodeReader(), ClaudeCodeReader()])
