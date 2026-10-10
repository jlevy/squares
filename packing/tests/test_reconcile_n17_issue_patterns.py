"""Refusal and overlap controls for the n17 issue metadata join."""

from __future__ import annotations

import copy
import time
from pathlib import Path
from typing import Any

import pytest

from devtools import reconcile_n17_issue_patterns as join

GROUP = ((0, 1, 2, 3), (3, 2, 1, 0))


def test_d4_equality_is_separate_from_containment() -> None:
    # Q=one cell, P=two cells: Q entails exclusion of P, not conversely.
    result = join.class_relations(3, {1: "small", 3: "equal", 7: "large"}, GROUP)
    assert result["equal_admitted"] == ["equal"]
    assert result["contained_admitted"] == ["small"]
    assert result["containing_admitted"] == ["large"]
    reverse = join.class_relations(1, {3: "large"}, GROUP)
    assert reverse["contained_admitted"] == []


def test_d4_union_overlap_and_fixed_margins() -> None:
    population = {3: 2, 5: 2, 7: 2}
    first = join.project(3, population, GROUP)
    image = join.project(12, population, GROUP)
    second = join.project(5, population, GROUP)
    assert first == image == {3, 7}
    assert second == {5, 7}
    assert join.population_count(population, first | second) == {"orbits": 3, "states": 6}
    assert join.population_count(population, second - first) == {"orbits": 1, "states": 2}


def test_report_history_keeps_unexplained_promotion() -> None:
    messages = [
        {"source": "body", "table": "| 1 | a, b | Computed | — |", "totals": None},
        {
            "source": "comment1",
            "table": "| 2 | c, d | Computed | — |",
            "totals": {"verified": 1, "computed": 1},
        },
    ]
    result = join.parse_reports(messages)
    assert len(result["rows"]) == 2
    assert result["row_totals"] == {"verified": 0, "computed": 2}
    assert len(result["aggregate_discrepancies"]) == 1
    corrected = copy.deepcopy(messages)
    corrected.append(
        {
            "source": "promotion",
            "table": "| 1 | a, b | Certificate verified | standing verifier (full) |",
            "totals": {"verified": 1, "computed": 1},
        }
    )
    corrected.append(
        {
            "source": "retraction",
            "table": "",
            "verifier_corrections": [
                {"row": 1, "verified_with": "parallel node checks plus fast"}
            ],
        }
    )
    updated = join.parse_reports(corrected)
    assert updated["row_totals"] == {"verified": 1, "computed": 1}
    assert updated["aggregate_discrepancies"][0]["resolved_by"] == "promotion"
    assert updated["unresolved_aggregate_discrepancies"] == []
    assert updated["rows"][0]["verified_with"] == "parallel node checks plus fast"
    assert updated["rows"][0]["history"][-2]["verified_with"] == "standing verifier (full)"
    bad_correction = copy.deepcopy(corrected)
    bad_correction[-1]["verifier_corrections"][0]["row"] = 3
    try:
        join.parse_reports(bad_correction)
    except join.RefusedError as exc:
        assert "unknown row" in str(exc)
    else:
        raise AssertionError("an unjoined verifier correction passed")
    changed = copy.deepcopy(messages)
    changed.append({"source": "comment2", "table": "| 1 | a, e | Computed | — |"})
    try:
        join.parse_reports(changed)
    except join.RefusedError as exc:
        assert "changed cells" in str(exc)
    else:
        raise AssertionError("an unexplained class replacement passed")


def test_unknown_duplicate_and_omitted_rosters_are_refused() -> None:
    bad = {"source": "body", "table": "| 1 | a, a | Computed | — |"}
    try:
        join.parse_reports([bad])
    except join.RefusedError as exc:
        assert "repeated cell" in str(exc)
    else:
        raise AssertionError("duplicate cells passed")
    try:
        join.require_roster([1, 1], [1, 2], "pilot")
    except join.RefusedError as exc:
        assert "pilot" in str(exc)
    else:
        raise AssertionError("omitted/duplicated pilot passed")
    unknown = {"source": "body", "table": "| 1 | a | Verified | fast |"}
    try:
        join.parse_reports([unknown])
    except join.RefusedError as exc:
        assert "status" in str(exc)
    else:
        raise AssertionError("unknown status passed")


def test_frozen_input_join_and_partial_proof_status() -> None:
    source = join.REPO / "packing/campaign/issue-intake/n17-20261008/github-issues.json"
    document = join.read_document(source)
    result = join.reconcile(document, deadline=time.monotonic() + 30)
    assert result["reported33_union"]["distance_two_tail"] == {"orbits": 1, "states": 8}
    assert result["reported33_union"]["first_eight_pilot"] == {"orbits": 0, "states": 0}
    assert result["standing_full_reported_rows"] == [1, 2]
    assert result["explicit_row_totals"] == {"verified": 22, "computed": 11}
    assert result["unresolved_aggregate_discrepancies"] == []
    assert result["certificate_verification_performed"] is False
    assert result["census_admission_proved"] is False
    assert all(row["premise_join"].startswith("unknown") for row in result["patterns"])
    assert not any(row["endpoint_assignment_in_projection"] for row in result["patterns"])
    for mutate, fragment in [
        (lambda d: d.update(cap="117/25"), "cap/frame"),
        (lambda d: d["pilot"]["masks"].pop(), "first-eight"),
        (
            lambda d: d["reports"][0].update(
                table=d["reports"][0]["table"].replace("side-S1", "unknown-cell", 1)
            ),
            "cell",
        ),
    ]:
        broken = copy.deepcopy(document)
        mutate(broken)
        try:
            join.reconcile(broken, deadline=time.monotonic() + 30)
        except ValueError as exc:
            assert fragment in str(exc)
        else:
            raise AssertionError("changed frame or incomplete/mismatched roster passed")
    try:
        join.reconcile(document, deadline=time.monotonic() - 1)
    except join.RefusedError as exc:
        assert "incomplete" in str(exc)
    else:
        raise AssertionError("expired metadata deadline passed")


@pytest.mark.parametrize("ids", [[""], [" "], [None], [[]], ["358-C1", "358-C1"], ["413-23"]])
def test_invalid_and_colliding_pattern_ids_are_refused_before_populations(
    monkeypatch: pytest.MonkeyPatch, ids: list[Any]
) -> None:
    document = {
        "schema": join.SOURCE_SCHEMA,
        "reports": [
            {
                "source": "synthetic",
                "table": "\n".join(f"| {i} | cell | Computed | — |" for i in range(1, 34)),
            }
        ],
        "companion_patterns": [{"id": identity} for identity in ids],
    }

    def no_populations(*_args: Any) -> None:
        pytest.fail("invalid pattern identity reached population reconstruction")

    monkeypatch.setattr(join, "populations", no_populations)
    with pytest.raises(join.RefusedError, match="pattern ID"):
        join.reconcile(document, deadline=time.monotonic() + 5)


def synthetic_publication(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> tuple[Path, list[str]]:
    output = tmp_path / "result.json"
    output.write_text("previous evidence", encoding="utf-8")
    monkeypatch.setattr(join, "read_document", lambda _path: {})
    monkeypatch.setattr(join, "reconcile", lambda *_args, **_kwargs: {"synthetic": True})
    return output, ["--source", "unused", "--output", str(output)]


@pytest.mark.parametrize("failure", ["write", "close", "replace"])
def test_cli_publication_failures_preserve_old_output_and_clean_staging(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
    failure: str,
) -> None:
    output, arguments = synthetic_publication(tmp_path, monkeypatch)
    write, close = join.os.write, join.os.close

    def partial_write(descriptor: int, contents: Any) -> int:
        write(descriptor, contents[:5])
        raise OSError("injected write failure")

    def failed_close(descriptor: int) -> None:
        close(descriptor)
        raise OSError("injected close failure")

    def failed_replace(_source: Path, _destination: Path) -> None:
        raise OSError("injected replace failure")

    if failure == "write":
        monkeypatch.setattr(join.os, "write", partial_write)
    elif failure == "close":
        monkeypatch.setattr(join.os, "close", failed_close)
    else:
        monkeypatch.setattr(join.os, "replace", failed_replace)
    assert join.main(arguments) == 1
    captured = capsys.readouterr()
    assert "REFUSED: injected " + failure + " failure" in captured.err
    assert "WROTE" not in captured.out
    assert output.read_text() == "previous evidence"
    assert list(tmp_path.iterdir()) == [output]


def test_publication_completes_short_writes_before_atomic_replacement(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    output = tmp_path / "result.json"
    output.write_text("previous evidence", encoding="utf-8")
    write, replace = join.os.write, join.os.replace
    text = '{"message":"complete λ receipt"}'
    writes = []

    def short_write(descriptor: int, contents: Any) -> int:
        count = write(descriptor, contents[:3])
        writes.append(count)
        return count

    def inspect_replace(source: Path, destination: Path) -> None:
        assert source.parent == destination.parent
        assert source.read_text() == text
        assert destination.read_text() == "previous evidence"
        replace(source, destination)

    monkeypatch.setattr(join.os, "write", short_write)
    monkeypatch.setattr(join.os, "replace", inspect_replace)
    join.publish_metadata(output, text)
    assert len(writes) > 1
    assert output.read_text() == text
    assert list(tmp_path.iterdir()) == [output]


def test_write_failure_remains_primary_when_close_and_cleanup_also_fail(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    output, arguments = synthetic_publication(tmp_path, monkeypatch)
    write, close = join.os.write, join.os.close

    def partial_write(descriptor: int, contents: Any) -> int:
        write(descriptor, contents[:5])
        raise OSError("primary partial write")

    def failed_close(descriptor: int) -> None:
        close(descriptor)
        raise OSError("secondary close failure")

    def failed_cleanup(path: Path, *, missing_ok: bool = False) -> None:
        assert missing_ok
        assert path.parent == output.parent
        assert path != output
        raise OSError("secondary cleanup failure")

    monkeypatch.setattr(join.os, "write", partial_write)
    monkeypatch.setattr(join.os, "close", failed_close)
    monkeypatch.setattr(Path, "unlink", failed_cleanup)
    assert join.main(arguments) == 1
    captured = capsys.readouterr()
    assert captured.err.startswith("REFUSED: primary partial write\n")
    assert "secondary close failure" in captured.err
    assert "secondary cleanup failure" in captured.err
    assert "WROTE" not in captured.out
    assert output.read_text() == "previous evidence"
    staging = [path for path in tmp_path.iterdir() if path != output]
    assert len(staging) == 1
    assert len(staging[0].read_bytes()) == 5


def test_zero_length_staging_write_is_refused_without_publication(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    output = tmp_path / "result.json"
    monkeypatch.setattr(join.os, "write", lambda *_args: 0)
    with pytest.raises(OSError, match="made no progress"):
        join.publish_metadata(output, "{}")
    assert list(tmp_path.iterdir()) == []


def test_publication_does_not_create_missing_parents(tmp_path: Path) -> None:
    parent = tmp_path / "missing"
    with pytest.raises(FileNotFoundError):
        join.publish_metadata(parent / "result.json", "{}")
    assert not parent.exists()


def test_a_ledger_that_grew_past_the_frozen_baseline_still_joins(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """The ledger only grows; dropping or renaming a baseline class is still refused.

    The frozen baseline's census admits 60 classes, and exp-317 admitted twelve more
    after it was frozen. The projection rests on the frozen census, so later admissions
    leave it unchanged, while a ledger that no longer admits a baseline class, or admits
    it under another name, does not describe the census any more.
    """
    source = join.REPO / "packing/campaign/issue-intake/n17-20261008/github-issues.json"
    document = join.read_document(source)
    real_load = join.load_yaml

    def ledger_with(change: Any) -> Any:
        def load(text: str) -> Any:
            ledger = real_load(text)
            if isinstance(ledger, dict) and "entries" in ledger:
                change(ledger["entries"])
            return ledger

        return load

    def drop_first_admitted(entries: list[dict[str, Any]]) -> None:
        entries.remove(next(entry for entry in entries if entry["status"] == "admitted"))

    def rename_first_admitted(entries: list[dict[str, Any]]) -> None:
        next(entry for entry in entries if entry["status"] == "admitted")["name"] = "renamed"

    for change in (drop_first_admitted, rename_first_admitted):
        monkeypatch.setattr(join, "load_yaml", ledger_with(change))
        with pytest.raises(join.RefusedError, match="ledger/census class identities differ"):
            join.reconcile(document, deadline=time.monotonic() + 30)
