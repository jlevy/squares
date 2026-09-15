---
type: is
id: is-01m298nrfg4gwvw04jtpypb6b5
title: test_candidate.py is stale against the page in two independent ways
kind: bug
status: open
priority: 1
version: 3
spec_path: docs/project/specs/active/plan-2026-09-11-workbench-from-spike-to-product.md
labels: []
dependencies: []
parent_id: is-01m28p7h39vcykq99dgjmvwv98
created_at: 2026-09-11T22:16:10.467Z
updated_at: 2026-09-15T16:05:26.708Z
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

## Notes

2026-09-14, PR #160 review lane D-tools (D67, commit 9baad048): `check_candidate` builds with `--all`, the false facts-layer opacity loop and its probe are removed, and it no longer claims the frozen spike views. It still fails on 15 stale text needles, and its browser checks stop at the first call because `atlasTransitions` refuses calls outside the Animate view (think-7sw8).

2026-09-15, think-xvjf (PR #178, commit 20229384): 5 of check_candidate's 15 stale static failures are gone, and the other 10 are unchanged in text. "index.html does not expose the review API" was a text needle for `window.atlasTransitions`, but the page assigns `win.atlasTransitions`; the check is now `benchmark/page-api-ready` evaluated at the top of browser_checks, with the same message. The four Revision 11 angle-map needles are replaced by a check of `payload["colour"]["angleToleranceDegrees"] == 0.5` on the page's atlas-data; the slot, free-slot and contact-shade behaviour is covered by tests/colour.test.ts. Still failing: the network scan, the timing defaults (twice), scarlet count, id="progress", class="nline", the three lower-note needles, and the unicode-range count.
