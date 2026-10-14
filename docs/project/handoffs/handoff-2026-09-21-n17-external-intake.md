# Handoff: the `n = 17` External Intake, 21 September 2026

Written at the end of session 149 for whoever picks this up.
Pull request [211](https://github.com/jlevy/squares/pull/211) carries the whole of it,
on branch `claude/n17-mira-guzhou-4613-intake` from main `061e9ffb`, tracked by
`think-pcd0`.

The important division is between **a result that is validated and ready to land** and
**research that was started and cut**. They are not the same object and should not
travel together.

## Part 1: validated, in the pull request, ready to land

`s(17) >= 461300/99999 = 4.61304613…` is registered as `T-032` at `V4/C4`. The previous
verified value was $459/100$, so the movement is $+0.02305$ and the gap to Bidwell’s
packing closes to $0.0625$. It is the first verified bound at this size that came from
outside this project.

Two certificates arrived together, both descended from this repository’s `T-019` and
both crediting it:

| Source | Claim | How it was decided here |
| --- | --- | --- |
| Guzhou0806 R012, 2026-09-20 | $\frac{461300}{99999}$ | Its own exact checker recomputed all 2925 parent-angle intervals (340 s), and this repository’s interval branch and bound certified the same 2925 entries over 34,465,227 boxes, none stalled, every bracket containing the source’s exact minimum (226 s) |
| Mira, 2026-09-07 | $\frac{4613}{1000}$ | Accepted unchanged by both stock verifiers: the exact sweep over 2881 directions (423 s) and the interval route over the doubled 5761-direction net (1702 s), agreeing on $\frac{1000002103}{1000000000}$ |

Four receipts are retained under
`packing/resources/web/n17-weighted-certificates-2026-09-20/receipts/`, and five fast
controls in `packing/tests/test_n17_external_weighted_certificates.py` pin the archived
bytes and refuse a forged measure.

The [proof review](../reviews/review-2026-09-20-n17-r012-and-mira-4613-proof-review.md)
found no error in either argument.
Eleven findings, none blocking.
It supplies the two steps R012’s written note omits: that the endpoint-only containment
test covers the whole angle interval, and that the inset from the endpoint minimum of
$f$ gives exactly the union of legal parent centres.

### What is left to land it

1. **The `T-031` identifier contest is settled.** Pull request 208, from the open
   overnight stack, claimed the same number.
   The register’s contiguity rule leaves no free number below it, so whichever landed
   second had to renumber.
   The stack merged into `main` first and kept `T-031` for the $n = 11$ octagon corner
   class; this result took `T-032` when `main` was merged into this branch, and its row
   moved to the end of the register, because `devtools/check_results.py` reads
   contiguity positionally rather than by label.
2. **Hosted CI is red on the first run** and was diagnosed, not guessed:
   - `frontend`: fixed in `48a3ad23`. The workbench layout check staged $n = 17$ to
     assert the “new result” star, which reports that a bound was first proved here;
     that is exactly the fact this branch changed.
     The fixture moved to $n = 18$.
   - `validate`: the session record needed a passing full-gate receipt, and `ledger.md`
     needed rendering. The ledger is rendered.
     The receipt line is deliberately **not** written yet, because no local `--fast` run
     has passed end to end; do not add it until one has.
   - `suite-b`: the same session-gate test, same cause.
   - `typecheck`: a hosted timing budget, 86.1 s against a recorded 55.67 s. Runner
     variance, unrelated to this branch.
   - Two subprocess signal tests failed under local load and pass in isolation.
3. **A local `--fast` run was in flight when this was written**, against commit
   `48a3ad23`. Read its result before claiming anything about it.

### What this part does not establish

The machines do not decide R012’s reduction from a packing to its 2925 finite
obligations: the angle folding, the endpoint containment test, the union of centre
squares, the counting and the rescaling.
Those are a careful reading in the review artifact.
A proof-assistant port is what would close that gap.

The exact leg is the source’s own checker, whose sweep descends from this repository’s,
so its independence is of method from the interval route and not of authorship from the
generator. The review’s scratch pass shows the stock kernel decides every entry in about
six minutes once its centre domain is a parameter; a retained first-party exact
instrument would make that leg first-party too.

Mira’s dilation endpoint $4.61302863588611\ldots$ is **not** adopted.
It needs a `T-022`-style proof note this certificate does not carry, and R012’s value is
larger anyway.

## Part 2: research that was started and cut

None of this is in the pull request, and none of it should be treated as a finding.

The session opened five research and review lanes.
Three finished and are in Part 1. Two were ideation lanes on how to get a materially
stronger bound at $n = 17$, and both were cut when the work was rescoped to correctness
and integration. What exists:

- **Inside the covering-measure method**: an unfinished 332-line draft, now at
  `attic/research-2026-09-20-n17-beyond-4613.md` in the worktree, deliberately not
  committed. It was to answer what the one-body covering ceiling is at this size, and
  what R012’s two extensions are worth when the measure is optimised against them rather
  than held fixed.
- **Outside it**: never started.
  The brief covered multi-body pose-space search, area and wall-waste ledgers combined
  with a measure, angle-dependent measure families, structural case splits, and
  clique-strengthened fractional bounds.

The open question worth the next block is narrow and concrete.
R012 gains only `1.7e-5` over Mira’s endpoint, on a **fixed** measure: all it changes is
which core each parent angle may use and where that core’s centre may sit.
Mira separately reports a failed attempt at $4.615$ on the unrestricted test.
So nobody has measured what the selector and the parent-centre restriction are worth
against a measure priced for them.
That is a covering-LP experiment this repository already has the machinery for, and it
is the cheapest informative thing to do next.

Note that pull request 204 (`X-040`, ten hypotheses on mechanisms beyond the one-body
ceiling) is open and covers adjacent ground.
Read it before opening anything new, and build on its identifiers rather than beside
them.

## Practical notes for the next agent

- The worktree is `.claude/worktrees/n17-4613-intake`. `npm ci` has been run there, so
  lefthook and the browser floor work; they did not at the start of the session.
- Cairo is not on the default path for direct renderer or pytest runs.
  Prefix them with `DYLD_FALLBACK_LIBRARY_PATH=/opt/homebrew/opt/cairo/lib` and invoke
  `.venv/bin/python3` directly, because `uv run` and `nohup` both strip `DYLD_*` under
  SIP. `packing-validate` supplies the path itself.
- The atlas rebuild is the slow step, about six minutes, and must run in the foreground
  for the same reason.
- Two checker contracts were widened rather than bypassed, and both say why in place:
  the rung-pointer convention no longer demands `certificate.json` naming of another
  author’s archived bytes, and the case-binding contract declares $n = 17$’s external
  reduction with its reason in `tests/test_rung_figures.py`.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
