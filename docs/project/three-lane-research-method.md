# The Three-Lane Research Method

How the 2026-09-04 block produced `T-017` and `T-018` — the first movement of `s(11)`
since 2003 — in about six hours, after the preceding three and a half hours of planning
produced nothing. Written so the next agent can run the same loop rather than rediscover
it.

## The finding that motivates all of it

The planning session before this block wrote 1,768 lines of agenda, dispatched three
independent plan reviews, and got the theorem wrong: it recorded the certificate as
proving `s(n) ≥ L/B` when it proves `s(n) ≥ L`. Three reviewers read that line and
passed it. Ten minutes of *running the instrument* caught it, because the n = 17 control
returned 4.51799 where the published value is 4.5058.

The lesson is not that planning is useless.
It is that **for a live instrument, the highest-value analysis is adversarial execution,
not more review**. Every real error in this block — the `L/B` misreading, the rounding
direction, the oracle’s cell set, the “negatives” that were grid artefacts — was found
by running something and comparing against a number that was already known.

## The three lanes

Run concurrently, on separate models, with one coordinator.
Four cores; two compute-heavy lanes is the practical ceiling.

| Lane | Model and effort | Owns | Never touches |
| --- | --- | --- | --- |
| **A — instrument** | Max reasoning | The search: oracle, LP, column generation | The verifier, the records |
| **B — mathematics** | Max reasoning | The theory: duals, ceilings, new targets | The search modules Lane A holds |
| **C — coordinator** | Fast, high effort | Verification, records, commits, sequencing | Neither lane’s files while it works |

File ownership is declared in each lane’s prompt and is not advisory: two agents editing
one module at 3am produces a merge no one can review.
Lanes that need each other’s code **import it** rather than copy it, so a fix in one
lane reaches the other.

### What the coordinator actually does

It does not do research.
It does four things, and the third is the one that matters:

1. **Sequences.** Launches lanes, kills work the evidence has killed, redirects a lane
   when its premise is refuted.
2. **Records.** Registers results, keeps the records tier green, commits and pushes on
   every result so nothing lives only in a scratch directory.
3. **Verifies independently of the lane that produced the result.** Every certificate in
   this block was re-decided by the coordinator from the file on disk, never from a
   lane’s report. This caught a live problem: Lane A rewrote a certificate file between
   the coordinator’s verification and its retention — 357 atoms became 381 — and only
   re-verifying the retained bytes caught it.
4. **Holds the check-in loop** so the block survives an idle agent or a stalled process.

## The loop

```
declare target ──► lane runs ──► coordinator verifies FROM DISK ──► register ──► push
      ▲                │                     │
      │                ▼                     ▼
      └──── redirect on refuted premise ◄─── control fails
```

Four rules make it work.

**Run the control before the target.** The generator reproduced Massaccesi’s published
`n = 17` optimum (203/12, from zero weights, never told the answer) before any new bound
was attempted. A falsifying control ran too: at a side where twelve unit squares
demonstrably fit, the same pipeline must refuse, and it did — converging to exactly 16.
An instrument that has not refused something has not been tested.

**Verify from disk, twice, by different code.** The project verifier decides; a second
verifier written from the theorem statement alone, with the implementation withheld,
decides again. That second verifier must reproduce a *published* result as its own
control, or it is only agreeing with itself.
Checksum the retained bytes against what the second verifier read.

**Round numbers are artefacts.** An LP optimum of exactly `18.0`, `25.0`, or `200/11` is
almost never the quantity you want; it is the site set.
Four “negatives” in this block were grid artefacts, and one of them — `n = 11` — was
reported as dead when the project’s own retained certificate already gave a better value
at that side. Before recording a negative, check it against every bound already in the
record.

**A refused candidate is a diagnosis, not a failure.** Two `n = 12` pushes converged
*below* the threshold and were refused by a hair.
That pattern — converged, then refused narrowly — is the signature of the search
optimising against a weaker constraint set than the verifier enforces.
It was, and fixing it (`D-434`) unlocked four rungs and the `n = 11` result within the
hour.

## Guards for unattended running

A block that runs while nobody watches needs guards against silently registering
something false. Three that earned their place:

- **Pin the verifier’s cell set.** The dangerous edit is not a wrong certificate but a
  verifier that quietly decides *fewer* placements: every retained certificate still
  passes, and everything becomes easier to accept.
  `test_the_sweep_scores_every_cell_it_scored_before` pins exact cell counts at five
  directions.
- **Keep a must-refuse fixture.** The same atoms in a container too large for them must
  be refused, with the exact least-covered-mass recorded.
- **Read the bound from the verified artifact**, never from a log line.
  The replay module returns the certificate’s own declared claim and the test compares
  it to the recomputed value.

## Model routing

Reasoning effort matters more than which lane is “important”.

- **Maximum** for anything where being wrong produces a confident wrong number: theorem
  application, dual feasibility, deciding which constraint set is correct.
- **High** for search driving, parameter choice, and reading results.
- **Fast, high effort** for the coordinator: it makes many small decisions quickly and
  its errors are recoverable.

Delegate the mathematics; keep the verification.

## What to avoid

- **Do not sweep incomparable settings.** Grid counts and insets explored as a product
  grid move the optimum in both directions, because those site sets are not nested.
  Take unions, which are monotone: adding sites can only lower a covering optimum.
- **Do not stop column generation at a round cap.** Both `n = 12` failures and the first
  `n = 11` stall were caps, not ceilings.
  Run until the dual is near feasible.
- **Do not let the coordinator plan instead of verify.** The failure mode of the
  preceding session was 96 of 212 minutes spent re-reading a CI failure already
  diagnosed as belonging to the base branch.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
