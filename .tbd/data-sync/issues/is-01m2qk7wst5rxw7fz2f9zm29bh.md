---
type: is
id: is-01m2qk7wst5rxw7fz2f9zm29bh
title: "Relational atoms at 153/40: run replacement-support column generation to convergence as a checkpointed tool"
kind: task
status: open
priority: 2
version: 1
spec_path: docs/project/specs/active/plan-2026-09-10-n11-daytime-strategy-and-explainer.md
labels:
  - n11
  - research
dependencies: []
parent_id: is-01m2exznj4k1zyz1rczby8ch2k
created_at: 2026-09-17T11:50:12.537Z
updated_at: 2026-09-17T11:50:12.537Z
---
From the 2026-09-17 overnight M1 lane (think-4woh; attic report block3/M1-report.txt on branch claude/n11-overnight-2026-09-17, summarised in X-037). Budget-one clique atoms and Chvatal-Gomory floor atoms (devtools.plateau_reader K4/K5/K6) cut every retained obstruction family at 153/40, but column generation over the pose net rebuilt an exact mass-11 depth<=1 replacement family within about ten pricing rounds, repeatedly (8 separations in 45 minutes, no terminal state). The decisive question -- does the chase terminate below 11 (a certificate candidate for a language beyond the threshold plateau) or at a mass-11 family satisfying every admissible atom (a new plateau) -- needs the scratch colgen4 loop turned into a guarded devtools module (OR-1) with checkpoints, deterministic receipts and an independent reader, run for hours. Blocked by the owner's atom-format decision think-g3j7 for any retained certificate, and by the missing sites-1 row checkpoint (see sibling bead).
