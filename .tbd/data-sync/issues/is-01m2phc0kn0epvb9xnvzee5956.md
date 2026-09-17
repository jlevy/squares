---
type: is
id: is-01m2phc0kn0epvb9xnvzee5956
title: "Senior-review and merge PR #190, the graded guidance plan"
kind: task
status: in_progress
priority: 1
version: 4
spec_path: docs/project/specs/active/plan-2026-09-11-annealing-as-a-search.md
labels:
  - workbench-roadmap
  - review
dependencies: []
parent_id: is-01m2gxkhmczffa661vb6emdxz5
created_at: 2026-09-17T01:58:15.924Z
updated_at: 2026-09-17T02:38:11.052Z
---
PR #190 (codex/guided-annealing-plan) adds O8/Phase 5A to the workbench plan, the graded-guidance section of the annealing plan and exploration X-036. Its senior review of 08264a4a was interrupted at 15:17 on 2026-09-16 with no verdict. The recovery added a9b19b7a (timing sits beside the receipt; the full-poses rung stays outside GuidanceTarget/v1). Done when an independent senior review approves the exact pushed head, the PR body's review line names that head and verdict, hosted checks are green, and the PR is merged.

## Notes

2026-09-17 independent senior review of PR #190 at exact head a9b19b7a (read-only; no tests run): CHANGES REQUESTED.

BLOCKER
B1. Touching-component tier and its size-preserving shuffle carry no information. The only featured records (n=11: 14 pair contacts; n=29: 52) are each one touching component, so the partition is {all n} and the shuffle is identical; with label-agnostic starts (Search grid/random, api/search-api.ts) any size-preserving shuffle is the same partition relabelled, so idea 183 cannot succeed or fail. Gate E (annealing plan ~508) names only rewired/thinned controls. Fix: state the tier's information is its component-size profile (membership matters only for previous/blocks starts); keep membership shuffle only there, else use a control that changes information (merged/split components); have think-rey9 report component counts per record and exclude single-component cells, or redefine the tier as near-flush/parallel clusters.

SHOULD-FIX
S1. Zero-strength byte-identical receipt contradicts receipts that name target/strength/schedule/use (workbench plan ~241 vs ~344, ~80, ~651; annealing ~185 vs ~205; campaign README ~403-405); canonicalizing the target away before execution tests only the canonicalizer; continuous strength is undefined for start/weld/constraint-band uses. Fix: requested-guidance record beside the receipt, byte identity only for the canonical effective receipt, an un-normalized strength-0 kernel test plus small-strength continuity, per-use strength and named unguided controls for discrete uses.
S2. Existing guidance path via relatedMask is unaddressed: simulation/kernel.ts ~105, ~571-577 restricts ordinary pairLaw attraction to masked pairs; Search accepts related_mask (search/pack-runner.ts ~182, ~375, ~524; api/search-api.ts ~73); the page builds masks from contact graph/blocks (api/workbench-api.ts ~39-47; application.js ~395-420). Today guidance strength is pairLaw.attraction, so the plans' separate axes do not yet exist. Fix under think-8ocb: name it, move it into GuidanceTarget/v1 + application config, refuse related_mask in registered cohorts until think-os1n adds a separate guidance force.
S3. Oriented face pairs: "never reveals absolute poses" is false (schema ~50-53: realising a full contact structure is a linear program; a complete oriented target fixes a rigid record up to congruence); mapping to contact-graph-with-types (typed flush/corner) under-states it; features exist only for n=11, 29 (25 corner-edge, 6 corner-corner, 35 edge-edge), so face alignment is undefined for many contacts and only two known-answer cells exist. Fix: "does not store", report remaining DOF per target, distinct rung or corrected mapping, define corner-contact semantics, state per-tier known-answer coverage before think-3yma freezes partitions.
S4. Oriented vs untyped contrast confounds information with a new aligning torque. Fix: wrong-feature control with equal torque budget, or equal-budget generic torque for the untyped arm.
S5. Equal-work currency undefined; README says no equal-pair-budget comparison is yet admissible; accept-rule clauses 3-4 are sqsearch-specific; workbench budget is proposalAttempts/physicsSteps/repairIterations (search/contracts.ts ~33-37) with no pair tests; guidance adds force work so X-036 "unequal effective work is invalid" invalidates every guided comparison; paired block differences conflict with median + non-overlapping ranges. Fix: declare the budget currency and how guidance work is charged, name workbench replacements for clauses 3-4, say which statistic decides.
S6. Prose dependency order vs tbd: Phase 5A "follows" think-o4wo/5tyy/gfqt but only think-0epc is blocked by o4wo/5tyy and none of 8ocb/rey9/os1n/qx88/gdkd depends on them or gfqt; gfqt is both prerequisite and deliverable and not blocked by 8ocb; think-wln2 is not blocked by think-c0rm/Phase 5A; annealing item 8 says the sweep follows think-czav but 0epc is not blocked by it; 0epc -> 3yma -> vhgz makes the headless sweep wait on browser Search mode just to freeze a partition; the unguided stickiness curve needs no guidance contract but sits behind 0epc. Fix: split guided-receipt work into a Phase 5A child blocked by 8ocb/os1n (or reword "follows"), add or drop the wln2 blocker consistently, reword item 8, move partition freeze into think-gdkd or a headless task, give the stickiness curve its own bead blocked by o4wo/5tyy.
S7. Research sweep gates product acceptance (workbench ~655, ~663 put think-0epc in Phase 5A gating think-wln2), contradicting ~621 (research authorization separate from shipping instruments) and O3 (~75). Fix: think-0epc is a consumer of Phase 5A like think-fj07; O8 evidence is a replayable demonstration cohort.
S8. Continuity guard targets the wrong path: Search trials run simulation/pack.ts (forceLawSubsteps); X-035/Phase 2A budgets are Animate trajectory.ts 60 Hz samples. Fix: name the sweep's runner and define the guard for Pack trials or limit it to Animate replays; justify o4wo/5tyy blockers accordingly.
S9. Adaptive ladder only partly pre-registered: the rule selecting which stickiness/strength/schedule carries forward and the full contrast list are not frozen. Fix: think-gdkd freezes both; held-out confirmation is the only decision gate.
S10. Wall-clock inputs reach outcomes: SearchSlot.timeoutMs (search/contracts.ts ~56, ~70; scheduler.ts ~157-189) changes status/partial result; elapsedMs sits inside SearchOutcome (~134-137). Fix: timeout_ms unset for registered cohorts; hash SearchTrialValue or a canonical successor.

NITS
N1 thinned control does not preserve edge count (schema ~68-71): compare thinned-true vs thinned-rewired at equal keep. N2 `shuffled` missing from PackingStrategy control enum (schema ~65): add under think-8ocb. N3 a9b19b7a misattributes springs: it is AtlasOptimize (Pack open-ended run, api/workbench-api.ts ~296-297), and full-pose springs also run in free mode (trajectory.ts ~693-695, ~768). N4 annealing ~14 "the shared search instrument exists" overstates (workbench ~609). N5 wall time in the cost vector vs think-qx88 "not wall clock"; browsers cannot measure CPU: label CPU/wall as operational context, CPU from Node only. N6 scope replay identity to Node and pinned Chromium. N7 one naming table: touching-component-partition / touching-partition / touching-cluster / connected-component; calibration vs code `tuning`.

CHECKED FINE: all 17 referenced beads exist with sensible states; generated ledger.md and SYNOPSIS.md agree with X-036; no result or verdict claimed.


2026-09-17: cdd9aad8 resolves the a9b19b7a findings (plan revision by a Claude sub-agent, coordinator-checked; records tier passed). tbd changes applied to match the prose: created think-10yz, think-05o4, think-9hdg; removed think-0epc<-think-3yma and think-qx88<-think-gdkd; added think-9hdg<-think-05o4, think-3yma<-think-05o4, think-czav<-think-10yz, think-wln2<-(think-czav, think-10yz), think-0epc<-(think-10yz, think-9hdg, think-05o4), think-9sdr<-(think-o4wo, think-5tyy); notes updated on think-8ocb (corrects the springs misattribution), think-rey9, think-os1n, think-gfqt, think-3yma, think-0epc. Re-review of cdd9aad8 in progress.
