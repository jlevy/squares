---
type: is
id: is-01m2hks7xdxm1whcf18gnj3j33
title: The suite tier runs at its 275 s ceiling on main and the stack; fix it by measurement
kind: bug
status: open
priority: 1
version: 3
labels: []
dependencies: []
created_at: 2026-09-15T04:04:14.381Z
updated_at: 2026-09-15T05:20:00.624Z
---
The pull-request `suite` job (`packing-validate --suite`, one step: `fast behavioral tests`) runs against its 275 s ceiling on `main`'s own PRs and across the workbench stack. Its recorded cost, 183.44 s, is stale.

| run | branch | tests | suite wall |
| --- | --- | ---: | ---: |
| 34920780923 | #176 `codex/n11-post-w5-route-selection` | 5,663 | 189.01 s (69%) |
| 34921194157 | #176 | 5,663 | 193.29 s (70%) |
| 34921505934 | #176 | 5,663 | 246.78 s (90%) |
| 34918365675 | #174 `codex/n11-w5-validation-efficiency` | 5,662 | 252.39 s (92%) |
| 34917733216 | #125 | 5,686 | 233.02 s (85%) |
| 34923097435 | #125 `bca21da0` | 5,707 | 258.17 s (94%) |
| 34926777301 | #160 `b2588268` | 6,041 | 274.81 s (100%, passed by 0.19 s) |

- **Runner variance:** the same branch reads 189 s and 247 s on #176, so variance alone spans a fifth of the ceiling.
- **Test count:** #160 adds about 330 tests; its review round moved the browser-floor liveness tests from skipping to running, and added the package's contract tests.
- **No single test dominates:** the slowest is `test_n5_local_rigidity.py::test_the_determination_never_claims_isolation` setup at 31.8 s. Every other test is under 12 s.

Fix by measurement, per `OR-13` and `OR-14`, not by rerunning until it passes:
1. Re-clock the tier at its reference shape.
2. Choose one of three moves:
   - shard `fast behavioral tests` across two runners, as `geometry` was split from `checks`, with the partition test still proving the jobs cover `--fast`;
   - move the one 31.8 s fixture setup, or cache it;
   - speed the slowest groups.
3. Record the new reading in `packing/devtools/gate-budgets.yaml`.

This is `main`'s infrastructure. The stack only adds tests, so the fix belongs on `main` (see also `think-lrs0` for the `checks` tier, fixed there by #174).

## Notes

**2026-09-14, the same test count at 72%.** #171 at `b7627cef` (run 34930296150) ran the same 6,041 tests in 198.22 s (72%), an hour after #160's 274.81 s (100%). The spread on one test count is 77 s, 28% of the ceiling, so the ceiling is inside runner variance. That argues for sharding or a second runner rather than trimming tests.

**2026-09-15, the first failure.** #175 at `9f88e4a7` (run 34931704686): 6,095 tests passed in 276.39 s against 275 s (101%), so `suite` and `packing-required` failed with every test green. The failed jobs were rerun once, to separate this from the code under review. The ceiling itself still needs the measured fix.
