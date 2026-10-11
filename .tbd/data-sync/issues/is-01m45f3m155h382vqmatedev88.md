---
type: is
id: is-01m45f3m155h382vqmatedev88
title: "PR #360 B1 (Medium): name archive/guzhou-review-a-333 in the Session 177-179 READMEs as the home of the cited BASE_REVISION commits"
kind: task
status: closed
priority: 1
version: 3
delegate: claude-code@vm
labels: []
dependencies: []
parent_id: is-01m45f3gxdbms4wekyer6s1j9e
hold: null
hold_until: null
created_at: 2026-10-05T07:23:02.053Z
updated_at: 2026-10-06T08:10:52.700Z
started_at: 2026-10-06T08:09:49.930Z
closed_at: 2026-10-06T08:10:52.700Z
close_reason: "Addressed: commit 3c6e272ff (in origin/main eb43ffe9a) adds the provenance paragraph naming tag archive/guzhou-review-a-333 (including the probes' BASE_REVISION values) to the Session 177-179 READMEs (X048-session-177-cached-collision/README.md:117, X048-session-178-full-core-ablation/README.md:94, X048-session-179-selective-halving/README.md:104). All eight cited commits (1b5340477, 9a8b4ef75, aba2b3123, 14d131c8a, 3348a22ab, a60cfc611, c6972548e, e2fe7aa8c) are ancestors of the tag at 9a1143ab9 (verified 2026-10-06)."
resolution: null
duplicate_of: null
---
Review B finding B1 on jlevy/squares#360 (https://github.com/jlevy/squares/pull/360#pullrequestreview-5411026851), at head 451154f60. probe_n17_cached_collision.py:42 (1b5340477), probe_n17_full_core_ablation.py:63 (9a8b4ef75) and probe_n17_selective_halving.py:46 (aba2b3123) cite commits that resolved only from branch guzhou/review-a-backup-333, as do 14d131c8a, 3348a22ab, a60cfc611, c6972548e, e2fe7aa8c in the records. Done: tag archive/guzhou-review-a-333 -> 9a1143ab9 preserves all eight (verified ancestors on 2026-10-05). Remaining: the README lines in the Session 177-179 explorations naming the tag, being added by the cascade lane. Close when that commit is on the layer head.
