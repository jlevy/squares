---
type: is
id: is-01m2heytmvgrt230zck1n4f68a
title: "PR #160 review D13: check_probes runs on no PR surface and passes a name in a missing group"
kind: bug
status: closed
priority: 2
version: 3
labels: []
dependencies: []
parent_id: is-01m2hb40z4hvrre5f0219zp1m9
created_at: 2026-09-15T02:39:54.522Z
updated_at: 2026-09-15T02:40:54.423Z
closed_at: 2026-09-15T02:40:54.422Z
close_reason: "Fixed on #160 at c78a9b31: the frontend step runs check_probes before the Chromium checks, and every constant name handed to the loader or a wrapper of it must resolve whatever its group; negative test in packages/workbench/tests/test_check_probes.py. The check_frontend port of the gap-bar assertion is lane D-page's."
resolution: null
duplicate_of: null
---
Review finding, PR #160 stack triage (2026-09-14), lane D-tools.

The page's behavioural checks ran on no PR surface, and `check_probes` resolved a missing name only when its first segment was an existing probe group, so `newgroup/zz_missing` passed.

Sources: #125 F9 (wiring and `check_probes` items); #155 R11 (not-in-CI item); #160 R21 (wiring item). Related: think-kpvc.

Files: `packing/src/sqpack/cli/validate.py` (frontend step), `packages/workbench/tools/workbench_tools/check_probes.py:139-140`. The `check_frontend` port of `check_workbench.py:575-594` belongs to lane D-page.
