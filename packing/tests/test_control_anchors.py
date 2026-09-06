#!/usr/bin/env python3
"""A negative control whose anchor no longer matches is not testing anything.

`D-403`. The control suite runs only in the full gate and a pull request runs `--fast`, so
six of a hundred and fifty had stopped firing before anyone looked. One had been broken
hours earlier by inserting a field into the middle of the block it anchored on; two more
anchored source the formatter had since wrapped.
"""

from __future__ import annotations

import re
from pathlib import Path

import pytest

import devtools.check_control_anchors as anchors
from devtools.check_control_anchors import CONTROLS, main
from sqpack.yamlio import safe_load


def controls() -> list[dict]:
    document = safe_load(CONTROLS.read_text(encoding="utf-8"))
    return document if isinstance(document, list) else document.get("controls", [])


def test_every_anchor_resolves() -> None:
    assert main() == 0


def test_the_suite_is_the_size_it_claims() -> None:
    """A shrinking suite is the failure this cannot otherwise see."""
    assert len(controls()) >= 150


def test_every_control_has_a_two_item_replace() -> None:
    for control in controls():
        replace = control.get("replace")
        assert isinstance(replace, list), control.get("name")
        assert len(replace) == 2, control.get("name")
        assert replace[0] != replace[1], control.get("name")


def test_a_broken_anchor_is_refused(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    """The guard has to bite; one that only ever passes is what D-403 is about."""
    spec = tmp_path / "controls.yaml"
    spec.write_text(
        "- name: fabricated\n"
        "  file: devtools/check_control_anchors.py\n"
        '  replace: ["a string that is definitely not in that file", "x"]\n'
        "  run: true\n"
        '  expect: "nothing"\n',
        encoding="utf-8",
    )
    monkeypatch.setattr(anchors, "CONTROLS", spec)
    assert anchors.main() == 1


def test_an_anchor_matching_twice_is_refused(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    """Two matches is as useless as none: the runner cannot know which one it mutated."""
    target = tmp_path / "twice.txt"
    target.write_text("repeated\nrepeated\n", encoding="utf-8")
    spec = tmp_path / "controls.yaml"
    spec.write_text(
        "- name: fabricated\n"
        f"  file: {target}\n"
        '  replace: ["repeated\\n", "x\\n"]\n'
        "  run: true\n"
        '  expect: "nothing"\n',
        encoding="utf-8",
    )
    monkeypatch.setattr(anchors, "CONTROLS", spec)
    monkeypatch.setattr(anchors, "ROOT", tmp_path)
    assert anchors.main() == 1


def test_the_injected_operating_rule_is_the_next_free_id() -> None:
    """A control that injects a *new* rule must inject one that does not exist yet.

    This broke twice on 2026-09-06 and cost `main` a red gate the second time. The
    control named below appends a rule to `operating-rules.md` and expects the renderer
    to report that `AGENTS.md`'s summary has drifted, which is only what happens when the
    injected rule is a legitimate next one. Inject an id that already exists and the
    renderer reports a duplicate instead; inject one past the end and it reports a gap.
    Either way the control fires with the wrong message and the suite calls it a failure
    -- correctly, but the message names contiguity rather than the stale literal, so the
    reader is sent to the wrong file.

    The anchor is fine in both cases, which is why `test_every_anchor_resolves` does not
    catch it: what goes stale is the *payload*, not the thing it attaches to. This runs in
    the quick lane so a rule added in a pull request fails there rather than after a merge,
    which is how the second occurrence reached `main`.
    """
    rules = (anchors.ROOT.parent / "operating-rules.md").read_text(encoding="utf-8")
    highest = max(int(m) for m in re.findall(r"^### OR-(\d+)", rules, re.M))
    control = next(
        item
        for item in controls()
        if item["name"] == "operating rules - a new rule never reaches the summary"
    )
    injected = re.search(r"## OR-(\d+):", "\n".join(control["replace"]))
    assert injected is not None, "the control no longer injects a rule heading"
    assert int(injected[1]) == highest + 1, (
        f"the control injects OR-{injected[1]} while operating-rules.md ends at "
        f"OR-{highest}; it must inject OR-{highest + 1} to be a new rule rather than a "
        "duplicate or a gap"
    )
