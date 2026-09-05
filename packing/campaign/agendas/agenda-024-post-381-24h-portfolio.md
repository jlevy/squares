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
    state: ready
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
    - packing/resources/web/literature-refresh-2026-09-05/README.md
    parallel_group: agenda024-control
    program: n11-post-381-portfolio
    next_evidence: >-
      One immutable launch contract that prevents parallel agents from changing the
      theorem, criteria, source corpus, or shared record underneath one another.
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
`T+0` is the coordinator commit that completes BC-219 and opens the initial six child
cells; the hour-four gate is four hours after that commit, not four hours after the
preflight begins.

The full rationale, resource packet, ownership matrix, and routing thresholds are in
[`X-016`](../explorations/X-016-after-381-two-managers-one-proof-boundary.md).
If prose in a child agenda conflicts with X-016 or BC-219’s frozen launch packet, stop
the cell and ask the coordinator; a worker does not resolve a proof-boundary conflict
locally.

## Gate packet

Each manager submits by gate minus 15 minutes:

- BC dispositions and checkpoint paths;
- frozen base SHA, transport identity, and changed-path manifest;
- exact checker receipts, invalid runs, and guard refusals;
- wall and CPU time;
- proposed next slices and hypothesis text; and
- shared-code or cross-program requests.

The coordinator integrates fractional before closure, regenerates shared views once, and
commits the gate. CI is not a reason for either manager to poll; disjoint theory or
review work remains available while hosted checks run.

## Delegation topology

The two managers own agendas, not just individual commands.
Each manager reads its whole packet, assigns bounded cells to workers, checks their
packets, and presents one coherent recommendation at the gate.
Workers never integrate each other’s output.
The coordinator claims tbd cells and creates or allocates hypotheses and experiment
records before dispatch.
A manager may update a coordinator-created experiment only inside its reserved range and
may not change its identity or acceptance rule.

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

Transport is explicit.
In a shared checkout, a manager leaves owned changes uncommitted and submits a patch
hash plus changed-path manifest.
In an isolated worktree, a manager may make local transport commits containing only
owned paths, but may not push, merge, rebase, or operate tbd.
The coordinator reviews and integrates either form, creates the shared records,
regenerates shared views, and makes the portfolio commit.
The gate packet names the frozen base SHA and either the patch SHA-256 or the local
commit SHA.

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

During the planning and launch window, the coordinator watches `origin/main`, PR #83,
and the namespace-owning PR #87. New `main` commits are fetched and absorbed through the
PR #83 stack while that pull request is open.
When PR #83 merges, this branch is rebased or retargeted to `main` before a new manager
starts. A changed base invalidates only path hashes or assumptions that differ; the
coordinator records the diff and reruns the preflight instead of making every manager
rediscover the repository.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
