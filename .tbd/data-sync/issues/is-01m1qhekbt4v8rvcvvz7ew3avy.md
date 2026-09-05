---
type: is
id: is-01m1qhekbt4v8rvcvvz7ew3avy
title: SYNOPSIS says four restricted optima were measured; the reach table now shows seven reports and one artifact
kind: bug
status: in_progress
priority: 2
version: 2
labels: []
dependencies: []
parent_id: is-01m1qcc9devr6mz0m6erxswxjc
created_at: 2026-09-05T01:03:13.273Z
updated_at: 2026-09-05T01:06:47.784Z
---
Found by the F26 port (think-k581): SYNOPSIS.md still says 'only four restricted optima have ever been measured' and names them (line ~3705), and separately narrates the 4.68 report (line ~444), while the reach table now lists seven reported covering values with their evidence status and shows exactly one is recomputable from a tracked artifact (and it is a feasible mass, not an optimum). The same F26 class in the parent's own prose; check_synopsis does not cross-check it. Fix the sentences against CERTIFICATE-REACH.md's table and consider a check_synopsis rule that holds the count to the renderer's table.
