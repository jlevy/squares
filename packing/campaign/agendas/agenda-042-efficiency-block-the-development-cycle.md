---
title: "agenda-042 — efficiency block: the development cycle"
softschema:
  contract: packing.squares:ExperimentAgenda/v1
  schema: ../schemas/agenda.schema.yaml
  envelope: agenda
  status: enforced
agenda:
  id: agenda-042
  title: Efficiency Block — the Development Cycle
  updated: '2026-09-23'
  status: active
  objective: >-
    A W5 efficiency-loop block entered on the owner's direction on 2026-09-23, right
    after PR #221 merged. Merging main into that branch hit seven conflicts, six of them
    committed atlas rasters and PDFs, and it needed two full atlas rebuilds to land. The
    owner asked two things: how much time goes to checking rasters and PDFs, and where
    CI testing and review time should be prioritised to keep development cycles fast.
    BASELINE, measured by four delegated lanes against main at f5c9c8453. The Packing
    pull-request wall has a median of 189 s over 13 recent runs, and 8 of the 13 are
    over OR-14's 180 s. 42 of 151 CI cycles went red (27.8%) across the last twenty
    merged pull requests. A full build_known_best_atlas --update costs about 4m45s, and
    main's DATA_REVISION rule requires one after every data commit and after every merge
    where both sides changed the data.
    PROFILE. Checking the atlas exports costs under one CPU-second per pull request and
    none of the wall. About 97% of an atlas rebuild's per-case pool re-proves the
    non-overlap of unchanged witnesses in mpmath; drawing the six exports is about 20 s.
    The pull-request wall is set by suite-a or suite-b in 10 of 15 runs and by frontend
    in 5, where biome, eslint and tsc have replaced Chromium as the tail. Of 15 sampled
    red runs, 6 were causes the --push floor catches locally, 4 were gate-budget timing
    findings, and 4 were inherited from a red main.
    TARGET. The Packing pull-request wall at or under 180 s on five consecutive
    exact-head runs, which is think-g4n9's own re-enforcement condition. An atlas re-pin
    under 60 s. The pre-push floor enforced by a hook at a measured cost. No pull request
    failed by a finding its change did not cause.
    GUARD. No check is deleted and none becomes optional. Nothing leaves the
    pull-request surface without OR-13's own measurement. Any faster regeneration path
    must produce output byte-identical to a full --update on the same tree, and the deep
    gate keeps its full rebuild from source.
  items:
  - id: BC-374
    purpose: tool_validation
    owner_focus: efficiency
    instances: [11]
    state: ready
    priority: 0
    question: >-
      Does a third suite shard, plus splitting frontend's lint and type work away from
      its Chromium step, bring the Packing pull-request wall back under 180 s without
      moving a check off the surface?
    budget: >-
      About two hours, efficiency-loop. The shard is scoped in think-g4n9 already:
      SUITE_SHARDS = 3, a --suite-c selection, a suite_c register entry, a workflow job
      and packing-required's needs. Refresh devtools/suite-file-costs.json from a fresh
      hosted cohort in the same change, because 31 of the 355 files the two shards ran
      on run 35800361316 are absent from it and fall to the unweighted crc32 hash.
      Predicted from that run's setup and work split: about 114 to 120 s per suite job
      against today's 163 to 173 s. The frontend split is a new candidate. The register
      comment at validate.py:3376 reads Chromium 59.09 s against biome 91.69 s at
      --jobs 2, so the 2026-09-17 fix moved the tail rather than removing it.
      Kill: any arrangement that makes a test optional or runs it only after merge.
    entry: >-
      The wall and shard receipts under results/agenda-042 are on record, with the run
      ids behind every figure.
    exit: >-
      Five consecutive exact-head hosted runs with the Packing and Pages walls at or
      under 180 s, and check_pr_wall switched back from advisory to enforcing, per
      think-g4n9's declared condition.
    bead: think-g4n9
    depends_on: []
    next_evidence: >-
      check_pr_wall --sample over the first five runs after the shard lands, recorded in
      gate-budgets.yaml's pull_request_walls.
    workflows: [efficiency-loop]
    program: development-cycle
    parallel_group: agenda042-ci
    artifacts:
    - packing/campaign/series/series-000-smoke-and-calibration/results/agenda-042/pr-wall-receipt.md
    - packing/campaign/series/series-000-smoke-and-calibration/results/agenda-042/suite-shards-receipt.md
  - id: BC-375
    purpose: tool_validation
    owner_focus: efficiency
    instances: [11]
    state: ready
    priority: 0
    question: >-
      Can a re-pin, or a regeneration after a merge, redraw the two atlas composites and
      their six exports without re-proving the 324 unchanged cases, and does the result
      match a full --update byte for byte?
    budget: >-
      About ninety minutes, efficiency-loop. Candidate (a) in the atlas exports receipt:
      an --update --composites path that draws both composites from the retained
      witnesses/known-best/*.yaml, estimated at about 40 s against about 4m45s. The
      variant memoizes witness.numerical_check by witness content, so a plain --update
      stops re-proving unchanged cases. On 2026-09-22 five re-pins cost about 24 minutes
      of full rebuilds, and one merge cost 9m29s, of which the second rebuild changed only
      a six-character footer stamp.
      Carried to the owner rather than decided here: option (d), committing exports
      stamped with the version alone and not the data hash, would take re-pins to zero
      but reverses the 2026-09-22 decision that the footer names the data revision.
      Option (b), rendering rasters and PDFs at deploy time instead of committing them,
      is the follow-up if repository growth matters. The six exports are 88.1 MB of the
      525 MiB pack after 28 days.
      Kill: moving the export check off --fast. It reads receipts in 0.72 s inside a job
      with about 90 s of slack, so moving it saves nothing, and OR-13 forbids it.
    entry: >-
      The atlas exports receipt under results/agenda-042, with its profile and its
      history of re-pins, regenerations and binary conflicts.
    exit: >-
      A re-pin measured under 60 s on the reference machine, output byte-identical to a
      full --update on the same tree, the procedure in development.md and release.py's
      rule 3 naming the fast path, and the owner's answer on option (d) recorded.
    bead: think-6grx
    depends_on: []
    next_evidence: >-
      Timed --update --composites against a full --update on one tree, and a byte
      comparison of their outputs.
    workflows: [efficiency-loop]
    program: development-cycle
    parallel_group: agenda042-atlas
    artifacts:
    - packing/campaign/series/series-000-smoke-and-calibration/results/agenda-042/atlas-exports-receipt.md
  - id: BC-376
    purpose: tool_validation
    owner_focus: process
    instances: [11]
    state: ready
    priority: 0
    question: >-
      Can the --push floor be enforced by a pre-push hook at a cost low enough that
      nobody bypasses it, and what does the type floor need to get there?
    budget: >-
      About ninety minutes, efficiency-loop then process-review. Six of the fifteen
      sampled red runs were causes the --push floor catches locally: generated-record
      drift, lint, format, type and one genuine test failure. PR #221's red cycles came
      from validating with --records instead. The floor is documented in AGENTS.md and
      development.md and enforced nowhere; lefthook has only a pre-commit hook. The
      --edit tier inside it measured 181.1 s at four CPUs on 2026-09-23, with
      basedpyright its longest step, so the floor costs about three minutes before any
      reachable test runs. The first narrow-diff reading is this block's own commit
      d1d43d0f2, which changed only Markdown and YAML. --push against origin/main
      selected 55 of 365 test files and took 464 s of wall at four CPUs. 360.6 s of that
      was reachable behavioural tests (1,641 of them), and basedpyright took 130.5 s. A
      documentation change should not reach six minutes of tests, so the selector's
      always-included walkers and text-mention rule are the first thing to measure,
      ahead of the type floor. Measure --push on a sample of narrow diffs, and measure
      what a narrower selection and an incremental or scoped type check buy, before
      proposing the hook.
      Kill: a hook whose median exceeds a declared ceiling on narrow diffs. A slow
      mandatory hook is bypassed, and a bypassed hook reports nothing.
    entry: >-
      The pull-request cycle receipt under results/agenda-042, with its red-cause
      taxonomy and the tier that catches each cause.
    exit: >-
      A lefthook pre-push running --push with a declared ceiling and a measured median
      on narrow diffs, or a recorded measurement showing why the floor cannot be made
      cheap enough and what replaces it.
    bead: think-oc16
    depends_on: []
    next_evidence: >-
      --push walls on five recent narrow diffs, with and without a cached type check.
    workflows: [efficiency-loop, process-review]
    program: development-cycle
    parallel_group: agenda042-process
    artifacts:
    - packing/campaign/series/series-000-smoke-and-calibration/results/agenda-042/pr-cycle-receipt.md
  - id: BC-377
    purpose: tool_validation
    owner_focus: process
    instances: [11]
    state: blocked
    priority: 1
    question: >-
      Which gate-budget findings should fail a pull request, and how is a red main kept
      from failing branches that did not cause it?
    budget: >-
      About an hour once the owner has decided. Four of the fifteen sampled red runs
      were gate-budget findings on pull requests that did not cause them (PRs 200, 205,
      212, 218), and four were inherited from a red main. PRs 208, 209 and 211 failed
      the identical test_session_gate assertion within about two hours while main was
      red at c2cc1cf6. No local tier catches either class. The candidates are to report
      stale and drift findings on the pull request and fail them on main or on a
      scheduled re-baseline through devtools.read_tier_walls, keeping the ceiling rule
      where it is. Nothing is relaxed on main.
    blocked_on: >-
      The owner's decision on which gate-budget rules fail a pull request. OR-17 and
      OR-14 were both set by the owner, so the change is theirs to make.
    entry: >-
      The pull-request cycle receipt's cause taxonomy, with the red runs it sampled.
    exit: >-
      The decision recorded in operating-rules.md or gate-budgets.yaml, the gate
      changed to match it, and the next twenty merged pull requests showing no red cycle
      from a gate-budget finding their change did not cause.
    bead: think-du2j
    depends_on: []
    next_evidence: >-
      The owner's answer, then the lane B count re-run over the next twenty merged pull
      requests.
    workflows: [process-review]
    program: development-cycle
    parallel_group: agenda042-process
    artifacts:
    - packing/campaign/series/series-000-smoke-and-calibration/results/agenda-042/pr-cycle-receipt.md
  - id: BC-378
    purpose: tool_validation
    owner_focus: efficiency
    instances: [11]
    state: ready
    priority: 2
    question: >-
      Can a pull request's cycle cost be read by a tool instead of narrated: its cycles,
      red share, runner-minutes, queue time and review-lane minutes?
    budget: >-
      About an hour, efficiency-loop. Three tool gaps turned up in this block's
      measurement, OR-1 gaps each. No devtool rolls up red against green runner-minutes
      over a sample of pull requests, and lane B's figure of about 443 of about 1,595
      runner-minutes is inferred from per-job averages. No devtool tracks queue time,
      though two outlier walls, 227 s and 282 s, were queue-driven. Review-lane minutes
      appear in one PR body of twenty and in no structured field, so review time could
      not be ranked. PR #221's self-reported cycle count did not reconcile with the
      Actions API either.
    entry: >-
      The four receipts under results/agenda-042 and their named gaps.
    exit: >-
      check_pr_wall, or the branch-cost rollup it feeds, reports a pull request's cycles,
      red share, queue time and runner-minutes, and a structured field records
      review-lane minutes.
    bead: think-d3z8
    depends_on: []
    next_evidence: >-
      The tool's output over the same twenty pull requests lane B counted, reconciled
      against the receipt.
    workflows: [efficiency-loop]
    program: development-cycle
    parallel_group: agenda042-ci
    artifacts:
    - packing/campaign/series/series-000-smoke-and-calibration/results/agenda-042/pr-cycle-receipt.md
    - packing/campaign/series/series-000-smoke-and-calibration/results/agenda-042/pr-wall-receipt.md
---
# agenda-042: Efficiency Block — the Development Cycle

The entry point is **W5 efficiency-loop**, declared before measuring (`OR-5`). The owner
opened it after watching PR #221 need two full atlas rebuilds to merge.
Their hypothesis was that checking rasters and PDFs slows the commit and merge cycle.

The block opened by measuring, as `OR-12` requires, in four disjoint lanes against
`main` at `f5c9c8453`. Each lane’s receipt is under
[`results/agenda-042`](../series/series-000-smoke-and-calibration/results/agenda-042/)
with the run ids and commits behind its figures:

- [pull-request wall](../series/series-000-smoke-and-calibration/results/agenda-042/pr-wall-receipt.md)
- [pull-request cycle](../series/series-000-smoke-and-calibration/results/agenda-042/pr-cycle-receipt.md)
- [atlas exports](../series/series-000-smoke-and-calibration/results/agenda-042/atlas-exports-receipt.md)
- [suite shards](../series/series-000-smoke-and-calibration/results/agenda-042/suite-shards-receipt.md)

## Checking the rasters and PDFs is not the slow part

Checking costs about one CPU-second per pull request and none of its wall.
`build_known_best_atlas --check` never draws a PNG or a PDF. It reads each export’s
receipt, the sha256 of the SVG it was drawn from, stored in the file, and compares it.
`render_composite_pdf --check` took 0.72 s on PR #221’s last run.
It runs inside the `sweeps` job, which finished about 90 s before the job that set the
wall.
The Pages `pdf` job draws the explainer in Chromium, not the atlas, and is also off
the critical path.

What is slow is **regenerating** and **merging**:

| Cost | Measured |
| --- | --- |
| One full `build_known_best_atlas --update` | about 4m45s |
| … share that re-proves unchanged witnesses in mpmath | about 97% of the per-case pool |
| … share that draws the six exports | about 20 s |
| Re-pins of `DATA_REVISION` on 2026-09-22, one full rebuild each | 5, so about 24 min at 4m45s each |
| PR #221’s merge of `main`: one rebuild to resolve, one to re-stamp | 9m29s |
| Merges since the exports appeared (2026-08-26) with both parents changing them | 4, 2 of them conflicting |
| The six exports’ history in the pack after 28 days | 88.1 MB of 525 MiB |

So the lever is `BC-375`: redraw only what changed.
Moving the check itself would save nothing, and `OR-13` forbids moving a check that
cheap.

## Where the cycle’s time goes, and what to do first

Ranked by what each costs every contributor, not by how easy it is:

1. **Red cycles, `BC-376` and `BC-377`.** 42 of 151 CI cycles went red over the last
   twenty merged pull requests.
   Every red cycle costs a full wall plus the author’s attention to diagnose and
   re-push. Of fifteen sampled red runs, six were causes the `--push` floor catches
   locally, and nothing enforces that floor.
   It is also expensive: on this block’s own commit, which changed only Markdown and
   YAML, `--push` reached 55 test files and took 464 s. A floor that costs almost eight
   minutes for a documentation change gets skipped, so `BC-376` measures the selector
   before it proposes a hook.
   Eight were not caused by the change under review at all: four gate-budget timing
   findings and four inherited from a red `main`. Those need an owner decision, so
   `BC-377` is blocked on it.
2. **The pull-request wall, `BC-374`.** Every cycle, green or red, pays it.
   The median is 189 s against a 180 s edge, and the third suite shard that `think-g4n9`
   scoped on 2026-09-17 is still unbuilt.
   It is predicted to take about 50 s off the critical path while moving no test.
3. **Atlas regeneration, `BC-375`.** It is paid by every change that moves a bound or
   the data, which is this project’s main output, and by every merge that crosses one.
4. **Measuring the cycle itself, `BC-378`.** The red-cycle cost above is inferred, and
   review time could not be ranked because it is not recorded in any structured form.

## Limits

This block measured; it changed no gate.
The runner-minute split in the cycle receipt is inferred from per-job averages.
The atlas fast path’s 40 s is an estimate for a path that does not exist yet.
Test cost is not concentrated the way `OR-13`’s 2026-09-05 figure describes: the top
twenty tests are 14.1% of the shards today, not about 70%. So the shard lever is
structural, and deferring individual tests would buy little.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
