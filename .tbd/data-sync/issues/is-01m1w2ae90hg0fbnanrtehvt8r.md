---
type: is
id: is-01m1w2ae90hg0fbnanrtehvt8r
title: "W5: measure and simplify mutation snapshot dependency retention"
kind: task
status: open
priority: 2
version: 1
spec_path: docs/project/specs/active/plan-2026-09-06-validation-efficiency-and-checkpoints.md
labels: []
dependencies: []
parent_id: is-01m1vrrktbrd2scnaqfe40eby4
created_at: 2026-09-06T19:15:00.511Z
updated_at: 2026-09-06T19:15:00.511Z
---
PR97+PR98 integrated source measured67,801,700 bytes against64MiB mutation-snapshot storage cap. Caches and generator-owned outputs were already excluded. No safe further exclusion was established; benchmark checkpoint pruning is undone by mandatory linked-target restoration. Xz-compressing809,937B summarylog would save733,533B but leave only40,697B headroom. Preserve frozen evidence and intended control refusals; cap raised deliberately to80MiB as bounded capacity headroom, without claiming a performance gain. Follow-up should use maintained per-path census and traced checker inputs to reduce actual copies only with green unmutated baselines and equivalent mutation outcomes; do not remove files merely because no control directly mutates them.
