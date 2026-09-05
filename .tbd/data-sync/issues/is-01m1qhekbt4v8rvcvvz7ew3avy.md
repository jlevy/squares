---
type: is
id: is-01m1qhekbt4v8rvcvvz7ew3avy
title: SYNOPSIS says four restricted optima were measured; the reach table now shows seven reports and one artifact
kind: bug
status: closed
priority: 2
version: 3
labels: []
dependencies: []
parent_id: is-01m1qcc9devr6mz0m6erxswxjc
created_at: 2026-09-05T01:03:13.273Z
updated_at: 2026-09-05T01:45:54.538Z
closed_at: 2026-09-05T01:45:54.537Z
close_reason: Ported/delivered (cherry-picked onto claude/port-pr80-findings from the sub-agent worktree commits 9618ba31, aac1bf57, 4c2053f9, 7356f0e8, 2e1a0c28; the last renumbered to D-452 and hand-merged with the concurrent synopsis check).
resolution: null
duplicate_of: null
---
Found by the F26 port (think-k581): SYNOPSIS.md still says 'only four restricted optima have ever been measured' and names them (line ~3705), and separately narrates the 4.68 report (line ~444), while the reach table now lists seven reported covering values with their evidence status and shows exactly one is recomputable from a tracked artifact (and it is a feasible mass, not an optimum). The same F26 class in the parent's own prose; check_synopsis does not cross-check it. Fix the sentences against CERTIFICATE-REACH.md's table and consider a check_synopsis rule that holds the count to the renderer's table.
