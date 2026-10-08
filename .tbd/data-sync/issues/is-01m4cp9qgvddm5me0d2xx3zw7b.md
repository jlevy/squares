---
type: is
id: is-01m4cp9qgvddm5me0d2xx3zw7b
title: Reconcile Mac external-storage test timing and Linux RSS assumptions
kind: task
status: in_progress
priority: 2
version: 2
spec_path: docs/project/specs/active/plan-2026-10-06-exact-side-values.md
delegate: codex-polynomial-01a118e4
labels: []
dependencies: []
parent_id: is-01m4cee7q2jdj5scgd5wa72y24
hold: null
hold_until: null
created_at: 2026-10-08T02:43:23.290Z
updated_at: 2026-10-08T03:54:55.935Z
started_at: 2026-10-08T03:54:55.934Z
---
PR435 whole-suite Mac run at fa93843ed exposed unchanged tests beyond the supported local edit floor: profile_n17_kernel_memory assumes non-null RSS readings; a negative-control tree snapshot hit its180s timeout; fake Rust-server startup tests exceeded0.5s/2s expectations before processing; reachable-progress child exceeded30s startup. Supported development.md assigns the complete checkpoint to Linux, while source and temporary files here must stay on the external volume. Diagnose with isolated bounded controls, preserve timeout/non-promotion safety contracts, and distinguish platform capability from a busy external filesystem. No precise performance cause is claimed from one contended run. Do not raise global gate ceilings or move caches/builds back onto the internal disk. Full run evidence is /Volumes/spud-ext1/agent-evidence/polynomial-catalogue-01a118e4/validation/mac-push.log.
