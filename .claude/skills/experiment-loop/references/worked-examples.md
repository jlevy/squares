# Worked Examples: Four Domains

How the campaign elements instantiate in four very different subjects.
Use the nearest one as a template, then adjust — the point of the mappings is that only
the adapter changes; the loop, the record, and the views do not.

## Systems performance (fdu — the heavy end)

| Element | Instantiation |
| --- | --- |
| Subject | a reference file tree pinned by content digest; host CPU/cores/memory; filesystem; cache regime |
| Hypotheses | “the walk is serial, a bounded parallel producer cuts wall time 3–4×” — each names the metric and predicted magnitude |
| Instrument | a probe binary + harness that interleaves variants and checks an oracle digest per trial |
| Metrics + roles | outcome `wall_ns`; cost `cpu_ns`; guards `peak_rss_bytes`, major faults; mechanism `component_ns`, user/system CPU, blocked time, context switches |
| Shape / tier | `paired`, confirmatory (12–20 interleaved pairs, bootstrap CI) |
| Decisions seen | accepted, rejected, superseded, blocked, baseline |
| Body holds | profile evidence, the mechanism, what the prediction got wrong, why warm was *not* a regression |

Gold-standard artifact:
[exp-051](https://github.com/jlevy/fdu/blob/main/docs/project/experiments/exp-051-memoize-the-parent-resolved-for-the-previous-upsert.md)
— note its verdict reason (numbers + interval + the one judgment) and its “Where the
prediction was wrong” section.
Generated views: `make perf-ledger` / `make perf-report`, drift-checked in `make check`;
the ledger it produces is
[the experiment ledger](https://github.com/jlevy/fdu/blob/main/docs/project/reports/report-2026-08-10-fdu-performance-experiments.md),
which leads with its failures.

## Full-stack web app load time (metabrowser — the light end)

| Element | Instantiation |
| --- | --- |
| Subject | generated corpus (files/dirs), browser, viewport, cold flag (fresh port = empty HTTP cache; fresh process = scan running) |
| Hypotheses | registry table rows, each naming its instrument; “the idle sweep is not viewport-bounded, so it requests folders the reader cannot see” |
| Instrument | a 772-line `run.py` (serve/record/compare/report) + a probe.js a person pastes into the page — measurement is operator-carried because browser automation was a dependency decision |
| Metrics + roles | outcome = the hypothesis’s named metric (`first_row_ms`, `subtree_requests`); cost `transferred_kb`; guard “nothing else moved the wrong way unaccounted”; mechanism render spans, long tasks |
| Shape / tier | `conditions` (median + min–max, n≥3–6), exploratory throughout |
| Decisions seen | accepted, unresolved (H3: instrumented, never reproduced, reason recorded) |
| Body holds | the code read that refined the hypothesis, all three variants tried (two rejected), the two methodology defects found and fixed |

Exemplar: `explorations/experiments/exp-003-*.md` on the `claude/perf-subtree-sweep`
branch (github.com/jlevy/metabrowser PR #66) — a full round in ~150 lines of file.

## Geometric packing search (the `record` shape)

Hypotheses are **algorithms or strategies**, and each artifact is the full research
report on trying one.

| Element | Instantiation |
| --- | --- |
| Subject | the problem instance, exactly: “pack 17 unit squares in the smallest enclosing square”, tolerance, any symmetry assumptions |
| Hypotheses | “simulated annealing with pairwise-swap moves reaches density ≥ X on instance Y”; “Graham-style corner packing beats random restarts at n≤20” |
| Instrument | the solver run under a declared compute budget + an **independent validity checker** (no overlaps, all inside the boundary) — the checker is the guard, and a solution failing it is invalid, not low-scoring |
| Metrics + roles | outcome best score (`record` shape, against the standing best and its source); cost CPU-hours/attempts; guard the validity checker; mechanism iterations, restarts, convergence curve |
| Shape / tier | `record` + a `determination` (`beat_record` pass/fail); exploratory while screening strategies, confirmatory for a claimed new record (independent re-check, exact arithmetic where possible) |
| Decisions seen | `abandoned` is the workhorse: budget spent, best reached, and `reopen_when` ("worth revisiting with a local-search polish phase, which annealing lacked") |
| Body holds | the algorithm’s description and code ref (commit, entry point, command), parameter choices and why, the convergence story, the best configuration found (coordinates committed as data), what to try next |

The registry is what makes this a campaign rather than a pile of solver runs: strategies
are enumerated up front, each attempt cites its strategy id via `strategy_refs`, and the
generated registry view shows which strategies are exhausted, abandoned-with-promise, or
untried — so a later agent (or a different model) picks up exactly where the search
stopped, and replications of the same strategy by different operators sit side by side
under one H-id.

Three pieces of this domain are worth naming because they are unusually easy to get
right here, and campaigns that skip them get much weaker records:

- **The standing best is already an artifact.** Where a project keeps a structured
  record of known bounds, `standing_best` and `standing_best_source` point straight at
  it instead of being retyped into each round.
  The record then cannot disagree with itself, and a round that moves the frontier
  updates one file.
- **The instance axis is `n`, and it comes with a free positive control.** A solved case
  is a case whose answer is known, so a searcher that cannot recover it has not earned
  an opinion about an open one.
  Make a solved neighbour the baseline round and a permanent cell of every sweep; it is
  the cheapest instrument guard in this subject.
- **The validity guard can be exact.** A separating-axis check over the packing’s own
  algebraic number field decides contact-versus-overlap exactly, where a float check
  needs a tolerance that is simultaneously a blind spot for small overlaps and a
  rejection of true tangency.
  Where an exact oracle exists, `beat_record: true` may only be recorded behind it.

## Proof / algorithm strategy portfolio (the `determination` shape)

| Element | Instantiation |
| --- | --- |
| Subject | the statement or problem, its formalization, the proof system or evaluation environment |
| Hypotheses | strategic approaches: “induction on n with strengthened invariant”, “reduce to the bounded case then exhaust”, “the greedy exchange argument closes the gap” |
| Instrument | the attempt itself under a declared budget + the independent checker (a proof kernel, a test oracle, a reviewer with stated criteria) |
| Metrics + roles | outcome a `determination` from a declared enum (`proved`, `refuted`, `counterexample`, `no-progress`); cost budget spent (time, tokens, attempts); guard the kernel/oracle accepting; mechanism subgoals closed, lemmas established, cases remaining |
| Shape / tier | `determination`, sometimes plus `conditions` for partial-progress metrics; a `proved` claim is confirmatory by construction — the checker is the confidence |
| Decisions seen | accepted (proved), rejected (approach refuted: “the invariant is not inductive, counterexample at n=4”), `abandoned` (budget spent; record the lemmas that *did* land, so the next approach inherits them), unresolved |
| Body holds | the strategy spelled out, the partial results with pointers to formalized lemmas (by commit), where it got stuck and *why*, what a different approach would need to reuse |

Pass/fail and incremental metrics coexist naturally here: the determination is the
outcome, and the mechanism metrics (subgoals closed) let an `abandoned` verdict record
real partial progress instead of a bare “gave up”.

## Choosing your nearest template

- Comparing two builds/configs of the same system → fdu’s shape (`paired` if you can
  automate interleaving; `conditions` if not).
- Improving a user-facing property with a hand-driven instrument → metabrowser’s shape.
- Searching a solution space for the best anything → packing’s shape (`record` + budgets
  \+ `abandoned`).
- A portfolio of qualitatively different strategies where attempts pass or fail → the
  proof shape (`determination` + partial-progress mechanisms).

Mixtures are normal.
Declare the shapes in the campaign README, put only those in the schema, and let each
hypothesis name which one resolves it.
