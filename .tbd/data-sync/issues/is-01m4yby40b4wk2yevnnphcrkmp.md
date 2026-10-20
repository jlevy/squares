---
type: is
id: is-01m4yby40b4wk2yevnnphcrkmp
title: Rebalance the type floor in broad local push checks
kind: task
status: open
priority: 2
version: 7
spec_path: docs/project/specs/active/plan-2026-10-14-ci-iteration-cost.md
delegate: null
labels: []
dependencies: []
parent_id: is-01m4xkf4v65pthd9zbd7a5a3qv
hold: null
hold_until: null
created_at: 2026-10-14T23:28:36.865Z
updated_at: 2026-10-18T19:07:00.687Z
started_at: 2026-10-18T14:32:24.447Z
---
Observed final prepush at7b802c723: after66of68checks completed by60s, the type floor remained active through180s; a process snapshot showed one BasedPyright Node process at124.2%CPU and about3.8GiB RSS. Source _type_floor sizes threads from cpus-minus-outer-jobs+1, so implicit10outer slots reserve onlyone type thread even after sibling floor work drains. The quick-test exclusive phase started around184s. Investigate a bounded allocation/scheduling fix using existing machinery, retain complete zero-finding coverage and host memory bounds, measure actual inclusive floor/push cost, and avoid a new framework or changing CI obligations. Standalone hosted typecheck already uses its own allocation; this observation is a local scheduling issue, not proof of a hosted regression. Follow stabilization.

## Notes

2026-10-19 Asia/Shanghai handback: release this performance task to open/unassigned, with no hold. No maintainable source or dependency optimization was implemented; the private worker-lifecycle candidates remain unadopted. Preserve all earlier measurements and rejected approaches below. The user now permits this laptop's local startup checks to exceed 240 seconds, which resolves a local operational constraint rather than this broader scheduling/performance objective.

A fresh unchanged-source/checker edit run passed 68/68 steps and 106/106 commands, zero skips/failures, in 469.764 seconds under the same two-CPU / 4 GiB / no-swap resources. This is advisory local-shape acceptance, not a passing enforced budget or paired performance improvement. Revised local startup and its independent audit are complete separately; their completion does not close this task. Future ownership should refresh source/requirements and use a maintainable proposal, equal diagnostic/coverage controls and measured inclusive cost. No source commit, PR, hosted regression or formal work window is claimed.

--- Historical investigation notes (superseded only for the revised local startup contract) ---

2026-10-18: Claimed the available child after pull/re-read, with no dependency or hold, for the narrow low-memory type-floor scheduling investigation related to think-q3h8. The parent remains with its existing delegate.

Unmodified source 804eff369 and locked BasedPyright 1.39.10 complete the full 68-step edit selection with zero skipped steps and zero functional findings under 2 CPUs, 4 GiB hard / 3686 MiB high memory and no swap. However, outer1/inner1 takes 532.439s and correctly FAILS the unchanged 240s budget. Type alone takes 252.824s. This is evidence of a local throughput problem, not a hosted regression or a passing gate.

Heap-specific probes did not establish strict readiness. A small fixture now confirms identical full-versus-batched canonical diagnostics for cross-file types/imports/cycles/generics and three errors plus one private-use warning, with omitted/duplicated manifest guards. Next is one fixed four-chunk timing diagnostic using the unchanged installed checker, exact original 1865-file discovery order, at most two serial checker children and the same total resource envelope. The enumeration-only instrumentation is isolated from acceptance. No checker package, lockfile, exclusion, diagnostic severity or budget has been changed. Full edit acceptance and independent review remain required before any source correction is accepted. No speedup claim yet.

2026-10-18 15:14 UTC update: The fixed four-chunk candidate is rejected after real-project diagnostic differences (two unused urllib imports reported by a chunk despite source use); missing final chunk/aggregation remains an incomplete diagnostic. No batching floor was adopted. Plain serial checking still times out at270.611s. Isolated published BasedPyright1.40.1 completes in237.565s with zero diagnostics, but is not adopted and does not resolve whole-edit240s acceptance. A CPU-profile attempt times out without a usable profile; no CPU attribution is claimed.

Current narrow mechanism: original workers keep completed targets open. Cache eviction followed by imported-file rebinding can make old targets require another check. A private in-memory Program-only close-previous probe preserves root tracking and avoids the extra callbacks produced by service-level closing. Independent review required URI, per-worker completion/pending-count, severity and cache-eviction controls. The expanded16-file fixture passes all15 comparisons across clean, error, warning-only, cycle and forced-cache-rebind phases, with the canonical bundle unchanged. This is fixture evidence only. A bounded trace-only original-behavior run is now measuring actual repeated old-target checks before any full-input candidate is justified. Original repo/lockfile/checker installation, diagnostics, resource limits and all68-step/240s acceptance remain unchanged. No source correction or passing full gate is claimed; think-q3h8 and independent audit remain open.

Recovery evidence update, 2026-10-18: A trace-only observation of the original workers measured 270 actual rechecks of already completed targets after cache eviction and imported-file rebinding. A private in-memory candidate closes the previous target directly in Program. With two workers it checked all 1,865 original roots exactly once, with zero errors, warnings or notes and no old-target rechecks, in 170.470 seconds and 330.012 whole-cgroup CPU seconds. A distinct candidate also changes routing to run that message loop with one worker: 193.352 seconds, 246.407 CPU seconds and a 3,391,197,184-byte peak. The original CLI's --threads 1 selects the serial path.

Both candidates passed a 16-file fixture with five phases and 15 diagnostic comparisons. Independent review confirmed their original trace coverage and identities. Neither candidate is installed or accepted as a dependency change.

A 120-second streaming profile retained partial attribution: 1,049 of 1,865 roots completed, with 11,582 worker samples and 35.7% unaccounted. It did not identify a safe dominant local rewrite. A separate scanner allocation screen preserved all 2,665 files, the ratchet and identical outputs. Default allocation took 17.419 seconds versus 16.345 with the child-only CPU-count override, below the declared 3-second AND 10% threshold. The override was rejected and is not persisted.

Canonical source 804eff369, submodule 515f4a08, lockfile, installed BasedPyright 1.39.10, diagnostics and the 4 GiB / two-CPU / no-swap limits remain unchanged. All owned computation has stopped with cleanup confirmed. Full edit acceptance remains INCOMPLETE: the original complete run passed all 68 functional steps with zero skips but FAILED the enforced 240-second ceiling at 532.439 seconds. Private type-check candidates do not substitute for that gate. No source commit, PR or hosted regression is claimed. Keep the task open; integration still needs a maintainable tool change, new cost evidence and complete acceptance.
