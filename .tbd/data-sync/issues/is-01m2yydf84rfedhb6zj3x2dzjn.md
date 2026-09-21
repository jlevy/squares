---
type: is
id: is-01m2yydf84rfedhb6zj3x2dzjn
title: "Land T-031: s(17) >= 461300/99999 from two external certificates (PR 211)"
kind: task
status: in_progress
priority: 1
version: 4
labels: []
dependencies: []
created_at: 2026-09-20T08:20:10.625Z
updated_at: 2026-09-21T08:22:35.265Z
---
Land the n = 17 external adoption (T-031) in PR 211.

## State

PR 211 (branch claude/n17-mira-guzhou-4613-intake, from main 061e9ffb) registers
s(17) >= 461300/99999 = 4.61304613... as T-031 at V4/C4, up from 459/100 (T-019).
Movement +0.02305; gap to Bidwell's 4.67553009 packing now 0.0625. It is the first
verified bound at any size in this project that came from outside it.

Full handoff, written to be read cold:
docs/project/handoff-2026-09-21-n17-external-intake.md

## Validated, and why it is trustworthy

Two external certificates, both descended from this repository's T-019 and both
crediting it. Four replays, all passing, each with a retained receipt under
packing/resources/web/n17-weighted-certificates-2026-09-20/receipts/:

- Guzhou0806 R012 (2026-09-20, s(17) >= 461300/99999): its own exact event-cell checker
  recomputed all 2925 parent-angle intervals here (340 s, catalogue minimum exactly
  gamma = 250023/250000); this repository's interval branch and bound certified the same
  2925 entries over 34,465,227 boxes, none stalled, every bracket containing the source's
  exact minimum (226 s). Two methods that fail differently.
- Mira (2026-09-07, s(17) >= 4613/1000): written in this repository's certificate schema,
  so both stock verifiers decide it unchanged and both accept. Exact sweep over 2881
  directions found least covered mass 1000002103/1000000000 at direction 2194; the
  interval route pinned the same rational to a zero-width enclosure on the doubled
  5761-direction net.

A Fable-max proof review (docs/project/reviews/review-2026-09-20-n17-r012-and-mira-4613-proof-review.md,
the result's review_artifact) found no error in either argument: eleven findings, none
blocking. It supplies the two steps R012's written note omits -- that the endpoint-only
containment test covers the whole parent-angle interval, and that the inset from the
endpoint minimum of f gives exactly the union of legal parent centres.

Five fast controls in packing/tests/test_n17_external_weighted_certificates.py pin the
archived bytes, the tight placements, and a forged measure that both routes refuse.

## To land it

1. BLOCKER, bookkeeping only: the T-031 identifier collides with PR 208 from the open
   overnight stack. The results register's contiguity rule leaves no free number below
   it, so whichever lands second renumbers.

2. CI is red on exactly one root cause, which is expected and is the last step: the
   session record needs a `full gate: fast at <commit>: passed` line in its `checks:`
   list, and no local packing-validate --fast run has yet completed end to end. Do NOT
   write that line until one genuinely passes; the earlier runs failed on the workbench
   star fixture (fixed in 48a3ad23), a hosted typecheck timing budget (runner variance),
   and two subprocess signal tests that pass in isolation under lower load.
   validate, packing-required and suite-b all fail on this one missing line; 17 other
   checks pass.

3. After the gate passes, update PR 211's Validation section with the real result.
   Note that the local gate covers 48a3ad23; the later commit ecce10da adds only the
   handoff document and a regenerated document map, and touches no code or record.

## Environment notes that cost time

- npm ci has been run in the worktree, so lefthook and the browser floor work; they did
  not at the start.
- Cairo is not on the default path for direct renderer or pytest runs. Prefix with
  DYLD_FALLBACK_LIBRARY_PATH=/opt/homebrew/opt/cairo/lib AND invoke .venv/bin/python3
  directly: uv run and nohup both strip DYLD_* under SIP. packing-validate supplies the
  path itself.
- The atlas rebuild is about six minutes and must run in the foreground for that reason.

## Explicitly out of scope, and not in the PR

Mira's dilation endpoint 4.61302863588611... is not adopted: it needs a T-022-style
proof note this certificate does not carry, and R012's value is larger anyway.

The machines do not decide R012's reduction from a packing to its 2925 finite
obligations (angle folding, endpoint containment, union of centre squares, counting,
rescaling). That is a careful reading in the review artifact; a proof-assistant port is
what would close it.

The exact leg is the source's own checker, whose sweep descends from this repository's,
so its independence is of method from the interval route, not of authorship from the
generator. A retained first-party exact instrument would fix that; the review's scratch
pass shows the stock kernel decides every entry in about six minutes once its centre
domain is a parameter.

Two ideation lanes on a STRONGER n = 17 bound were started and cut when the work was
rescoped to correctness. One is an unfinished draft left uncommitted at
attic/research-2026-09-20-n17-beyond-4613.md in the worktree; the other never started.
Neither is a finding and neither is in the PR. The concrete open question: R012 gains
only 1.7e-5 over Mira on a FIXED measure, changing only which core each parent angle may
use and where its centre may sit; Mira separately reports a failed attempt at 4.615 on
the unrestricted test. Nobody has measured what the selector and the parent-centre
restriction are worth against a measure priced for them -- a covering-LP experiment this
repository already has machinery for. PR 204 (X-040) covers adjacent ground; read it
first and build on its identifiers.
