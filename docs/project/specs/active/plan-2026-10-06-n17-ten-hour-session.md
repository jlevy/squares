---
title: n17 Ten-Hour Overnight Session
date: 2026-10-06
status: active
---
# n17 Ten-Hour Overnight Session

## Mandate and Baseline

Make the most useful progress toward `s(17) = S*` in ten elapsed hours by combining
mathematical strategy, retained instruments, rigorous exclusions and proof integration.
The [W3 consolidation](../../reviews/review-2026-10-06-n17-w3-consolidation.md) selects
the approach;
[agenda 043](../../../../packing/campaign/agendas/agenda-043-n17-ten-hour-continuation.md)
owns commitments and readiness.
BC-418 remains the program owner.

The planning block launched no targets.
Actual work began in
[Session 184](../../../../packing/campaign/agent-sessions/session-184-n17-proof-contracts-and-instruments.md)
at **2026-10-07 00:08:33 PDT**, with a **10:08:33 PDT** deadline and protected
finalization beginning at **09:08:33 PDT**. Its contemporaneous session record owns
actual phases, delegations, measurements and dispositions; this document owns the
schedule and selection rules.
The launch source is `f3a13e3a217d2f8c17e96570c31ca1c9eda66c63` on
`codex/n17-state-review`.

Freeze the launch source and ledger before targets.
The assessed main is `ef79288a4`: R071 gives `4.66044275 < s(17)`, the outward upper
ceiling is `4.6755300936045509516342148538535054`, and Session 183 records 36,784 states
/ 4,685 orbits under 58 admitted entries.
Reconcile any intervening merges instead of assuming these are still the launch
baseline.

## Models, Ownership and Parallelism

**GPT-6 Astra owns every strategic mathematical choice and new derivation.** Use one
Astra sub-agent, normally at high thinking, raising to xhigh for the widened-theorem
contract or a consequential proof choice.
It cycles among proof interfaces, capture mathematics, alternate-terminal bounds and
hard-tail strategy. It returns bounded written contracts; it does not spend its lane on
uploads, routine tests or task updates.

**GPT-6.1 Sol owns coordination, mechanical evidence reconciliation, engineering,
factual review and task management.** Use medium thinking for routine inventory and
records, high for checker-boundary or certificate engineering.
Sol may implement and review Astra’s specified mathematics; new mathematical decisions
return to Astra. An engineering review does not imply independent mathematical
confirmation by another Astra reviewer.
Record actual configurations and assurance limits.

With four available agent slots, keep one Sol coordinator, one Astra strategist and two
Sol workers. The workers rotate among the independent lanes below.
More lanes than workers are a work queue, not a claim of extra concurrent agents.
When Astra has no strategic question, release that slot to a Sol review/engineering
worker; never run a second Astra concurrently.
Do not manufacture duplicate work to fill capacity.

The coordinator alone allocates IDs and writes agendas, hypotheses, experiments,
admission ledgers, manifests, generated views and the session record.
Worker source edits are disjoint and reviewed before shared integration.
Worktree use follows the repository’s existing worktree policy; each checkout has its
own Cargo target.

## Host and Artifact Preflight: First 30 Minutes

Select the host at launch; the Mac and the prior container are different regimes.
Record CPU count, physical memory, available memory, disk, load, interpreter, tool
versions and actual asset inventory.
Verify the external scratch volume is mounted and writable before any Mac build or
disk-heavy command. Pause disk-heavy work if it is unavailable; do not fall back to
internal scratch.

On this Mac, use `/Volumes/spud-ext1/agent-scratch/n17-session-<id>/` for disposable
work, `TMPDIR`, `UV_CACHE_DIR`, and a separate `CARGO_TARGET_DIR` per checkout.
Keep unique scientific evidence in the repository or retained hosted storage.
Use `packing/.venv/bin/python3` or frozen uv commands, never the PATH `python3`. Pin
BLAS/OpenMP to one thread per numerical worker.
macOS has no assumed GNU timeout or Linux `setsid`: identify and review a timeout
wrapper or platform command before launch, preserving owned-process cleanup and partial
records.

Current local limitations:

- The 200 hosted certificate objects, held closure nodes and pilot-2 checkpoint nodes
  are absent here; receipts and the small mutation fixture are present.
- The previous host’s resource logs are absent on the Mac.
- The n11 mask-0 and pose-control inputs are retained locally; confirm the chosen
  control’s complete dependency inventory before running it.
- Compression repair PR402 has a fixed candidate at `3745534eb29dc`, imported into this
  branch at `917163641` and reviewed with exact membership/fallback controls.
  The optional native RSS guard is integrated; the known-case target still needs
  registration and production evidence.
  The upstream PR402 merge is not claimed.
- `hosted_data publish` requires all manifest objects locally.
  Recover them from the owning host before trying publication; an empty release cannot
  supply them.

Budget at most 30 minutes for access/inventory diagnosis.
If remote objects are unavailable, record the blocked custody/held-node lanes and
continue local proof, instrument and fresh-run work.
No host-access blocker stops the whole night.

At first, allow at most two heavy compute processes.
Reserve two logical CPUs and at least 4 GiB available memory for coordination, reviews
and gates. After measuring peak RSS, raise compute slots to at most
`min(4, logical CPUs - 2, memory slots)`. Compute memory slots as the integer quotient
of available memory after the reserve by the measured per-worker memory ceiling.
On a four-CPU host keep at most two heavy processes; on the Mac’s reported ten-CPU
shape, extra cores do not accelerate a sequential kernel step automatically.
Do not launch if projected scratch headroom after outputs is below 8 GiB; pause a lane
before available memory falls below 3 GiB. Checkpoints count against disk limits.
The native macOS current-RSS adapter and optional pilot guard are integrated with
independent controls.
Lifetime peak RSS remains a reporting metric.
The guard samples at explicit seed/producer/checker/replay boundaries; a heavy call may
overshoot before the next sample.
It is a cooperative guard, not a hard PID monitor.
The known-case target must register its memory cap and preserve incomplete checkpoints.

## Lane Contracts

| Lane | Owner and available work | Exit / refusal | Dependencies and fallback |
| --- | --- | --- | --- |
| P: proof interfaces | Astra specifies frame, caps, branch/state coverage, exact-root allowance, slider box and terminal premises; Sol makes an obligation table and checks source joins | Every arrow has inputs, evidence, checker and unresolved premise; any mismatch is a tracked blocker, not a theorem | Ready from source. First contract by hour 2; deepen reachable joins while other lanes compute. |
| R: cheap widened-terminal reconnaissance | Astra specifies correct LP/dual and feature-branch semantics, adversarial mixed-angle/slider directions; Sol retains the instrument and reader | Endpoint value, finite-angle rows, slider domains and feature-branch controls pass before the newly registered reconnaissance. Report valid dual candidates, unsupported branches and sampled curvature; no sampled basis census is exhaustive coverage | Can start alongside compression repair. If build exceeds two 30-minute slices without a checkable control, split scope and retain the contract. |
| C: compression and capture control | Sol reviews the externally owned repair, preserves exact membership/fallback checks, freezes source, and implements the known-case run; Astra approves its scientific discriminator | Synthetic recession target and n11 contraction control recorded separately. Control extent at most 0.5 by round 15 supports readiness; at least 0.9 refuses n17 interpretation; the middle is inconclusive | Repair ref plus complete n11 inputs. If external repair stalls, audit its contract and prepare controls; do not duplicate its implementation. |
| G: actual-residue and exclusion tail | Sol extends retained stratification to the current admitted ledger, inventories genuine fixed points and caps; Astra selects a frozen representative workload | Exact current-residue counts, endpoint survival, classes (including untested and diagnostics-unavailable) and honest cost distribution; no forecast from the 26/29 hypothetical arity-eight sample | Existing survey’s arity7/arity8 populations are historical. Build/review ledger-backed mode before targets. Missing saved nodes permit newly registered fresh rebuilds, not fictional resume. |
| A: custody and held admission | Sol recovers objects, publishes/fetches, verifies integrity and replays representative certificates; prepares held-control evidence | All manifest objects accounted for; replay scope explicit. Held entries stay unadmitted without their required ruling | External host/access dependency. If blocked, produce inventory and exact transfer instructions; continue independent lanes. |
| E: efficiency and assurance | Sol measures instrument/control/test phases, updates records and reviews candidate source changes | Timings with source/configuration/outcomes, failed and interrupted runs included; independent engineering review before target admission | Runs beside analysis; avoid full gates competing with peak-memory compute. Existing verifier receipts do not certify a changed instrument. |

All new scientific measurements receive their own preregistered H/exp contracts after
Astra specifies the claim and before any target command.
Do not reuse an accepted H-264/H-274 criterion for a different sample, cap, instrument
or outcome metric. Numerical counterexample candidates require exact verification before
mathematical use.

## Ten-Hour Clock

There are twenty 30-minute slots.
Each active slice has a checkable artifact by minute 20 and a stop/renew decision at
minute 30. Renew only with evidence and within the original session deadline.
Long registered compute may span slots under its unchanged lease while supervision,
checkpoint recording and independent lanes continue.

| Elapsed time | Coordinator and Astra | Sol worker 1 | Sol worker 2 | Checkpoint decision |
| --- | --- | --- | --- | --- |
| 00:00–00:30 | W10 launch, resource/source/ID freeze; prioritize mathematical contracts | Asset/ref inventory and repair ownership | Baseline records/tool/control-input checks | Commit registration before targets. Record blocked lanes. |
| 00:30–02:00 | Astra: proof joins and widened LP contract | Build the retained finite-angle LP instrument and its controls | Review repair, freeze n11 control; ledger-backed residue inventory when waiting | At hour 2, accept only reviewed instrument readiness; cheap reconnaissance earns priority before expensive capture. |
| 02:00–04:00 | Astra: interpret reconnaissance, resolve terminal-region/outer-reach obligations | Registered LP sample and adversarial probes; independent output reader | Registered n11 control; tail survey/custody during compute | At hour 4, decide whether n17 scaling is feasible within remaining wall and memory. |
| 04:00–06:00 | Astra: select capture A/B discriminator or alternate-terminal contract; choose actual-tail cases | Capture preparation/scaling only if admitted; otherwise LP certificate grammar or proof joins | Bounded fresh/saved exclusions after controls, or current-tail tool/readiness | At hour 6, route fixed points versus resolution losses; no blanket sweep. |
| 06:00–08:00 | Astra: integrate mathematical information and select next proof slice | Renew only evidence-producing compute; checkpoint partial preparation if verdict cannot fit | Verify/admit eligible closures, custody replay, hard-tail diagnosis | At hour 8, stop new expensive targets; choose verifiable outputs for close. |
| 08:00–09:00 | W2/W10 integration; Astra reviews mathematical claims; Sol reconciles record and beads | Complete full verification or preserve unresolved objects | Focused tests and portability/readiness review | Workers stop shared writing before hour 9. Finalization inputs freeze. |
| 09:00–10:00 | Protected finalization in two slots: measured receipts, views, qualifying checks, commit/push/CI and handoff | Read-only final checks; no new research | Read-only final checks; no new research | Record exact achieved, negative, incomplete, refused and blocked dispositions. |

The schedule is a maximum allocation, not artificial pacing.
A completed slice releases its worker immediately.
Re-screen future slots at hours 2, 4, 6 and 8 against measured costs, source
dependencies, memory and scientific information gained.

## Capture and Exclusion Selection Rules

R9’s full n17 stage 1 is sequential, historically about 35,000 seconds just to rebuild
round 17 and about 20–22 CPU-hours overall.
Do not promise its verdict in this ten-hour night by multiplying available cores.
Launch a verdict-producing scaling round only when measured throughput and admissible
checkpoint readiness fit before hour 9 with verification reserve.
A changed producer cannot silently resume an old checkpoint.
Otherwise register a checkpoint-producing preparation round with its own explicit
unresolved exit and keep the full scaling successor unfunded for this night.

For a new scaling contract, freeze all-owner and mixed outcomes: R9 proposes at least
20-percent angle contraction at doubled rows and 40 percent at quadrupled rows for the
row-driven interpretation; within 5 percent of old ranges at fourfold rows supports the
box-set interpretation.
Intermediate or mixed outcomes remain inconclusive.
Only positive controlled evidence earns the expensive position-onset step.
Neither box contraction nor a widened terminal theorem discharges outer capture from
cells.

Measure row-refinement response against a onefold-row baseline rebuilt with the same
repaired producer; comparisons with historical pilot 2 are separate.
Freeze side-W2’s into-wall turn side and side-N0/side-N2’s full turn ranges as the three
observables. Verify actual angular refinement, not merely the requested row-cap
multiplier.

For widened LP reconnaissance, feature-branch value is the supremum of feasible dual
lower bounds; any outer minimum is over allowed branches.
A bad sheet is not a counterexample.
Resolve the 100,000 versus 1,000,000 patch routing thresholds and degenerate
unseen-basis estimation in the new contract.
Sampling informs cost and candidate duals, not complete directional coverage.

For exclusions, use current-orbit reduction per total producer, self-check, full
verification and storage cost.
Do not repeat H-274’s four completed retries.
Held BC-423/426 closures wait on their ruling.
Apply the existing extended-row recipe only to genuinely remaining cap stalls under
valid controls. C2 aimed splits require a remaining loss-limited sample; C5 requires
producer/checker/consumer support proving all closed children cover the parent,
including seams. Either is a conditional build, not an automatic overnight allocation.

Freeze the SW9 exclusion checkout independently of the capture repair.
Reserve full verification before launching a producer: the existing 7,000-second
production plus 4,000-second verification ceilings require about 3.1 hours.
With the hour-9 research cutoff, the last such launch is about elapsed 05:56; later jobs
need shorter declared ceilings or an explicitly incomplete checkpoint-producing purpose.
A complete fixed-angle evaluation may require up to `2^9` feature branches, each with
its own LP. Distinguish the proposed 8,000 sampled direction/radius points from the
number of LP solves.
Calibrate complete point evaluations before selecting a sample that fits the worker-hour
ceiling.

Branch-and-bound remains an optional reserve until new representative calibration passes
its frozen criterion and total certification fits.
Native search speed does not repair calibration.
Further side refinement with the unchanged R071 charge is parked: its remaining `2.5e-8`
runway cannot materially resolve the current gap.
Astra may scope a genuinely new charge or architecture obstruction as a bounded reserve
after critical-path work.

## Validation, Recovery and Morning Handoff

### Fast Iteration and Hourly Goal Check

The user’s priority is mathematically significant progress toward completing n17
optimality. Every hour, reread this objective and identify the proof obligation each
active lane advances, new information gained, remaining time and the next informative
action. Stop or narrow mechanical work that cannot name the mathematical dependency it
unblocks. One Astra makes strategic mathematical decisions; GPT-6.1 Sol handles the
checks, records and engineering.
Hourly reminders support these decisions, not new administrative reports.

Use the existing validation tiers without waiting on broad CI after each small edit.
While iterating, run the relevant focused test or instrument control and the edit tier
when its surface changes.
Before push, run the required change-reachable push checks.
Push at coherent integration points and observe CI asynchronously while independent
mathematical lanes continue.
A red soundness check blocks its dependent instrument or admission; an unrelated CI
delay does not idle the entire team.
Keep full certificate verification mandatory before admission.

Select deeper repository checks at the hour-4 integration boundary and final close, and
earlier for changes to certificate/checker contracts.
Launch them beside independent proof work from pinned inputs.
Budget routine mechanical investigation to one 30-minute slice: renew only when measured
evidence shows it unblocks a named proof obligation.
Record CI/test waiting and mechanical effort at the hourly checkpoint; reallocate when
these crowd out mathematical progress.
Do not repeatedly run unchanged passing suites or spend multiple minutes watching CI
after every commit. Full closeout evidence remains required for a certified handover; a
pending gate stays pending.

Use existing retained tools; no one-off measurement scripts.
Tool help at the frozen revision determines commands.
From `packing/`, the common checks are frozen `packing-ledger check`,
`packing-validate --records`, `--edit` during engineering, `--push` before push, and
full `packing-validate` for a completed session handover.
If the deadline prevents that checkpoint, retain an incomplete handover with the full
gate outstanding. Full standing certificate verification is distinct from repository CI
and never replaced by sample mode.
A gate above its routine ceiling needs an explicit selection and the evidence sought.
CI runs beside independent work and is observed at boundaries.

Every long job retains phase timings, source revision, settings, worker count, memory,
output location, status, and a resumable checkpoint where supported.
Stop owned workers before switching their source or running conflicting gates.
On soundness alarms, freeze the instrument and candidates, admit nothing, and continue
unaffected analysis.
On ordinary guard/clock stops, retain partial data without inventing a scientific
negative. Never change frozen criteria after seeing results.

Morning deliverables, even on a blocked-asset host:

1. A current proof-interface and unresolved-arrow table, with Astra’s mathematical
   judgments distinguished from Sol’s factual/engineering checks.
2. A retained widened-projection instrument with controls and a registered result, or an
   honest readiness stop and precise remaining build work.
3. Reviewed compression/control evidence or its external dependency disposition; a
   controlled capture decision or priced unresolved preparation checkpoint.
4. Actual-residue strata, a selected hard-tail workload and any fully verified new
   exclusions, with overlap and endpoint controls charged.
5. Asset custody and held-admission dispositions, measured costs, updated views, clean
   branch/PR evidence, and one next coordinating entry with bounded lanes.

The wall deadline is the user’s ten-hour limit.
Finish research by hour 9. If CI or certification cannot finish by the deadline, stop
research, preserve the branch and declare the outstanding certification owner; do not
claim a completed certified handover.
No automation, external worker dispatch or overnight launch is created by this plan
alone.

## Session Evidence and Selected Follow-Up

At the five-hour checkpoint, the original U-cap census has60 admitted entries and36,768
states /4,683 D4 orbits remaining, with the endpoint retained.
Two new ordinary full standing admissions account for the change from the58-entry launch
baseline. The conditional cone, cap and coarse-slider results remain scoped to their
checked premises; none supplies global capture or an improved unconditional lower bound.

The new numeric-cap full17 first round completed all16 contracting-owner updates and
fresh zero-production replay.
Its separate
[H290 intake](../../../../packing/campaign/series/series-000-smoke-and-calibration/experiments/exp-277-h290-numeric-checkpoint-capture.md)
accepted49 exact intervals and all17 endpoint poses, while every geometric terminal
predicate remained false.
Astra found that every active owner still represents the full orientation interval.
This diagnoses the represented relaxation; it supplies no packing counterexample or
claim about the physical feasible subset.

The centered-cap interface subsequently passed its full standing STALL control in
[exp280](../../../../packing/campaign/series/series-000-smoke-and-calibration/experiments/exp-280-h291-centered-endpoint-hull-capacity.md).
It retained the known endpoint and established no exclusion.
The cheap conditional support test
[exp282](../../../../packing/campaign/series/series-000-smoke-and-calibration/experiments/exp-282-h292-conditional-owned-hull-scoped-input.md)
then constructed five additional strictly owned points for owner0 under the closed
angular guard `[13/32,27/64]`, with fresh finite verification.
All four support gains exceeded the preregistered `1/1024` threshold; the unguarded test
failed it. These are conditional ownership facts, not global capture.

The guarded continuation produced16 updates in
[exp284](../../../../packing/campaign/series/series-000-smoke-and-calibration/experiments/exp-284-h293-parent-guard-native-custody.md),
but its fresh300-second replay stopped incomplete.
Its geometry remains unaccepted and is excluded from subsequent proof inputs.
The separately registered finite four-case test
[exp285](../../../../packing/campaign/series/series-000-smoke-and-calibration/experiments/exp-285-h294-pooled-parent-center-cases.md)
used only accepted original-parent kernels and the five verified points.
Its construction and fresh reconstruction completed in20.74 seconds, but neither the
unsplit test nor any of the four closed centre cases found a common collision point.
This is a completed negative result for that finite recipe, not a physical packing
counterexample.

The separately registered
[exp286](../../../../packing/campaign/series/series-000-smoke-and-calibration/experiments/exp-286-h295-pooled-forbidden-cover.md)
tested the union of strict collision regions under the same angular guard.
Construction and fresh finite verification completed in20.73 seconds; all18 necessary
pieces remained uncovered in both matched controls.
The fixed single-square trial exp287 passed ownership and foreign avoidance but failed
container containment.
The separately registered exp288 imposed walls before selecting the centre and then
passed all original pose predicates in fresh reconstruction.
It completed in1.120 seconds under the fixed60+60-second construction/replay ceilings.
This is an accepted witness for the particular retained-point relaxation, not a17-square
packing, capture, exclusion or census admission.
The actual supervisor samples a4GiB RSS ceiling per live process and cleans up the owned
group; exp286’s aggregate-memory declaration was a metadata error preserved in its
outcome record.

[Session184](../../../../packing/campaign/agent-sessions/session-184-n17-proof-contracts-and-instruments.md)
owns the current30-minute slices, fixed target budgets and disjoint agent deliverables.
One Astra remains on mathematical strategy and review; two Sol workers handle source,
custody and focused checks, beside the Sol coordinator.
A full ordinary checkpoint runs on predecessor969588d09 in an isolated checkout, beside
additive checks for later source.
Its launch incorrectly retained a project-root override, affecting37 mutation controls;
preserve that failure and rerun only those controls with project discovery restored.
Do not relabel the full checkpoint as passed.
The research cutoff and protected finalization hour remain unchanged.

The final
[W3 route selection](../../research/research-2026-10-07-n17-w3-capacity-and-route-selection.md)
prioritizes a1–2-hour block using complete partner centre-and-angle covers, with exact
replay profiling in parallel.
The mathematical criterion is a checked closed exclusion or capture region beyond the
point-only control. The engineering criterion is a measured hotspot and exact-equivalent
replay; a twofold end-to-end gain is an acceptance target, not a prediction.
A2–4-hour deeper optimization block is justified by the unaccepted exp284 replay,
conditional on that profile.

Certificate-family lifting and a necessary structural normal-form lemma are fallback
mathematical slices.
Extend work to1–2 days only if checked coverage grows, a reusable uniform implication
replaces cases, or certificate cost materially falls.
There is no defensible proof-completion estimate yet.
More unchanged propagation or isolated local patches without a global capture domain do
not meet the renewal criterion.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
