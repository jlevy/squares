# The checkers’ probes

One JavaScript expression per file, loaded by `probes.probe("<name>")` and handed to
`page.evaluate`. See [`../probes.py`](../probes.py) for the contract; the short version
is that a probe takes its values as its **one argument** rather than having them
formatted into its text.

Names are grouped by what they are about, not by which checker uses them, so two
checkers asking the same question of the page ask it with the same file.

## The one file here that is not a probe

[`atlas-transitions.d.ts`](atlas-transitions.d.ts) declares `window.atlasTransitions`,
the page’s own API, which every probe reaches and nothing else describes.
It is read off the object literal at the end of the IIFE in
[`../assets/workbench.js`](../assets/workbench.js), so it says what the page offers
rather than what the probes happen to have called so far.

It exists so `tsc -p tsconfig.probes.json` can check these files at the repository’s
type floor, and it is the reason one `.d.ts` replaced what would otherwise have been 180
local annotations.
Nothing loads it: a declaration file has no emit, and `probes.probe()`
still hands the browser each `.js` file exactly as it sits on disk.
`check_probes.py` globs `*.js`, so it does not count this file as a probe.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
