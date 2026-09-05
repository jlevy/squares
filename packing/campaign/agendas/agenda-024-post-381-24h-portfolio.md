---
title: "agenda-024 — post-3.81 24-hour portfolio control"
softschema:
  contract: packing.squares:ExperimentAgenda/v1
  schema: ../schemas/agenda.schema.yaml
  envelope: agenda
  status: enforced
agenda:
  id: agenda-024
  title: "Post-3.81 24-Hour Portfolio Control"
  updated: '2026-09-05'
  status: active
  objective: >-
    Coordinate two disjoint research agendas for the next 24 hours without allowing
    parallel work to split the proof record. Agenda-025 owns the exact fractional
    frontier and agenda-026 owns density, typed stationarity, and Trump capture. This
    agenda owns the frozen base and source packets, shared namespaces and records,
    six four-hour integration gates, all routing decisions, and W10 closeout. The
    research horizon is a replanning checkpoint rather than a stop condition. PR 87
    owns agenda-023 and BC-214 through BC-218; this portfolio starts at BC-219 and
    quarantines H-066 through H-069 and exp-065 through exp-069 until that sibling is
    terminal.
  items:
  - id: BC-219
    purpose: tool_validation
    owner_focus: process
    instances: [11]
    state: complete
    priority: 0
    question: >-
      Are the stack base, source packets, ID ranges, manager write scopes, exact
      controls, checkpoints, and four-hour report contract frozen tightly enough that
      the two managers can work in parallel without shared-state or evidence drift?
    budget: >-
      45 elapsed minutes, coordinator only, review-planning-oversight. Recheck PR 83,
      PR 87 and any newly merged operating rules at launch. Freeze the exact base SHA;
      common, fractional and closure resource manifests; BC, H, experiment and
      exploration ranges; manager and worker write exclusions; and the gate packet
      template. Validate that every local source named in X-016 exists. Kill on any
      unresolved sibling ID collision, missing control, dangling path, or ambiguous
      retention owner.
    entry: >-
      X-016 and all three agendas are validated; think-any0 and think-57v6 are closed;
      the branch has been reconciled to PR 83's current head.
    exit: >-
      A committed launch packet names the exact base, hashes or paths every input,
      assigns disjoint writes and IDs, and leaves BC-230, BC-232, BC-233, BC-240,
      BC-242 and BC-245 takeable by their managers.
    bead: think-9pzv
    workflows: [review-planning-oversight]
    depends_on: []
    artifacts:
    - packing/campaign/explorations/X-016-after-381-two-managers-one-proof-boundary.md
    - packing/campaign/agendas/agenda-025-adaptive-fractional-frontier.md
    - packing/campaign/agendas/agenda-026-density-stationarity-and-trump-capture.md
    - packing/resources/web/literature-refresh-2026-09-05/README.md
    parallel_group: agenda024-control
    program: n11-post-381-portfolio
    next_evidence: >-
      One immutable launch contract that prevents parallel agents from changing the
      theorem, criteria, source corpus, or shared record underneath one another.
    outcomes:
    - scope: >-
        The post-3.81 launch base, local inputs, namespaces, ownership, transport,
        controls, timing, dependencies, and initial agent allocation.
      classification: achieved
      result: >-
        PR #83 passed its full validation and merged as 663ca37e. This branch was
        rebased onto that origin/main commit. PR #87 was frozen at 26709263 with its
        agenda-023 and BC-214..218 namespace disjoint. A manager-level audit and an
        independent portfolio audit verified the local paths, commands, hashes,
        quantitative guards, schemas, dependency graph, and four-slot schedule after
        correcting the identified contradictions. BC-230, BC-232, BC-233, BC-240,
        BC-242, and BC-245 are the only manager cells opened at T+0.
      evidence:
      - packing/campaign/explorations/X-016-after-381-two-managers-one-proof-boundary.md
      - packing/campaign/agendas/agenda-025-adaptive-fractional-frontier.md
      - packing/campaign/agendas/agenda-026-density-stationarity-and-trump-capture.md
      - packing/resources/web/literature-refresh-2026-09-05/README.md
      disposition: retire-success
      follow_up: null
  - id: BC-220
    purpose: measurement_validation
    owner_focus: correctness
    instances: [11]
    state: blocked
    priority: 0
    question: >-
      At hour four, have both managers produced valid theorem and control packets, and
      which exact cells are allowed to run in the second block?
    budget: >-
      30 elapsed minutes at T+4h, coordinator only. Freeze launches 15 minutes before
      the gate; inspect both changed-path manifests, exact receipts, refusals, costs,
      checkpoints and proposed hypotheses; validate fractional then closure; integrate
      sequentially; check IDs and references whole-set; regenerate shared views once;
      commit the routing decision. Hosted checks remain asynchronous.
    entry: >-
      The initial six manager cells have submitted packets under BC-219's frozen
      contract.
    exit: >-
      Every submitted artifact is accepted, refused or returned with one concrete gap;
      the hour-four instrument/control readiness decision and next block are committed.
    bead: think-u7i4
    workflows: [factual-review, review-planning-oversight]
    depends_on: [BC-230, BC-232, BC-233, BC-240, BC-242, BC-245]
    parallel_group: agenda024-control
    program: n11-post-381-portfolio
    next_evidence: >-
      Whether adaptive cores, the resumed bracket, local radius packaging, and the
      full-size weak-dual pilot are sound enough to receive more compute.
  - id: BC-221
    purpose: measurement_validation
    owner_focus: insight
    instances: [11]
    state: blocked
    priority: 0
    question: >-
      At hour eight, what do the first exact measurements say about the fastest path to
      a bound above 3.81 and the viability of the two closure endpoints?
    budget: >-
      30 elapsed minutes at T+8h under the same frozen packet and sequential integration
      protocol as BC-220. Apply only X-016's predeclared routing rules; do not move an
      accept threshold to rescue a run.
    entry: >-
      BC-220 has committed the second block and both managers submit by gate minus 15
      minutes.
    exit: >-
      Exact measurements and costs are reconciled, any candidate is diverted to
      independent replay, and the third block is frozen.
    bead: think-gt06
    workflows: [factual-review, review-planning-oversight]
    depends_on: [BC-220]
    parallel_group: agenda024-control
    program: n11-post-381-portfolio
    next_evidence: >-
      A comparable exact-yield-per-hour reading across the adaptive, bracket, radius,
      and density routes.
  - id: BC-222
    purpose: research
    owner_focus: insight
    instances: [11]
    state: blocked
    priority: 0
    question: >-
      At hour twelve, which program has earned the portfolio pivot, and which routes
      should be preserved, demoted, or stopped?
    budget: >-
      35 elapsed minutes at T+12h. Compare verified improvement, bracket shrinkage,
      theorem closure, exact decision cost, and guard failures. Reallocate within the
      frozen two-program scope; a cross-program route needs an explicit patch request
      and coordinator decision.
    entry: >-
      BC-221 is committed and both managers have six hours of post-readiness evidence.
    exit: >-
      The portfolio pivot cites exact evidence for every promotion and demotion and
      freezes the hour-12 through hour-16 block.
    bead: think-gxcm
    workflows: [research-loop, review-planning-oversight]
    depends_on: [BC-221]
    parallel_group: agenda024-control
    program: n11-post-381-portfolio
    next_evidence: >-
      Whether the direct-bound route, equality-density route, or local-to-global route
      now has the strongest verifier-backed expected gain.
  - id: BC-223
    purpose: measurement_validation
    owner_focus: correctness
    instances: [11]
    state: blocked
    priority: 0
    question: >-
      At hour sixteen, has any candidate or theorem packet earned independent
      exactification, and can the other lane continue without touching its proof state?
    budget: >-
      30 elapsed minutes at T+16h. Freeze candidate bytes before inspecting them; demand
      a source-distinct decision and falsifying controls for a bound, or an independent
      128-branch replay for the Trump theorem. Reserve roughly 75 percent of the next
      block for a qualifying bound candidate.
    entry: >-
      BC-222's pivot is committed and the selected deep cells have submitted complete
      packets.
    exit: >-
      Candidate, theorem and negative-result packets have typed dispositions and the
      hour-16 through hour-20 allocation is committed.
    bead: think-dlj8
    workflows: [factual-review]
    depends_on: [BC-222]
    parallel_group: agenda024-control
    program: n11-post-381-portfolio
    next_evidence: >-
      A frozen candidate that survives independent exact decision, or a precise reason
      no branch has earned final-block exactification.
  - id: BC-224
    purpose: tool_validation
    owner_focus: process
    instances: [11]
    state: blocked
    priority: 0
    question: >-
      At hour twenty, can new instrument work stop and every remaining resource move to
      exactification, replication, and closeout-quality evidence?
    budget: >-
      25 elapsed minutes at T+20h. Stop opening new instruments. Preserve any unfinished
      checkpoint with its reopen condition, assign independent replays and documentation
      review, and freeze the final four hours. No late idea bypasses the earlier controls.
    entry: >-
      BC-223 is committed and both managers submit their final candidate and cost
      positions.
    exit: >-
      The final block contains only exactification, independent replay, disposition,
      documentation and validation work.
    bead: think-wo94
    workflows: [review-planning-oversight, documentation-pass]
    depends_on: [BC-223]
    parallel_group: agenda024-control
    program: n11-post-381-portfolio
    next_evidence: >-
      Review-ready evidence rather than another partially built research surface.
  - id: BC-225
    purpose: measurement_validation
    owner_focus: process
    instances: [11]
    state: blocked
    priority: 0
    question: >-
      At hour twenty-four, is every research cell honestly classified and reprioritized,
      with the record validated and exactly one next entry selected but not executed?
    budget: >-
      60 elapsed minutes beginning at T+23h. Apply W10 to all three agendas: achieved,
      bounded-negative, time-limited, guard-refused, technical-failure, never-opened, or
      inconclusive; record disposition and reopen conditions; run the documentation
      guidelines pass and full validation on the final commit; update the PR's cost and
      result summary; select one next entry. Mechanical closeout may exceed the research
      horizon, but no new research starts after T+20h.
    entry: >-
      BC-224 froze the final block, and BC-239 and BC-249 submitted terminal manager
      packets by T+23h45.
    exit: >-
      The three agendas, their tbd trees, checkpoints, documentation and validation
      evidence agree; every route is disposed; exactly one next entry is selected and
      left unexecuted for the operator.
    bead: think-3ilu
    workflows: [documentation-pass, review-planning-oversight]
    depends_on: [BC-224, BC-239, BC-249]
    parallel_group: agenda024-control
    program: n11-post-381-portfolio
    next_evidence: >-
      The durable result of the 24-hour portfolio and the single highest-value
      continuation after all costs and negative results are known.
---
# Agenda 024 — Post-3.81 24-Hour Portfolio Control

This is the control plane for [`agenda-025`](agenda-025-adaptive-fractional-frontier.md)
and [`agenda-026`](agenda-026-density-stationarity-and-trump-capture.md).
It performs no manager experiment.
Its job is to keep theorem statements, evidence, IDs, shared files, and routing
decisions single-owned while the two research programs work concurrently.

BC-219 is a preflight outside the research clock.
Its completion makes the initial six child cells takeable; it does not start their
budgets. `T+0` is the later coordinator dispatch record that names all four live agent
contexts, claims the six cells, and freezes the first-block experiment identities.
The hour-four gate is four hours after that dispatch, not four hours after the BC-219
preflight commit.

The full rationale, resource packet, ownership matrix, and routing thresholds are in
[`X-016`](../explorations/X-016-after-381-two-managers-one-proof-boundary.md).
If prose in a child agenda conflicts with X-016 or BC-219’s frozen launch packet, stop
the cell and ask the coordinator; a worker does not resolve a proof-boundary conflict
locally.

## Coordinator entry point

PR #83 is terminal and merged as `663ca37eb622508d9df00c594b8ef11d2c256f55`. The
portfolio branch is `codex/next-research-strategy`, carried by PR #89 against `main`;
its merge base with the frozen `origin/main` is the same commit.
Only the coordinator fetches or reconciles upstream state.
Managers begin from the committed packet and do not need network access.

Run these read-only checks from the repository root immediately before dispatch:

```sh
git status --short --branch
git merge-base --is-ancestor 663ca37eb622508d9df00c594b8ef11d2c256f55 HEAD
tbd show think-9pzv think-c678 think-gmdy think-jbat \
  think-4ln1 think-9xxh think-do04 think-u7i4 --max-lines 40
```

The base check succeeds silently.
The local bead graph must show BC-219 (`think-9pzv`) closed; the six initial cells open
and unblocked; and BC-220 (`think-u7i4`) blocked by exactly those six cells.
Do not select work from the repository-wide `tbd ready` list, which contains unrelated
agendas.

The coordinator then performs the only tbd mutation in the launch step:

```sh
tbd update think-c678 think-gmdy think-jbat think-4ln1 think-9xxh think-do04 \
  --status in_progress
```

Before either numerical process starts, the coordinator creates the required hypothesis
and experiment artifacts in the reserved ranges and freezes their criteria, operator,
instance, regime, budget, and input hashes.
BC-232 continues H-064 but still needs a new experiment record.
BC-233 needs both a preregistered hypothesis and an experiment record.
The theorem-drafting cells may start without placeholder experiments; any measurement
they later trigger needs a coordinator-created record first.

Do not use `packing-campaign claim` to allocate these records.
That harness permits one in-progress round, chooses the next global experiment ID
(`exp-065` on this base), and expects its packing-pose JSONL contract; it neither honors
this portfolio’s reserved blocks nor represents the fractional and theorem records.
Create hypotheses under `packing/campaign/hypotheses/` and experiments under
`packing/campaign/series/series-000-smoke-and-calibration/experiments/` using the
neighboring soft-schema artifacts as contracts, then run the whole-set record checks
before dispatching their commands.

Record `T+0` only after those steps pass.
Write the dispatch record to
`packing/campaign/series/series-000-smoke-and-calibration/results/agenda-024/launch-t-plus-00.md`.
It carries the current branch HEAD, `origin/main`, current PR #87 head, the six tbd
claims, allocated H/exp IDs, four agent identities, and the two manager gate paths
below.

## Gate packets and decision paths

The fixed packet paths are:

| Owner | Hour-NN packet |
| --- | --- |
| Fractional manager | `packing/campaign/series/series-000-smoke-and-calibration/results/agenda-025/gate-hour-NN.md` |
| Closure manager | `packing/campaign/series/series-000-smoke-and-calibration/results/agenda-026/gate-hour-NN.md` |
| Coordinator | `packing/campaign/series/series-000-smoke-and-calibration/results/agenda-024/gate-hour-NN-decision.md` |

Each owner may create its reserved result directory on first write.
These paths are planned outputs until a packet exists.
`NN` is `04`, `08`, `12`, `16`, `20`, or `24`.

Each manager submits by gate minus 15 minutes:

- BC dispositions and checkpoint paths;
- frozen base SHA, transport identity, and a complete changed-path content manifest;
- exact checker receipts, invalid runs, and guard refusals;
- wall and CPU time;
- proposed next slices and hypothesis text; and
- shared-code or cross-program requests.

In a shared checkout, the content manifest lists every modified and untracked owned path
from `git status --short --untracked-files=all -- <owned-paths>` and gives the SHA-256
of every listed regular file; deleted paths are marked `DELETED`. A `git diff` hash
alone is insufficient because it omits untracked result artifacts.
In an isolated worktree, the packet gives the local transport commit and its complete
name-status list.

The coordinator integrates fractional before closure, regenerates shared views once, and
records every accepted and refused path in the coordinator decision packet before
committing the gate.
CI is not a reason for either manager to poll; disjoint theory or review work remains
available while hosted checks run.

## Delegation topology

The two managers own agendas, not just individual commands.
Each manager reads its whole packet, assigns bounded cells to workers, checks their
packets, and presents one coherent recommendation at the gate.
Workers never integrate each other’s output.
The coordinator claims tbd cells and creates or allocates hypotheses and experiment
records before dispatch.
A manager may update a coordinator-created experiment only inside its reserved range and
may not change its identity or acceptance rule.

The word *owns* refers to scientific work and manager-local output, not ID authority:

| Surface | Reserved range | Writer or allocator |
| --- | --- | --- |
| Coordinator BCs | BC-219 through BC-225 | Coordinator |
| Fractional BCs | BC-230 through BC-239 | Fractional manager; coordinator alone mutates tbd |
| Closure BCs | BC-240 through BC-249 | Closure manager; coordinator alone mutates tbd |
| Fractional hypotheses and experiments | H-070 through H-079; exp-070 through exp-089 | Coordinator creates and freezes identity and criterion; manager appends allocated outcomes |
| Closure hypotheses and experiments | H-080 through H-089; exp-090 through exp-109 | Coordinator creates and freezes identity and criterion; manager appends allocated outcomes |
| Cross-program explorations | X-017 through X-019 | Coordinator, after a fresh collision check |
| Ledgers, maps, frontier, schemas, PR, and retention | Shared; no manager range | Coordinator |

| Manager | First worker wave | Later worker wave |
| --- | --- | --- |
| Fractional | adaptive theorem and verifier inventory; retained 3.82 resume; inset-seed control | adaptive target run; kernel theorem/verifier; source-distinct candidate replay |
| Closure | Trump theorem packaging; density semantics and weak-dual pilot; typed-stationarity language | independent 128-branch replay; solved-case branch pricing; guarded equality or residue route |

With four concurrent agent slots, reserve one for the coordinator and one for each
manager; the fourth is a floating worker assigned to the current critical path.
In the default first block it drafts BC-240 while the fractional manager owns BC-230 and
supervises BC-232 and BC-233 as background single-core processes.
A compute process is not another agent slot.
A manager collects the floating worker’s terminal packet and releases the slot before
the other manager delegates.
With more slots, add workers only to distinct BC cells; never duplicate a generator and
its independent reviewer in the same worker context.
Under the four-slot cap, neither manager spawns another agent in the first block.
Delegation requests go through the coordinator, which transfers the one floating slot
only after its prior packet is terminal.

Transport is explicit.
In a shared checkout, a manager leaves owned changes uncommitted and submits the content
manifest defined above.
In an isolated worktree, a manager may make local transport commits containing only
owned paths, but may not push, merge, rebase, or operate tbd.
The coordinator reviews and integrates either form, creates the shared records,
regenerates shared views, and makes the portfolio commit.
The gate packet names the frozen base SHA and either the shared-checkout content
manifest or the local commit SHA.

## First four-hour dispatch

The coordinator sends three bounded handoffs at `T+0` and keeps the fourth context.
Each handoff names this agenda, X-016, the manager’s full child agenda, the frozen base,
the owned paths, the exact BCs, and its gate packet path.

| Time | Coordinator | Fractional manager | Closure manager | Floating worker |
| --- | --- | --- | --- | --- |
| T+0 to T+15 min | Record launch identities; watch upstream and shared paths | From `packing/`, verify the agenda-025 packet; launch the pinned BC-232 and BC-233 processes; begin BC-230 | From the repository root, verify the agenda-026 packet; begin BC-242 | Author BC-240 from the retained packet; do not rerun the radius generator |
| T+15 to T+105 min | Reject unallocated records and cross-scope writes | Draft BC-230 while supervising the exact background processes | Finish BC-242 and begin BC-245 | Finish BC-240, run its allowed tangent replay and aggregate self-check, and return the packet |
| T+105 to T+135 min | Hold the floating slot transfer until BC-240 paths are final | Freeze BC-230 author draft and continue supervising processes | Review BC-240 and BC-242; return concrete corrections | Move to the source-distinct BC-230 review |
| T+135 to T+195 min | Check proposed H/exp text without allocating a new run | Reconcile concrete BC-230 blockers and supervise only the fractional processes | Finish BC-245 and map its solved controls | Complete the BC-230 theorem, seam, specialization, and refusal audit |
| T+195 to T+225 min | Check manifests, IDs, packet completeness, and exact receipts | Reconcile BC-230, BC-232, and BC-233 dispositions | Specify BC-243 without running it; reconcile BC-240, BC-242, and BC-245 | Return terminal review; start nothing else |
| T+225 to T+240 min | Freeze launches; accept packets only at the fixed paths | Write `gate-hour-04.md`; no new process | Write `gate-hour-04.md`; no new work | Available only for a coordinator-assigned manifest check |
| T+240 to T+270 min | Run BC-220: validate fractional, then closure; write the central decision; regenerate shared views once; commit | Await the decision without polling CI | Await the decision without polling CI | Released |

The child agendas carry the exact numerical and replay commands.
Their working-directory declarations are binding: agenda-025 runs its research commands
from `packing/`; agenda-026 runs from the repository root and enters `packing/` inside
each command block. Do not transplant a command between those directories or replace the
project Python 3.14 environment with the `python3` on `PATH`.

After sequential integration at T+240, run the coordinator gate from `packing/`:

```sh
uv run --frozen --all-extras --group dev packing-validate --edit
```

This is the local gate for the commit, not permission to skip a candidate’s exact
decision routes or a manager’s cell-specific controls.

## Default block matrix

The gates may reallocate this schedule, but only from evidence already named in X-016.
It is a default continuation, not permission to keep a route alive after its kill rule.

| Hours | Fractional program | Closure program | Coordinator |
| --- | --- | --- | --- |
| 0–4 | BC-230 theorem contract, BC-232 resumed bracket, BC-233 seed/control | BC-240 theorem packet, BC-242 density semantics, BC-245 typed completeness | freeze launch; reject shared writes; run BC-220 |
| 4–8 | BC-231 verifier if its theorem passed; otherwise concentrate on BC-232 | BC-241 independent replay; BC-243 pilot only if weak dual is proved; price BC-247 from the BC-245 contract | compare exact yield and cost at BC-221 |
| 8–12 | BC-234 first adaptive rung if both controls pass; otherwise finish the retained bracket or open BC-235 | finish the density kill and small-case price; BC-246 only after the typed language passes review | make the BC-222 portfolio pivot |
| 12–16 | leading direct-bound route receives two-thirds of available compute; preserve one falsifier or theorem worker | leading closure route receives two-thirds only if no bound candidate qualifies; otherwise retain one local/global control worker | freeze candidate bytes and run BC-223 |
| 16–20 | exactify any candidate; otherwise one last predeclared rung or bounded-negative close | independently replay the local theorem or exactify the one closure route that passed its guards | stop new instruments at BC-224 |
| 20–24 | BC-238 if a candidate exists, then BC-239 | independent replay or residue checkpoint, then BC-249 | documentation, validation, W10, and BC-225 |

The hour-12 rule prevents a fashionable long-horizon program from consuming the block
merely because its endpoint would be important.
The hour-16 rule does the opposite for a real candidate: once frozen bytes cross an
accept threshold, independent decision outranks further search.

## Upstream reconciliation

PR #83 is merged and no longer needs polling.
During the planning and launch window, the coordinator watches `origin/main`, PR #89,
and the namespace-owning PR #87. Managers never fetch, merge, rebase, or reinterpret an
upstream delta. If `origin/main` moves, the coordinator freezes new launches, reconciles
the portfolio branch, records the old and new base plus the changed paths, and reruns
the affected preflight checks before another manager starts.
A sibling-head change does not rewrite a historical launch snapshot.
The coordinator logs its old and new heads, checks namespace and named-input overlap,
and either records a no-invalidation disposition or appends a superseding manifest.

The first post-freeze sibling check found one noninvalidating change:

| Observed | Ref movement | Changed paths | Disposition |
| --- | --- | --- | --- |
| 2026-09-05 after BC-219 | PR #87: `26709263f740f3d9aece654e0272dae3c168d18d` to `3c6c5e7fc0c1662a57a1a3d06246a3a5e0730b89` | `development.md`, `packing/devtools/gate-budgets.yaml`, `packing/tests/test_module_boundaries.py` | No agenda, BC, H, exp, exploration, manager-output, or named-input collision. Preserve the frozen BC-219 row; apply the new validation-budget behavior only after PR #87 reaches `main`. |
| 2026-09-05 launch-spike close | PR #87: `3c6c5e7fc0c1662a57a1a3d06246a3a5e0730b89` to `b9d357db7a0f46ff8e0cd5bcfcb157686003b8a2` | `packing/src/sqpack/cli/validate.py`, `packing/tests/test_validation_cli.py` | No namespace, manager-output, research-input, or scientific-verdict collision. The change sizes the quick test lane to available CPUs; keep this branch’s measured push receipt and adopt the runner behavior only when PR #87 reaches `main`. |

## BC-219 launch snapshot

The coordinator froze this snapshot at `2026-09-05T21:54:16Z` and then rebased the
strategy stack directly onto the merged parent:

- `origin/main`: `663ca37eb622508d9df00c594b8ef11d2c256f55`;
- PR #83: merged at that commit after all required checks passed; final head
  `927eb820f100eb155dc9799145bc47ff6db0f739`;
- PR #87: open draft at `26709263f740f3d9aece654e0272dae3c168d18d`, owning agenda-023
  and `BC-214..218`; and
- this stack before the launch-gate commit: review `5389fc06`, archive `5214b57b`, and
  strategy `d1a436de`.

This portfolio owns agendas 024--026, `BC-219..225`, `BC-230..249`, `H-070..089`, and
`exp-070..109`. `X-016` is the launch synthesis; only the coordinator may allocate
`X-017..019`, after another upstream collision check.
PR #87’s `H-066..069` and `exp-065..069` gap remains quarantined.
The manager output roots are
`packing/campaign/series/series-000-smoke-and-calibration/results/agenda-024/`,
`packing/campaign/series/series-000-smoke-and-calibration/results/agenda-025/` and
`packing/campaign/series/series-000-smoke-and-calibration/results/agenda-026/`; they are
reserved paths, not evidence that a result exists.

The following SHA-256 manifest binds every common strategy input and the central exact
checkpoints. Manager-specific packets add their implementation and control hashes.
The Git commit containing this section binds agenda-024 itself.
The values below are the historical BC-219 snapshot and are never silently replaced.
Accepted edits after this snapshot require a superseding dispatch manifest before `T+0`;
the coordinator computes that manifest only after both child-agenda edits are final.

```text
dd03fe3d200cf9f1c2335c40103da45269716d20d7de38cd642d832205e962b2  operating-rules.md
17df0f04d4759625d18231d5cd1fdc69872367b9d7665b25e8e4c2e76e694011  docs/project/reviews/review-2026-09-05-strategy-gpt-56-pro-gemini-grok.md
ff5e0c07584a224ff1f28ce030388ed05692b9a5e77a20d0cd47e2628e2cf8f5  packing/resources/README.md
b9e28065dc76367b5f3fcc4c035a7263c533013dc2ea3f0267976c00e7549f53  packing/resources/web/literature-refresh-2026-09-05/README.md
b48c0c31cf62366d44cd12f02cf321dd38b5a23391caec95f04445938e0b3d75  packing/resources/web/n17-lower-bounds-2026/README.md
78782e710ab3058b12e106721447fa2589e7cf525a9085e7ac7ddaa2b27484bf  packing/campaign/explorations/X-014-closing-from-both-ends.md
6e49cfd993b51f350249d87d31d3d24984e0e942f7660a2e7fa209a747bbd916  packing/campaign/explorations/X-015-the-map-and-the-three-programs.md
772452abc153410a015b3d32ae1cd9fb0323d62b04134fbee1782610a1bc8629  packing/campaign/explorations/X-016-after-381-two-managers-one-proof-boundary.md
5375cb548038062122dbd971b70bd124ee1f44428c99c0eb6960db08c2c7fa75  packing/campaign/agendas/agenda-021-three-numbers-and-a-wall.md
766240b02a4bb4418c1fc0ede090867fd629849f0918a7c9930fec958cae0e6c  packing/campaign/agendas/agenda-022-the-conditional-route.md
48a2d71ceb70599a7f24e8e1dc3b84408f5932a67f88f9532fb819c715227cc1  packing/campaign/agendas/agenda-025-adaptive-fractional-frontier.md
0b7226eb31a59ee51d1144ef92a01e05e3a65cf763a2530bf9ba68c1421fbbcb  packing/campaign/agendas/agenda-026-density-stationarity-and-trump-capture.md
3d10438c28d7a8167179a7d129dd1d0bad804b9aa85ee1c7e4cde11e4e4d5319  packing/campaign/series/series-000-smoke-and-calibration/experiments/exp-060-h-064-n11-fractional-packing-floor.md
5042894a870c3d1374ffbb7774eda715c0181150df8b23b422016736b80cc60f  packing/campaign/series/series-000-smoke-and-calibration/experiments/exp-063-h-065-n11-near-tight-cell-census.md
a0b75ac0ab2a77436d6fe9edae0d526b6fe7d06ab73459b8ee7aa6aea87da0ea  packing/campaign/series/series-000-smoke-and-calibration/experiments/exp-064-h-063-two-threshold-class-program.md
db124b9956d8051682388cbba3b16772e65406a0003debba1c92b915c0c489a8  packing/campaign/series/series-000-smoke-and-calibration/results/bc-199-trump-isolation-radius.json
8df0b9aa530149b44367842a2e6389949b27189df038d68e9d1afa8fd87df8c6  packing/campaign/series/series-000-smoke-and-calibration/results/bc-200-state-191-50.json
84070a20d9954916260f7b2703bdec886523c7eccb912edbc110102731440219  packing/cases/n11_fractional_certificate/t-018-proof-card.md
3b4f754b8a77c0a6edb12a8f669e705594817992f9983956d308aa7b343031b4  packing/cases/trump11/isolation_radius.py
bc01c636302f26ce4072ee8886c83463a9648f0e35d918541377cf52559aea2c  packing/frontier/n-011.md
```

### Post-BC-219 Planning-Spike Manifest

The coordinator froze this amendment at `2026-09-05T23:12:46Z` after the bounded launch
audits tracked by `think-e7si` and the strict-JSON repair tracked by `think-quwt`. It
supersedes the two child-agenda hashes in the historical snapshot and adds the only
implementation and test files changed by the spike:

```text
96ce2d608dd51bae6637e65b81545623315f2ffd4e597396d5cbe8c35aa70155  packing/campaign/agendas/agenda-025-adaptive-fractional-frontier.md
3e544c5a316d57af21530a5d8269df6a87942d6bdc7537d35d128bbb30cb8b72  packing/campaign/agendas/agenda-026-density-stationarity-and-trump-capture.md
8c35796d7d7d3b3dbfa8eafd29d63078131ebb9d0b921a71c178ff77530eda01  packing/devtools/run_fractional_colgen.py
f7f87469d7ee1c3a04679cd9f58bcc032ed79baed927aaf0a7222ec6c7587e43  packing/tests/test_run_fractional_colgen.py
```

This amendment does not start `T+0`, claim a research cell, or allocate an H or exp ID.
The launch record still rechecks these bytes against its commit and names the actual
operators and experiment identities before either numerical lane starts.

The four-slot launch is coordinator, fractional manager, closure manager, and one
floating worker. The floating worker authors BC-240, then reviews BC-230; BC-232 and
BC-233 run as separately pinned background processes.
The only takeable research cells at `T+0` are BC-230, BC-232, BC-233, BC-240, BC-242,
and BC-245. Any changed manifest byte, sibling namespace collision, or new upstream
change to a named input returns BC-219 to preflight before another manager starts.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
