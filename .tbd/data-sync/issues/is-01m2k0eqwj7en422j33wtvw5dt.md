---
type: is
id: is-01m2k0eqwj7en422j33wtvw5dt
title: "[epic] PR CI back under OR-14: aggressive speed review, 2026-09-15"
kind: epic
status: open
priority: 1
version: 2
labels: []
dependencies: []
created_at: 2026-09-15T17:04:56.205Z
updated_at: 2026-09-15T20:00:58.203Z
---
Owner, 2026-09-15: "this looks like it's taking a long time to do PR CI checks can you do an aggressive review to see what can be sped up to make sure that they're as fast as reasonable? We already have done work on this, and we should revisit it. I am concerned if it spiraled again."

Readings at the start:
- **Packing validation:** about 5 min on PRs, set by `suite` at 290-301 s.
  - `suite`'s tier sits at its 275 s ceiling and failed once at 276.39 s with every test passing (think-jblb).
  - `checks` is at 141 s after #174's rollup fix (think-lrs0).
- **Certificate page (Pages):** about 9 min on the workbench stack's PRs (`prepare` 79 s, then `build` 402 s, then `font-loading` webkit 175 s and firefox 137 s). It does not run on PRs to main that avoid its paths.
- **OR-14's target:** 2 to 2.5 min.

Plan:
1. Three read-only audits: the Packing validation job and step breakdown; the Pages workflow on PRs; the prior validation-efficiency work and where it drifted. Outputs go to attic/ci-review/.
2. One synthesis with ranked speedups, each with measured savings and its OR-13 coverage argument.
3. Implementation as measured PRs against main, each recording its reading in packing/devtools/gate-budgets.yaml.

## Notes

**2026-09-15, review done; the owner chose all three lanes as PRs into `main`.**
- **Synthesis:** `attic/ci-review/synthesis.md` in the squares-viz-explanations worktree. The three audits sit beside it.
- **Lanes:**
  - Lane 1: Pages parallel and scoped, `claude/ci-pages-parallel`, in `lane-d-tools`.
  - Lane 2: Packing validation shard and speed, `claude/ci-validation-shard`, in `consolidate-stack`. It also covers the post-merge skip and the per-file test cost.
  - Lane 3: PR-wall budget, no empty records, no ratchet, bead hygiene, `claude/ci-wall-budget`, in `nojs-guard`.
- **Main has moved:** it is now at `5ce2839f`, so the workbench stack needs a main merge after the three land.
- **Superseded:** the suite-ceiling task chip (`think-jblb`) is folded into lane 2.
