---
type: is
id: is-01m4cp9qgvddm5me0d2xx3zw7b
title: Reconcile Mac external-storage test timing and Linux RSS assumptions
kind: task
status: in_progress
priority: 2
version: 7
spec_path: docs/project/specs/active/plan-2026-10-06-exact-side-values.md
delegate: codex@spud10
labels: []
dependencies: []
parent_id: is-01m4cee7q2jdj5scgd5wa72y24
hold: null
hold_until: null
created_at: 2026-10-08T02:43:23.290Z
updated_at: 2026-10-08T09:35:49.600Z
started_at: 2026-10-08T03:54:55.934Z
---
PR435 whole-suite Mac run at fa93843ed exposed unchanged tests beyond the supported local edit floor: profile_n17_kernel_memory assumes non-null RSS readings; a negative-control tree snapshot hit its180s timeout; fake Rust-server startup tests exceeded0.5s/2s expectations before processing; reachable-progress child exceeded30s startup. Supported development.md assigns the complete checkpoint to Linux, while source and temporary files here must stay on the external volume. Diagnose with isolated bounded controls, preserve timeout/non-promotion safety contracts, and distinguish platform capability from a busy external filesystem. No precise performance cause is claimed from one contended run. Do not raise global gate ceilings or move caches/builds back onto the internal disk. Full run evidence is /Volumes/spud-ext1/agent-evidence/polynomial-catalogue-01a118e4/validation/mac-push.log.

## Notes

Final source-tail local push on frozen CPython3.14.7:1093.99s total, one failed step because reachable behavioral tests timed out at901.02s against900s; all other applicable floor steps passed, including exact register replay31.93s. Raw output reaches94 percent pytest progress but exposes no unfinished node or stack; no correctness failure was identified, and the cause is unresolved. Targeted process checks confirm the gate workers and trackers8675/8946 ended. No per-worker progress receipts were enabled: env.sh and command omit PACKING_VALIDATION_ARTIFACT_DIR. Preserve raw push-final-tail.log under external agent-evidence validation; future reproduction should enable that existing progress instrumentation, use the same source/shape, and diagnose the exact stalled node before changing production behavior. Keep ceilings and external-storage policy intact. Final Linux checkpoint on clean1d094ccb114a46d9836581c7ac8157593939817e is37724292281; PR Packing and Pages on that head already pass. Earlier Mac startup/RSS/copy failures remain separately evidenced in mac-push.log.

Web precommit Mac push, 2026-10-08: 1020.89 s wall, reachable step 907.27 s; 12,718 passed, 14 failed, 214 setup errors. Eleven failures concern unchanged process startup, child-pytest timing, snapshot copy or RSS/profiling controls; three solver-snapshot failures belong to think-e4qp. The 214 site setup errors cascade from the deliberate HEAD-tree link contract seeing five newly staged documents; rerun publication on the committed web head before attributing those to platform behavior. Full raw evidence is agent-evidence/polynomial-catalogue-01a118e4/validation/web-push.log on the external volume. Focused web tests pass 57 in 9.13 s. Ceilings unchanged; no claim of a precise contention cause. Gate subprocesses have exited.
