"""A retained JSON file over the threshold is written in `sqpack.retained_json`'s layout.

`devtools.check_retained_json` is the sweep that keeps the convention from eroding one
`indent=2` writer at a time. These tests plant each failure it exists to catch in a small
tree of its own, and hold the repository's own tree to it.
"""

from __future__ import annotations

import json
import subprocess
from pathlib import Path
from typing import Any

import pytest

from devtools import check_retained_json as sweep
from devtools.check_retained_json import Exemption, Policy
from sqpack import retained_json

#: Small enough that a ten-record document is over it, written either way.
THRESHOLD = 12
RECORDS: dict[str, Any] = {
    "contract": "example/v1",
    "rows": [{"n": n, "side": f"{n}/7", "ok": n % 2 == 0} for n in range(10)],
}


def _policy(*exemptions: Exemption) -> Policy:
    return Policy(THRESHOLD, exemptions)


def _exempt(pattern: str, reason: str = "digest-bound", *, glob: bool = False) -> Exemption:
    bead = "think-test" if reason == "pending" else None
    return Exemption(pattern, glob, reason, "a test names its bytes", bead)


def _write(root: Path, relative: str, text: str) -> Path:
    path = root / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return path


def _indented(document: Any = RECORDS) -> str:
    return json.dumps(document, indent=2) + "\n"


def _laid(document: Any = RECORDS) -> str:
    return retained_json.dumps(document)


def _failures(root: Path, policy: Policy) -> list[str]:
    failures, _ = sweep.check(root, policy=policy)
    return failures


def test_the_repository_as_it_stands_passes() -> None:
    failures, held = sweep.check()
    assert failures == []
    assert held > 0


def test_the_policy_reads_and_every_entry_has_its_reason() -> None:
    policy = sweep.load_policy()
    assert policy.threshold_lines == 5000
    assert {entry.reason for entry in policy.exemptions} <= sweep.REASONS
    assert all(entry.bound_by.strip() for entry in policy.exemptions)


def test_an_indented_result_over_the_threshold_fails(tmp_path: Path) -> None:
    _write(tmp_path, "results/census.json", _indented())
    failures = _failures(tmp_path, _policy())
    assert len(failures) == 1
    assert failures[0].startswith("results/census.json: ")
    assert "not in the retained layout" in failures[0]
    assert "--fix" in failures[0]


def test_the_same_result_in_the_layout_passes(tmp_path: Path) -> None:
    document = {"rows": [{"n": n, "pad": "x" * 30} for n in range(40)]}
    assert _laid(document).count("\n") > THRESHOLD
    _write(tmp_path, "results/census.json", _laid(document))
    assert _failures(tmp_path, _policy()) == []
    # The layout is the shared writer's at its own width; another width is another layout.
    narrow = retained_json.dumps(document, width=40)
    assert narrow != _laid(document)
    _write(tmp_path, "results/census.json", narrow)
    assert len(_failures(tmp_path, _policy())) == 1


def test_a_hand_edited_line_fails_even_with_the_same_value(tmp_path: Path) -> None:
    document = {"rows": [{"n": n, "pad": "x" * 60} for n in range(40)]}
    text = _laid(document)
    edited = text.replace('{"n":3,', '{"n": 3,', 1)
    assert json.loads(edited) == json.loads(text)
    _write(tmp_path, "results/census.json", edited)
    assert len(_failures(tmp_path, _policy())) == 1


def test_a_file_at_or_under_the_threshold_is_never_read_past_its_size(tmp_path: Path) -> None:
    """The sweep's cost is the tree's few large files, not its thousands of small ones."""
    _write(tmp_path, "small.json", "{\n" + "  not json at all\n" * (THRESHOLD - 1))
    assert _failures(tmp_path, _policy()) == []


def test_ensure_ascii_is_read_off_the_bytes(tmp_path: Path) -> None:
    """A writer that keeps non-ASCII raw and one that escapes it both pass: the sweep
    reads which one wrote a file from its bytes rather than asking."""
    document = {"rows": [{"name": f"Bašić {n}", "pad": "y" * 950} for n in range(20)]}
    raw = retained_json.dumps(document, ensure_ascii=False)
    escaped = retained_json.dumps(document)
    assert not raw.isascii()
    assert escaped.isascii()
    for text in (raw, escaped):
        assert text.count("\n") > THRESHOLD
        _write(tmp_path, "results/names.json", text)
        assert _failures(tmp_path, _policy()) == []
    _write(tmp_path, "results/names.json", json.dumps(document, indent=2, ensure_ascii=False))
    assert len(_failures(tmp_path, _policy())) == 1


def test_schemas_and_biome_owned_json_are_not_swept(tmp_path: Path) -> None:
    _write(
        tmp_path,
        "biome.json",
        json.dumps({"files": {"includes": ["packages/web/**/*.json", "!vendor", "**/*.ts"]}}),
    )
    _write(tmp_path, "packages/web/tests/fixtures/big.json", _indented())
    _write(tmp_path, "records/result.schema.json", _indented())
    assert _failures(tmp_path, _policy()) == []
    _write(tmp_path, "packages/other/big.json", _indented())
    assert [line.split(":")[0] for line in _failures(tmp_path, _policy())] == [
        "packages/other/big.json"
    ]


def test_an_exempt_file_is_left_alone(tmp_path: Path) -> None:
    _write(tmp_path, "results/pinned.json", _indented())
    _write(tmp_path, "archive/a/source.json", _indented())
    _write(tmp_path, "archive/b/source.json", _indented())
    policy = _policy(
        _exempt("results/pinned.json"), _exempt("archive/**", "archive", glob=True)
    )
    assert _failures(tmp_path, policy) == []


def test_an_exemption_that_covers_nothing_fails(tmp_path: Path) -> None:
    """The list only shrinks: an entry outliving its reason is a failure, not slack."""
    _write(tmp_path, "results/small.json", _laid({"n": 1}))
    _write(tmp_path, "results/big.json", _indented())
    policy = _policy(
        _exempt("results/big.json"),
        _exempt("results/gone.json"),
        _exempt("results/small.json"),
        _exempt("nowhere/**", "archive", glob=True),
    )
    failures = _failures(tmp_path, policy)
    assert len(failures) == 3
    assert any(
        line.startswith("results/gone.json: ") and "is gone" in line for line in failures
    )
    assert any(
        line.startswith("results/small.json: ") and "not over the threshold" in line
        for line in failures
    )
    assert any(
        line.startswith("nowhere/**: ") and "matches no tracked" in line for line in failures
    )


def test_a_pending_conversion_already_made_fails_until_its_entry_goes(tmp_path: Path) -> None:
    document = {"rows": [{"n": n, "pad": "z" * 990} for n in range(20)]}
    _write(tmp_path, "results/converted.json", _laid(document))
    pending = _policy(_exempt("results/converted.json", "pending"))
    [failure] = _failures(tmp_path, pending)
    assert "pending (think-test) but already in the retained layout" in failure
    # A digest-bound file is not re-laid to ask: whatever binds it would break first.
    assert _failures(tmp_path, _policy(_exempt("results/converted.json"))) == []
    assert _failures(tmp_path, _policy()) == []


def test_fix_re_lays_without_changing_the_value(tmp_path: Path) -> None:
    path = _write(tmp_path, "results/census.json", _indented())
    assert sweep.fix([path], tmp_path, policy=_policy()) == []
    text = path.read_text(encoding="utf-8")
    assert text == _laid()
    assert sweep.canonical(json.loads(text)) == sweep.canonical(RECORDS)
    assert _failures(tmp_path, _policy()) == []


def test_fix_refuses_a_duplicate_key_rather_than_dropping_it(tmp_path: Path) -> None:
    original = '{\n "n": 1,\n "n": 2\n}\n'
    path = _write(tmp_path, "results/duplicate.json", original)
    [refusal] = sweep.fix([path], tmp_path, policy=_policy())
    assert "duplicate keys ['n']" in refusal
    assert path.read_text(encoding="utf-8") == original


def test_fix_refuses_a_file_exempt_for_its_bytes(tmp_path: Path) -> None:
    original = _indented()
    path = _write(tmp_path, "results/pinned.json", original)
    [refusal] = sweep.fix([path], tmp_path, policy=_policy(_exempt("results/pinned.json")))
    assert "exempt (digest-bound" in refusal
    assert path.read_text(encoding="utf-8") == original
    pending = _policy(_exempt("results/pinned.json", "pending"))
    assert sweep.fix([path], tmp_path, policy=pending) == []
    assert path.read_text(encoding="utf-8") == _laid()


def test_canonical_tells_apart_what_equality_does_not() -> None:
    assert json.loads("[1]") == json.loads("[1.0]") == json.loads("[true]")
    assert len({sweep.canonical(json.loads(text)) for text in ("[1]", "[1.0]", "[true]")}) == 3
    assert sweep.canonical({"a": 1, "b": 2}) != sweep.canonical({"b": 2, "a": 1})


def test_the_sweep_reads_the_tracked_tree_and_not_the_working_directory(
    tmp_path: Path,
) -> None:
    """Scratch output in a checkout is not a retained result, so it cannot fail the step."""
    subprocess.run(("git", "-C", str(tmp_path), "init", "-q"), check=True)
    _write(tmp_path, "scratch.json", _indented())
    assert _failures(tmp_path, _policy()) == []
    subprocess.run(("git", "-C", str(tmp_path), "add", "scratch.json"), check=True)
    assert len(_failures(tmp_path, _policy())) == 1


@pytest.mark.parametrize(
    ("entry", "message"),
    [
        ({"path": "a.json", "reason": "archive"}, "needs a bound_by"),
        ({"path": "a.json", "reason": "tidy", "bound_by": "x"}, "reason must be one of"),
        ({"path": "a.json", "reason": "pending", "bound_by": "x"}, "names its bead"),
        (
            {"path": "a.json", "reason": "frozen", "bound_by": "x", "bead": "b"},
            "names its bead",
        ),
        ({"reason": "frozen", "bound_by": "x"}, "exactly one of path or glob"),
        ({"path": "a.json", "reason": "frozen", "bound_by": "x", "note": 1}, "unknown keys"),
    ],
)
def test_a_malformed_policy_entry_is_refused(
    tmp_path: Path, entry: dict[str, Any], message: str
) -> None:
    policy = tmp_path / "retained-json.yaml"
    policy.write_text(json.dumps({"threshold_lines": 10, "exempt": [entry]}), encoding="utf-8")
    with pytest.raises(ValueError, match=message):
        sweep.load_policy(policy)


def test_globs_cross_directories_only_where_they_say_so() -> None:
    entry = _exempt("packing/cases/*_certificate/*.json", "certificate", glob=True)
    assert entry.matches("packing/cases/n11_fractional_certificate/certificate.json")
    assert not entry.matches("packing/cases/n11_fractional_certificate/deep/certificate.json")
    archive = _exempt("packing/resources/**", "archive", glob=True)
    assert archive.matches("packing/resources/web/a/b/c.json")
    assert not archive.matches("packing/resourcesx/a.json")
