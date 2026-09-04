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

Six rules make it work.

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

**Check what the loop stopped on before diagnosing why the verifier refused.** That
signature has a twin which looks identical from outside and means the opposite.
At `n = 11`, side `3.81`, a program with 25,022 rows reported an objective of `10.8603`
— comfortably below eleven — and the exact sweep refused it at directions 55 to 63,
least cell `199531/200000`. Converged, then refused by a hair: the `D-434` pattern
exactly.
Except the row loop’s own last line read `least 0.9999`, so it was still finding
violated placements when it stopped.
The objective was an estimate from below rather than the restricted optimum, and the
verifier was deciding cells the loop had not finished covering.
Neither component was wrong; the run was simply unfinished.
A candidate is a candidate only when the row loop stopped because it could find no
violated placement. Report the loop’s final `least` alongside its objective — an
objective below `n` with `least` short of `1` is not a result.

**A verdict must mean one thing in every mode the verifier runs in.** The interval
verifier decides coverage by branch and bound against a threshold it takes from its
mode: mass `1` when asked whether the certificate holds, the best value seen so far when
asked to enclose the minimum.
Both are right. Reading the same `certified` status out of both was not.
Under enclosure that status says the minimum was pinned, not that the pinned value
reaches `1` — so the verifier accepted atoms whose least covered mass it had itself
measured, correctly, at `99993/100000` (`D-435`). The defect sat in the property whose
name is the whole contract, and no test caught it, because every retained certificate
passes under either reading.
Read the acceptance path itself before registering an instrument as evidence; passing
tests only show that the instrument agrees with the cases you already believed.

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

## Model routing, and when to spend the expensive reasoning

The coordinator runs at the strongest available orchestration setting and **stays
orchestrating**. It does not do the mathematics; it decides what gets done, verifies
what comes back, and owns the record.
Its errors are recoverable because every result it accepts is re-decided from disk.

**Reserve maximum-reasoning delegation for two things, and be strict about it:**

1. **Mathematical innovation** — applying or extending a theorem, deciding which
   constraint set a condition must quantify over, establishing dual feasibility,
   designing a new certificate object.
   The test: *would being wrong here produce a confident wrong number rather than an
   error?* Every real defect in the founding block was of that kind.
   `L/B` in place of `L` would have overstated a published result; a verifier that
   narrowed its cell set would have accepted false certificates.
   Neither fails loudly.
2. **Careful technical review** — an independent check written from the theorem
   statement with the implementation withheld, required to reproduce a *published* value
   as its own control.

**Do not spend it on** parameter sweeps, driving a search whose method is settled,
re-running a converged pipeline at a new value, records, registration, or formatting.
That work is high-volume, its errors surface immediately, and spending deep reasoning on
it starves the lanes that need it.

The rule in one line: **delegate the mathematics and the adversarial review; keep the
orchestration, the verification, and the record.**

## Validation scales with how notable the result is

A bound nobody has moved in twenty years will be checked by people who have neither this
repository nor any wish to trust it.
Package for them, and scale the effort to the claim:

| Claim | What ships with it |
| --- | --- |
| Routine (`S1`–`S2`) | Exact artifact, replay command, one exact decision |
| Substantive (`S3`–`S4`) | The above, plus a second decision by different code and a control on a published value |
| Notable (`S5`) | The above, plus a self-contained third-party package: the certificate as plain data, the conditions written out as a checkable statement independent of this codebase, and a verifier a stranger can run against their own arithmetic |

The obligations that make a package third-party checkable, in order of what a sceptic
reaches for first:

- **The artifact is plain data.** Exact rationals as strings in a documented schema — no
  pickles, no project types, nothing that must be imported to be read.
- **The conditions are stated, not just coded.** A reader must be able to check the
  claim against the printed theorem without reading our implementation.
- **A control on someone else’s published number.** A verifier that has only ever
  confirmed our own results has confirmed nothing.
- **Falsification is demonstrated.** Show the perturbations that are refused, and by
  which condition.
- **Every number is exact and reproducible from the artifact alone**, including the
  quantities that make the claim tight.

## Committing while lanes are live

The coordinator owns the record, which makes it the one that commits — and that is
exactly where it can damage a lane’s work.
Committing with a wholesale `git add -A` while agents are editing captures whatever
half-finished state happens to be on disk.
It happened in the founding block: a coordinator commit captured a lane’s file
mid-ablation, with one entry missing from a set it was deliberately testing, in a state
whose own test fails.
The lane noticed; nothing broke; it easily could have.

Two rules, both learned the hard way:

- **Stage paths, not the tree.** Add the files you changed.
  A lane’s files get committed when that lane reports, or as an explicitly labelled
  checkpoint after its tests, lint and type floors pass — never as a side effect of
  committing something else.
- **A checkpoint commit says so.** If a lane’s work is committed while it is still
  working, the message must say it is in progress and what was and was not verified, so
  the history does not read as a completed change.

The corresponding failure in the other direction is refusing to commit at all.
Test the state before assuming it is broken: in the founding block the coordinator
declined three times to commit an agent’s in-flight files, and when it finally ran the
tests they were green.
A feature branch loses nothing by carrying an honest checkpoint.

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
