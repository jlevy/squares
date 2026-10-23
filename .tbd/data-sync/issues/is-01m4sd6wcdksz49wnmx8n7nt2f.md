---
type: is
id: is-01m4sd6wcdksz49wnmx8n7nt2f
title: "Pages prepare: the n11 explainer's twin renders can disagree on inline-math attribute order"
kind: bug
status: closed
priority: 1
version: 6
delegate: c-lane-twin-render-1022
labels:
  - ci
dependencies: []
hold: null
hold_until: null
created_at: 2026-10-13T01:14:40.396Z
updated_at: 2026-10-23T01:41:56.316Z
started_at: 2026-10-22T21:56:51.552Z
closed_at: 2026-10-23T01:41:56.316Z
close_reason: "#741 merged ed6c4ff27"
resolution: null
duplicate_of: null
---
On PR https://github.com/jlevy/squares/pull/560 at 187d8ed1f, job https://github.com/jlevy/squares/actions/runs/38330415238/job/115078796669 failed the render-twin step (two concurrent renders of papers/n11-lower-bounds-explainer.html must be byte-identical): at one inline math span (data-kpress-math-source="n") one render emitted style="" before the data-kpress-math-* attributes and the other after data-kpress-math-display="inline". Attempt 2 of the same run passed, and the job passed on 5325ec843, 813a8181f, 2b08364ce and bfd05e075, so the serialization order in the math pre-render (kpress / render_n11_lower_bounds_explainer --prepare-math) is nondeterministic. Fix: make the pre-render's attribute order canonical (or drop empty style attributes) so the twin check cannot flake; add a test that serializes a span whose style is set and cleared.

## Notes

2026-10-22 21:58Z coord-intake-1021b: hit main. Certificate page run 39858025544 on bfc04b659 (#735 merge) failed prepare (twin renders disagree at the \tau^* \lt n inline span), skipping deploy, so T-194 News item did not publish. Full re-run requested (attempt 2). Lanes comparing paper renders on 22 Oct saw the same style="" position noise between two renders of one tree. Raised to P1; fix lane started.

2026-10-23 01:45Z c-lane-twin-render-1022: fix in draft PR https://github.com/jlevy/squares/pull/741 (branch claude/twin-render-canonical-attrs, head db13131e7). Root cause: Chromium adds a style written through CSSOM to the element's attribute list only when something first reads that list. KPress hideNode writes visibility before renderMarkup sets data-kpress-math-*, and showNode leaves style="". It normally serializes last; under CPU contention the list is sometimes read inside the render call (traced: class aria-hidden data-kpress-math-pending style data-kpress-math-source ...), so one formula gets style first. The formula varies by run (n, x<(191/50)c, Q_i, s(11)>=3.82, w). Fix: measure_math.js re-appends every extracted style attribute last; no KPress change. Rates (pinned Chromium 151.0.7922.34): concurrent twin --prepare-math pairs failed diff 2 of 6 before (pair 5 reproduced CI's exact n diff), 0 of 6 after; first-context harness under contention showed early style in 3 of 20 runs before, 0 of 20 after. No paper bytes change: fixed renders equal unfixed renders whose twins agreed (12 of 12), and the other three papers are identical (126 files). The ReleaseNoPublicChange record covers the explainer and the survey, which the gate selects through measure_math.js. New test test_extraction_serializes_a_lazily_written_style_in_one_place fails on main's probe and passes on the fix. Labelled S2; not marked ready or merged.

2026-10-23 01:42Z coord-intake-1021b: #741 merged as ed6c4ff27 (review A approve, no findings: https://github.com/jlevy/squares/pull/741#issuecomment-6355342863). measure_math.js re-appends descendants style last; test reaches both live orders; no paper bytes changed (ReleaseNoPublicChange for explainer and survey).
