# Unattended and Parallel Operation

Load this when rounds will run without a human watching, or when more than one agent
works one registry. It covers the claim protocol that stops duplicated work, the budgets
and stop conditions, what an unwatched runner may and may not decide, merging parallel
records, and the report that greets the human in the morning.

The premise: **an unwatched loop is only as trustworthy as its refusals.** Everything
below is about making the failure modes loud and the boundaries mechanical, so a
campaign that ran for eight hours alone produces a record its author can still believe.

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

```python
import fcntl
from pathlib import Path

def claim(directory: Path, slug: str, body: str) -> Path:
    """Allocate the next free experiment id and write the claim, atomically."""
    directory.mkdir(parents=True, exist_ok=True)
    with open(directory / ".idlock", "a") as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)          # released when the block exits
        taken = [int(p.name[4:7]) for p in directory.glob("exp-[0-9][0-9][0-9]-*.md")]
        path = directory / f"exp-{max(taken, default=0) + 1:03d}-{slug}.md"
        path.write_text(body)
        return path
```

Verified with 64 concurrent OS processes: 64 distinct ids, no gaps, no strays.
`flock` is POSIX; on Windows use `msvcrt.locking`, or give each round its own directory
(`experiments/exp-NNN/`) and let `mkdir` be the atomic reservation, which is worth doing
anyway when a round produces raw run files that want somewhere to live.

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
