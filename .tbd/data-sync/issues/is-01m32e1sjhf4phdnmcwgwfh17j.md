---
type: is
id: is-01m32e1sjhf4phdnmcwgwfh17j
title: Renumber PR 211's T-031 to T-032 (positional contiguity, 32 of 33 occurrences)
kind: task
status: open
priority: 1
version: 1
labels: []
dependencies: []
parent_id: is-01m2yydf84rfedhb6zj3x2dzjn
created_at: 2026-09-21T16:51:08.496Z
updated_at: 2026-09-21T16:51:08.496Z
---
Verified against check_results.py:186-189: contiguity is POSITIONAL. expected_ids = [f'T-{i:03d}' for i in range(1, len(results)+1)] must equal the ids in array ORDER. So renumbering the row also means MOVING it after the stack's T-031 in results.yaml. Next free id is T-032 once the stack lands (main tops out at T-030; the stack adds T-031). Re-verify on the tip that actually lands with: git show <tip>:packing/frontier/results.yaml | grep -c '^  - id: T-'

33 occurrences across 16 files. EXACTLY ONE must NOT be renumbered:
  packing/campaign/agent-sessions/session-141-n100-research.md:769 -- a '## T-id recipe' forward-pointer that exists verbatim on main and that PR 211 does not touch.

So 32 change, in 15 files.

FOUR are generated -- regenerate, never hand-edit:
  packing/frontier/RESULTS.md:32,:68 (render_results --update)
  packing/campaign/ledger.md:160 (packing-ledger render; its text is session-148's next_action, so fix session-148-n17-external-intake.md:195 and re-render)
  SYNOPSIS.md:104 (inside the results-headline generated block)

TWENTY-EIGHT are hand-edit:
  results.yaml:1779 (+ move the whole 82-line row)
  n-017.md:53,:169  n-018.md:53
  README.md:137,138,193,221,282
  SYNOPSIS.md:1033,1037,1101
  docs/project/handoff-2026-09-21-n17-external-intake.md:14,:41
  docs/project/specs/active/plan-2026-08-23-overnight-cartography-run.md:345
  packages/workbench/tools/workbench_tools/check_layout.py:73
  packing/campaign/agent-sessions/session-148-n17-external-intake.md:88,103,110,127,162,195,236
  packing/devtools/audit_ds7_lower_bounds.py:91
  packing/devtools/check_rung_figures.py:105
  packing/tests/test_audit_ds7_lower_bounds.py:92
  packing/tests/test_rung_figures.py:686,:700

SEVEN of those are narrative ABOUT the collision ('pull request 208 claims T-031'). Substituting T-032 makes them false. conventions.md:88-91 requires the renumber be recorded as an annotation, never a silent edit, so rewrite them to record the resolution: the stack kept T-031, this result took T-032. They are SYNOPSIS.md:1037,:1101, handoff:41, plan-2026-08-23:345, session-148-n17:195,:236, and ledger.md:160 via :195.
