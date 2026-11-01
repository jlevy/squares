---
type: is
id: is-01m68g3hqcfvxxbpxaxmxpemac
title: "CI: frontend worker gw1 crashed in test_site_case_records.py, 757 s against 105 s (run 41175767887, #850 review A3)"
kind: bug
status: open
priority: 3
version: 2
labels: []
dependencies: []
parent_id: is-01m684vnbc5mmkjn950c3edw3w
created_at: 2026-10-31T08:09:35.212Z
updated_at: 2026-10-31T09:28:25.646Z
---
Review A3 of #850 (31 October 2026): in Packing validation run 41175767887 (PR #850 at 40df512a1), the frontend job's step "site table layout in Chromium" ran 756.77 s against a recorded 104.74 s (7.23x; the tier's ceiling is 165 s) and failed because pytest-xdist worker gw1 crashed while running tests/test_site_case_records.py::test_a_frontier_row_opens_its_record_and_steps_to_the_next. Every other job of the run passed, and the next runs of the same tree (41178188203 at fea8351b2, 41180240126 at e4cac5eb1) passed. The branch changed no frontend or site code (packets, evidence and coverage records only), so it reads as host load or a browser crash, not a code fault; the empty commit 8f8eabb5b was pushed to re-run CI because the re-run API was not open to that session.

A sevenfold overrun on a pull-request tier is what OR-17's wall ceiling exists to catch. To do: read run 41175767887's frontend artifact (validation-timings-frontend-1, artifact 13033306637) for the crashed worker's last output and the step's timings; decide whether the test or its browser start needs a guard (a per-test timeout, a crash-retry, or a quarantine), or record it as runner variance under think-ht59 with the measurement.

## Notes

Diagnosis, 31 October 2026 (bold-ritchie-ci-diag): this is runner contention inside the step. What the site renders has not regressed.

- **The step has run at this wall for a week.** The frontend job's step "Run the frontend source and built-page contracts" took 448 to 849 s across about 120 pull-request runs sampled from 23 to 31 October; green runs include 663 s (23 October, job 120508882905) and 794 s (31 October, job 124492645558). The "recorded 104.74s" that the tier compares against is stale. #850's 757 s and #854's 626 s (run 41186384687, job 124494111956) fall inside that range, and #854's is below the median. The site table-layout selection is 508 tests in green and red runs alike.
- **The stalls happen in every run.** Each run, green ones included, prints 5 to 7 `faulthandler_timeout=60` dumps (5 on 23 October, 6 green on 31 October, 7 in #854). Their stacks are module fixtures that render the whole site from records in each xdist worker: `tests/site_renders.py` `case_records`, then `devtools/render_case_pages.py`, then kpress Markdown rendering and `validate_schemas` YAML loads. pytest bills that work as setup. For example, `test_site_atlas_views.py::test_an_explicit_small_address_opens_triangle_under_its_two_tabs` took 99.42 s of setup on 23 October, 158.35 s in the green 31 October run and 157.93 s in #854's red run. Three such workers and their Chromiums share a four-cpu runner with the workbench browser step (182 s) and the browser floor (103 s), which run beside them.
- **The failing call.** `test_an_atlas_cell_opens_the_same_record` usually takes 3.30 s (23 October) to 5.88 s (31 October, green) of call time. In #854 the `popover.locator('[data-case-body] article.site-case[data-case="11"]').wait_for()` at `tests/test_site_case_records.py:292` reached Playwright's 30 s default under that load, for a call of 34.29 s. #850's crash of worker gw1 happened in the same step under the same load.
- **Rate.** 2 of about 45 completed pull-request frontend jobs on 31 October were red: 41175767887 (#850) and 41186384687 (#854).
- **Today's records did not cause it.** The render setup is the same 158 s in today's green and red runs. Between 23 and 31 October it grew from 99 s to 158 s, and these readings cannot tell whether that growth came from the week's records or from runner draws.
- **Options, none done here.** Render the site once per session and share it across workers through a file-locked cache, instead of once per worker module. Or run the site step at `-n 2`. Leave the 30 s wait alone unless a measurement justifies changing it; no test was skipped or relaxed.
