# Continuation Addendum: Post-3.81 Portfolio, T+2 Through T+10

Status: **bound launch contract; active research remains held until the final local
gates pass and the coordinator releases the four acknowledged roles.**

Continue Agenda 024 from active portfolio minute 120 through minute 600 under this
addendum. It reconciles the two post-T+2 readiness audits and controls execution through
the T+4 and T+8 gates and the T+10 intermediate handoff.
It does not replace or amend a frozen scientific result.

## Authority and Frozen Boundary

[`agenda-024`](../../packing/campaign/agendas/agenda-024-post-381-24h-portfolio.md)
remains the portfolio control plane.
Its
[`agenda-025`](../../packing/campaign/agendas/agenda-025-adaptive-fractional-frontier.md)
and
[`agenda-026`](../../packing/campaign/agendas/agenda-026-density-stationarity-and-trump-capture.md)
manager programs remain authoritative except where this addendum narrows or sequences
work after T+2. The [`T+2 handoff`](handoff-2026-09-06-post-381-t2-commissioning.md) and
its linked manager and coordinator packets remain the evidence boundary for the
completed commissioning block.

If these documents conflict about work after T+2, use this order:

1. Frozen input bytes, preregistrations, result packets, and their original claim
   labels.
2. This continuation addendum for T+2 through T+10 execution.
3. Agenda 024, then the applicable manager agenda.
4. A later coordinator gate packet, but only for work that the preceding gate was
   authorized to choose.

The addendum changes no frozen hash, experimental observation, or proof status.
New work writes fresh paths.
No worker edits a T+0-to-T+2 result packet, retained certificate, archived source,
generated ledger, frontier view, or session-close record.

The continuation starts from these fixed facts:

| Item | Frozen value |
| --- | --- |
| Detached post-PR89 staging base | `00e774de8c3cbb6695402615992d92ab1b4f4c93` |
| Scientific launch revision | `c55726e1e885227f63110131c0a914665175ff89` |
| Frozen preregistration revision | `f1b6c641e8d3a2fea39cf5aa5292cb8fc1221772` |
| T+0 | `2026-09-06T03:31:00Z` |
| T+2 boundary | `2026-09-06T05:33:28Z` |
| Portfolio allocation | 120 active minutes consumed; 1,320 remain |
| BC-232 retained leg-01 state | `f91999b452bf89f49e2d4cda9827efbf57623a4196688b5feba0819bc7e851e2` |
| BC-232 retained leg-01 summary | `d8c50db8770b12d43baa6d9e2c7384a52a0f250f8cee26b6a036c99b3cb3350e` |
| BC-232 retained leg-01 family | `4cfbdce5cb659d77d652c011854de74ddcad94c903eff30af07bbcb5d8d9cc3f` |
| Trump tangent record | `60a4b7c48034b37063509a8a641974ed5eae86dccd056e9cbc6cf2fd7f2f0661` |
| BC-199 radius record | `db124b9956d8051682388cbba3b16772e65406a0003debba1c92b915c0c489a8` |
| Exact Trump witness source | `3b4eae938c37c13af6252ac5d83fa99aa95f6b1627b99920c5df8be94c56bea9` |

The T+2 handoff’s landing receipt owns the complete post-freeze packet manifest.
The table above repeats only the inputs used directly in the next block.

### Prospective Prose-Digest Reconciliation

Two prose artifacts no longer reproduce their historical checkpoint digests:

| Artifact | Historical digest | Live digest at this draft base | Classification |
| --- | --- | --- | --- |
| `packing/campaign/series/series-000-smoke-and-calibration/results/agenda-025/bc-232-disposition.md` | `462f4049a518073be0e1a1f519d47a12c832bd94e670194329652744af9cb387` | `2816e4437fdf18599b1a00e5d680e5affa3d056bb985927628be8fa5ef50cbf2` | provenance unreproduced |
| `packing/campaign/series/series-000-smoke-and-calibration/experiments/exp-070-h-064-n11-fractional-resume.md` | `36d546ca...` | `618947d5e48041c5de0a9a0068ebe11ee084a61693ddb7ad8d483bd690b44a06` | provenance unreproduced |

The readiness audit retained only the `36d546ca...` historical prefix for the exp-070
note. Do not expand it by guessing or reconstruct either earlier prose body.
These are prose-provenance mismatches, not scientific-data drift.
The BC-232 leg-01 log, state, summary, and family still match their frozen machine
hashes `431737c5...`, `f91999b4...`, `d8c50db...`, and `4cfbdce5...`; no scientific
value, endpoint, command, or interpretation changes.
The T+4 packet must carry both prose-digest pairs and this classification instead of
rewriting the historical T+2 manifests.

Preserve these claim labels:

- `T-018` remains the formal first-party claim `s(11) >= 381/100`.
- BC-232 reports an exact packing-family lower endpoint and a separate row-converged
  floating computational upper endpoint.
  Neither label transfers to the other quantity.
- BC-240 is a retained-record-dependent, labelled, anchored, fixed-side local-isolation
  and side-stability theorem only.
  BC-241 cannot turn it into global capture, global uniqueness, or global optimality.
- BC-242 proves weak duality for the absolutely continuous primal and Lebesgue-a.e.
  dual. It proves no strong duality, attainment, singular-primal theorem, or numerical
  endpoint.
- BC-245 is a finite typed stationary-language theorem, not an enumerated or complete
  `n = 11` atlas.
- BC-243 may report only an exact dual lower value and the one-sided interval
  `[D, infinity)`. Continuum primal coverage belongs entirely to BC-244.

## Coordinator Binding Required Before Launch

This transport draft may be committed with the delimited tokens below.
The coordinator must replace every token with observed data in a later binding commit
and push that commit before releasing active research.
Opening the continuation pull request may precede the binding commit so its URL can be
observed. Do not infer the PR #89 merge commit from its former open head.

<!-- BEGIN COORDINATOR BINDING: REQUIRED BEFORE ACTIVE RESEARCH -->

| Binding | Observed value |
| --- | --- |
| PR #89 merge commit on `origin/main` | `6b21d14b64c19003d597ed3c993c051b64336b0c` |
| Final `origin/main` base | `6b21d14b64c19003d597ed3c993c051b64336b0c` |
| New branch name | `codex/post-381-t2-t10` |
| New-branch transport head before the binding commit | `552e0c6969a6aa3a5a2e2a539e826c0bab8c7c83` |
| Continuation pull-request URL | <https://github.com/jlevy/squares/pull/97> |
| Cooperative-stop implementation commit on this branch | `228806215149549032522506325bd524a71cbd4d` (transport provenance `37ca074d2a9e0027d334be03c982b24ffb6acd4a`) |
| Coordinator identity and acknowledgement UTC | `/root`; `2026-09-06T09:43:25Z` |
| Fractional-manager identity and acknowledgement UTC | `/root/fractional_manager`; `2026-09-06T09:42:33Z` |
| Closure-manager identity and acknowledgement UTC | `/root/closure_manager`; `2026-09-06T09:42:29Z` |
| Floating-reviewer identity and acknowledgement UTC | `/root/closure_manager/bc241_source_reviewer`; `2026-09-06T09:42:33Z` |
| PR #93 | MERGED as `3122c49766e7fc70c8cb299bd8b6b09558447d8a` at `2026-09-06T09:06:10Z` |
| PR #94 | OPEN and `DIRTY` at `9c82dc2ac5fecfa94d9388ef61c6b1d4bc21169b` |
| Continuation release-authorization UTC | `2026-09-06T09:43:25Z` |

<!-- END COORDINATOR BINDING -->

At `2026-09-06T09:43:25Z`, `/root` recorded: “I bind the four roles, frozen inputs,
clocks, execution graph, and fresh output paths in this addendum.
I alone will move a shared gate or claim.”
The three delegated acknowledgements are the verbatim statements in the role table
below, tied to the identities and UTCs above.

The staged cooperative-stop manifest is:

| Path | SHA-256 |
| --- | --- |
| `packing/devtools/run_fractional_cutting.py` | `38648bc40d811df91005c4b7391601500d31816526543ef39b9d21e43c867b05` |
| `packing/src/sqpack/fractional/cutting.py` | `6ed0043bd66ca9525cca74d757a596bbf5e5b4eaea96f91e79a70b22bea6f4b4` |
| `packing/tests/test_fractional_cutting.py` | `56bd0f1a4c20e24a5459af87372ac5bd14a50fbdfa704544cfdad47a4ed12c43` |
| `packing/tests/test_run_fractional_cutting.py` | `25769fabee0aa19642d764d2dd5bf70369000232780bcc2d52eba657d9ff6084` |

The release-authorization UTC is a committed not-before boundary, not the actual T+2
restart. It authorizes the launch transaction below but does not start the active
portfolio clock. Actual manager and reviewer restart UTCs belong in their first
microreceipts, not in this binding block.

## Launch Release Sequence

Before active research starts, the coordinator must:

1. Create the new branch from the bound final `origin/main` base.
   Replace every binding token that is then observable, including the
   release-authorization UTC, new-branch transport head, and all four role
   acknowledgements; only the new pull-request URL may remain unfilled.
2. On the new branch, run the focused cooperative-stop checks recorded by `think-qke4`
   and the repository’s local edit gate.
   Both must pass.
3. Commit and push the staged stack durably, then open the continuation pull request.
4. Record the observed pull-request URL, rerun the local focused and edit gates, commit
   the fully bound addendum, and push that exact binding commit to the open pull
   request.
5. Confirm the four leg-02 output paths are still absent and no earlier scientific
   process is live, then release the two managers and floating reviewer.

Do not wait for hosted CI to turn green before that first release.
Hosted checks run concurrently with the research block after the local focused and edit
gates, durable push, and open pull request exist.
If a required hosted check reports failure, record the failure UTC, pause the active
portfolio clock, repair and validate outside active time, push the repair, and resume
only after the local focused and edit gates pass again.
An already authorized numerical process may reach its frozen stop while the clock is
held; record its actual process wall and CPU cost and do not extend or restart it.

## Roles and Acknowledgements

Use exactly four live contexts: one coordinator, two managers, and one transferable
reviewer. A background numerical process is not another agent slot.

| Role | Reasoning | Exclusive responsibility | Required acknowledgement |
| --- | --- | --- | --- |
| Coordinator | `max` | Shared state, tbd, criteria, gates, upstream integration, claim promotion, commits, pushes, and handoffs | “I bind the four roles, frozen inputs, clocks, execution graph, and fresh output paths in this addendum. I alone will move a shared gate or claim.” |
| Fractional manager | `max` | Agenda 025 work, BC-232 and scalar process supervision, BC-231 routing, and `results/agenda-025/` packets | “I accept the frozen fractional commands, stop rules, labels, budgets, and output stems. I will not spend leg 03 before BC-220.” |
| Closure manager | `max` | Agenda 026 work, final BC-241 and BC-243 dispositions, and `results/agenda-026/` packets | “I accept BC-240’s local-only boundary and BC-243’s dual-only boundary. I will not open BC-243 before BC-220 or BC-244 without a later gate.” |
| Floating reviewer | `xhigh`; `high` only for deterministic mechanics | One bounded source-distinct review or implementation-control assignment at a time. For BC-241, the only reserved writes are `packing/devtools/review_trump_local_theorem.py`, `packing/tests/test_review_trump_local_theorem.py`, and `packing/campaign/series/series-000-smoke-and-calibration/results/bc-241-trump-local-theorem-review.json`. | “I accept only the current assigned paths and checklist. I will not change criteria, promote a claim, edit shared state, or retain the slot after my packet is terminal.” |

The floating reviewer is one transferable context, not one worker per manager.
It begins with BC-241. A manager may receive it only after the preceding manager accepts
a terminal packet and the coordinator records the transfer.
Generator authors and source-distinct reviewers must be different contexts.
Any mathematical choice found during a `high` mechanical check stops that check and
returns to a `max` manager.

Managers may write only their reserved source, test, and result roots.
The coordinator alone mutates tbd or shared generated records.
No manager or worker pushes, merges, rebases, changes a budget, or reallocates an ID.

Each manager and the floating reviewer records its actual restart UTC in its first
microreceipt. The first coordinator receipt records the effective T+2 clock start.
Every first continuation microreceipt also binds the wall authorization
`2026-09-06T08:22:36Z`, eight-hour target `2026-09-06T16:22:36Z`, and outer deadline
`2026-09-06T18:22:36Z`. These fixed wall-clock controls neither start nor advance active
portfolio time. That time is no earlier than the committed release-authorization UTC,
every required role’s acknowledgement UTC, completion of the local focused and edit
gates, the durable branch push, and creation of the pull request.
If the contexts start at different times, the shared clock starts at the latest
required-role restart; no receipt backdates it into the launch transaction.

## Time and Cost Accounting

The active portfolio clock resumes at T+2, active minute 120. It reaches T+4 at minute
240, T+8 at minute 480, and T+10 at minute 600. Reaching T+10 consumes 480 continuation
minutes and leaves 840 of Agenda 024’s 1,440-minute allocation.
T+10 is an intermediate handoff, not the T+12 portfolio pivot.

Use the clocks as distinct measurements:

| Measurement | Meaning |
| --- | --- |
| `active_portfolio_minutes` | Progress on the synchronized Agenda 024 schedule. Parallel roles count once, and a shared gate holds this clock. |
| Wall time | UTC elapsed time, including operational holds. The unattended authorization asks for eight wall hours of progress and a ten-wall-hour outer handoff window; neither duration may be relabelled as active time. |
| Process wall | Each command’s actual elapsed wall time. A command’s `--minutes` value is its frozen maximum process-wall budget. |
| Process CPU | Measured CPU time when available. If no terminal sample exists, report unknown and retain any live sample only as a lower bound. |
| `role_assigned_minutes` | Time a context held a role, including intervals when attentive telemetry is absent. |
| `agent_minutes` | Attentive work observed directly or reported explicitly by the context. Unknown attention stays unknown. |
| Gate mechanics | Integration, regeneration, validation, commit, push, hosted CI, tool recovery, upstream reconciliation, and handoff. These consume wall and labor, not active portfolio minutes. |

Pause the affected lane and the shared gate for quota or usage loss, approval wait,
unavailable agent or host, worktree setup, tool failure, process recovery, upstream
integration, or gate mechanics.
The unaffected lane may finish already authorized work but may not cross the gate,
borrow the next block, or change a criterion.
A timeout is never extended after inspecting its result.

No assignment may run for more than 30 active portfolio minutes without a written
microreceipt. Each receipt records the active interval, role holder, completed work,
fresh or changed paths and hashes, process identity and status, exact endpoint labels,
actual process wall and CPU observations, directly observed attention or `unknown`, and
the next unchanged action.
Long background processes continue across these slices; the manager checks them without
restarting them.

If the ten-wall-hour outer window arrives before active minute 600, stop at the actual
active minute, freeze both lanes, and publish a partial handoff.
Do not write a T+10 receipt or claim 480 continuation minutes.

## Bound Execution Graph

The execution epic is `think-jgnv`. Its authoritative direct-child set lives in tbd; the
set observed by this launch-graph audit is listed below so a later child addition cannot
hide behind a hard-coded count.
Do not select substitute work from the repository-wide ready list.

| Child | Boundary | Bound work |
| --- | --- | --- |
| `think-5pj8` | Pre-release; terminal | Land PR #89 and cut `codex/post-381-t2-t10` without starting the active clock. |
| `think-yjh8` | Pre-release | Complete this launch addendum and role contract. |
| `think-qke4` | Pre-release; terminal | Implement and verify the opt-in cooperative fractional stop outside active research time. |
| `think-6yx2` | T+2 to T+4 | Manage the fractional lane. |
| `think-gab1` | T+2 to T+4 | Manage the closure lane. |
| `think-vniz` | T+4 gate | Hold and decide BC-220. |
| `think-0p1m` | T+4 to T+8 | Manage the fractional lane. |
| `think-v55y` | T+4 to T+8 | Manage the closure lane. |
| `think-u8h0` | T+8 gate | Hold and decide BC-221. |
| `think-522z` | T+8 to T+10 | Manage the fractional lane. |
| `think-y1zc` | T+8 to T+10 | Manage the closure lane. |
| `think-2jzh` | T+10 landing | Land the intermediate checkpoint and cold-agent handoff. |
| `think-f5t7` | T+2 through T+10 | Monitor PRs #93 and #94 and integrate only commits landed on `origin/main`. |
| `think-g024` | Pre-release blocker | Reconcile the n=11 Lean formalization spike before continuation release. |
| `think-ualx` | Pre-release; terminal | Correct the fractional-certificate proof scope and checker trust boundary; integrated at `7e932f1b`. |
| `think-i6q1` | Pre-release blocker | Harden continuation state, ownership, clocks, and review supersession. |
| `think-a70y` | Longer-term; nonblocking | Design a proof-producing Condition 5 arrangement receipt. |
| `think-283c` | Pre-release blocker | Reconcile the final integration audit before the T+2 release. |
| `think-57kj` | Pre-release; pending | Audit and disposition the dilation corollary and possible sharper supremum bound above 3.81. |

Before either lane restarts, `think-yjh8`, `think-g024`, `think-i6q1`, `think-283c`, and
`think-57kj` must be terminal; `think-qke4` and `think-ualx` are already terminal.
The two T+2-to-T+4 lane beads require the addendum, and the fractional lane also
requires the cooperative-stop implementation.
Both lane beads feed the T+4 gate.
The T+4 gate bead `think-vniz` also requires the existing `think-jeyp` hashed
provisional packet. The coordinator must record that edge with
`tbd dep add think-vniz think-jeyp` before release.
`think-jeyp` is a prerequisite, not a direct child of this continuation epic.
The two T+4-to-T+8 lane beads feed the T+8 gate, and the two final lane beads feed the
T+10 landing. `think-a70y` is explicitly longer-term and cannot block release or consume
this continuation’s active time.
`think-f5t7` runs as coordinator work across the whole continuation and never imports an
open pull-request head.

## Cooperative Fractional Stop

`think-qke4` adds the opt-in flag `--stop-on-covering-below-n` to the production cutting
path before either continuation command runs.
Default behavior without the flag remains unchanged.

With the flag present, stop only when the current covering solution has a finite
`solution.objective < n` and `solution.converged` is true.
Evaluate the predicate after the iteration’s exact separation has completed and before
any new sites are added.
Then take the ordinary serialization path: preserve the log, state, summary, and
best-family outputs with a machine-readable stop reason.
The state must remain acceptable to `devtools.freeze_cutting_primal`.

A converged solution with a non-finite objective is a technical refusal at that same
boundary.
Return nonzero before publishing the iteration or state; do not serialize it as
an ordinary non-triggering checkpoint.

The implementation controls must prove that:

- a finite, converged objective below `n` stops before site addition and writes all
  requested outputs normally;
- equality, a finite value above `n`, and an unconverged value below `n` do not trigger
  the stop;
- a converged non-finite objective produces a technical refusal before iteration or
  state publication;
- omitting the flag preserves existing behavior; and
- a stopped state can enter the existing covering bridge without manual repair.

This safety work is operational and consumes no active research time.
A production run cannot start until its implementation commit and complete changed-path
hash manifest are in the coordinator binding.

## T+2 to T+4: BC-232 and BC-241

Run four slices of at most 30 active minutes.
BC-232 is the fractional manager’s only long process.
The closure manager supervises the source-distinct BC-241 review, and the floating
reviewer executes that frozen checklist.
No BC-243 implementation or pilot may start before BC-220.

### BC-232 Leg 02

Require the four leg-02 output paths to be absent.
From `packing/`, launch this literal command once:

```bash
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 \
uv run --frozen --all-extras --group dev python -m devtools.run_fractional_cutting \
  --n 11 --side 191/50 --shrink 9977/10000 \
  --angle-limit 207107/500000 --steps 180 \
  --minutes 105 --iterations 40 --cap 150 --support-cap 96 \
  --rows-rounds 2 --rows-per-direction 3 \
  --stop-on-covering-below-n \
  --warm campaign/series/series-000-smoke-and-calibration/results/agenda-025/bc-232-leg-01-state.json \
  --log campaign/series/series-000-smoke-and-calibration/results/agenda-025/bc-232-leg-02.log \
  --state campaign/series/series-000-smoke-and-calibration/results/agenda-025/bc-232-leg-02-state.json \
  --json campaign/series/series-000-smoke-and-calibration/results/agenda-025/bc-232-leg-02-summary.json \
  --freeze campaign/series/series-000-smoke-and-calibration/results/agenda-025/bc-232-leg-02-family.json
```

The flag is the sole command amendment to the unused leg-02 continuation in the T+2
packet. It enforces that packet’s existing crossing stop; it changes no input, numerical
parameter, budget, endpoint definition, or scientific criterion.

If a safe crossing stops the run, preserve all four outputs and require both bridge
paths below to be absent.
Then run this literal command once from `packing/`:

```bash
uv run --frozen --all-extras --group dev python -m devtools.freeze_cutting_primal \
  --n 11 \
  --state campaign/series/series-000-smoke-and-calibration/results/agenda-025/bc-232-leg-02-state.json \
  --angle-limit 207107/500000 --steps 180 \
  --rows-rounds 2 --rows-per-direction 3 --scale 4000000 \
  --deadline-seconds 1200 \
  --freeze campaign/series/series-000-smoke-and-calibration/results/agenda-025/bc-232-leg-02-covering-candidate.json \
  --json campaign/series/series-000-smoke-and-calibration/results/agenda-025/bc-232-leg-02-covering-bridge-receipt.json
```

The 1,200-second deadline is cooperative inside the row-generation loop.
A convergence detected before the deadline may be followed by a final solve,
rationalization, and publication tail, so report actual total wall time even when it
exceeds 1,200 seconds.
A deadline, unconverged row loop, rejected program, rationalized total at least eleven,
or existing output path is a pre-publication refusal.
It writes neither candidate nor success receipt and does not authorize a rerun.
An I/O error or interruption may instead leave a candidate-only or partial path.
Preserve any such path as a terminal technical failure; never submit it to declaration
or decision. Do not rerun or replace it unless a later coordinator gate authorizes a
fresh stem.

Only after the bridge exits zero and both fresh paths exist, run this exact sequence
from `packing/`:

```bash
shasum -a 256 \
  campaign/series/series-000-smoke-and-calibration/results/agenda-025/bc-232-leg-02-covering-candidate.json
uv run --frozen --all-extras --group dev python -m devtools.declare_least_cell_mass \
  campaign/series/series-000-smoke-and-calibration/results/agenda-025/bc-232-leg-02-covering-candidate.json
shasum -a 256 \
  campaign/series/series-000-smoke-and-calibration/results/agenda-025/bc-232-leg-02-covering-candidate.json
uv run --frozen --all-extras --group dev python -m devtools.decide_certificate \
  campaign/series/series-000-smoke-and-calibration/results/agenda-025/bc-232-leg-02-covering-candidate.json
.venv/bin/python3 cases/n11_fractional_certificate/minimal_verify.py \
  --unpinned \
  campaign/series/series-000-smoke-and-calibration/results/agenda-025/bc-232-leg-02-covering-candidate.json
```

Record the raw and declared candidate hashes separately.
A crossing, bridge success, declaration, decision, and independent verification are
distinct evidence steps; a failure in one does not inherit the prior step’s label.
Propose no further fractional search before this sequence terminates.
If no crossing occurs, let the 105-minute maximum expire.
At T+4, the BC-232 section of
`packing/campaign/series/series-000-smoke-and-calibration/results/agenda-025/gate-hour-04.md`
is the `think-jeyp` provisional checkpoint.
It must hash all four outputs, report the cumulative exact lower endpoint and smallest
row-converged computational upper endpoint, separate actual process wall from CPU time,
give a no-live-process receipt, retain the final 30 one-core minutes, and leave BC-232
open.

### BC-241 Source-Distinct Review

The reviewer must not be the BC-240 author.
It writes
`packing/campaign/series/series-000-smoke-and-calibration/results/bc-241-trump-local-theorem-review.json`
and reserves `packing/devtools/review_trump_local_theorem.py` plus
`packing/tests/test_review_trump_local_theorem.py` for its reusable exact review and
mutation controls. It writes no shared record.
The closure manager makes the final `max` disposition in
`results/agenda-026/gate-hour-04.md`.

The review must:

1. Verify every frozen hash, including the exact Trump witness-source hash, and classify
   the documented source drift without treating the current source as a frozen BC-199
   input. Do not rerun `cases.trump11.verify_exact`.

2. Run exactly one source-distinct replay of the retained exp-013 tangent record from
   `packing/`:

   ```bash
   uv run --frozen python -m cases.trump11.tangent_cones \
     --replay campaign/series/series-000-smoke-and-calibration/results/exp-013-h-026-trump-tangent.json
   ```

   A failed invocation is the replay result.
   Do not repeat it into the same review.

3. Independently recompute the aggregate rational minimum, all shared caps, uniform and
   per-row norm conversions, and the published preferred radius and quadratic constant
   from the retained BC-199 bytes in `review_trump_local_theorem.py`. Keep the check in
   repository code; do not leave the measurement in a one-off script.

4. Audit selected branch and face calculations against the archived generator source.
   For every audited row, recompute the exact scale `factor_j = 2/K_j` and require the
   rational identity `factor_j * K_j = 2`.

5. Run all three falsifying controls: change one active-row coefficient, reverse one
   selected separating-axis row while retaining its stress, and change one per-row
   factor from `2/K_j` to `1/K_j`. The last mutation changes the exact product from two
   to one and must be rejected before any preferred-radius comparison can pass.

The packet must distinguish the exact tangent replay from the retained-record arithmetic
review. BC-199 lacks a replay surface and complete per-face witnesses, so BC-241 may not
claim an independent replay of the full radius generator.
Do not rerun that generator, repeat BC-240, or widen the theorem’s local claim.

### T+2-to-T+4 Slice Receipts

| Active interval | Fractional lane | Closure lane and floating reviewer |
| --- | --- | --- |
| T+2 to T+2:30 | In the first microreceipt, bind the authorization, eight-hour target, outer deadline, and actual restart UTC; launch leg 02 once; bind PID, fresh stems, warm-state hash, and safety flag. | In both first microreceipts, bind the authorization, eight-hour target, outer deadline, and actual restart UTCs; bind reviewer identity, hashes, source drift, and the witness-source hash; launch the one tangent replay. |
| T+2:30 to T+3 | Supervise without restart; report completed iterations and properly labelled endpoints. | Complete the tangent replay and independent aggregate/cap arithmetic. |
| T+3 to T+3:30 | Supervise; if the safe predicate fires, freeze and start only the declared bridge. | Audit selected branch and face calculations and run the three mutations. |
| T+3:30 to T+4 | Freeze leg-02 outputs or its earlier stop; write `think-jeyp` inside the manager gate packet. | Return the source-distinct packet, make the `max` local-scope disposition, and release the worker. |

## T+4 Gate

At active minute 240, pause the clock.
The required packets are:

- `packing/campaign/series/series-000-smoke-and-calibration/results/agenda-025/gate-hour-04.md`;
- `packing/campaign/series/series-000-smoke-and-calibration/results/agenda-026/gate-hour-04.md`;
  and
- `packing/campaign/series/series-000-smoke-and-calibration/results/agenda-024/gate-hour-04-decision.md`.

The coordinator integrates fractional before closure, checks the complete changed-path
and hash manifests, and runs BC-220. The decision packet accepts or refuses BC-241 at
its exact scope, records BC-232’s remaining 30-minute process budget, freezes every next
output stem, assigns the one floating reviewer, and preregisters BC-231 and BC-243 work
before either begins.
Regeneration, validation, commit, push, hosted CI, and any landed upstream
reconciliation run while the active clock is held.

Restart at T+4 only after the local focused and edit gates pass and the gate commit is
pushed durably to the open pull request.
Hosted checks run concurrently.
A required hosted failure pauses active time for repair under the launch rule above.
The final BC-232 leg, scalar probe, BC-231, and BC-243 remain unauthorized until the
local gate and durable push are complete.

## T+4 to T+8: Fractional Lane

Launch BC-232 leg 03 and the scalar `61/16` probe concurrently after BC-220 opens them.
Both are single-core background processes.
Require all named paths to be absent and run each command once from `packing/`.

### Literal BC-232 Leg 03

```bash
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 \
uv run --frozen --all-extras --group dev python -m devtools.run_fractional_cutting \
  --n 11 --side 191/50 --shrink 9977/10000 \
  --angle-limit 207107/500000 --steps 180 \
  --minutes 30 --iterations 40 --cap 150 --support-cap 96 \
  --rows-rounds 2 --rows-per-direction 3 \
  --stop-on-covering-below-n \
  --warm campaign/series/series-000-smoke-and-calibration/results/agenda-025/bc-232-leg-02-state.json \
  --log campaign/series/series-000-smoke-and-calibration/results/agenda-025/bc-232-leg-03.log \
  --state campaign/series/series-000-smoke-and-calibration/results/agenda-025/bc-232-leg-03-state.json \
  --json campaign/series/series-000-smoke-and-calibration/results/agenda-025/bc-232-leg-03-summary.json \
  --freeze campaign/series/series-000-smoke-and-calibration/results/agenda-025/bc-232-leg-03-family.json
```

Leg 03 is the final 30 one-core minutes of BC-232’s frozen four-hour evidence budget.
After it ends, apply the 25-percent width rule to the cumulative record: continue this
checkpoint only if the new width is at most `0.86078351094543675`. Record a method
closure, a safe crossing, or a time-limited width disposition without changing the
criterion.

### Scalar `61/16` Launch

```bash
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 \
uv run --frozen --all-extras --group dev python -m devtools.run_fractional_cutting \
  --n 11 --side 61/16 --shrink 9977/10000 \
  --angle-limit 207107/500000 --steps 180 \
  --minutes 150 --iterations 40 --cap 150 --support-cap 96 \
  --rows-rounds 2 --rows-per-direction 3 \
  --stop-on-covering-below-n \
  --seed-certificate cases/n11_fractional_certificate/certificate.json --seed-map scale \
  --log campaign/series/series-000-smoke-and-calibration/results/agenda-025/bc-234-scalar-61-16-leg-01.log \
  --state campaign/series/series-000-smoke-and-calibration/results/agenda-025/bc-234-scalar-61-16-leg-01-state.json \
  --json campaign/series/series-000-smoke-and-calibration/results/agenda-025/bc-234-scalar-61-16-leg-01-summary.json \
  --freeze campaign/series/series-000-smoke-and-calibration/results/agenda-025/bc-234-scalar-61-16-leg-01-family.json
```

A row-converged objective below eleven stops either process and opens only the existing
`devtools.freeze_cutting_primal` bridge on its fresh state.
The float is a candidate, not a bound.
Hash the bridge output before and after the declaration step, run the existing decision
and independent verification route, and send any decided mass below eleven to BC-238.
Candidate exactification outranks BC-231 or any unpriced expansion.

An exact `verify_ceiling` family of total at least eleven closes the corresponding
one-body formulation; it is not a lower-bound certificate.
A deadline, technical failure, missing output, or unconverged value never earns a rerun
into the same stem. BC-231 may implement only the reviewed BC-230 contract, within the
allocation frozen by BC-220, and requires a source-distinct review before retention.

## T+4 to T+8: BC-243 Dual-Only Pilot

BC-220 must first commit the unimplemented interface at
`packing/campaign/series/series-000-smoke-and-calibration/results/agenda-026/bc-243-dual-pilot-spec.json`.
This is a preregistration, not an executable command and not evidence that the verifier
exists. Implementation remains under the Agenda 026 reserved
`packing/src/sqpack/full_size_density/`, `packing/cases/n11_full_size_density/`, and
`packing/tests/test_full_size_density_*.py` roots.

The frozen interface accepts an exact finite family containing:

- exact placements at Trump’s side, represented in the existing exact algebraic field;
- nonnegative rational weights;
- deterministic exact deduplication with coalesced weights;
- exact containment rows for every retained placement; and
- an arrangement-completeness input or producer receipt consumed by an independent
  checker.

Its result records the input hashes, exact atom count, exact `D = sum_i a_i`, exact
containment verdict, every full-dimensional arrangement cell, the maximum rational depth
on those cells, the finite edge-and-vertex null set, control dispositions, elapsed wall
and CPU measurements, and one of `sound`, `unsound`, or `time_limited`. Only a complete
exact arrangement with maximum full-dimensional depth at most one may report
`[D, infinity)`.

The first proposed family is the exact `D4` orbit of Trump’s packing: at most 88 atoms
after exact deduplication, with nonnegative rational weights.
Its uniform orbit control must recover exact `D = 11`; edge and corner touching must
remain allowed under the Lebesgue-a.e. semantics.
This control does not kill equality.

Independent controls must also:

- reject a wall-crossing atom by exact containment;
- reject an interior perturbation that creates positive-area overlap;
- reject a rational weight mutation that makes one full-dimensional arrangement cell
  overweight;
- reject a negative weight and any malformed or non-exact weight;
- reject an omitted arrangement cell or incomplete arrangement-completeness receipt; and
- preserve deterministic exact deduplication and total weight under a reordered input.

The active-minute envelope is exactly 180 minutes:

| Work | Active-minute cap |
| --- | ---: |
| Implementation against the frozen interface | 120 |
| Source-distinct controls and review | 40 |
| First bounded pilot | 20 |
| **Total** | **180** |

Split every allocation into microreceipts of at most 30 active minutes.
The implementer and source-distinct reviewer must be different contexts, using the
closure manager and the one transferable reviewer; BC-220 records which context owns
each side. Stop when a cap expires and preserve an incomplete implementation or pilot
honestly.

A sound exact `D > 11` kills the mass-eleven equality-density route.
Exact `D = 11` is a non-kill control, not evidence that a mass-eleven primal exists.
A failed semantic, containment, arrangement, arithmetic, or mutation control makes the
pilot `unsound`. Any sound `D <= 11` remains a one-sided non-kill result.
No BC-243 output has primal upper-bound semantics, and no sampled density, continuum
coverage guard, singular measure, inverse design, or BC-244 work may enter this
180-minute envelope.

After a terminal BC-243 packet, the closure manager may use only the remaining
allocation that BC-220 priced for lazy n=3/n=4 controls and Trump compatibility.
It may not open a global `n = 11` atlas or invoke the BC-240 theorem globally.

## T+8 Gate and T+8-to-T+10 Slices

At active minute 480, pause the clock.
Require:

- `packing/campaign/series/series-000-smoke-and-calibration/results/agenda-025/gate-hour-08.md`;
- `packing/campaign/series/series-000-smoke-and-calibration/results/agenda-026/gate-hour-08.md`;
  and
- `packing/campaign/series/series-000-smoke-and-calibration/results/agenda-024/gate-hour-08-decision.md`.

BC-221 compares exact scientific returns and measured costs.
Candidate exactification and independent replay rank first.
A reviewed adaptive rung ranks second.
Explicit closure of the retained BC-232 bracket ranks third.
The gate freezes the selected commands, output paths, budgets, owners, and stop rules
before restarting at T+8. As at T+4, restart after the local focused and edit gates pass
and the gate commit is pushed durably to the open pull request; hosted checks run
concurrently, and a required failure pauses active time for repair.

The fractional manager then executes exactly four slices of at most 30 active minutes on
the selected route. It may not improvise another generator option.
The closure manager also executes four bounded slices only on the route BC-221 selected,
normally priced lazy n=3/n=4 controls plus Trump compatibility after a terminal BC-243
packet. BC-244 and every theorem invocation remain behind their explicit prerequisites.

If either lane becomes terminal early, it freezes its packet and releases the floating
reviewer. It does not borrow from a future block.
The other lane may finish its current authorized work but waits at the shared T+10
boundary.

## T+10 Receipt and Cold Handoff

At active minute 600, hold the clock.
The exact landing paths are:

- `packing/campaign/series/series-000-smoke-and-calibration/results/agenda-025/checkpoint-hour-10.md`;
- `packing/campaign/series/series-000-smoke-and-calibration/results/agenda-026/checkpoint-hour-10.md`;
- `packing/campaign/series/series-000-smoke-and-calibration/results/agenda-024/checkpoint-hour-10-decision.md`;
  and
- `docs/project/handoff-2026-09-06-post-381-t10.md`.

Each manager packet gives every BC and experiment disposition, frozen input and output
hash, invalid and mutation run, exact endpoint with its claim label, remaining process
and active budget, actual process wall and CPU measurement, role-assigned time, observed
`agent_minutes` or `unknown`, complete changed-path manifest, and proposed next slice.
The coordinator packet records 480 continuation active minutes and 840 remaining only if
the clock actually reached minute 600.

The coordinator integrates fractional before closure, closes or carries every execution
bead with an exact reason, reconciles only landed `origin/main`, regenerates shared
views, runs the full checkpoint, commits, pushes, waits for required hosted CI, and
writes the pull request with the branch’s measured cost first.
The cold handoff names the next entry from the T+10 evidence.
It must not execute or pre-decide the T+12 pivot.

## PR #93 and PR #94 Integration

`think-f5t7` monitors both pull requests through T+10. An open head is never an upstream
input and never blocks scientific work.
At each held gate, the coordinator fetches `origin/main`, records the exact landed merge
commits, verifies ancestry, and inspects the landed diff before integration.

If a landed commit changes a frozen scientific input, do not rebase a running process or
silently substitute the new bytes.
Freeze the affected lane and request a `max` disposition.
If it changes only operational or shared record surfaces, reconcile it during the held
gate, retain both provenance lines, and validate the integrated tree before restarting
the clock.
New timing instrumentation applies prospectively; it never backfills attentive
labor, CPU time, or active minutes.

If PR #94 lands, preserve PR #89’s live Agenda 024 authority, union the three review
registrations, retain the genuine `c743d7bb` full-gate receipt, and preserve the current
sequence: Session 087 completed, BC-214 completed, and BC-215 next.
Regenerate the ledger and session-close views only in the coordinator’s gate
transaction; this addendum does not edit either generated artifact.

PR #93 landed as `3122c49766e7fc70c8cb299bd8b6b09558447d8a` at `2026-09-06T09:06:10Z`
and is present in the detached staging base `00e774de8c3cbb6695402615992d92ab1b4f4c93`.
Continue to verify any fetch, failure, or live-timing claim on the integrated tree.
Record each accepted operational change and its prospective clock boundary in the
coordinator packet.

If PR #94 remains open by T+10, record that state and continue.
Do not merge, cherry-pick, or copy its open head.

## Stop and Refusal Rules

- Stop immediately on a decided, independently verified candidate below eleven and route
  it to BC-238 before lower-priority work.
  Preserve the float crossing only as its proposer.
- Stop a fractional process on an exact feasible family of total at least eleven and
  close only that one-body formulation.
  Do not describe it as a lower bound.
- After BC-232 leg 03, apply its frozen width test exactly.
  Do not extend the process or revise the threshold after seeing the result.
- Stop BC-241 as `not accepted` if a frozen hash, exact replay, rational constant,
  selected source calculation, or required mutation fails.
  BC-240 retains its author packet and local-only label.
- Stop BC-243 as `unsound` when any semantic or exact control fails, as `time_limited`
  when its 180 active minutes expire without a terminal sound packet, and as a route
  kill only for a sound exact `D > 11`.
- Stop any run with a missing, reused, malformed, or non-strict output as a technical
  failure. Preserve the paths and allocate no replacement stem without a coordinator
  gate.
- Never rerun T+0 preflight, BC-232 leg 01, BC-233, BC-240’s radius generator, BC-242,
  or BC-245. Never overwrite their packets to reflect later understanding.
- Never use an unconverged row objective as an endpoint, sampled primal coverage as an
  upper bound, local isolation as global capture, or a typed language as an enumerated
  atlas.
- Hold the shared gate whenever a required role, host, tool, or authority is absent.
  Operational urgency changes wall time, not criteria or active-time accounting.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
