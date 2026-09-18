---
type: is
id: is-01m2qk7y4msb762704fz3hyytv
title: Retain or regenerate the sites-1 rows-complete checkpoint at 153/40
kind: task
status: open
priority: 2
version: 3
spec_path: docs/project/specs/active/plan-2026-09-10-n11-daytime-strategy-and-explainer.md
labels:
  - n11
  - research
dependencies: []
parent_id: is-01m2exznj4k1zyz1rczby8ch2k
created_at: 2026-09-17T11:50:13.907Z
updated_at: 2026-09-18T06:16:35.526Z
---
The rows-complete covering LP at 153/40 (15,021 rows over 17,389 sites, the A6 sites-1 checkpoint) exists only as unretained scratch on another host, which blocked the decisive M1 test on 2026-09-17 (think-4woh). Regenerate it with the repository's own producer, retain it under a deterministic, source-bound receipt (size permitting, or a regeneration command plus digest), and record the command, cost and location, so relational-atom columns can be tested against the real rows-complete LP.

## Notes

Session 139 Lane B (2026-09-18): A6 153/40 sites-1 matrix is not in-repo (no sites.json/atoms.json/rows.json; lp-run4 unretained). run_fractional_colgen cannot emit it. Landed packing/devtools/regenerate_sites1_checkpoint.py (OR-1 retain-or-refuse). --check writes nothing. Real run wrote packing/campaign/series/series-000-smoke-and-calibration/results/agenda-037/sites-1-receipt.json status=missing-inputs rows_complete=false producer_ready=false. Missing: agenda-037/lp-run4/{sites,atoms,rows}.json plus sepcore.FamilyGeometry.vertex_candidates, sepcore.atom_columns, lp383.HighsLP. Present: bc-200-state-191-50.json sha256 8df0b9aa530149b44367842a2e6389949b27189df038d68e9d1afa8fd87df8c6. Commit 2fcf67546803c6ff101a10c2ba778e81372c0356. Do not close: checkpoint still missing. Regeneration was not started (producer not ready and inputs missing). think-gyzw must refuse the H-217 covering LP until this receipt is status=retained.
