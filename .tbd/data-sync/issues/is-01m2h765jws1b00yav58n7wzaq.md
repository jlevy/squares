---
type: is
id: is-01m2h765jws1b00yav58n7wzaq
title: Extract JavaScript from the workbench package checkers
kind: task
status: open
priority: 1
version: 5
labels: []
dependencies: []
parent_id: is-01m2h76347zn3abcahzd3642ac
created_at: 2026-09-15T00:24:06.491Z
updated_at: 2026-09-15T03:33:27.651Z
---
Extract the remaining JavaScript strings in `packages/workbench/tools/workbench_tools/` (about 50 lines over 8 files) into the package's `probes/`.

The files include `check_pack_panel.py` (8 calls), `check_probes.py`, `check_workbench.py` and others the guard lists. The two `check_workbench.py` strings added on 2026-09-14 are among them: the stage-rect read in `headline_gaps` and the `getSelection().removeAllRanges()` call.

Do this after PRs #160 and #171 have had their reviews addressed, because the same files are likely to change there. Acceptance: the allowlist is empty and `check_probes` covers the new probes.

## Notes

2026-09-14, PR #160 review lane D-tools (D56, commit 269fefcc): the published workbench now carries a Content-Security-Policy, and it grants `'unsafe-eval'` only because Playwright evaluates this package's expression-string `wait_for_function` predicates with `eval` (`check_pack_panel` failed without it). When those predicates are probe files, remove `'unsafe-eval'` from `build_site.CONTENT_SECURITY_POLICY` and its test.

2026-09-14, PR #160 review lane D-tools, correction to the note above (commit d4891db4): the published policy no longer grants `'unsafe-eval'`. Instead `check_pack_panel.check` opens its page with `bypass_csp=True`, because its mobile-fit `wait_for_function` predicate is an expression string, which Playwright compiles inside the page. Measured: a function-shaped predicate, including a probe file's text, runs under the policy. So `bypass_csp` can go once that predicate is a probe file. `check_page_policy` loads the page without the bypass, and `benchmark.py`'s expression predicate passes today only because it is already true at its first poll.

2026-09-14, lane D-page: the three retired legacy checkers (46b8f14e) take their embedded-JavaScript sites with them (check_workbench's screenshot helper evaluated two strings); every new browser assertion on PR #160's lane D-page is a probe file. check_pack_panel.py's existing string sites are unchanged in count. The #175 allowlist will need its check_workbench entry removed at merge-up.
