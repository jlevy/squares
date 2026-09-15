---
type: is
id: is-01m2chr65cx0jhfd1gsmx3r31y
title: Put workbench behavioral checks on the PR validation surface
kind: task
status: open
priority: 1
version: 13
spec_path: docs/project/specs/active/plan-2026-09-11-workbench-from-spike-to-product.md
labels:
  - workbench-roadmap
  - workbench-phase-2
dependencies:
  - type: blocks
    target: is-01m2chahf57z4w9tj5gehbs0td
  - type: blocks
    target: is-01m2ckzvnsawqg79z9ybspc3yt
  - type: blocks
    target: is-01m2chakgrn8keadss1jcs401b
parent_id: is-01m28p7h39vcykq99dgjmvwv98
created_at: 2026-09-13T04:52:30.506Z
updated_at: 2026-09-15T16:05:02.579Z
---
Review: build_workbench_site claims workbench checkers run in packing-validate, but reviewed leaf only wires Biome/tsc; workbench Python Playwright programs are outside default tests and validation. Choose a small semantic suite for startup, run/reset/mode transitions, finite validity, shared seed replay, raw/repaired results and frame/export provenance. Wire into the existing tier partition with measured budgets and config-contract tests. Preserve unique spike assertions during package migration; do not gate source-string/revision checks by default.

## Notes

2026-09-13 PR #160 checkpoint cdcd5149: focused Pack, Search, Animate, and accessibility built-page checks pass locally and in GitHub frontend CI; all 12 active CI checks pass. First CI attempt exposed Pack checker resize-event timing race, fixed at cdcd5149. Local broad push tier had seven sandbox-bound process/loopback failures; all seven passed with host permissions. Keep open for final tier/disposition requirements and historical check_workbench retirement.

2026-09-14, PR #160 review lane D-tools (D13, bead think-rj9v, closed): `check_probes` now runs on the PR surface as the first command of the frontend step (`workbench browser behavior in Chromium`, commit c78a9b31), and it resolves every constant name handed to the probe loader or a wrapper of it. The port of `check_workbench`'s unique gap-bar assertion into `check_frontend` (D13 remainder) and D60 are lane D-page's.

2026-09-14, lane D-page (PR #160 review D13, the check_frontend port): check_frontend now runs check_animate_view, whose sections and animate_view_contract.py carry every still-meaningful assertion of check_workbench, check_legend and check_revision7 as probes (1ca13c91..fcca803c, port 3dfc7f11). The three legacy checkers are retired in 46b8f14e. The wiring of check_probes into validate.py is lane D-tools' (c78a9b31).

2026-09-14, PR #125 review suggestion S5 ("Fixed waits"), deferred here: checkers that `check_frontend` runs on the PR surface still sleep instead of waiting for a condition. At `91cf28d6` (#171), `check_accessibility.py:54` and `check_animate_view.py:696` sleep 500 ms after `page.goto` rather than waiting for `window.atlasTransitions`; `check_pack_panel.py:204` sleeps 1000 ms for a run to progress; `check_stage_resize.py:144` and `:154` sleep 200 ms after a viewport change. The ready wait already exists as the function probe `probes/benchmark/page-api-ready.js` (`benchmark.py:302`), so the two load waits are a cheap swap; each settle wait needs its own condition (a step count, a resize observation). The Pack resize race at cdcd5149, above, is the failure a fixed wait invites.

2026-09-15, think-xvjf (PR #178, commit f02ba485): check_accessibility's 500 ms load wait is now `page.wait_for_function(probe("benchmark/page-api-ready"))`. The page installs `window.atlasTransitions` synchronously as it loads, so the first poll satisfies the wait. Against one built page it passed 20 of 20 runs, and check_frontend passes; on a page with the API assignment renamed, it fails at the wait with a 30 s TimeoutError. Still open from S5:
- check_animate_view.py:702 has the same 500 ms load wait and takes the same swap. It was outside think-xvjf's files.
- check_pack_panel.py:204's 1,000 ms wait was left deliberately: it is the window over which the check counts live-region mutations (and requires at least 20 steps), so waiting on a step count instead would change what is measured.
- check_stage_resize.py:144 and :154, the 200 ms waits after a viewport change, each need their own condition.
