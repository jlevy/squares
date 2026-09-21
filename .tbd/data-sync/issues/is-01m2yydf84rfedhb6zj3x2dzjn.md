---
type: is
id: is-01m2yydf84rfedhb6zj3x2dzjn
title: "Land T-032: s(17) >= 461300/99999 from two external certificates (PR 211)"
kind: task
status: in_progress
priority: 1
version: 8
labels: []
dependencies: []
child_order_hints:
  - is-01m32e1sjhf4phdnmcwgwfh17j
created_at: 2026-09-20T08:20:10.625Z
updated_at: 2026-09-21T18:27:31.846Z
---
Land the n = 17 external adoption (T-032) in PR 211.

## State

PR 211 (branch claude/n17-mira-guzhou-4613-intake, from main 061e9ffb) registers
s(17) >= 461300/99999 = 4.61304613... as T-032 at V4/C4, up from 459/100 (T-019).
It registered as T-031 until the agenda-040 stack landed that id first.
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

## Certification: obtained, at 4479f2f5

The debt this bead briefly carried is discharged. `packing-validate --fast` ran on
`4479f2f5` and passed in full -- hosted run 35637803410, pages run 35637803857, every
job green -- and the session record declares it:

    full gate: fast at 4479f2f5: passed (hosted run 35637803410; pages run 35637803857)

`session-149-n17-external-intake.md` is `completed` again and no longer carries
`certification_pending`, which is what the schema means by removing the field only after
an actual qualifying pass covers the handed-over source. Its two `failed` declarations
stay, naming hosted runs 35636483146 at `bf2821e2` and 35636079542 at `9ca74721`: they
are the real history of how the branch got there.

The route was not obvious and is worth reading before the next record is written. A
record authored `status: completed` in its first commit can never earn its own first
receipt, because the step that reads one fails at every commit where the record is
terminal; and the `in_progress` state the usual lifecycle passes through is itself
refused once the session's clocks have expired. The record had to first say something
true about having no receipt -- `stopped` with `certification_pending` -- before any run
could go green and be cited. `think-3umt` carries that ordering constraint, which no
document states.

## To land it

1. DONE. The `T-031` identifier collided with PR 208 from the open overnight stack. The
   stack merged into `main` first and kept `T-031` for the n = 11 octagon corner class;
   this result took `T-032`, and its 82-line row moved to the end of
   `frontier/results.yaml` because `devtools/check_results.py` reads contiguity
   positionally. The two records that both claimed `session-148` were separated at the
   same time: chunk 5 keeps 148 and the intake is `session-149`.

2. DONE. CI's one remaining root cause was the missing `full gate:` line. No line was
   invented at any point: the record first declared itself uncertified, which let a run
   go green, and that run is what the passing declaration now names. See the section
   above.

3. DONE. PR 211's description carries the renumber, the corrected public ladder and the
   uncertified-checkpoint status.

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
