# Square-packing workbench

This package owns the workbench’s typed browser modules and Python adapters.
The
[workbench plan](../../docs/project/specs/active/plan-2026-09-11-workbench-from-spike-to-product.md)
defines the finished product and migration phases; the
[review](../../docs/project/reviews/review-2026-09-12-workbench-stack-architecture.md)
tracks repairs and their evidence.

The current migration checkpoint builds strict API, geometry-admission, force-law,
navigation, corpus and timeline modules into the existing Pack/Animate page.
The retained application and several build/capture consumers still live under the spike
and `packing/devtools`. Consolidation, strict graduation of every retained source,
arbitrary-n Pack and Search remain active work in the plan.

## Development

Use Node 24 (the baseline is pinned in the repository’s `.node-version`) and the
repository’s Python 3.14 environment.
From the repository root:

```bash
npm ci
npm run check --workspace @squares/workbench
```

The package check builds the browser and benchmark bundles, runs Biome and the
type-aware promise floor, type-checks the modules, and runs the Node contract tests.
Python adapters are installed with the repository’s `workbench` extra.
From `packing/`:

```bash
uv run --frozen --all-extras --group dev python -m pytest ../packages/workbench/tests
uv run --frozen --all-extras --group dev python -m devtools.build_workbench_site
```

The latter builds the self-contained page in `packing/site/workbench/`. Its publisher
checks the generated full corpus, source identity, local links and deterministic output.
The GitHub Pages deployment is owned by the repository workflow.

## Contracts and ownership

- `src/api` defines the public browser API. Runtime installation and probe declarations
  consume this contract.
- `src/core` owns seed semantics, snapshot checks and navigation.
  Packing poses use radians internally; the retained public browser API uses degrees.
- `src/data` validates the versioned corpus and its stable identities.
  The builder supplies palette/shades from `sqpack.render`; workbench angle clustering
  has a separate declared tolerance.
- `src/animation` computes timing, arrival, range progress and deterministic seeking.
  These operations do not call a solver or require a DOM.
- `probes` holds checked browser instruments.
  Python code does not embed their programs in string literals.
- `tools/workbench_tools` contains Python import, geometry, trial and report contracts.
  Numerical admission retains the exact checked snapshot and its tolerance.

## Reproducible block reports

From `packing/`, a cohort manifest and a JSONL envelope file produce the report:

```bash
uv run --frozen --all-extras --group dev python -m workbench_tools.block_report \
    /path/to/manifest.json /path/to/trials.jsonl --out /path/to/report.json
```

The manifest schema is `squares.workbench.cohort/v1`. It declares the full source
commit, repository-relative benchmark path (`instrument`), catalogue directory
(`reference_source`), purpose (`research` or `software-validation`) and cohorts.
Each cohort declares its ID, n, style, requested parameter overrides, tuning/held-out or
exploratory partition, block size, step and repair budgets, and ordered seed slots.
Slots explicitly say completed, failed, cancelled or not-started.
Completed slots have exactly one JSONL envelope: `{"cohort":"cohort-id","trial":{...}}`,
with an `AnnealingTrial/v2` receipt.
The [contract tests](tests/test_block_report.py) include an executable complete example.

The report admits geometry through the same rule as run/replay/sweep, checks effective
settings and source/runtime agreement, and preserves unsuccessful blocks and partial
tails.
Rates name their denominators; distributions conditioned on valid outcomes say so.
Wilson intervals describe independent-block sampling assumptions rather than
establishing that a deterministic seed campaign sampled independently.
Zero reference-to-grid gaps have no normalized score.
Unknown cost stays unknown.

Historical summaries are audited by `workbench_tools.historical_summary_audit`; they
cannot be used as raw trials.
See the [annealing runbook](../../packing/campaign/results/annealing/README.md) for
record validation and the limits of the retained evidence.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
