---
title: n17 Three-Block Session Plan
date: '2026-10-10'
status: prepared
---
# n17 Three-Block Session Plan

**Prepared, not launched.** Plan one continuous run of three eight-hour blocks, with
mathematical distance toward a complete n17 proof as the objective.
Each block replans from retained evidence before dispatch.
Capture/terminal mathematics and nonterminal exclusions or stronger domain constraints
remain co-primary; confirmation and integration support those obligations.
This document creates no active session, actual clock, experiment, automation or
scientific claim, and does not itself authorize execution.

[Agenda 046](../../../../packing/campaign/agendas/agenda-046-n17-eight-hour-proof-block.md)
owns commitments and beads;
[X-052](../../../../packing/campaign/explorations/X-052-n17-status-survey-and-completion-plan.md)
owns the exploration and remaining proof map.
The [eight-hour block plan](plan-2026-10-10-n17-eight-hour-proof-block.md) supplies
Block 1’s complete 16-slice schedule, scientific controls, resource guards and portable
commands. The [session README](../../../../packing/campaign/agent-sessions/README.md),
[AgentSession/v2 schema](../../../../packing/campaign/schemas/agent-session.schema.yaml)
and
[Session 186](../../../../packing/campaign/agent-sessions/session-186-n17-mathematics-and-efficiency.md)
supply the record format; retained history is evidence, not a template for overrunning a
lease or inventing validation.
Read the current handoff and owning beads at every launch.

## One Run, Three Complete Session Records

Use three sequential eight-hour AgentSessions for the user-level run.
Each block has its own protected finalization, terminal resource receipt, certification
disposition and successor decision.
AgentSession/v2 requires a contiguous finalization tail; a new block therefore receives
a new record rather than reopening a finalized session.
The scientific chain and its frozen contracts continue across records.
The coordinator allocates each complete record serially immediately before its block
starts, never three empty reserved IDs.
Any independently tracked lane session is allocated by the same coordinator.

The prospective run has at most 24 hours and 48 half-hour slots, including all block
boundaries. Nominal offsets are H0–8, H8–16 and H16–24; these are planning offsets, not
observed timestamps.
At first launch observe offset-aware $S$ and set the outer deadline $D=S+1440$ minutes.
Observe each block start $B_k$ and set its deadline to $\min(B_k+480\text{ minutes},D)$.
Launch a successor when its predecessor closes; do not wait to consume unused time.
A delayed transition reduces remaining capacity rather than moving $D$; if a full block
cannot fit, record a shortened prospective allocation before launch.
Recovery terminalizes an expired lease or session from retained evidence first.

All H6/H7 cutoffs and tables below describe the full 480-minute allocation.
For an actual block deadline $T$, scientific/code freeze is $T-120$ minutes, gate launch
is by $T-105$, finalization starts at $T-60$, and the gate ends by $T-45$. Before
opening a shortened block, reprice its useful reviewed obligation and prune the future
rows against those cutoffs.
Retain the 120-minute freeze-to-closure envelope; if even one useful 30-minute work
lease cannot fit with it, select closure and a ranked handoff with explicit
certification debt instead of opening another research block.

For each block use the existing session fields:

| Field | Prospective contract; instantiate with actual launch evidence |
| --- | --- |
| `id`, `title`, `date`, `started_at`, `deadline_at`, `branch` | Next serial ID, block-specific title, observed offset-aware start/date, bounded deadline and attributed live branch |
| `goal`, `primary_bead` | Resolve the selected capture/terminal and nonterminal obligations; Block 1 coordinator `think-wnbr`; later blocks select the actual open coordinator bead under BC-418 |
| `status`, `workflow_phases` | `in_progress` only after launch; complete first phase contract before dispatch; exactly one active coordinator phase |
| `budget` | `wall_minutes: 480`, `max_cycles: 16`, `orientation_minutes: 10`, `checkpoint_minutes: 20`, `slice_minutes: 30`, `finalization_minutes: 60`; reduce prospectively if $D$ requires |
| `stop_conditions` | Phase lease, frozen target/command ceiling, soundness or resource refusal, scientific/source freeze at $T-120$, finalization at $T-60$, hard session/run deadline; H6/H7 only for a full block |
| `progress` | Metric: exact obligations and domain coverage; `before`: launch proof map/census; `after: null` while active, actual scoped disposition at closure |
| `delegations` | Contemporaneous owning phase, operator, scope, guards, clocks and output/check contracts before long work; terminal fields stay null until a receipt exists |
| `outputs`, `checks`, `resource_rollups` | Actual artifacts, actual source-bound verdicts and native privacy-reduced receipts; no estimated cost or planned gate is a receipt |
| `stop_reason`, `next_action`, `ended_at` | Null stop reason while active; at closure actual stopping reason/end, exact owning bead and selected successor; failed/absent certification remains explicit debt |

Do not attach enforced AgentSession frontmatter to this prepared plan: `prepared` and
relative offsets are not live schema values.
At launch replace prospective values with observations and validate the complete record.
A stopped uncertified block uses the same follow-up bead in `certification_pending` and
`next_action`; a passing record names the actual source-bound gate.
Apply the README’s narrow measured/unmeasured resource rules, not reconstructed totals.
Join terminal records through the existing research logbook.

## Capacity and Continuous Mathematical Ownership

Each block runs two `gpt-6-astra` authors at `xhigh`: one for capture/terminal
interfaces, one for nonterminal mathematics.
Use `max` for a consequential counterexample.
One latest Sol (`gpt-6.1-sol`, `high`, `xhigh` for checker repair) owns shared
engineering. A fresh Astra `max` reviewer rotates through a freed slot and never reviews
its own authored packet.
Preserve disjoint write sets and other agents’ edits; the coordinator alone owns
registries, identifiers, records and integration.
Delegations inherit the parent phase unless they open an independently tracked session;
never put two active phases in one record to represent parallel work.

Plan 80% proof, 5% repeated confirmation and 15% integration separately for CPU and
worker-agent effort.
Initial soundness review of new mathematics belongs to proof; independent repeated
confirmation remains visible.
Comparator/H-348 support has at most 60 worker-agent minutes per block, at most 30 per
artifact, and renews only when the checkpoint names a critical dependency it resolves.
Unused confirmation capacity does not create repayment work.
Full H-348 remains deferred; unchanged receipts are reused.

Twenty-four wall hours with three occupied worker slots gives a nominal upper capacity
of 72 worker-agent hours, including rotating review.
It is neither a reservation nor measured usage; coordinator effort is separate, and
availability, queue, setup and actual native cost remain unknown until observed.
Charge phases once and retain failed attempts.
A block ending early does not manufacture unused worker-agent hours as actual effort.

Retain the host envelope: four compute cores, 12 GiB aggregate task RSS, one heavy
process, at most 1 GiB new outputs and a 2 GiB free-space floor.
The prepared host reported 10 logical CPUs, 32 GiB RAM and about 11 GiB external free
space; remeasure at each launch and expensive process.
Use the prepared external scratch environment, explicit `TMPDIR`, `UV_CACHE_DIR`,
worktree-specific `CARGO_TARGET_DIR`, Python 3.14, `PYTHON_CPU_COUNT=4` and BLAS threads
set to one. The output cap is cumulative over this run, not a fresh allowance to
accumulate 3 GiB; preserve unique evidence before disposing of owned outputs.
Queue time under the single heavy-process lease is included in target pricing.
Missing compute, storage or guard readiness selects exact mathematics rather than
waiting.

## Complete Phase Contracts

Each active phase is at most 30 minutes, preserves evidence by minute 20 and closes or
renews prospectively from new evidence.
Slot numbers account for wall time; phase numbers account for material changes of
objective/workflow/focus, so record both when they differ.
A row in the schedules below selects a contract, not a running phase.
Fill every field below before dispatch; repeat a kind only with a new bounded objective
and evidence-based switch reason.
Only future allocations change at replan; old deadlines remain in history.
Agenda 046 and the table’s beads are Block 1 anchors.
Each later replan binds the actual open commitment and coordinator/lane beads under
BC-418; never restart a closed bead or preallocate future commitment, session or
experiment IDs.

| Phase field | Binding for every material phase |
| --- | --- |
| `workflow`, `focus`, `clock_role`, `bead` | Phase-kind table below; select one exact bead when alternatives are listed |
| `objective`, `expected_output`, `validation_command`, `kill_condition`, `fallback`, `next_action` | The selected kind’s contract, specialized to named coordinates/domain/rows, exact source, artifact paths and command argv |
| `start_offset`, `deadline_offset` | Schedule’s local block slot; actual lease may start later or finish earlier, never exceed 30 minutes or the relevant cutoff; these offsets stay in plan/body, not unsupported schema keys |
| `recording`, `status`, `entered_by`, `switch_reason` | `contemporaneous`, `in_progress`; first phase `session_start`/null, later `planned_checkpoint`, `evidence_checkpoint` or `user_request` with its actual reason |
| `budget_minutes`, `started_at`, `deadline_at` | Positive remaining lease, at most 30; observed offset-aware start and exact deadline bounded by block/run cutoffs |
| `outcome`, `evidence`, `stop_reason` | Null/empty/null while active; observed result, exact receipts and reason before the successor opens |

| Kind | `workflow` / `focus` / `clock_role` | `bead` | `objective` and `expected_output` | `validation_command` | `kill_condition` and `fallback` | `next_action` |
| --- | --- | --- | --- | --- | --- | --- |
| K: launch/replan | W10 `review-planning-oversight` / process / work | `think-wnbr` | Freeze actual evidence, costs, ownership and selected obligations; complete session, assignments and resource admission | V0; direct cross-check of proof map and scientific source contracts | Missing mandatory input or guard: no target; dispatch scoped exact derivation | Open M, P or T with its complete contract |
| M: exact mathematics | W3 `insight-iteration` / insight / work | `think-9tmv` or `think-lhty` | One exact conversion/slider/pose implication, counterexample or complete scoped obstruction; named-domain argument and source premises | V1; independent argument review against all quantified domain and separator alternatives | Premise fails, old relation repeats or scope incomplete: retain witness/missing premise; choose a genuinely changed relation | R for deciding soundness, then priced next mathematical obligation |
| P: instrument readiness | W7 `pipeline-improvement` / correctness / work | `think-ydg5`, `think-9tmv` or `think-lhty` | Smallest reusable instrument required by a named mathematical consumer; source, controls and explicit readiness decision | V2 plus exact newly affected tests frozen before the lease | Failed control or unaffordable complete recipe: retain premeasurement stop; switch to M | R, then T only after reviewed readiness and registration |
| T: registered target | W6 `research-loop` / insight / work | `think-ydg5` or `think-lhty` | One frozen complete production/replay pair or same-chain continuation; exact result, negative or censored disposition | V3, frozen before any target sample | Target/command cap, lost endpoint, invalid replay or resource floor: stop/reap and retain receipt; no scope or criterion extension | R and exact admission/union decision, or M for the diagnosed blocker |
| R: new-artifact review | W2 `factual-review` / correctness / work | `think-mfsn` | Fresh independent deciding review, smallest counterexample or exact accepted scope | V1 and the artifact’s exact frozen replay/control argv | Soundness finding: stop unconditional use, retain witness; return to M/P | I or one reviewed bounded successor |
| C: repeated support | W5 `efficiency-loop` / efficiency / work | `think-n53s` or `think-hye3` | Only a selected critical dependency: retained-receipt comparison or fixed-data H-348 support within its cap | Exact retained fixture/refusal commands declared before support starts; V0 on resulting records | Per-artifact/combined cap or no critical dependency: stop and return capacity to M | Record support’s scoped disposition; no mandatory next case |
| I: checkpoint integration | W10 `review-planning-oversight` / process / work | `think-wnbr` | Stable checkpoint, exact obligation/census changes, costs and future allocation | V0, V4 and reachable push checks for actual changes | Writers active or evidence incomplete: stop integration; preserve debt/partial scope | Reopen only prospectively selected M/P/T/R |
| G: gate supervision | W2 `factual-review` / correctness / work before H7, finalization afterward | `think-wnbr` | Frozen-source full gate, command receipt and explicit certification status | V5 under unchanged outer/resource guards | Gate ceiling, cleanup failure or changed source: stop/reap; retain actual failure/debt | F, with exact certification follow-up if needed |
| F: block closure/replan | W10 `review-planning-oversight` / process / finalization | `think-wnbr` | Terminal dispositions, native resource receipt, W10 documentation review, successor selection and durable handoff | V0, V4, session clocks/gate/rollup checks and exact changed-record checks | Hard deadline: no new research; close existing evidence with explicit debt | Next block’s K on its actual clock, or final ranked handoff |

W3 may produce a structural argument without a numerical experiment.
Its deciding proof review is R; do not represent a candidate as certified merely because
it was written. Instrument readiness and target measurement are separate boundaries.
New measured claims need serially allocated hypothesis/experiment records before
measurement; reuse existing IDs only for their unchanged registered scope.
A continuing command may span several supervision leases with the same frozen command
ceiling; renewed leases do not extend its scientific budget or erase cumulative cost.

All command bindings run from `packing/` under the prepared environment; substitute
exact repository-relative paths and argv before the active phase is recorded:

| Binding | Prospective exact command or deciding check |
| --- | --- |
| V0 | `uv run --frozen --all-extras --group dev packing-validate --records --jobs 2 --inner-jobs 1`, then `uv run --frozen packing-ledger check`; use only reachable subsets for later unchanged-record checks |
| V1 | Fresh Astra max quantified-domain proof review; exact maintained checker/replay command named in the new artifact if computational evidence is used |
| V2 | `uv run --frozen --all-extras --group dev pytest -q tests/test_score_n17_capture.py tests/test_check_n17_capture_checkpoint.py tests/test_pilot_n17_capture.py`; replace/add exact affected converter/pose tests when those are selected |
| V3 | Exact registered producer plus FULL verifier/replay argv and endpoint/domain controls; no generic command or provisional path may survive into the active phase |
| V4 | `git diff --check`, configured Flowmark check, actual generated-view checks and exact source-aware session checks; inspect every changed/staged path |
| V5 | The eight-hour plan’s `devtools.supervise_posix --max-seconds 3580 --max-memory-mib 8192` command around `packing-validate --jobs 1 --inner-jobs 4`, with block-specific retained output and outer/resource guards |

## Evidence-Based Selection at Every Block Boundary

Freeze the mathematical result and its exact scope, initial soundness/admission status,
remaining premises, achieved domain coverage, failures, cumulative costs and source
state. Then select two named mathematical obligations and the smallest engineering
dependency. Every selected target receives a new prospective resource envelope; an
unfinished experiment retains its original ceiling and cannot receive a fresh budget by
renaming its block. Reuse named premises while repeated confirmation is pending; known
soundness faults still block unconditional use.

| Retained evidence | Block 2 selection | Block 3 selection only if earned |
| --- | --- | --- |
| H-347 allowance table incomplete but its contract is sound | Price completion of all 45 entries from the registered 10–20 agent-hour estimate and actual remaining scope; completion is not promised; then choose one actual anisotropic per-square slide extension | Compose the reviewed extension with effective capture radii, or resolve its exact remaining premise |
| H-347 complete and below its unchanged criterion | One per-square extension selected by capture burden, with whole-slider/root/frame/D4/seam obligations | Exploit that measured or priced gain in one capture/localization interface |
| Allowance threshold obstruction or inconsistent input join | Retain exact reduced target and isolate one root/slider/frame obstruction; repair or prove a conditional interface | Changed bound/relation or exact counterexample; a repeated unchanged table is not progress |
| H-345 complete contraction at its actual registered scope | Preserve its round-20 verdict; price an exact capture argument from that output, or preregister any extension’s objective, criterion and cumulative budget before further production | Only a demonstrated complete-domain implication earns a capture claim; otherwise retain remaining reach/feature obligations |
| Capture readiness/calibration fails or replay/20 rounds cannot fit | Select exact slider/localization mathematics or the scoped perturbation-bridge candidate; renewed repair needs new evidence and a complete-run price | Exploit a proved interface, or change the relation after its precise obstruction |
| New exclusions with a working production/FULL/admission pipeline | Freeze one new small greedy marginal-coverage batch and new complete pricing; no extrapolated closure rate | One newly priced batch only if exact coverage and resources justify it; report union after overlap removal |
| Stronger joint-pose lemma has certified nonzero gain | Complete its quantified scope and consumer/source contract, or retain an exact failing witness | Transfer it to one further state or one precisely defined wall-chain class, with full domain/separator proof; never infer closure of the 94 distance-two orbits (736 states at preparation) |
| Complete bounded negative or no certified gain | Diagnose the frozen domain and smallest deciding obstruction; select a genuinely changed relation | Test/prove the changed relation or retire it at scope; infrastructure readiness is separate |

For H-342, rank current eligible rows by exact greedy marginal uncovered-orbit coverage,
ties by row ID; freeze one bin configuration per row.
A new small batch needs a complete production/FULL/admission reserve before every next
launch and one priced envelope, as in Block 1. Three selected rows cannot decide the
full-population hypothesis.
Preserve certificate size/budget and exclusion soundness as separate verdicts; no census
changes before applicable verification and admission.

H-345 may resume across blocks only from the verified same frozen chain, retaining all
rounds, endpoints, fresh replay and cumulative costs.
This resumes an incomplete experiment within its original 20-round scope.
Additional rounds after a completed verdict require a new prospectively registered
measurement contract; a shared physical chain does not extend the old scope.
The original contract must permit checkpoint/restart, or a separately preregistered
continuation must preserve its prior censored verdict and cumulative budget; do not
reset an expired command deadline.
It still needs accepted H-337 calibration and all 20 rounds.
Its 5–20 CPU-hour estimate is not eight hours of wall time.
Ten-percent motion is not capture.
For a stronger tail lemma retain full outer pose ranges, every separator/seam, common
centre/angle per owner across contacts and saved-node induction history.
The exhausted shared-centre LP and unchanged 96-row binary consistency selection remain
excluded.

A separately priced candidate is the
[restricted family-cell audit](../../research/research-2026-10-09-n17-family-cell-audit.md)
perturbation bridge.
Investigate the implication suggested by $409960561/423200000<(99/100)^2$: seven
alternative-cell incircle exclusions could persist for blocker-centre Euclidean shifts
at most $1/100$ under the retained slider scope.
A useful bridge must also prove all sixteen occupied-cell assignments, the cover/frame
hypotheses and the near-family-core-to-free-square assignment.
This is a candidate for new derivation and independent review, not a retained
perturbed-core result or arbitrary reach claim.
Register any chosen measured target before sampling.

## Block 1: Establish the Two Mathematical Routes

Slots 1–16 use the complete existing eight-hour plan.
At local H0 freeze H-347 and BC-460 contracts and disjoint ownership; at H1 pivot
unaffordable nonterminal inputs to a stronger surviving-mask relation; at H1:30
explicitly switch Sol if capture readiness or complete pricing failed.
At H4 integrate actual mathematical scope and reprice only future work.
Stop scientific/code writes at H6, launch the full gate by H6:15, cut it off by H7:15
and close/replan by H8. Block 2’s choice is an output of this block, not today’s
prediction substituted for evidence.

## Block 2: Finish One Interface and One Nonterminal Discriminator

These are complete maximum allocations, local offsets from observed $B_2$; slots 17–32
are nominal run offsets H8–16. A selected row inherits the full phase contract above.
M names one or both source-only mathematical delegations; P/T/R/I name the coordinator’s
primary material phase, with disjoint mathematics continuing where its dependencies
allow.

| Slot | Local offset | Capture/terminal Astra lane | Nonterminal Astra lane | Sol, review and coordinator |
| --- | --- | --- | --- | --- |
| 17 | H0–0:30 | K: choose incomplete allowance or demonstrated interface gain | K: choose exact new batch or changed joint-pose relation | Observe clocks, recheck resources, freeze scopes and costs |
| 18 | 0:30–1 | M: finish named missing coordinate charges | M: freeze exact coverage or full surviving-mask domain | P: only the selected mathematical dependency |
| 19 | H1–1:30 | M: complete root/frame/D4/whole-slider joins | M: simultaneous three-owner argument or exact witness | R: fresh admission review; reject unaffordable target |
| 20 | 1:30–2 | M: complete table or exact obstruction | T if pipeline/pricing ready; otherwise M | Explicit Sol switch to exact converter/constraint if capture misses readiness |
| 21 | H2–2:30 | M: derive one anisotropic per-square extension | M/T: complete selected domain or production/replay pair | P: reviewed implementation, positive and refusal controls |
| 22 | 2:30–3 | M: close seams and square-6/frame obligations | M/T: FULL decision/admission before next row | R: soundness and complete-command evidence |
| 23 | H3–3:30 | M/R: exact extension result or scoped counterexample | M/R: complete discriminator or full scoped diagnosis | Stop unaffordable growth; price next dependency |
| 24 | 3:30–4 | Stop lane writes by H3:45 | Stop lane writes by H3:45 | I: source-bound H4 checkpoint, exact union and future selection |
| 25 | H4–4:30 | M: compose proved extension/effective radii | M: selected changed relation, not automatic larger population | P/R: smallest remaining mathematical dependency |
| 26 | 4:30–5 | M/T: priced same-chain continuation or bridge derivation | M/T: one complete changed-domain test if admitted | Keep cumulative target caps; C only for a critical dependency |
| 27 | H5–5:30 | R: independent exact scope/remaining premises | R: independent gain/witness review | Sol: integrate reviewed source, price Block 3 options |
| 28 | 5:30–6 | Final exact interface packet | Final exact result/diagnosis packet | Stop scientific/code writes by H6; preserve source/base |
| 29 | H6–6:30 | Read-only argument audit | Read-only domain audit | G: launch stable full gate by H6:15 |
| 30 | 6:30–7 | Read-only scope interpretation | Read-only overlap/induction interpretation | G: renew supervision lease without changing command ceiling |
| 31 | H7–7:30 | Finalization only | Finalization only | G/F: gate cutoff H7:15; actual receipts, records and certification |
| 32 | 7:30–8 | Finalization only | Finalization only | F: complete W10 Block 3 selection, publication and terminal handoff |

## Block 3: Transfer a Demonstrated Gain or Close Its Obstruction

Local offsets use observed $B_3$; slots 33–48 are nominal H16–24. The Block 2
disposition selects the actual branch.
A transfer earns its own quantified proof; a changed relation is a new unresolved
candidate until its deciding evidence exists.

| Slot | Local offset | Capture/terminal Astra lane | Nonterminal Astra lane | Sol, review and coordinator |
| --- | --- | --- | --- | --- |
| 33 | H0–0:30 | K: select one proved gain or exact missing bridge premise | K: select one further state/precise wall-chain class or changed relation | Observe clocks; admit only a complete remaining-budget recipe |
| 34 | 0:30–1 | M: compose anisotropic interface with capture inequalities | M: freeze transfer domain, all alternatives and old-relation control | P: freeze required source/control scope |
| 35 | H1–1:30 | M: derive full-domain localization or scoped bridge obligation | M: prove transfer implication or produce exact witness | R: fresh source/domain review; retain any blocked premise |
| 36 | 1:30–2 | M/T: only admitted same-chain capture continuation | M/T: one finite discriminator if registered and affordable | Explicit Sol mathematical-support switch on readiness/pricing miss |
| 37 | H2–2:30 | M: endpoint, feature, slider and frame composition | M: full transferred-domain/separator argument | P/R: exact implementation and refusal checks |
| 38 | 2:30–3 | M/T: finish selected capture implication or retain residual gap | M/T: finish production/FULL pair or exact domain diagnosis | Complete decision/admission reserve before another target |
| 39 | H3–3:30 | R: independent argument/counterexample review | R: independent transfer/gain/witness review | Sol: reviewed outputs and actual costs |
| 40 | 3:30–4 | Stop lane writes by H3:45 | Stop lane writes by H3:45 | I: final H4 selection by unresolved mathematical payoff |
| 41 | H4–4:30 | M: discharge one remaining composition premise | M: complete one transfer premise or changed relation | P/R: selected exact support; no catch-up confirmation |
| 42 | 4:30–5 | M/T: finish only a fully priced declared result | M/T: finish only the selected bounded scope | Preserve censoring, unchanged hypotheses and cumulative costs |
| 43 | H5–5:30 | R: final exact scope and global-gap audit | R: final exact union/domain/witness audit | Sol: stable-source integration and certification readiness |
| 44 | 5:30–6 | Final proved implication or scoped obstruction | Final admitted exclusion/lemma or bounded negative | Scientific/code freeze H6; record exact continuation beyond this run |
| 45 | H6–6:30 | Read-only composition audit | Read-only quantified-domain audit | G: launch stable full gate by H6:15 |
| 46 | 6:30–7 | Read-only interpretation | Read-only interpretation | G: bounded supervision, actual verdict and cleanup |
| 47 | H7–7:30 | Finalization only | Finalization only | G/F: cutoff H7:15; final resource, certification and document receipts |
| 48 | 7:30–8 | Finalization only | Finalization only | F: complete run disposition, publication and one ranked next entry |

## Gates, Replanning and Realistic Outcomes

At each H4 checkpoint lane writes end 15 minutes before integration.
At each H6 freeze, all scientific/code writers stop before source sealing and broad
checks. Start V5 by H6:15 with its 3,580-second supervisor cutoff inside a 3,600-second
outer envelope; stop by H7:15, leaving 45 minutes for records, publication and handoff.
These nominal offsets apply only to a full block; a shortened block uses its actual
deadline cutoffs and repriced schedule above.
Split supervision and finalization into at-most-30-minute leases.
A late launch shortens the command ceiling; changed source invalidates affected
certification, and an unaffordable rerun remains explicit debt.
No gate wait leaves exact read-only review idle.

At every block boundary disposition each commitment: proved/validated scope, bounded
negative, censored/unresolved work, infrastructure-only change, or skipped/blocked
input. Record why the successor’s mathematical payoff exceeds its cost and why any
repeated confirmation is a critical dependency.
Apply the documentation/common-guidelines and de-slop pass once per block; preserve
source, failure receipts and unique research.
Resource measurements follow native task-tree receipts, not 72-hour arithmetic; terminal
closeout renders existing views and retains honest certification status.

| Scenario after three blocks | Realistic mathematical outcome and remaining limit |
| --- | --- |
| Best scoped result | Complete H-347 table, one reviewed useful anisotropic slider/bridge interface, and some newly admitted exact exclusions or one stronger joint-pose lemma transferred to a further state/precise class; any complete capture implication earns only its proved domain |
| Plausible partial result | Reusable exact allowances/conditional interface and one decisive nonterminal result, with missing localization, transfer or pose premises named and priced |
| Bounded negative | Exact allowance obstruction, failed changed pose relation with a witness, or complete target miss under frozen controls; diagnoses one route without declaring a global architecture failure |
| Readiness/resource stop | Source/control progress and explicit mathematical dependencies; no target verdict and no mathematical closure inferred from implementation |

Three blocks do not promise a complete global proof.
Remaining obligations may include all unexcluded nonterminal orbits under the same
cover/cap, outer-family reach and feature localization, every required slider/frame/root
join, terminal certification across the actual captured domain, and the composed proof’s
required admission/assurance package.
Track their exact AND/OR dependencies and exclusion unions after overlap removal; task
or lemma counts and selected-row rates are not proof percentages.

Do not automatically launch the roughly 308-CPU-hour H-343 production sweep, H-344’s
estimated one-to-two-agent-week build, H-346’s roughly 25-agent-hour build, or full
H-348’s 20–30-agent-hour checker.
They require their own measured/priced selection; a bounded component can be chosen only
when it closes a current mathematical dependency.
After the final block, retain a ranked, costed continuation from observed evidence and
one coordinating bead/workflow.
Further work requires its own scope and clocks; the 24-hour estimate is not a claim that
the remaining global gaps will close.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
