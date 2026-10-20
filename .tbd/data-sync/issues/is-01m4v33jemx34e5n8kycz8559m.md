---
type: is
id: is-01m4v33jemx34e5n8kycz8559m
title: test_case_summaries_keep_math_and_layout_when_fetched[light-1280] measures n = 291 before the resize back to 1280 settles
kind: bug
status: open
priority: 2
version: 4
labels: []
dependencies: []
created_at: 2026-10-13T16:56:35.026Z
updated_at: 2026-10-14T22:44:15.719Z
---
On #571's head 3aeaa2e68 (Packing validation run 38433380791, job 115421046134) the frontend job failed on `tests/test_site_case_records.py::test_case_summaries_keep_math_and_layout_when_fetched[light-1280]`: `fetched["drawingWidth"] == approx(direct["drawingWidth"], abs=1)` gave 320 against 288 ± 1. The same test passed on #571's previous head 7ad0f6204, on #560's 2993cb1d2 and on #577's f497f1fb3, whose tree contains #571's. The runner was slow: the frontend tier took 351.6 s against its recorded 104.7 s (3.4x).

Cause, from the test: only the light-1280 case resizes the direct page. For n = 291, `_case_bounds_at_the_two_column_boundary` takes the viewport down to about 560 px, and the test then calls `direct_page.set_viewport_size({"width": 1280, ...})` and evaluates LAYOUT straight away. The helper's own loop waits for KPress's reduced-motion transition at every step (`expect(...).to_have_css("inline-size", ...)`, "still completes on the next paint"), but nothing waits after that last resize. The direct page was measured at 288 px (18rem, the narrow layout) while the fetched popover was already at 320 px (20rem).

Fix: after the resize back to `width`, wait for the layout to settle before `direct = direct_page.evaluate(LAYOUT)`. Either repeat the helper's `to_have_css` wait on `.site-case-bounds > :last-child`, or poll LAYOUT across animation frames until `drawingWidth` and `articleWidth` read the same twice. Done when the light-1280 case no longer depends on paint timing. Nothing in the record or the site needs to change.

## Notes

The assertion carries no message, so the log does not name which case failed. n = 291 is inferred: the light-1280 variant is the only one that resizes a page, and 288 px is the narrow layout's drawing width. Confirm by adding the case number to that assertion's message when fixing it.


2026-10-14: two more occurrences, same parametrization and the same 320 against 288. #597's first frontend run (Packing validation run 38543823546), on main at f73e9de13 plus a check_requests change that touches no site file; its rerun passed. #514's run 38551576411 (job 115810545771), on 586cf4dad merged into f73e9de13. Main's own frontend job passed on f73e9de13. Locally the test passes, as do 30 plain and 20 throttled (CDP CPU rate 6) repetitions of the n = 291 sequence. The cause is now shown deterministically. In a scratch test that reuses the module's fixtures, LAYOUT probe and helper, `Animation.setPlaybackRate` 0 is sent over CDP after `_case_bounds_at_the_two_column_boundary` and before the resize back to 1280. The direct page then reads drawingWidth 320 at load, 288 at the boundary, 288 right after the resize, and 320 once the timeline runs again. The result is the same on #514's 586cf4dad and on main at f73e9de13. The stale value is KPress's reduced-motion rule (`.kpress [class]`, a 0.01 ms transition of every property) on `.site-case-figure`'s container-query `inline-size`. A cleaner fix than a wait is to run the boundary exercise on a throwaway page in the same context, so the direct page is never resized.



2026-10-14 22:29Z: recurred on PR #514 at 3b3d6af18 (run 38647258125, job 116137088672), same test test_case_summaries_keep_math_and_layout_when_fetched[light-1280], 320 against 288; attempt 2 passed.
