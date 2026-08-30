#!/usr/bin/env python3
"""Every negative control's anchor still matches the file it names, exactly once.

`D-403`. The control suite runs only in the full gate, and a pull request runs `--fast`, so
a branch can be green on every push for its whole life while its controls rot. Six of a
hundred and fifty were not firing when that was noticed, and one of them had been broken
hours earlier by inserting a field into the middle of the block it anchored on.

A control that does not fire is worse than an absent one, because the suite reports a count
that reads as coverage. `run_negative_controls` is honest about this -- it refuses an
anchor matching other than exactly once, and distinguishes "failed with the expected
message" from "failed, but not with the expected message" -- but that information only
exists once someone has spent half an hour running it.

This resolves anchors without running anything: no snapshot, no mutation, no subprocess,
no restore. It is string containment over the files the controls already name, which makes
it a `--records` step and puts the answer seconds after the edit that breaks it rather
than a merge later.

It deliberately does NOT check that a control still *catches* what it was written for.
That needs the mutation and the command, and it is what the full suite is for. Passing here
means every control can still fire, which is a strictly weaker and much cheaper claim.

Usage, from `packing/`:
    uv run --frozen --all-extras --group dev python -m devtools.check_control_anchors
"""

from __future__ import annotations

import sys
from pathlib import Path

from devtools.run_negative_controls import resolve_control_target
from sqpack.yamlio import safe_load

ROOT = Path(__file__).resolve().parent.parent
CONTROLS = ROOT / "devtools" / "controls.yaml"


def main() -> int:
    document = safe_load(CONTROLS.read_text(encoding="utf-8"))
    controls = document if isinstance(document, list) else document.get("controls", [])

    problems: list[str] = []
    checked = 0

    for control in controls:
        name = control.get("name", "<unnamed>")
        replace = control.get("replace")
        if not isinstance(replace, list) or len(replace) != 2:
            problems.append(f"{name}: replace must be a two-item [old, new] list")
            continue

        # The runner's own resolver, so this cannot drift from what it checks. `tree` and
        # `work` are the real checkout here rather than a snapshot, which is the point:
        # the anchors have to match the tree a session is editing.
        try:
            target = resolve_control_target(control.get("file"), tree=ROOT.parent, work=ROOT)
        except ValueError as error:
            problems.append(f"{name}: {error}")
            continue

        old = replace[0]
        try:
            text = target.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            problems.append(f"{name}: {control['file']} is not UTF-8")
            continue

        found = text.count(old)
        if found != 1:
            excerpt = old.strip().splitlines()[0][:70] if old.strip() else "<empty>"
            problems.append(
                f"{name}: anchor appears {found} times in {control['file']}, expected 1"
                f"\n      first line of the anchor: {excerpt}"
            )
            continue
        checked += 1

    if problems:
        print(f"{len(problems)} of {len(controls)} negative controls cannot fire:")
        for problem in problems:
            print(f"  {problem}")
        print("\n  A control whose anchor does not match is not testing anything.")
        return 1

    print(f"{checked} negative control anchors each match their file exactly once")
    return 0


if __name__ == "__main__":
    sys.exit(main())
