---
type: is
id: is-01m3smrzvr7qhfacgdffajbw7x
title: Update the complete atlas regression for confirmed n11 optimality
kind: bug
status: closed
priority: 1
version: 4
spec_path: docs/project/specs/active/plan-2026-09-29-proof-verification-consolidation.md
labels: []
dependencies: []
parent_id: is-01m3sken298psm0jfn7tmbcqp9
created_at: 2026-09-30T17:11:11.991Z
updated_at: 2026-09-30T17:42:05.133Z
closed_at: 2026-09-30T17:42:05.133Z
close_reason: Merged in PR246 at d44ec0408 after green final-head424b6be3a CI. Sol repairs and Astra-max review retained full2095 row/source/deadline coverage and exact39-case atlas classification; targeted evidence plus unaffected deferred executions is recorded in PR comments and Session164.
resolution: null
duplicate_of: null
---
Deferred checkpoint36746969192 at6a307f6a4 rebuilt the atlas and matched the retained SVG, then failed an obsolete assertion expecting38 solved-case equalities; actual39 includes newly confirmed T060. Reuse the existing quick composite/epistemic classification contract rather than merely masking a changed count. Preserve the complete atlas/case/square checks; verify the changed assertion against retained output and narrow controls, without another local whole-atlas rebuild. Sol repairs, Astra reviews.

## Notes

Fixed in ebbfec10e, test-only. Explicit set of 39 solved cases, ordered labels, n11 equality and E-n011-global-optimality-independent evidence replace stale count38. Four quick retained-artifact controls pass in0.98s; hosted original test already passed full atlas rebuild and retained SVG equality before the stale final assertion. Astra max approved SHA86a507db12e9ced6b102557ac74a6aad86d4e565384829cfdbfdaf12196db9a8. No atlas rebuild repeated or artifact changed. Await publication/current-head normal CI.
