---
type: is
id: is-01m2m47462x0k56sjh3t4qzjsp
title: "Probe trees and node scripts: the Pages filters and the selection map do not cover them"
kind: bug
status: open
priority: 2
version: 1
labels: []
dependencies: []
parent_id: is-01m2k0eqwj7en422j33wtvw5dt
created_at: 2026-09-16T03:29:55.392Z
updated_at: 2026-09-16T03:29:55.392Z
---
Found by a review lane on 2026-09-16, while reviewing the no-JavaScript-in-Python series (`think-m0zb`). Three gaps in what selects the browser code's checks, all measured:

**1. The Pages workflow's path filters miss three of the five probe trees.** `devtools.check_probes` discovers five roots; the workflow's 44 patterns cover one whole and part of a second:

| tree | `.js` files | covered by a `pages.yml` filter |
| --- | ---: | --- |
| `packages/workbench/probes` | 177 | yes, `packages/workbench/**` |
| `packing/devtools/probes` | 131 | yes, `packing/devtools/probes/**` |
| `packing/tests/probes` | 11 | only `pdf_math_browser/**`; `no_embedded_js/` is not |
| `packing/atlas/known-best/video/spikes/v2-transitions/probes` | 61 | no |
| `packing/atlas/known-best/video/spikes/v1-slideshow/probes` | 6 | no |

`packing/devtools/node/**` and `packing/tests/node/**` are not filtered either.

**2. The test that guards this cannot catch it.** `packing/tests/test_pages_workflow.py:35-51` hard-codes a two-element tuple of trees rather than asking `check_probes` what the trees are. The loader takes a caller-supplied root (`sqpack/probes.py:53`), so a pages-run test module can load a probe outside both the filter and the tuple and the test still passes: `tests/test_pdf_math_browser.py:31` already roots at `packing/tests/probes`, beside the uncovered `no_embedded_js/`.

**3. A step's `touches` omits the Node script it runs.** `validate.py:3649-3665` declares `"X-027 mathematics parses with pinned KaTeX"` with `check_katex.py` but not `devtools/node/check-katex.mjs`, which `check_katex.py:51` executes. Measured: editing the `.mjs` selects 14 steps, and the katex step is not among them. The browser floor is selected (`validate.py:3064` does declare `packing/devtools/node/*`), and `tests/test_check_katex.py` reaches it through the behavioural lane, so this is a selection gap rather than a hole in coverage. `test_change_scoped_selection.py:264-275` asserts a node script selects the browser floor; nothing asserts it selects the step that runs it.

Done when: the workflow's filters and the test derive the probe trees from `check_probes`' own discovery rather than a typed list; each step that shells out to a Node script declares it; and a negative control shows each rule failing when a tree or a script is left out.

Note for PR #183 (`think-6d3d`): that branch rewrites `pages.yml`'s filters into a declared-input scope, so the fix belongs there or immediately after it, not on `main` in parallel.
