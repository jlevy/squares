---
type: is
id: is-01m3qvn66t22qdk6fjsfbrns1r
title: "W7: reconcile current upstream provider results and integrate PR246"
kind: task
status: closed
priority: 1
version: 3
spec_path: packing/campaign/agent-sessions/session-164-upstream-merge-and-certification.md
labels:
  - W7
dependencies: []
parent_id: is-01m3qcan8g6wnnpkvaemzt7rfm
child_order_hints:
  - is-01m3qvth7kp6exefpeegtb7q4x
created_at: 2026-09-30T00:32:58.570Z
updated_at: 2026-09-30T16:08:32.689Z
closed_at: 2026-09-30T16:08:32.687Z
close_reason: Current main 886b1783a35e99f9f250894e9b0492f1fc7e0bf3 is integrated. Provider claims and historical ID mappings are reconciled, lazy reports classified without promotion, reader/data views agree, and required packing/Pages/mergeability pass at 180326e81. Separate unmerged PR249 remains coordinated through think-d15x.
resolution: null
duplicate_of: null
---
Refresh origin/main at execution and record its immutable SHA. At creation GitHub main is 886b1783a35e99f9f250894e9b0492f1fc7e0bf3 (PR248), already ancestry-merged into local cb7bc3998228b7102f42ecc7cbac4ab68bf25355 but not published or finally certified. Reconcile all provider results landed since the last certified PR integration, including Couzo/de Winter T-056/T-057 and wand125 canonical T-058/T-059. Inventory new claims, preserve pinned sources and credit, assign explicit V/C/S plus novelty and significance rationale/date/scorer to every imported result under epistemics.md, and retain exact scope, evidence, controls, gaps and next-rung beads. Preserve archived provisional identifiers with mappings; do not overwrite evidence or promote from samples. Integrate any newly arrived main commits without losing current W7 work. Finish affected generated views and release/atlas consistency once at the integration checkpoint, then publish and verify required automatic final-head checks. General slow repository testing is batched and kept outside proof-tool iteration; do not manually repeat full checkpoints. Acceptance: upstream delta accounted for, every qualifying result registered and scored, no unresolved ID collision, current reader views, preserved proof receipts, final-head integration evidence, and PR comment documenting remaining mathematical gaps.
