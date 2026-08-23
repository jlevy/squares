# The Failure Catalog

Every entry here happened in a real campaign (fdu’s performance loop or metabrowser’s
exploration loop) and was expensive once.
Each is a trap and its guard.
Skim at setup; re-read whenever a result surprises you — the trap you are in is usually
listed.

## Before measuring

**Optimizing what is not slow.** Intuition about where time goes is reliably wrong —
fdu’s baseline put 20% of a walk in `open`, which nobody predicted.
*Guard: profile (or otherwise attribute cost) before forming the hypothesis; read a
caller tree, not a flat profile — `malloc` at the top tells you nothing actionable; the
tree says which layer is allocating.*

**Two hypotheses competing for one cost.** Whichever lands first captures the win; the
second measures noise.
Happened twice in one campaign.
*Guard: re-screen the open queue after every landing rather than working down the list.*

**Predicting a metric the rule does not score.** exp-051 predicted “≥15%” for a
component; the component moved 16.6%, the wall 7.35%, and the prediction was graded
against the wall. A category error, not a near miss.
*Guard: the hypothesis names the exact metric the accept rule scores.
Pre-register an alternative criterion in the registry if the claim is genuinely about a
component.*

**A hypothesis without an instrument.** Measuring badly because the right probe does not
exist yet corrupts the record.
*Guard: registry rows carry an `instrument` field; no instrument means status `blocked`,
not a bad measurement.*

## While measuring

**Machine drift measured as improvement.** Timings drift several percent over minutes
(thermal, background load, cache warmth).
All-of-A-then-all-of-B measures the drift.
*Guard: pair and interleave; decide on paired differences at equal ordinals.*

**The ratio of medians impersonating the paired change.** Under drift they disagree — in
fdu’s record by more than two points on 21% of entries, sometimes in sign (exp-005:
+2.8% by ratio, −3.9% paired).
*Guard: carry both medians and the paired change as separate numbers; never invite a
reader to divide one into the other.*

**The harness inside its own profile.** A probe’s verification digest was 38.8% of one
profile; quoting percentages without subtracting it attributes harness cost to the
system. *Guard: identify the harness’s share before quoting any percentage.*

**A faster wrong answer.** Timing before verifying output identity rewards bugs.
*Guard: verify identical output across every mode first — and check the control against
itself to learn which fields are legitimately nondeterministic.*

**A fresh process is not a cold cache.** Restarting the server resets the app’s state,
not the OS page cache; a walk that took 29 s cold took 2.7 s warm, and the regimes
produce different findings.
*Guard: name the regime the run met (cold/warm, scanning/settled) and record it in
`subject`; get a genuinely cold state deliberately (fresh origin/port for HTTP caches;
cache drop where the OS allows it) or say you did not.*

**The instrument deferring work invisibly.** A hidden browser pane may never run idle
callbacks — one `requestIdleCallback` with a 2 s timeout measured at 30+ seconds.
Anything deferred is unmeasurable in that state.
*Guard: record instrument state that gates scheduling (visibility, focus, power) and
require the states the finding depends on.*

**Reusing warmed instrument state.** A port whose earlier run was never recorded has
still been loaded once — reusing it hands the next run a warm cache.
*Guard: consume fresh state per run and log every unit handed out, recorded or not.*

**Position bias on surprising results.** A-then-B and B-then-A disagreeing on sign means
the effect is ordering, not code.
*Guard: run both orderings before believing any surprise.*

**A plausible number believed on first sight.** A 3.42% regression with a clean interval
— mechanically plausible, the code path really was reached — vanished at more pairs,
flipped under reversed ordering, and read +0.54% on a second harness.
*Guard: a surprising result is noise until it survives independent measurement; budget
roughly three measurements to kill one believable number.*

## Instrumentation

**The counter that reads zero.** Twice in one sitting: a serial path instrumented while
the parallel path did the work, and a lint fix that hoisted a call out of a scrutinee
taking the counter with it.
Both compiled, both passed tests, both reported zero — and a page of zeroes reads as
“the work did not happen”.
*Guard: a test asserting equality against the system’s own totals (not non-zero),
covering every path; verify it by deleting a counter and watching it fail.
Where a number cannot be obtained, leave the counter out and say why — absent is honest,
pinned to zero is a lie with a plausible face.*

**The instrument measuring itself.** A shared atomic in a parallel section measures the
counter’s contention, not the work; a clock read costs 10× an increment.
*Guard: thread-local non-atomic tallies folded at exit; count events, time only whole
phases; measure the instrument’s overhead and record it as an experiment.*

**Believing a proxy’s coverage.** `/proc/self/io`’s `syscr` looks like a syscall
counter; it counts only the read/write families — a 17k-entry walk of `getdents64` +
`statx` moved it by 30. *Guard: know which facts each source can supply; cross-check
application counters against kernel ground truth (`strace -c`) once per campaign.*

**The dead instrument producing live-looking numbers.** Six runs measured in a 0×0
browser pane: every layout-dependent number measured against nothing, timings entirely
plausible. *Guard: the instrument proves it was measuring something — record its
dimensions/ state and refuse runs below the floor at record time.*

**The harness waiting out its own subject.** A serve step that waited for `/` to render
waited out most of the scan being studied.
*Guard: the harness readiness check must not consume the phenomenon under study (wait
for the socket, not the page).*

## The record

**One boolean where four facts live.** A single `significant` flag cannot separate
“regression” from “no evidence” from “improvement under the bar”.
*Guard: `passes_acceptance`, `ci_excludes_zero`, `direction`, and any margin
classification as independent fields, derived from the interval.*

**A median without its range.** Quoted alone it claims precision the run does not have.
*Guard: print them together, in artifacts, ledgers, and PR descriptions alike.*

**Id collisions from parallel campaigns.** Two branches numbered from the same next-free
id; every artifact was individually valid; nothing noticed until the branches met.
*Guard: a whole-set identity check whenever views regenerate; duplicate ids are fatal;
renumber the newer campaign (id, filename, cross-references).*

**Implicit variant order.** The run document sorted its keys; falling back to mapping
order silently inverted control and candidate on older runs.
*Guard: record `variant_order` (or control/candidate names) explicitly; refuse ambiguous
recordings rather than resolving them.*

**The registry exempt from its own discipline.** Both reference projects kept hypotheses
in a hand-maintained table: free-text ids, no existence check, status edited by hand —
making pre-registration unenforceable.
*Guard: one artifact per hypothesis; status generated from referencing experiments; an
unknown referenced id fails the build.*

**Back-dated pre-registration.** Converting an old table wholesale stamps registration
dates on rows that were never pre-registered, laundering post-hoc choices.
*Guard: converted rows carry `registered: retroactive`.*

**Editing the story instead of the record.** A hand-maintained report drifts from its
artifacts and keeps asserting old numbers with the record’s authority.
*Guard: views are generated with a “do not edit by hand” header; where the record is big
enough to matter, a check target re-derives them and fails on drift — and verify that
gate once by mutating an artifact and watching it fail.*

**Rewriting a defective artifact.** Deleting or silently fixing history hides what the
campaign once believed and why.
*Guard: correct with an annotation stating what stands (a comparison whose both arms met
the same defect) and what does not (its absolute numbers).*

## Unattended operation

These have no counterpart in a watched session, because a human notices them in the
first minute.

**The runner that moved the bar.** A loop that relaxes its threshold when nothing passes
has measured nothing, and the record will not show it happened.
*Guard: the accept rule, thresholds, metric vector and metric roles are read-only to
runners; changing any of them is a human commit against a stated reason.*

**The quiet night that was a broken harness.** Every round refused by a validity guard,
the session exits zero, and the morning report reads as bad luck rather than as an
instrument that stopped working.
*Guard: stop after three consecutive guard refusals or crashes, exit non-zero, and put
the stop condition in the report’s health section.*

**The id lock that locked the wrong thing.** Reserving an experiment id with an
exclusive create of the final `exp-NNN-<slug>.md` reserves the *filename*, not the id:
two runners choosing different slugs both succeed and both own id `NNN`. Measured on
2026-08-22, 64 concurrent claimers under that scheme produced 49 distinct ids for 64
rounds — and every artifact was individually valid, so nothing complained.
Reserving an id-only name and renaming it to the slugged one fails differently: the
rename frees the reservation and a later claimer re-allocates the id.
*Guard: put the scan and the create in one critical section (`flock` on a single
allocation lock, or `mkdir` of a per-round directory), and test it with concurrent
processes rather than reasoning about it.*

**The fleet that agreed with itself.** N runners all pick the top-priority hypothesis at
the same instant and spend the night replicating one result.
*Guard: claim before working — create the experiment artifact with an exclusive create —
and treat (hypothesis, instance, operator) as the duplication key.*

**The stale claim that looked like work in progress.** A crashed runner leaves an
`in-progress` artifact forever; the queue looks busy and nothing is running.
*Guard: leases with an expiry; the view surfaces expired claims as stale, and any runner
may reclaim one after recording that it did.*

**The budget that did not bind.** A run declared a move budget and a restart cap, and
the restart cap always stopped the chain first — so the declared budget was inert, and
two strategies compared “at equal budget” got unequal work.
Found here on the first baseline round, by the numbers being *worse* at a larger
declared budget. *Guard: assert that the binding limit is the one you named — log which
stop condition ended each run, and check that varying the declared budget actually
changes the work done.*

**A budget denominated in rounds.** Forty rounds of a search that gets slower each round
is not a bounded night.
*Guard: budget the resource that actually runs out — wall time, CPU-hours, tokens — and
check it between rounds, not only at the start.*

**Uncommitted work at 3am.** A session that dies with results only in the working tree
loses them, and the loss is silent.
*Guard: commit artifacts, raw runs, and regenerated views after every round.*

**The explorer that reproposed an abandoned idea.** An explorer given only the campaign
question rediscovers what was already refuted last week.
*Guard: brief explorers with the current ledger and registry, not just the question —
`reopen_when` on an abandoned round is exactly the input they need.*

**The registry edited underneath a running fleet.** Priorities change mid-session and
two runners disagree about what the top item was.
*Guard: one single-threaded codifier, and freeze the registry while runners are working;
new hypotheses raised mid-round are appended, never reordered.*
