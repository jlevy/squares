---
type: is
id: is-01m21brwj6et9vbnf7fvnpva2x
title: Keep queued math hidden through bootstrap recovery
kind: bug
status: in_progress
priority: 1
version: 5
spec_path: docs/project/specs/active/plan-2026-09-07-math-text-face.md
delegate: kpress_font_pipeline
labels: []
dependencies: []
parent_id: is-01m20v1mq20k9d9p1wg9s5qdsq
created_at: 2026-09-08T20:36:23.236Z
updated_at: 2026-09-11T09:55:39.153Z
---
Pages34274946315 exposed a real slow-startup gap: the3s root recovery timer can reveal prepared formulas whose queued hydration has not begun. Give collected static targets independent pending visibility until completion or readable fallback, preserve the runtime deadline and no-JS behavior, and retain a delayed-queue/held-font regression. Delegate kpress_font_pipeline; independent review caption_rendering.

## Notes

PR #149 head `d932bccf` reproduced a different timing interaction from the product gap
that opened this bead. The repeated WebKit artifact had 18 visible parameter readout
bases and 351 hidden bases before release, 10 held math-font requests, the first held
request near 733 ms, and the geometry release near 5474 ms. All 18 exposed bases came
from dynamic `squaresMath.render(...)` calls.

The geometry instrument inserted at the start of `<head>` intercepts
`kpressMathText.render` and `hydrate`, then postpones entry into the real runtime until
after it has constructed and measured an altered before-state. That artificial delay
also let KPress's independent three-second root recovery timer expire. The dynamic
readouts were therefore exposed before the real runtime received the synchronous call
that normally gives each node its own pending visibility. The production template has
no corresponding interceptor, and PR #149's only unique template change strengthens
reduced-motion selectors. This CI failure is a probe timing defect, not evidence of a
new product regression on the branch.

The fix pauses the root watchdog inside `_GEOMETRY_FONT_TRACE`, just as the existing
instrument already postpones the per-render font clocks. The separate queue-watchdog
control continues to expire the real root deadline while a delayed static producer and
real font transfers are held; its visibility assertion is unchanged. A Node regression
now proves the geometry instrument cancels the root watchdog while preserving the
pending marker and still refuses release before the before-snapshot.

Validation in `/private/tmp/squares-pr149-ci`: all 16
`tests/test_prepare_explainer_math.py` tests pass; Ruff passes on both changed files;
BasedPyright reports 0 errors, 0 warnings, 0 notes. An actual local Chromium geometry
and host run held 10 math-font requests and reported 0 visible bases before release, 0
hidden bases after release, complete 450-target/369-box coverage, and no findings.
Exact local WebKit replay was unavailable because the checkout requires Playwright
WebKit revision 2336 while the machine cache contains revision 2287; hosted CI has the
pinned revision.

The final edit-tier command was
`env PATH=/private/tmp/squares-pr149-ci/packing/.venv/bin:/Users/levy/.local/bin:/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin .venv/bin/packing-validate --edit --jobs 2 --inner-jobs 1`.
It passed 45 of 74 named-tier steps in 103.06 seconds, including Ruff over 1,782 files,
BasedPyright at 0 errors/0 warnings/0 notes, all record/schema/derivation checks, and the
pinned KaTeX parser over 1,022 X-027 math spans. The worktree contains only the two
intended modified files.
