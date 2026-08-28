---
type: is
id: is-01m15442akdex5khfn7z8hrarb
title: Repoint the Python path constants
kind: task
status: closed
priority: 0
version: 4
labels: []
dependencies:
  - type: blocks
    target: is-01m15443qrx72drzbbdpc6eqrk
  - type: blocks
    target: is-01m15444sqtndc8k38h7bd5k6w
parent_id: is-01m15219m6eh8fww5pm9sc2sqd
created_at: 2026-08-28T21:23:56.883Z
updated_at: 2026-08-28T23:27:56.785Z
closed_at: 2026-08-28T23:27:56.785Z
close_reason: Landed on refactor/hoist-packing-to-root
resolution: null
duplicate_of: null
---
Two distinct groups, both mechanical once separated.

**Group 1, constants that reach above the packing directory.** After the move the
packing project lives one level below the repo root instead of two, so each of these
loses exactly one level:

- `packing/devtools/build_known_best_atlas.py:83` REPOSITORY_ROOT = ROOT.parents[1] -> parents[0]
- `packing/devtools/build_prospective_atlas.py:31` same
- `packing/devtools/check_documentation.py:18` same
- `packing/devtools/check_generated_markdown.py:24` REPO = PACKING.parent.parent -> PACKING.parent
- `packing/devtools/run_negative_controls.py:83` REPO = ROOT.parent.parent -> ROOT.parent
- `packing/devtools/check_bead_tree.py:38` REPO = parents[3] -> parents[2]
- `packing/src/sqpack/cli/validate.py:39` REPOSITORY_ROOT = PROJECT_ROOT.parents[1] -> parents[0]
- `packing/tests/test_module_boundaries.py:20` same

**Group 2, constants that own documents which have moved to the root.** These break in
the opposite direction: ROOT still resolves to `packing/`, but the file it names is no
longer there.

- `check_readme.py` README, SYNOPSIS, RESEARCH (`docs/project/research`)
- `check_synopsis.py` its SYNOPSIS target
- `render_defects.py` its `defects.md` output path
- `render_research_tables.py:34` MAIN, the n=11 report
- `check_documentation.py` its durable-document scan root

Note `render_defects.py` now writes a generated view at the repo root from a source in
`packing/defects.yaml`. That split is intentional and fine, but the output path must be
explicit rather than derived from the yaml's own directory.

Leave alone: everything using `ROOT = Path(__file__).resolve().parent.parent` in
`devtools/` or `parents[2]` in `cases/`. Those still resolve to `packing/` and are
correct unchanged. `src/sqpack/project.py` also needs no logic change: it finds the
project by marker discovery (`pyproject.toml`, `campaign`, `cases`, `devtools`,
`frontier`) and all five markers stay together inside `packing/`. Only its error-message
text on line 51 mentions the old path.
