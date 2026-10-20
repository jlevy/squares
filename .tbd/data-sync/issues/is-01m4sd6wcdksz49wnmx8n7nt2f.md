---
type: is
id: is-01m4sd6wcdksz49wnmx8n7nt2f
title: "Pages prepare: the n11 explainer's twin renders can disagree on inline-math attribute order"
kind: bug
status: open
priority: 2
version: 1
labels:
  - ci
dependencies: []
created_at: 2026-10-13T01:14:40.396Z
updated_at: 2026-10-13T01:14:40.396Z
---
On PR https://github.com/jlevy/squares/pull/560 at 187d8ed1f, job https://github.com/jlevy/squares/actions/runs/38330415238/job/115078796669 failed the render-twin step (two concurrent renders of papers/n11-lower-bounds-explainer.html must be byte-identical): at one inline math span (data-kpress-math-source="n") one render emitted style="" before the data-kpress-math-* attributes and the other after data-kpress-math-display="inline". Attempt 2 of the same run passed, and the job passed on 5325ec843, 813a8181f, 2b08364ce and bfd05e075, so the serialization order in the math pre-render (kpress / render_n11_lower_bounds_explainer --prepare-math) is nondeterministic. Fix: make the pre-render's attribute order canonical (or drop empty style attributes) so the twin check cannot flake; add a test that serializes a span whose style is set and cleared.
