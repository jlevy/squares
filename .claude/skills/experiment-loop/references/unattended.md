# Unattended and Parallel Operation

Load this when rounds will run without a human watching, or when more than one agent
works one registry. It covers the claim protocol that stops duplicated work, the budgets
and stop conditions, what an unwatched runner may and may not decide, merging parallel
records, and the report that greets the human in the morning.

The premise: **an unwatched loop is only as trustworthy as its refusals.** Everything
below is about making the failure modes loud and the boundaries mechanical, so a
campaign that ran for eight hours alone produces a record its author can still believe.

## What running unattended actually costs you

Before building any of this, price the thing you are giving up.

Campaigns that keep a defect log can read their own answer off it: tabulate what caught
each defect. One campaign’s 29 entries came out as **12 review, 5 inspection, 4 control
cell, 3 anomaly, 2 drift check, 1 pre-registered rule, 1 design — and 1 automated
gate.** Twenty-four of twenty-nine were found by a person or agent *reading with
intent*. The gate found one, and none of the six soundness defects.

That distribution is not a criticism of the gate; it is what gates are.
A gate confirms what someone already thought to check.
The things that catch the rest are devices built to be *surprised* — a control cell
whose answer is known in advance, a rule written down before the measurement, a
generated view contradicting its own source — and a reader who notices that a number is
strange.

**Running unattended removes the dominant detector.** So the question is not “can the
runner execute rounds” but “what is watching, now that nobody is”.
Three answers, and you want all three:

- **Move detectors from review into the gate** where you can.
  Every guard listed below is a review-detector mechanised.
- **Prefer the surprise-shaped devices.** Control cells and pre-registered rules keep
  working when nobody is awake; a checklist does not.
- **Make the morning read cheap.** The session report exists so the human’s first hour
  recovers as much of the lost attention as possible, which is why it leads with what
  the runner would not decide.

And price the other axis: **how much of a round is machine time?** One campaign recorded
275 agent-minutes against 16.4 cpu-minutes across ten rounds — seventeen to one.
A runner only removes the waiting; it does nothing for the seventeen.
Automating an agent-bound loop buys very little and can cost a night of debugging, so
measure the ratio from your own effort fields before deciding this is worth building.
Where the ratio is the other way round, unattended operation is the whole game.

## Build the harness as steps, not as a session

The tempting shape is one program that runs the night: pick, run, judge, record, repeat.
It is the wrong shape, for a reason that only shows up at 3am — when it fails, you have
no move except to restart it, and you do not know what it had already done.

Build **one subcommand per step of the loop**, each doing one thing the same way every
time, and let something else sequence them:

```
harness status              where things stand
harness preflight           fire every guard and report
harness claim <hypothesis>  allocate the id, write the in-progress stub  -> exp-041
harness execute exp-041     run the round's declared command, archive the output
harness record  exp-041     read the archive, decide, write the round, commit
harness release exp-041     give up a stuck round; recovery, not routine
harness run                 the middle three, over the queue, unattended
```

Two properties make this worth the small extra structure:

- **State lives on disk, never between steps.** `claim` writes the stub, `execute`
  appends to the archive beside it, `record` reads that archive back.
  A step that dies loses nothing a re-run cannot rebuild, and `status` can always answer
  where you are. Make `execute` truncate its archive first, so re-running it never
  double-counts.
- **Failure recovery is re-running one step**, not restarting a session.
  When `record` refuses because the whole-set checker rejected the artifact, the fix is
  to correct what the checker named and run `record` again — the hours of compute in the
  archive are untouched.
  A session-shaped harness makes that same failure cost the night.

An agent is perfectly capable of sequencing these and recovering when one fails.
What it cannot do is recover from a monolith that died halfway with its state in memory.
`run` is then a thin loop over the same three steps, for a night with nobody watching,
and anything it can do you can do by hand.

## The harness holds no experiment code

**An experiment is a declared command, not a branch in the harness.** Put the command in
the registry artifact, have the harness substitute the instance and the seed, run it,
archive what it prints, and enforce one fixed contract on that output.

```yaml
runner:
  command: './engine --n {n} --seed {seed} --budget 100000000'
  cells: [17]
  seeds: [1, 2, 3, 4, 5]
  timebox: 1h
```

The contract is the whole interface.
A useful one, adapt the field names:

> Print JSON Lines to stdout.
> Carry the outcome metric, the instance, and the seed on every result line.
> Carry whatever the validity guard reads on those same lines.
> Exit 0.

Two consequences, and they are the point:

- **Adding an experiment never edits the harness.** If it would, the contract is wrong
  and the contract is the thing to fix.
  Per-round parsing written into the harness is code that runs once, at 3am, having
  never been exercised — which is the most reliable way to lose a night.
- **The guard is one piece of code every round exercises**, rather than one per
  experiment. That matters more than it sounds: a validity check reimplemented per
  experiment is a validity check that is wrong in one of them.

Writing new *experiment* code is expected and fine — a new probe is a script obeying the
contract. Writing new *harness* code per round is the thing to refuse.

Carry the instance and seed on every result line even when it feels redundant.
It is what lets the harness group results exactly, instead of inferring which line was a
summary or assuming every seed printed the same number of lines.
Both inferences are wrong eventually and neither fails loudly.

## Do not build coordination you do not need

Most campaigns run one session at a time.
For those, the entire claim protocol below — locks, id reservation, lease reclamation,
the duplication key — is machinery that can only introduce bugs, and the honest
implementation is one line:

> Refuse to start when a round is already in progress.

That enforces the assumption instead of trusting it, and it costs nothing.
Read the rest of this section when a fleet is actually the plan, and lift the allocator
from it then.

## The claim is the artifact

Do not build a separate lock file for each round.
Allocate the id and write the claim in one step, before any work starts:

1. Take the allocation lock for `experiments/`.
2. Scan for the highest `exp-NNN`; the claim is the next number.
3. Write `experiments/exp-NNN-<slug>.md` with `verdict.decision: in-progress`,
   `method.operator`, the `hypotheses` it claims, the instance point, and
   `lease.expires`. Release the lock.
4. Do the work. Rewrite the same file with the real verdict when done.

The record and the lock are one object, so there is nothing to garbage-collect and no
way to hold a claim without leaving evidence.
A runner that crashes leaves an `in-progress` artifact whose lease has expired, which
the ledger surfaces as a **stale claim** — not as silence.

**The scan and the create must be one critical section.** The tempting version — skip
the lock and rely on an exclusive create of the final filename — is wrong, and wrong in
a way that passes a careless test: `O_EXCL` reserves the *filename*, and two runners
choosing different slugs produce two different filenames carrying the same id.
Measured on 2026-08-22: 64 concurrent claimers under that scheme produced 49 distinct
ids for 64 rounds. Reserving an id-only name and renaming it to the slugged one is also
wrong — the rename frees the reservation, so a later claimer re-allocates the id.

**Reserve with `mkdir`, not with a lock.** The obvious implementation takes an advisory
lock — `flock` on a lock file — and it is the wrong default, because advisory locking is
the one filesystem primitive that quietly does not work where a fleet is most likely to
live.
Over NFS `flock` was purely local before Linux 2.6.37 and is emulated through POSIX
byte-range locks after it, needing a working lock daemon; on macOS over SMB or a
VM-shared mount it may return `ENOTSUP` or simply fail to exclude other hosts.
Two runners then both believe they hold the lock, which is the duplicate id the lock
existed to prevent.

`mkdir` needs no daemon and no advisory-lock support: creating a directory that already
exists fails, atomically, on every filesystem worth running on, NFS included.
So make the reservation a marker directory named for the id.

```python
import re
from pathlib import Path

def claim(experiments: Path, markers: Path, slug: str, body: str) -> Path:
    """Allocate the next free experiment id and write the claim."""
    experiments.mkdir(parents=True, exist_ok=True)
    markers.mkdir(parents=True, exist_ok=True)

    seen = [int(m.group(1)) for p in experiments.glob("exp-*.md")
            if (m := re.match(r"exp-(\d{3})-", p.name))]
    seen += [int(m.group(1)) for d in markers.iterdir()
             if (m := re.match(r"exp-(\d{3})$", d.name))]
    nid = max(seen, default=0) + 1

    while True:
        try:
            (markers / f"exp-{nid:03d}").mkdir()   # atomic; exactly one racer wins
        except FileExistsError:
            nid += 1
            continue
        break

    path = experiments / f"exp-{nid:03d}-{slug}.md"
    path.write_text(body)
    return path
```

Three properties worth naming, because each removes a failure the lock version has:

- **Nothing is held while the round runs.** The marker is a fact, not a lease, so there
  is no stale lock to time out and no crashed runner blocking the allocator.
  (The lease on the *artifact* is a separate mechanism covering a different failure —
  see above.)
- **The reservation is never freed.** That is what kills the rename trap: reserving an
  id-only filename and renaming it to the slugged one frees the reservation, and a later
  claimer re-allocates the id.
- **The scan does not have to be exact.** It only seeds the search; correctness rests on
  the `mkdir`. A scan that races and reads a stale directory listing costs one extra
  loop iteration, not a duplicate id.

Verified with 32 and 64 concurrent OS processes: distinct ids, no gaps, no strays.
Test the function you ship, not a copy of it pasted into the test — a rehearsal of a
reimplementation proves the reimplementation works.

**All of this assumes the runners share a filesystem.** On separate branches or
worktrees they do not, so assign **disjoint id blocks** up front instead — runner A
takes 100–199, runner B 200–299 — and record the assignment in the runbook.
Ids stay unique and never reused; they are monotonic within a block rather than
globally, which is all invariant 8 needs.

## What counts as duplicated work

The unit is the triple **(hypothesis, instance point, operator)**. Two runners on the
same hypothesis are duplicating only when all three match.

| Situation | Verdict |
| --- | --- |
| Same H, same instance, same operator | duplication — skip; another runner holds it |
| Same H, different instance point | **the sweep**, run it |
| Same H, same instance, different operator | **a replication**, run it if the registry says `replication: welcome` |
| Different H, same instance | normal parallel work |

Before claiming, a runner reads every `in-progress` artifact with a live lease and
excludes those triples.
That read is the coordination; there is no broker.

A hypothesis that is expensive and un-replicated should say `replication: welcome` only
when a second opinion is worth the budget.
Default it off, or an overnight fleet will spend the night agreeing with itself.

## Budgets and stop conditions

Declare all of these in the runbook before the first unattended night.
A runner without a stop condition does not stop; it degrades.

| Budget | Example |
| --- | --- |
| Per round | 20 min wall, or 10⁶ solver iterations, or 50k tokens |
| Per session | 8 hours, or 40 rounds, or a token ceiling |
| Per hypothesis | at most 3 rounds before it must be `abandoned` with `reopen_when` |

Stop — do not adapt — on any of:

- **Budget exhausted** (any of the three above).
- **Queue empty**: no open hypothesis whose instrument exists.
- **Harness broken**: 3 consecutive runs refused by a validity guard, or 3 consecutive
  crashes. Three guard refusals in a row is far more likely to be a broken instrument
  than three bad candidates, and continuing fills the record with noise.
- **The standing best moved unexpectedly**, or any invariant check fails (duplicate id,
  dangling hypothesis reference, view drift).
- **A decision needs the human**: anything in the refusal list below.

On stop, write the session report and exit non-zero if the stop was abnormal.
Exiting zero on a harness failure is how a broken night looks like a quiet one.

## What an unwatched runner may not do

Mechanical rules, because “use judgment” does not survive hour six.

**Never, without a human:**

- Change the accept rule, a threshold, the metric vector, or the metric roles.
  A campaign whose bar moved mid-run has measured nothing.
- Edit or delete an existing artifact’s findings.
  Corrections are **annotations** appended to the body, stating what stands and what
  does not (invariant 11).
- Delete raw run data, or a result that came out badly.
- Widen the subject or the instance axis beyond what the runbook declares.
- Install a new dependency, or change a version pin.
- Force-push, rewrite history, or push to a shared branch (unless the runbook explicitly
  grants it).
- Claim `accepted` on a confirmatory hypothesis without the evidence its tier requires.
- Invent a criterion mid-round because the predicted one did not move.

**Always:**

- Record the round whatever happened.
  A crash is `unresolved` with the reason in `verdict.reason`, not a missing file.
- Refuse a run that fails a validity guard, at record time, and count it toward the
  consecutive-failure stop.
- Register a new hypothesis (`registered: <date>`, citing the round that raised it)
  before measuring anything the queue did not predict.
- Regenerate the views after each round, so an interrupted session still has a current
  ledger.
- Leave the working tree committed.
  Uncommitted work at 3am is work that will be lost.

The one judgment clause of the accept rule — *is the change worth its complexity* — is
the boundary case. An unwatched runner may apply it only in the conservative direction:
it may decline a marginal win, recording why, and it may not accept one.
Anything it declined on judgment goes in the morning report’s review section.

**Build that as a structural refusal, not a behavioural one.** The strong form is a
runner that *cannot express* the accepting verdict — the code path does not exist, so
the strongest thing it can write is a pass on the arithmetic clauses flagged for review.
A rule saying “the runner should be careful here” is one prompt, one refactor, or one
plausible special case away from being violated at 4am with nobody reading.
A missing code path is not.
Wherever a refusal in this list can be made unrepresentable rather than merely
forbidden, make it unrepresentable; the rest is what the review section is for.

## The queue needs a machine-readable half

A registry written for humans describes its instrument in prose — *“the stock annealer
at 100x budget, five seeds, gated by the selftest”*. That is the right thing to write
and an unwatched runner cannot execute it.
The gap gets closed one of two ways, and only one of them is safe: either the runner
parses prose and improvises a command, or the registry carries a second, explicitly
machine-readable field alongside the prose.

Carry both. Keep the prose field as the human’s account of what the round is, and add a
recipe field naming an executor and its parameters.
Then:

- **A hypothesis with no recipe is never run unattended.** It is reported as needing an
  operator, which is the escalate-instead-of-guess rule applied at the queue rather than
  mid-round.
- **The recipe cannot widen the subject.** Its instance points must lie inside the
  declared sweep, and the runner refuses one that does not — otherwise a recipe becomes
  a quiet way to edit the campaign’s scope.
- **Adding an executor is a deliberate change with its own rehearsal.** Never something
  a runner does at 3am.

This also keeps the registry honest about readiness: the set of hypotheses carrying a
recipe *is* the overnight queue, so its depth is countable before the night rather than
discovered during it.

## Escalating instead of guessing

When a runner hits something the runbook does not cover, the correct move is to record a
`blocked` artifact naming precisely what is missing, and move to the next queue item.
`blocked` is a cheap, honest, resumable state; a guess is an expensive one that looks
like a result.

## The three roles, running unattended

The pipeline in `SKILL.md` — explorer, codifier, runner — maps onto an overnight fleet
with one ordering constraint: **the registry is frozen while runners are working on
it.**

A practical schedule:

1. **Evening, explorer(s):** one or more agents read widely and write
   `explorations/X-NNN-*.md`. They may run in parallel without coordination; reports do
   not conflict. Brief each of them with `ideas.md` — one page that says what has already
   been considered, parked, and killed, which is the cheapest possible way to stop an
   explorer rediscovering last week’s dead end.
2. **Evening, codifier:** one agent, alone, lands the new ideas on `ideas.md`, converts
   the ones that can be stated so they could be wrong into registry artifacts, and
   assigns priorities. Run this single-threaded — the codifier is the only writer of
   `ideas.md` and `hypotheses/`, which makes H-id allocation trivially safe and keeps
   de-duplication of near-identical claims possible.
3. **Overnight, runners:** N agents claim and execute rounds under the protocol above.
   Runners never write `hypotheses/` except to add a new one raised by a round, and each
   such addition takes the next free H-id by the same exclusive-create trick.
4. **Morning, human:** reads the session report, resolves the review queue, and
   re-screens the registry.

Give the explorers the campaign question, the idea board, and the current ledger — an
explorer that does not know what has already been abandoned proposes it again.

## Merging parallel records

The record is built to be reconciled, because everything is one file per experiment:

- Parallel branches add artifacts; git merges them as file additions.
- **Ids are the merge surface.** Two campaigns numbering from the same next-free id
  collide silently — each side stays internally valid, so only a whole-set check catches
  it. After any merge, check id uniqueness; on collision, renumber the newer campaign’s
  artifacts (id, filename, cross-references) and regenerate the views.
  Disjoint id blocks prevent this; use them whenever branches are the plan.
- **The same hypothesis tried twice is a replication, not a conflict.** Keep both
  artifacts referencing the same H-id with different exp-ids, and let `method.operator`
  distinguish them, so different models attacking the same problem can be compared on
  the same registry.
- Views are regenerated after every merge, never hand-reconciled.

Run this after every merge and at the end of every session:

```
[ ] every exp-NNN and H-NNN id appears exactly once
[ ] every hypothesis id referenced by an experiment exists in the registry
[ ] every experiment references at least one hypothesis
[ ] every H-NNN named on the idea board exists, and every hypothesis appears on the board
[ ] no in-progress artifact holds an expired lease (else: reclaim or mark unresolved)
[ ] every artifact validates against its schema
[ ] the regenerated views match the committed ones
```

## Before the first unattended night

A rehearsal, in this order.
Each step has killed a campaign that skipped it.

1. **One supervised round, end to end**, including the record and the view regeneration.
   A loop nobody has watched complete one round will not complete fifty.
2. **Fire the validity guard on purpose.** Feed it a run that must fail and watch it
   refuse. A guard nobody has seen fire is not yet evidence.
3. **Kill a runner mid-round** and confirm the stale claim is visible and reclaimable.
4. **Race the id allocator with concurrent processes**, not threads and not reasoning —
   at least 16 at once — and assert distinct ids with no gaps.
   This is the step that catches a claim protocol that locks the filename instead of the
   id.
5. **Break the harness deliberately** and confirm the consecutive-failure stop fires and
   exits non-zero.
6. **Check the budget accounting** against a short run, so the per-session ceiling means
   what it says.
7. **Count the queue, and price it against the machine you will actually use.** How many
   hypotheses carry a recipe, are not already resolved, and are not waiting on an
   instrument that does not exist?
   Multiply by their timeboxes.
   A perfect runner in front of a one-item queue is an idle night, and this is the step
   that tells you *before* rather than at breakfast.
   Price it on the target hardware, not the one you developed on: a measured 40M ops/s
   workstation and a 15M ops/s cloud container differ by enough to turn a comfortable
   night into an overrun, and a timebox sized on the wrong one is how a round comes back
   `abandoned` with nothing learned.
8. **Read the gate’s skip list on a clean clone.** Your development machine has every
   optional dependency installed and will never show you the checks a fresh environment
   silently drops. See the green-gate trap in `traps.md`.

## The session report

Generated, never hand-written, and written even when the session ended badly.
It is the handoff to the human, so it leads with what needs them:

```markdown
# Session <date> — <campaign>

## Needs review            <- first, always
Marginal results declined on judgment; blocked rounds and what they need;
stale claims; anything the runner refused to decide.

## What ran
N rounds by <operators>, <budget> spent of <budget> allotted.
Table: exp-id | H-id | instance | operator | decision | primary criterion.

## What moved
Verdicts that changed the standing best or resolved a hypothesis, with numbers
and spreads.

## What died
Rejections and abandonments, with reopen_when — the most reusable section.

## Queue after this session
Open hypotheses by priority; sweep cells still empty; newly registered claims.

## Health
Guard refusals, crashes, invalid runs, stop condition that ended the session.
```

Lead with the failures.
fdu’s ledger does, and it is why its queue is trusted.
