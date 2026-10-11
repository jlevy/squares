---
type: is
id: is-01m45jbcd572ww0nz30knjpy6k
title: "Session 182 W5 block: gate walls and producer self-check against the standing verifier (OR-12)"
kind: task
status: open
priority: 2
version: 1
spec_path: docs/project/specs/active/plan-2026-10-05-n17-overnight.md
labels: []
dependencies: []
parent_id: is-01m3xkd6zmq1jqwtn628h2k7zy
created_at: 2026-10-05T08:19:42.117Z
updated_at: 2026-10-05T08:19:42.117Z
---
OR-12 W5 block added at session-182's W10 phase: the count read from the ledger is at least eight (34 terminal cells since BC-369, the last efficiency-loop cell; 9 terminal sessions since session-180's efficiency-loop phase). Measures packing-validate --edit and --push against their ceilings (240 s, 1,800 s) and the kernel producer's in-process self-check against the standing kernel verifier per row (0.91 against 0.18 s a row on N1) from tonight's lane A and K receipts. No extra compute while lanes A and K hold the CPUs.
