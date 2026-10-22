---
type: is
id: is-01m4sd6wcdksz49wnmx8n7nt2f
title: "Pages prepare: the n11 explainer's twin renders can disagree on inline-math attribute order"
kind: bug
status: in_progress
priority: 1
version: 3
delegate: c-lane-twin-render-1022
labels:
  - ci
dependencies: []
hold: null
hold_until: null
created_at: 2026-10-13T01:14:40.396Z
updated_at: 2026-10-22T21:56:51.552Z
started_at: 2026-10-22T21:56:51.552Z
---
On PR https://github.com/jlevy/squares/pull/560 at 187d8ed1f, job https://github.com/jlevy/squares/actions/runs/38330415238/job/115078796669 failed the render-twin step (two concurrent renders of papers/n11-lower-bounds-explainer.html must be byte-identical): at one inline math span (data-kpress-math-source="n") one render emitted style="" before the data-kpress-math-* attributes and the other after data-kpress-math-display="inline". Attempt 2 of the same run passed, and the job passed on 5325ec843, 813a8181f, 2b08364ce and bfd05e075, so the serialization order in the math pre-render (kpress / render_n11_lower_bounds_explainer --prepare-math) is nondeterministic. Fix: make the pre-render's attribute order canonical (or drop empty style attributes) so the twin check cannot flake; add a test that serializes a span whose style is set and cleared.

## Notes

2026-10-22 21:58Z coord-intake-1021b: hit main. Certificate page run 39858025544 on bfc04b659 (#735 merge) failed prepare (twin renders disagree at the \tau^* \lt n inline span), skipping deploy, so T-194 News item did not publish. Full re-run requested (attempt 2). Lanes comparing paper renders on 22 Oct saw the same style="" position noise between two renders of one tree. Raised to P1; fix lane started.
