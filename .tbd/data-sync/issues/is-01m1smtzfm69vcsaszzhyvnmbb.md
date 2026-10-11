---
type: is
id: is-01m1smtzfm69vcsaszzhyvnmbb
title: Migrate Markdown to LaTeX math, on a branch of its own, after the current work lands
kind: task
status: closed
priority: 2
version: 2
labels: []
dependencies: []
created_at: 2026-09-05T20:40:53.491Z
updated_at: 2026-10-06T08:41:25.374Z
closed_at: 2026-10-06T08:41:25.374Z
close_reason: "Done: 00346a270 (2026-09-29) 'Merge the LaTeX math migration for the reader documents' (5bff221b2), with devtools migrate_math and the check_math_markup ratchet (3eebc2bdf). README.md and TUTORIAL.md on origin/main write their math as $...$."
resolution: null
duplicate_of: null
---
DEFERRED: do not start until the explainer branch is merged and live. Then check out a new branch.

Goal: move the repository's Markdown from typewriter-font math to real LaTeX math, rendered as KaTeX by kpress on our own pages and by GitHub's own math support on github.com. The owner's standard: a few limitations are acceptable as long as the result is not strictly worse than the current typewriter font, which is uglier.

Scope, in order: README.md and TUTORIAL.md first as the most important pages, then the explainer, confirming each renders correctly in BOTH surfaces. Rendering on github.com must be verified, not assumed.

Two things to establish first. That the current flowmark does not corrupt or damage math when it formats: prior art is devtools/check_math_spans, which re-measures on a copy that the pinned flowmark-rs 0.4.0 keeps all 7,618 dollar-delimited spans in the literature archive whole, so the instrument already exists and should be pointed at the migrated documents. And what GitHub's math rendering cannot do, since it is a different engine from KaTeX-in-kpress and the two will disagree somewhere; enumerate the differences rather than discover them one document at a time.

Land it as an ongoing PR toward math notation rather than one large change.
