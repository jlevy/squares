---
type: is
id: is-01m2h765jws1b00yav58n7wzaq
title: Extract JavaScript from the workbench package checkers
kind: task
status: closed
priority: 1
version: 8
labels: []
dependencies: []
parent_id: is-01m2h76347zn3abcahzd3642ac
created_at: 2026-09-15T00:24:06.491Z
updated_at: 2026-09-15T16:05:27.344Z
closed_at: 2026-09-15T16:05:27.343Z
close_reason: "PR #178 (https://github.com/jlevy/squares/pull/178): all 13 embedded-JavaScript sites in the workbench package's 4 files are removed and their allowlist entries dropped; check_probes covers the 5 new probes (181 total); check_frontend and the package tests pass."
resolution: null
duplicate_of: null
---
Extract the remaining JavaScript strings in `packages/workbench/tools/workbench_tools/` (about 50 lines over 8 files) into the package's `probes/`.

The files include `check_pack_panel.py` (8 calls), `check_probes.py`, `check_workbench.py` and others the guard lists. The two `check_workbench.py` strings added on 2026-09-14 are among them: the stage-rect read in `headline_gaps` and the `getSelection().removeAllRanges()` call.

Do this after PRs #160 and #171 have had their reviews addressed, because the same files are likely to change there. Acceptance: the allowlist is empty and `check_probes` covers the new probes.

## Notes

2026-09-14, PR #160 review lane D-tools (D56, commit 269fefcc): the published workbench now carries a Content-Security-Policy, and it grants `'unsafe-eval'` only because Playwright evaluates this package's expression-string `wait_for_function` predicates with `eval` (`check_pack_panel` failed without it). When those predicates are probe files, remove `'unsafe-eval'` from `build_site.CONTENT_SECURITY_POLICY` and its test.

2026-09-14, PR #160 review lane D-tools, correction to the note above (commit d4891db4): the published policy no longer grants `'unsafe-eval'`. Instead `check_pack_panel.check` opens its page with `bypass_csp=True`, because its mobile-fit `wait_for_function` predicate is an expression string, which Playwright compiles inside the page. Measured: a function-shaped predicate, including a probe file's text, runs under the policy. So `bypass_csp` can go once that predicate is a probe file. `check_page_policy` loads the page without the bypass, and `benchmark.py`'s expression predicate passes today only because it is already true at its first poll.

2026-09-14, lane D-page: the three retired legacy checkers (46b8f14e) take their embedded-JavaScript sites with them (check_workbench's screenshot helper evaluated two strings); every new browser assertion on PR #160's lane D-page is a probe file. check_pack_panel.py's existing string sites are unchanged in count. The #175 allowlist will need its check_workbench entry removed at merge-up.

2026-09-15, #175 merge-up (head 9f88e4a7): this bead's scope fell from 30 sites in 10 files to 13 sites in 4.
- The check_workbench entry left (2 sites; file retired by the stack).
- benchmark.py (5 sites) and check_search_panel.py (1) left: the stack converted them to probes.
- check_animation_editor.py (3) and check_stage_resize.py (4) left: Lane E's probe conversions.
- workbench_tools/check_probes.py (1) left: #175 retired it. devtools.check_probes now resolves every loaded name whatever its group, applying #160's c78a9b31 rule, and finds loader wrappers (look, _look, Session.look) across the package without the CALLERS list. validate.py's frontend step runs it, and the old tests are ported to packing/tests/test_no_embedded_js_contract.py.
- check_pack_panel.py fell from 8 sites to 7. Its mobile-fit wait is the probe pack/stage-fits-viewport, and bypass_csp is gone. The checker passes under the published policy, and the old expression string fails there with EvalError.
- check_page_policy now imports sqpack.probes.applied.

Remaining: check_pack_panel.py (7), check_candidate.py (3), check_accessibility.py (2), tests/test_self_contained.py (1, a script body in a fixture).

2026-09-15, PR #178 (claude/no-js-workbench-checkers, head 98afc346, base claude/no-js-in-python-guard at 9f88e4a7): all 13 sites in the 4 files are gone, and the four allowlist entries are removed. The guard reports 447 sites in 38 files, none in packages/workbench.
- check_accessibility (2): new probe accessibility/active-pack-index. Its 500 ms load wait is now benchmark/page-api-ready (S5, noted on think-kpvc).
- check_pack_panel (7): new probes dom/transforms, pack/scene-matches-snapshot, api/refusal and layout/scroll-width, plus the existing pack/apply.
- check_candidate (3): the stale needles were deleted with their assertions preserved. The API check is now a page-api-ready probe, and the angle tolerance is checked on the page's data (noted on think-tn0j).
- test_self_contained (1): tests/fixtures/self-contained/allowed/blob-object-url.html. Biome's includes name no *.html, and the guard reads only *.py.
Evidence: both checkers' output is byte-identical on one built page, and on 7 page mutants the old and new checkers give the same failure text, except check_accessibility on the no-API page, which now fails at the new wait. check_probes reports 181 probes; check_frontend, npm lint, typecheck and the workspace check pass. The shared "Now 460 sites in 42 files" comment in embedded-javascript.yaml was left for the coordinator.
