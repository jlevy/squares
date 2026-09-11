---
type: is
id: is-01m298nrfg4gwvw04jtpypb6b5
title: test_candidate.py is stale against the page in two independent ways
kind: bug
status: open
priority: 1
version: 1
spec_path: docs/project/specs/active/plan-2026-09-11-workbench-from-spike-to-product.md
labels: []
dependencies: []
parent_id: is-01m28p7h39vcykq99dgjmvwv98
created_at: 2026-09-11T22:16:10.467Z
updated_at: 2026-09-11T22:16:10.467Z
---
`test_candidate.py` exits 1 against the current page, and has for some time. Two separate failures, and the second is the serious one.

**Eleven static findings**, all of them the checker describing a page three revisions old:

    retained index.html differs from a fresh build
    index.html references the network
    timing defaults are {'dwell': 0.8, 'move': 0.8, 'settle': 0.8}
    transition-stats.json timing disagrees with the page
    scarlet appears 22 times, expected once
    index.html lacks id="progress"
    index.html lacks class="nline"
    index.html lacks .lower-note {
    index.html lacks 'lower-note'
    index.html lacks 'proved lower bound'
    20 faces carry a unicode-range, expected 5

Several are demonstrably the checker's fault rather than the page's: `id="progress"` went when revision 9 dropped the progress bar, `class="nline"` went when the headline became one rendered equation, and 'references the network' is the naive `http://` scan that `render_explainer.EXTERNAL_REFERENCE` replaced everywhere else -- KaTeX's radical carries an `xmlns`.

**And `browser_checks` never runs.** `main()` returns on the static failures before reaching it, so the browser half of this checker -- where most of its 129 probes live -- has not executed in a long time. Driven directly it throws on `#facts-a .n-val` at the facts-layer check, which is another element the headline change removed.

Do the static half first, since it is what gates the rest; then run the browser half and find out what else has drifted. Related: think-lmf5, the same shape in smoke_styles.py.
