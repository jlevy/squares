---
type: is
id: is-01m2hh8ja7yhzapce2vvxabdmx
title: "PR #160 review D60: new page assertions cannot fail"
kind: bug
status: closed
priority: 2
version: 2
labels: []
dependencies: []
parent_id: is-01m2hb40z4hvrre5f0219zp1m9
created_at: 2026-09-15T03:20:10.822Z
updated_at: 2026-09-15T03:32:52.028Z
closed_at: 2026-09-15T03:32:52.027Z
close_reason: "Fixed on PR #160 in e0f67fe7 (facts handover check independent of the page's matching rule, text-only slots and the 0.2 s window included), c68b6e93 (headline roll, drawn-text owners and one-line slots, headline space; each fails against a mutant), 3dfc7f11 and 46b8f14e (port and retirement of the legacy checkers)."
resolution: null
duplicate_of: null
---
Canonical defect D60 from the 2026-09-14 stack triage (Medium). Source: #155 R11 (assertion items).

New page assertions could not fail: the `faded` minimum included seek(0); `headline/still.js` read a transform the page no longer writes and checked one layer; `facts/handover.js` skipped text-only slots, never checked the 0.2 s crossfade, and the going-and-coming guard skipped one-sided changes; the "removed" checks tested names (`#kind-tag`, `.exact`). Ten of 21 mutations still passed `check_workbench.py`.

Files: `packages/workbench/tools/workbench_tools/check_workbench.py` (~:3172-3175, :3191, :3213, :2557), `packages/workbench/probes/headline/still.js` (:19, :28-29), `packages/workbench/probes/facts/handover.js` (:14-34) @bb3f7c99. Related: think-kpvc, think-cqfc, think-7sw8, think-xvjf.
