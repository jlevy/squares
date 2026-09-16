---
type: is
id: is-01m2k0eqwj7en422j33wtvw5dt
title: "[epic] PR CI back under OR-14: aggressive speed review, 2026-09-15"
kind: epic
status: open
priority: 1
version: 8
labels: []
dependencies: []
child_order_hints:
  - is-01m2kam88w7r9959zvwcswccx3
  - is-01m2kanffw38jyd10dxqqh8831
  - is-01m2kb4xhaqh3bv0cnnqnqvvsp
  - is-01m21mgmrpatjx0n66y23mmjc8
  - is-01m2m47462x0k56sjh3t4qzjsp
created_at: 2026-09-15T17:04:56.205Z
updated_at: 2026-09-16T03:29:55.392Z
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
**2026-09-16, after a machine restart and a rate-limit interruption cut every lane's agent off mid-flight.** All three lanes' work is committed, pushed and open as pull requests, each stating plainly what is done and what is not:

| Lane | Bead | PR | State |
| --- | --- | --- | --- |
| 1, the certificate page | `think-6d3d` | #183 | Pushed. Wall 472 s → **200.3 s** measured over three runs of the split shape; fifteen jobs each with a recorded cost and ceiling in the register's new `pages` section. #184 demonstrates a pull request that skips both halves. |
| 2, `Packing validation` | `think-t7zm` | #185 | Pushed. `suite` sharded in two, the type floor on its own runner, the browser floor's liveness tests moved to `frontend`, two costly fixtures cut, merged-tree verification written but not wired. |
| 3, the guardrail | `think-z121` | #186 | Pushed. `check_pr_wall.py`, `read_tier_walls.py`, the three register rules, records for `checks`, `frontend` and `sweeps`, and the rules written into `OR-14` and `development.md`. |

**Fixed while stabilising:**
- A step with no reachable pattern: moving the liveness tests left them selected by no probe path, which `test_every_step_is_reachable_from_a_declared_pattern` caught on CI. The fix is a probe, not a wider pattern (`9fc36b5f`).
- `test_every_page_job_a_pull_request_runs_is_budgeted` asserted a `pages` register section that did not exist; it is now written from named runs (`e2a53642`).
- `think-uwow` sat open under a closed parent and failed the bead-tree check on every pull request; re-parented under `think-z121`.

**Not done, and named in each pull request:** `sweeps` unparallelised, the post-merge skip unwired, sparse checkout, the per-file test-cost feed, and the wall check itself unproven on a hosted run. Pages remains above `OR-14`'s target at 200 s, and the next cut is inside the browser jobs rather than between them.
