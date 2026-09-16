# Foundation Benchmark Replay Fixture

This is a software-validation fixture, collected from clean, published commit
`4ae3a8ee6ff6cb23dc4672b40e3176efaf199aa5` on 2026-09-15. It checks the actual browser
instrument, raw JSONL, geometry admission and disjoint-block reporter together.
It is not a research campaign or evidence of packing performance.

The page was built with `squares-workbench-build --check`, which rebuilt it and found it
byte-identical and self-contained; its SHA-256 matches the `page_sha256` every row
records. The six n=5 trials used seeds 0–5, bodies, inflation 1.12, anneal 3 and a
60-second launch budget.
All six completed and passed admission under the validity contract at 1e-9; none reached
the retained reference within the report tolerance.
Their source, page digest, effective configuration (including the pair law, wall law,
beat and annealed span, `AnnealingConfiguration/v2`), browser and runtime, exact poses
and measured costs are in [trials.jsonl](trials.jsonl).
The manifest groups them into three disjoint blocks of two.

The previous rows, collected from `f9099096` on 2026-09-13, used
`AnnealingConfiguration/v1`, which records no law or beat; admission refuses such rows,
so they were replaced rather than kept beside these.

Run the reporter from `packing/`:

```bash
uv run --frozen --all-extras --group dev python -m workbench_tools.block_report \
  ../packages/workbench/tests/fixtures/benchmark-foundation/manifest.json \
  ../packages/workbench/tests/fixtures/benchmark-foundation/trials.jsonl \
  --cohort foundation-n5 --out ../attic/workbench-foundation-report.json
```

The package regression test compares that result with [report.json](report.json).
Timing measurements replay as recorded observations; repeating the browser run is not
expected to reproduce wall-clock costs.
The collection commands, run from `packing/` at the source commit, were:

```bash
uv run --frozen --all-extras --group dev squares-workbench-build --check
uv run --frozen --all-extras --group dev squares-workbench-benchmark \
  --n 5 --seeds 6 --seed-from 0 --style bodies --inflate 1.12 --anneal 3 \
  --budget 60 --out ../attic/workbench-foundation-trials.jsonl
```

This fixture does not replace the missing historical campaign trials.
Its small sample was chosen to exercise the software path, so its block intervals are
not offered as research conclusions.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
