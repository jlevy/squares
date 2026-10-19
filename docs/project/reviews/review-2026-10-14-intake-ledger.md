# Review: the 2026-10-14 upper-bound intake ledger

Reviewer: Claude, Fable family, strong tier, max reasoning.
Mathematical and correctness review for coordinator session squares-43.

Under review: `packing/devtools/intake_ledger.py`, `packing/tests/test_intake_ledger.py`
and `packing/campaign/issue-intake/upper-bounds-20261014/` (sources.yaml,
github-issues.json, ledger.yaml, ledger.json, README.md) at branch
`claude/serene-hopper-xxh80m`, commit 1dc253e5e, read against `main` f73e9de13 (the
merge base; the branch changes nothing under `packing/frontier/`, so the tree the ledger
reads its starts from equals that commit).
The working tree was left as found.
Scratch code and data are beside this file; its `README.md` says what each program read
and printed.

## Summary

The recorded set is right.
I recomputed every verdict at all 163 counts (306 claim steps) from the primary data
with my own span model, my own walk, rigorous interval evaluation of the case records’
closed forms, and the certificate headers at the pinned upstream commits.
305 of 306 steps agree with the ledger; the one disagreement is in the conservative
direction (the ledger leaves undecided a comparison that is decidable as “not
recorded”), so no claim the ledger records is unrecorded by my computation and vice
versa.
The provenance of all 280 lane-backed claims and all 26 transcribed claims matches
the sources (one cosmetic print difference), the 8 claims timed by an edit or a later
commit carry the right times to within seconds, and the 19 refinement/new-packing marks
I sampled (the two the coordinator asked about among them) say what their cited sources
say, with the two caveats below.

What needs the owner’s attention before the records lane acts:

1. **The start reads only the case’s reported lane** (`tree_starts`,
   intake_ledger.py:584). The verified lane holds an exact side at 61 of the 149
   in-horizon counts where the reported lane is a print.
   At n = 11 the verified lane is the proved optimum, the root of `P_trump11`, and PR
   #574’s rational side lies above it (by less than 3e-90, exact sign test): the rule
   gives “not recorded”, the ledger says “undecided”.
   No recorded verdict changes at any count, but the structure is wrong and the “what
   would decide it” column asks for sides the case records already state.
2. **Closed forms with `sqrt` are never evaluated**, and the one claim compared by a
   `binary64` print (#593 at 51) has an exact side the lane README states from the
   pinned certificate. With both, #593’s 51 is above the record (16+5√2)/3 by 7.69e-20,
   so “not recorded (above record T-126)”, not “undecided”.
3. **The render reads the working tree, not `read_at_main`**: `render --check` and
   `test_render_check_passes_on_the_committed_ledger` will fail on `main` as soon as the
   records lane adopts what this ledger records, and a re-render then silently rewrites
   the verdicts (each recorded PR #574 refinement becomes “not recorded (equal
   record)”).
4. **Two latent walk defects**, both reproduced against the module: `lowered` picks the
   unlowered record when two pending register bounds overlap each other, so a claim
   above both is recorded; and `compare` is asymmetric when a frozen lane relation
   applies, so a record a claim is decidably below can stay in the standing set.
5. **#573 at 153 and 207 is marked “new packing” on the source’s word**, as the contract
   says it must be, but a geometric measurement contradicts the word at 207: every one
   of the 207 squares lies within 2.8e-4 of PingYou’s T-147 packing (200 within 1e-6),
   and the side is 1.49e-9 below it, which is what a re-solve of the same packing looks
   like. At 153 the match is partial (51 squares coincide to 1e-6, 147 of 153 within 0.1,
   side within 2.6e-12 of T-148’s). Credit at these counts is an owner decision; both
   are superseded by PR #574’s exact attainments in any case.

Nothing is blocking.
Findings 1 to 5 are major; the rest are minor or notes.

## Answer to the coordinator’s question: #573 at 153 and 207

What the sources say.
Issue #573 (Mishapolk, 2026-10-12T23:58:50Z), under “Lineage and credit”: “153: new
arrangement discovered using basin hopping with tilted grain boundary corridors, refined
via exact rational finishing.
207: new arrangement discovered using basin hopping with tilted boundary corridors,
refined via exact rational finishing.”
The issue’s comparison column names #504 (12.870013850408) and #503 (14.880960373044),
PingYou’s T-148 and T-147, and calls the differences “improvement[s]” of 2.56e-12 and
1.49e-9. The mishapolk lane’s packet README at d4c198d0d
(`mishapolk-exact-certificates-2026-10-12`) reports the same: “153, 207 and 209 are new
arrangements from basin hopping with tilted boundary corridors”, adds that “The README
at the pin calls 153, 154, 175, 207, 209, 237, 263, 267 and 270 'brand new geometric
topologies'”, and says of itself “This packet compares sides only and makes no finding
about where a packing came from.”
So the ledger’s `new_packing` mark at 153 and 207 is exactly what both sources say, and
the ledger’s contract ("classified only where a source says what it is") is met.

What a measurement says (`compare_geometry.py`, rational centres from the witness facts,
best of the box’s 8 symmetries):

| pair | sides (diff) | max centre displacement | within 1e-6 / 1e-3 / 0.1 |
| --- | --- | --- | --- |
| #573 n153 vs PingYou T-148 (main) | 12.870013850404479 vs 12.870013850407044 (−2.56e-12) | 0.139 | 51 / 53 / 147 of 153 |
| #573 n153 vs PingYou #504 refinement | −2.55e-12 | 0.139 | 51 / 53 / 147 of 153 |
| #573 n207 vs PingYou T-147 (main) | 14.880960371558000 vs 14.880960373043676 (−1.49e-9) | 2.8e-4 | 200 / 207 / 207 of 207 |
| #573 n207 vs PingYou #503 refinement | −5.56e-13 | 0.076 | 192 / 196 / 207 of 207 |
| PingYou #504 refinement vs T-148 (control: the same packing by the author’s own word) | −1.00e-14 | 0.090 | 151 / 151 / 153 of 153 |

At 207 the #573 certificate is PingYou’s T-147 arrangement with every square moved by at
most 2.8e-4 and the side re-solved 1.49e-9 lower; PR #574’s degree-5 exact attainment of
the same construction (14.880960371556, “PingYou’s own constructions attained exactly”
per the pr574 lane README) is a further 2.42e-12 below it, which is the picture of three
certificates of one contact topology.
At 153 the two packings share the same structure at the 0.1 scale with 100 squares
displaced by 1e-3 to 0.1 and six by more; two different local optima with sides 2.6e-12
apart would be a coincidence, so this too looks like the same load-bearing structure
with rattlers rearranged, but the measurement is less conclusive.
Under epistemics.md ("the record never says in its own voice that a regularization is
the same packing … unless the item’s `identity.basis` is `measured`, a decision made
here"), these measurements are recorded beside the source’s claim and decide nothing;
the owner decides whether #573’s 153 and 207 enter as Mishapolk’s new packings or as
refinements of PingYou’s (credited as regularizations).
Also relevant: #593’s n153.cert and n207.cert are byte for byte #573’s (mishapolk lane
README), and the ledger’s `restates` marks for #593 do not say so at 103, 153, 207 and
258\.

## Findings

### Major

**M1. The start ignores the verified upper lane.** `tree_starts`
(intake_ledger.py:583-588) takes `reported_upper_bound` only.
`cases-scan.txt` shows 61 in-horizon ledger counts whose verified lane carries an exact
form the reported lane lacks (never a verified value below the reported one, so no
recorded verdict flips).
Concrete consequence at n = 11: `frontier/n-011.md` holds
`verified_upper_bound.exact_form: root(P_trump11, 3.87708...)` with `status: proved`,
and PR #574’s N11 side is the rational
`9967775525129488857910847345.../2570946768024373398277950050...` (951 characters, in
the pull request’s own `claims.json` at 4c319c24a and in ledger.yaml).
An exact sign test of `P_trump11` at that rational puts it above the root, by less than
3e-90 (`recompute-output.txt`, “Special comparisons”); the pr574 lane README says the
same in words ("N11 lies above the case’s verified bound … which no rational reader can
compare"). By the rule the claim is weaker than the bound on record: “not recorded
(above the verified lane)”. The ledger prints “undecided (record T-011)” and asks the
owner for “the exact side behind the record’s print 3.87708359002281”, which the case
record states. Similarly at 17 the verified lane is the rational
`23377650468022754758171074269267527/5e33` and PR #574’s side is 1.04e-22 below it
(undecided only against Bidwell’s L in the reported lane), and at 29 PR #574’s side is
1.57e-36 below T-155’s exact form in the verified lane; the verdicts stay undecided
there, but the decider column should name L and the Kingbird print, not “the exact side
behind the record’s print”.
Fix: make the start the set of both lanes (each exact where it has a rational form, a
closed-form interval where it has a `sqrt` form, a polynomial-root enclosure where it
has a `root(...)` form, else its print ± u), lowered as now, and let `walk` take a list
of starts; the standing-set machinery already supports several members.

**M2. `sqrt` closed forms are never evaluated, and the exact side of #593’s 51 is not
used.** `rational_form` (intake_ledger.py:470-478) returns None for any form with a
root, so a case whose reported lane is `(16+5*sqrt(2))/3`, `2 + (1/2)sqrt(2)`,
`7 - (1/2)sqrt(2) + sqrt(1 +
sqrt(2))` and so on is compared as its print ± u. The only algebraic comparisons the
ledger makes are the lanes’ frozen `record_relation` values for PR #574’s 60 algebraic
claims (my rigorous intervals are consistent with all 53 “equal” and 4 “below”
relations). The one verdict this loses: #593 at 51. The mishapolk lane README at
d4c198d0d holds the certificate out of the declaration but states its side from the
pinned file, `S = 7690355937288491748079718099723/10^30`, and that S is above (16+5√2)/3
“by about 7.69e-20, which is the radical side dilated by 1 + 10^-20”; I fetched
`certificates/n51.cert` at 46f638c (SHA-256 e066f65f …, as the README states) and
confirm the header. With that side and the closed form evaluated as an interval at 90
digits, S − (16+5√2)/3 = 7.690e-20 > 0: “not recorded (above record T-126 by 7.69e-20)”.
The ledger has “undecided (record T-126)” with decider “the exact side of #593 at n =
51; an exact comparison with the closed form (16+5*sqrt(2))/3”, both of which were
available. This is the single disagreement in the 306-step recomputation.
Fix: (a) let `Claim.exact` be filled from a lane README or the pinned certificate for
#593’s 51, as the module’s own rule says ("where a lane’s frozen claim record or the
certificate itself states it"); (b) evaluate `sqrt` forms with `mpmath` intervals
(already a dependency) to a width below every claim’s span, and keep the print ± u only
for `root(...)` forms without a polynomial.

**M3. `render` and `render --check` depend on the working tree, not on `read_at_main`.**
`rendered` → `tree_starts` reads `view.load_records()`,
`coverage_check.parse_case(FRONTIER /
...)` and `coverage_check.COVERAGE` from the checkout (intake_ledger.py:573-594). Today
the branch’s frontier equals f73e9de13’s, so the README’s “Read against main at
f73e9de13” holds. After the records lane registers what this ledger records, every
lowered start changes: PR #574’s refinement at 68, for instance, becomes the case’s
reported bound, so PR #574’s own claim becomes “not recorded (equal record T-xxx)” and
#593’s “not recorded (above … PR #574)” becomes “not recorded (above … record)”.
`render --check` then fails, and so does
`test_render_check_passes_on_the_committed_ledger` (tests/test_intake_ledger.py:212), on
`main`, in the fast tier, on the merge the ledger itself directs; a `render --write` to
quiet it rewrites the verdicts.
Fix: have `gather` snapshot the starts (per count: the two lanes’ values and forms, the
pending entries, the beyond-horizon row) into the directory, render from the snapshot,
and make the tree comparison a separate `check --tree` that reports drift without being
a validation gate.

**M4. `lowered` ignores every pending register bound when two of them overlap each
other.** `lowered` (intake_ledger.py:536-544) keeps only a pending side decidably below
every other pending side; with two cut-decimal bounds that overlap, `smallest` is empty
and the unlowered record is returned.
`bug_demos.py` part 1: record 21/2, pending T-901 stated `10.40…` (span [10.40, 10.41))
and T-902 stated `10.405…` ([10.405, 10.406)); a claim at exactly 10.45 is **recorded
against record T-001** although it is above both pending bounds.
Not triggered by this ledger (T-121, T-122 and T-123 are alone at 106, 152 and 177), but
a silent wrong-verdict path.
Fix: return the minimal set (every pending side nothing is decidably below, plus the
record if nothing is below it) and seed `walk`’s standing set with all of them.

**M5. #573 at 153 and 207, and the “new packing” marks generally, rest on the source’s
word where a measurement contradicts it.** See the coordinator’s answer above.
The ledger’s contract is met; the record’s policy is that identity is the source’s claim
until measured here, and the lane READMEs already carry measurements for the PingYou
refinements (pingyou-n105: “Measured square for square against T-130’s certificate … it
is the same packing”). The same measurement at 207 says #573’s packing is PingYou’s.
Recommendation: the Per Report and Per Count tables should carry a `measured` column (or
the register entry an `identity.basis: measured` item) at every count where a lane or
this review measured the geometry, so a “new packing” credit is never registered against
a measurement nobody read.

### Minor

**m1. `compare` is asymmetric under a frozen relation** (intake_ledger.py:636-646). The
relation is consulted only when `side` carries it and `other` is the record; the walk’s
drop test calls `compare(member, side)` (line 703), which uses spans.
`bug_demos.py` part 2: record `2 + (1/2)sqrt(2)` printed 2.70710678118654, claim #2 with
a frozen relation `below` and a 40-place print, claim #1 a print undecided against both;
after the walk the standing set is `['record T-005', '#1', '#2']` although #2 is
decidably below the record.
No verdict is wrong (the set only gains a redundant member), but `best_now` would show
the record. Fix: make `compare` consult the relation in both argument orders, inverting
it.

**m2. The `binary64` model is stated as a bound and is not one.** The docstring (lines
32-36, 271-277) reads the print as “within one ulp of float(p) plus u”. Under the
correctly-rounded model (x → nearest double d, |x−d| ≤ ulp/2; d printed at 16 places,
|d−p| ≤ u/2) the sound span is ulp/2 + u/2, half the ledger’s. But the data violate the
model: against the lane’s exact sides, #593’s prints at 180 (1.08e-15 off, bound
9.4e-16) and 263 (2.43e-15 off, bound 1.83e-15) lie outside it, so the author’s
`side_float` was not correctly rounded from the exact side (the mishapolk lane README:
the prints “neither equal nor round up the exact sides”). The ledger’s ulp + u covers
all 73 with a worst ratio of 0.665, as an empirical envelope with no guarantee.
No verdict depends on it (72 of 73 #593 claims carry exact sides; the 73rd is M2). Fix:
say in the docstring that the span is an envelope measured on #593’s 73 prints, and
refuse a `binary64` claim without an exact side where the comparison is within 3 ulp.

**m3. Pre-edit claims are dropped and edits are dated by their announcing comments.**
#564’s 302 (original side 17.8702753841786227538399992 at 21:27:25Z, refined by an edit
at 22:16:43Z, comment 6133625109 at 22:17:00Z), #566’s 146 and #567’s 261 (edits at
23:41:36Z and 23:45:35Z, comments at 23:41:41Z and 23:45:41Z) enter only as the refined
claim at the comment’s time; #575’s 304 is dated by comment 6138078023 (04:13:31Z; the
edit 04:13:29Z). GitHub’s `userContentEdits` gives the edit times
(`github/edits-N.json`). No ordering changes (nothing else arrived in the gaps), but the
original #564/#566/#567 claims were reports under the rule and would have been recorded
at their issue’s creation; the ledger’s “first reported” times at 302, 146 and 261 are
later than the truth by 50 to 65 minutes.
Fix: date edit-added claims by `editedAt`, and list a replaced claim as its own step
("superseded by the author’s edit") so the report’s first time at the count is kept.

**m4. `_selected` can drop lane rows silently** (intake_ledger.py:1574-1582). With
neither `all` nor `counts`, a row is taken only when `printed_in == url`; a row printed
at another URL form (a comment anchor, a README) vanishes without a word, and
`problems()` notices only when a report ends with no claims.
Fix: after `gather`, require every row of every lane record read to be claimed by some
report or named in an explicit `not_ours` list.

**m5. `cross_check` warnings are printed and not kept.** `gather` returns them to
`main`, which prints `WARN` lines; the directory records nothing.
The README cannot show whether the lanes’ readings of each other agreed.
Fix: write them to `cross-check.txt` beside the snapshot.

**m6. `#562`’s 176 is a claim the issue says it does not make.** The issue states “Not
requested: 176 … so we do not ask for 176”; the ledger lists it (not recorded, above
#561) and the “Certificate Committed Before the Report” table shows it as a claim whose
certificate predates #561. Harmless to the verdicts, misleading as an owner decision.
The same claim’s `printed` is the issue’s `13.808663234387` (rounding `up`) while the
lane’s `offered_side` is the README’s `13.808663234386957`; both round the same exact
side, so this is cosmetic (the only discrepancy my audit of 280 lane-backed claims
found).

**m7. `nearest` is admitted and treated as `unstated`** (`printed_side`, line 278). A
side rounded to nearest lies within u/2; the ledger spans u. Sound, unused by any claim,
and the records’ prints are rightly read as unstated (a catalogue print can lie below a
rational ceiling, as `upper_bound_reports.House.reported_rounding` says).

**m8. `restates` marks are incomplete.** #593’s 103, 153, 207 and 258 certificates are
byte for byte #573’s (mishapolk lane README); the ledger marks none of them as restating
#573. #593 at 154 is marked as restating #570’s packing ("the same exact side")
correctly.

**m9. PR #574’s claim times for the 51 certificates that “retain identical v1 bytes”.**
The pull request’s own `claims.json` (`retained_v1_count: 51`) says 51 proposals keep
the v1 bytes, whose binding commit 9fafe786a (00:11:32Z) predates the pull request; the
lane dates all 83 rational rows by the v2 binding commit 0ab26a794 (00:24:05Z), and the
ledger follows. No report at those counts arrived between 00:13:11Z and 00:24:05Z, so no
verdict moves, but `first_committed` is 12 minutes late for those 51 under the lane’s
own definition.

### Notes

**n1. The span mathematics is sound.** `up` (p−u, p], `cut`
[p, p+u), `unstated`/`nearest` [p−u, p+u], `exact` a point, and `below` with the
open-endpoint rule are each sound (every number the print could stand for is in the
span) and, apart from m2 and m7, no wider than needed; `below` is transitive across the
open-endpoint cases, which the walk’s correctness needs.
Ties are exact equality of two exact sides (`compare`, line 644), never an overlap of
prints, which is right: equal prints do not mean equal numbers.

**n2. The walk records only claims below everything earlier.** Every side ever seen is
either in the standing set, or was dropped because a later side is decidably below it,
or was refused because it is above or equal to a member; each case chains by
transitivity to a current member, so a claim below every member is below every earlier
side.
I found no counterexample in the data or by construction (the only reachable oddity
is m1’s redundant member).
The reading of the owner’s rule for undecided comparisons (hold the claim beside the
standing side; a later claim must beat both; never guess) is the conservative one of the
two possible readings (the other treats “not shown stronger” as “not stronger” and
refuses the claim); it is implemented as stated (lines 690-704) and the alternative
would risk refusing a genuinely stronger claim, so I would keep it and let the owner
rule on the 23 undecided rows.

**n3. Ordering.** `reported_at` strings are fixed-width UTC, so string order is time
order; ties break by label, deterministically.
PR #574’s later-commit times match GitHub (0ab26a794 00:24:05Z, a006c4525 01:29:11Z,
48f063d84 01:58:06Z); the ledger’s correction of the lane’s 00:29:11Z to 01:29:11Z for
N153/N302 is right (the commit is 02:29:11+01:00). Publication times are the committer
dates of the named commits (93570ef 21:31:43Z, 4596670 13:53:57Z, b85dee2 17:30:53Z,
e646c47 19:06:24Z, c284cd0 00:05:31Z); 4596670’s author date is 2026-10-12T23:00:16Z,
about fifteen hours earlier, which would not reorder anything at 375 or 376 but shows
that a rebased publication’s “first commit” is a committer date.

**n4. Pending adoption.** `check_standing.improvements` on the tree reports exactly
T-121 (106), T-122 (152) and T-123 (177), each a cut-decimal bound read as [v, v+u); my
own scan of every register entry’s stated `s(n) ≤ v` at the ledger’s counts finds the
same three and no other entry stating a bound below both case lanes.

**n5. Exceptions** are empty; the mechanism marks a claim “recorded by exception”
without moving the standing side (test covers it), which matches “unless there’s some
key reason”.

**n6. Tests.** `pytest tests/test_intake_ledger.py`: 14 passed; `render --check`: up to
date; `check`: 28 reports, 306 claims.
The suite does not cover M4, m1 or a two-lane start.

## Recomputation

Method: `recompute.py` (see the scratch README). Starts: the set of both case lanes at n
≤ 324 (exact where the form is rational, a 90-digit interval where it has `sqrt`, a
polynomial-root enclosure by exact sign change at n = 11, else the print ± u), lowered
by register entries whose words state a bound decidably below both lanes; the current
beyond-horizon row ± u above 324, else the grid.
Claims: the lanes’ exact sides at the commits in the README’s table (280 claims), the
algebraic sides as the lanes’ 40-place prints ± 1e-40, and 26 transcribed sides read
from the issue texts and the certificate headers at the pinned upstream commits
(`upstream/`). Times: issue and comment creation from `gh`, PR commit dates, GraphQL
edit times, publication committer dates.
Walk: my own (above).
Result: 306 steps, 305 agree, 1 disagrees (n = 51, #593: ledger undecided, mine not
recorded, above record T-126 by 7.69e-20; M2). 53 further steps are “not recorded
(equal)” by the lane’s exact relation and “undecided” by my intervals, which cannot
prove equality; I list them as consistent, and every one of the 4 “below” relations is
confirmed.
With the reported lane alone as the start (the ledger’s model) my verdicts are
identical to those with both lanes except that n = 11 becomes decidable only by the
exact sign test (M1). The table covers every count of the owner-decision sections, 154,
176, 211, 241, 302, 303, 304 and 381, all PR #574 refinement counts, every
beyond-horizon count and every refinement chain.

Every count (306 steps; a step reads `report: ledger verdict → recomputed verdict`; one
verdict means both agree):

| n | report: ledger verdict → recomputed | agree |
| ---: | --- | --- |
| 5 | PR #574: not recorded → undecided (interval cannot prove equality) | yes |
| 10 | PR #574: not recorded → undecided (interval cannot prove equality) | yes |
| 11 | PR #574: undecided | yes |
| 17 | PR #574: undecided | yes |
| 18 | PR #574: not recorded → undecided (interval cannot prove equality) | yes |
| 19 | PR #574: not recorded → undecided (interval cannot prove equality) | yes |
| 26 | PR #574: not recorded → undecided (interval cannot prove equality) | yes |
| 27 | PR #574: not recorded → undecided (interval cannot prove equality) | yes |
| 28 | PR #574: undecided | yes |
| 29 | PR #574: undecided | yes |
| 37 | PR #574: undecided | yes |
| 38 | PR #574: not recorded → undecided (interval cannot prove equality) | yes |
| 39 | PR #574: undecided | yes |
| 40 | PR #574: not recorded → undecided (interval cannot prove equality) | yes |
| 41 | PR #574: undecided | yes |
| 50 | PR #574: not recorded | yes |
| 51 | PR #574: not recorded → undecided (interval cannot prove equality); #593: undecided → not recorded **DISAGREE** | NO |
| 52 | PR #574: not recorded → undecided (interval cannot prove equality) | yes |
| 53 | PR #574: not recorded → undecided (interval cannot prove equality) | yes |
| 54 | PR #574: undecided | yes |
| 55 | PR #574: undecided | yes |
| 65 | PR #574: not recorded → undecided (interval cannot prove equality) | yes |
| 66 | PR #574: not recorded → undecided (interval cannot prove equality) | yes |
| 67 | PR #574: not recorded → undecided (interval cannot prove equality) | yes |
| 68 | PR #574: recorded; #593: not recorded | yes |
| 69 | PR #574: undecided | yes |
| 70 | PR #574: recorded; #593: not recorded | yes |
| 71 | PR #574: undecided | yes |
| 82 | PR #574: not recorded → undecided (interval cannot prove equality) | yes |
| 83 | PR #574: undecided | yes |
| 84 | PR #574: recorded; #593: not recorded | yes |
| 85 | PR #574: not recorded → undecided (interval cannot prove equality) | yes |
| 86 | PR #574: recorded; #593: not recorded | yes |
| 87 | PR #574: undecided | yes |
| 88 | PR #574: recorded; #593: not recorded | yes |
| 89 | PR #574: not recorded → undecided (interval cannot prove equality) | yes |
| 101 | PR #574: not recorded → undecided (interval cannot prove equality) | yes |
| 102 | #529: not recorded; PR #574: recorded; #593: not recorded | yes |
| 103 | #573: not recorded; PR #574: recorded; #593: not recorded | yes |
| 104 | PR #574: not recorded → undecided (interval cannot prove equality) | yes |
| 105 | #568: recorded; PR #574: recorded; #593: not recorded | yes |
| 106 | PR #574: undecided; #593: not recorded | yes |
| 107 | PR #574: undecided | yes |
| 108 | #573: not recorded; PR #574: recorded; #593: not recorded | yes |
| 109 | PR #574: not recorded → undecided (interval cannot prove equality) | yes |
| 110 | PR #574: recorded; #593: not recorded | yes |
| 122 | PR #574: not recorded → undecided (interval cannot prove equality) | yes |
| 123 | PR #574: recorded; #593: not recorded | yes |
| 124 | PR #574: not recorded → undecided (interval cannot prove equality) | yes |
| 125 | PR #574: not recorded → undecided (interval cannot prove equality) | yes |
| 126 | PR #574: recorded; #593: not recorded | yes |
| 127 | #573: not recorded; PR #574: recorded; #593: not recorded | yes |
| 128 | PR #574: undecided | yes |
| 129 | #562: recorded; PR #574: recorded; #593: not recorded | yes |
| 130 | PR #574: recorded; #593: not recorded | yes |
| 131 | #573: not recorded; PR #574: recorded; #593: not recorded | yes |
| 132 | PR #574: recorded; #593: not recorded | yes |
| 145 | PR #574: not recorded → undecided (interval cannot prove equality) | yes |
| 146 | #566: recorded; PR #574: recorded; #593: not recorded | yes |
| 147 | PR #574: not recorded → undecided (interval cannot prove equality) | yes |
| 148 | PR #574: not recorded → undecided (interval cannot prove equality) | yes |
| 149 | PR #574: not recorded → undecided (interval cannot prove equality) | yes |
| 150 | PR #574: not recorded → undecided (interval cannot prove equality) | yes |
| 151 | PR #574: not recorded → undecided (interval cannot prove equality) | yes |
| 152 | PR #574: undecided; #593: not recorded | yes |
| 153 | #504 comment 6133737268: recorded; #573: recorded; PR #574: recorded; #593: not recorded | yes |
| 154 | #552: recorded; #570: recorded; #573: not recorded; #583: not recorded; #586: recorded; #593: not recorded | yes |
| 155 | #528: not recorded; PR #574: recorded; #593: not recorded | yes |
| 156 | #528: not recorded; #561: recorded; PR #574: recorded; #593: not recorded | yes |
| 170 | PR #574: not recorded → undecided (interval cannot prove equality) | yes |
| 171 | PR #574: not recorded | yes |
| 172 | PR #574: recorded; #593: not recorded | yes |
| 173 | PR #574: not recorded → undecided (interval cannot prove equality) | yes |
| 174 | PR #574: not recorded → undecided (interval cannot prove equality) | yes |
| 175 | #528: recorded; #573: not recorded; PR #574: recorded; #593: not recorded | yes |
| 176 | #561: recorded; #562: not recorded; franciscouzo/square-packing@93570ef: recorded; PR #574: recorded; #575: not recorded; #593: not recorded | yes |
| 177 | PR #574: undecided; #593: not recorded | yes |
| 178 | PR #574: undecided | yes |
| 179 | PR #574: recorded; #593: not recorded | yes |
| 180 | #573: not recorded; PR #574: recorded; #593: not recorded | yes |
| 181 | PR #574: recorded; #593: not recorded | yes |
| 182 | PR #574: recorded; #593: not recorded | yes |
| 197 | PR #574: not recorded → undecided (interval cannot prove equality) | yes |
| 198 | PR #574: not recorded | yes |
| 199 | PR #574: recorded; #593: not recorded | yes |
| 200 | PR #574: not recorded → undecided (interval cannot prove equality) | yes |
| 201 | PR #574: not recorded → undecided (interval cannot prove equality) | yes |
| 202 | PR #574: not recorded → undecided (interval cannot prove equality) | yes |
| 203 | PR #574: not recorded → undecided (interval cannot prove equality) | yes |
| 204 | #562: recorded; PR #574: recorded; #593: not recorded | yes |
| 205 | PR #574: undecided | yes |
| 206 | PR #574: recorded; #593: not recorded | yes |
| 207 | #503 comment 6133755143: recorded; #573: recorded; PR #574: recorded; #593: not recorded | yes |
| 208 | PR #574: recorded; #593: not recorded | yes |
| 209 | #573: not recorded; PR #574: recorded; #593: not recorded | yes |
| 210 | PR #574: recorded; #593: not recorded | yes |
| 211 | #528: not recorded; PR #574: recorded; #575: recorded; #583: recorded; #586: recorded; #593: not recorded | yes |
| 226 | PR #574: not recorded → undecided (interval cannot prove equality) | yes |
| 227 | PR #574: not recorded → undecided (interval cannot prove equality) | yes |
| 228 | PR #574: recorded; #593: not recorded | yes |
| 229 | PR #574: not recorded → undecided (interval cannot prove equality) | yes |
| 230 | PR #574: not recorded | yes |
| 231 | PR #574: not recorded → undecided (interval cannot prove equality) | yes |
| 232 | #528: recorded; PR #574: recorded; #593: not recorded | yes |
| 233 | PR #574: not recorded → undecided (interval cannot prove equality) | yes |
| 234 | PR #574: not recorded → undecided (interval cannot prove equality) | yes |
| 235 | PR #574: undecided | yes |
| 236 | #573: not recorded; PR #574: recorded; #593: not recorded | yes |
| 237 | #561: recorded; #573: not recorded; PR #574: recorded; #593: recorded | yes |
| 238 | PR #574: recorded; #593: not recorded | yes |
| 239 | PR #574: recorded; #593: not recorded | yes |
| 240 | PR #574: recorded; #593: not recorded | yes |
| 241 | PR #574: recorded; #575: recorded; #583: recorded; #586: recorded; #593: not recorded | yes |
| 257 | PR #574: not recorded → undecided (interval cannot prove equality) | yes |
| 258 | #573: not recorded; PR #574: recorded; #593: not recorded | yes |
| 259 | PR #574: recorded; #593: not recorded | yes |
| 260 | PR #574: not recorded → undecided (interval cannot prove equality) | yes |
| 261 | #567: recorded; PR #574: recorded; #593: not recorded | yes |
| 262 | PR #574: not recorded → undecided (interval cannot prove equality) | yes |
| 263 | #573: not recorded; PR #574: recorded; #593: not recorded | yes |
| 264 | #528: recorded; PR #574: recorded; #593: not recorded | yes |
| 265 | PR #574: not recorded → undecided (interval cannot prove equality) | yes |
| 266 | PR #574: recorded; #593: not recorded | yes |
| 267 | #573: not recorded; PR #574: recorded; #593: not recorded | yes |
| 268 | PR #574: recorded; #593: not recorded | yes |
| 269 | PR #574: recorded; #593: not recorded | yes |
| 270 | #573: not recorded; PR #574: recorded; #593: not recorded | yes |
| 271 | #561: recorded; PR #574: recorded; #593: not recorded | yes |
| 272 | #569: recorded; PR #574: recorded; #593: not recorded | yes |
| 273 | PR #574: recorded; #593: not recorded | yes |
| 290 | PR #574: not recorded → undecided (interval cannot prove equality) | yes |
| 291 | PR #574: not recorded → undecided (interval cannot prove equality) | yes |
| 292 | PR #574: recorded; #593: not recorded | yes |
| 293 | PR #574: not recorded | yes |
| 294 | PR #574: not recorded → undecided (interval cannot prove equality) | yes |
| 295 | PR #574: recorded; #593: not recorded | yes |
| 296 | PR #574: not recorded → undecided (interval cannot prove equality) | yes |
| 297 | PR #574: recorded; #593: not recorded | yes |
| 298 | PR #574: not recorded → undecided (interval cannot prove equality) | yes |
| 299 | PR #574: not recorded → undecided (interval cannot prove equality) | yes |
| 300 | PR #574: undecided | yes |
| 301 | PR #574: recorded; #593: not recorded | yes |
| 302 | #564: recorded; #573: not recorded; PR #574: recorded; #583: recorded; #593: not recorded | yes |
| 303 | #562: recorded; #573: not recorded; PR #574: recorded; #593: not recorded | yes |
| 304 | PR #574: recorded; #575: recorded; #593: not recorded | yes |
| 305 | PR #574: recorded; #593: not recorded | yes |
| 306 | #573: not recorded; PR #574: recorded; #593: not recorded | yes |
| 307 | PR #574: recorded; #593: not recorded | yes |
| 308 | PR #574: recorded; #593: not recorded | yes |
| 338 | #561: recorded | yes |
| 339 | #583: recorded; #584: recorded; #586: recorded | yes |
| 344 | #561: recorded; franciscouzo/square-packing@b85dee2: recorded | yes |
| 364 | #584: recorded | yes |
| 365 | #596: recorded | yes |
| 370 | #596: recorded | yes |
| 375 | #561: recorded; franciscouzo/square-packing@4596670: recorded; #584: recorded | yes |
| 376 | #561: recorded; franciscouzo/square-packing@4596670: recorded | yes |
| 378 | #561: recorded; franciscouzo/square-packing@b85dee2: recorded | yes |
| 379 | #570: recorded; #583: recorded; #586: recorded | yes |
| 380 | TheSnakeFang/squarepack-certs@e646c47: recorded; #583: recorded; #586: recorded | yes |
| 381 | TheSnakeFang/squarepack-certs@e646c47: recorded; #582: not recorded; #583: recorded; #589: not recorded | yes |
| 382 | TheSnakeFang/squarepack-certs@c284cd0: recorded; #583: recorded; #586: recorded | yes |
| 460 | #596: recorded | yes |

## Provenance samples

Audit of every lane-backed claim (280): `exact` equals the lane’s `exact_side` (or the
lane’s fraction `offered_side` for #573’s 13 and #593’s 72 rows), `printed` equals the
lane’s `offered_side`/`side_decimal` or the issue’s own table (#593: all 73 prints equal
the issue’s), `first_committed` equals the lane’s (with the N153/N302 correction),
`reported_at` is the issue, comment or PR creation, the later commit, the announcing
comment or the publication commit as the README states.
One discrepancy, m6 (#562/176’s print is the issue’s, not the README’s). Audit of the 26
transcribed claims against my own reads of the sources (`upstream/`, issue texts): all
identical except #593/51 (M2).

The 8 claims timed by an edit or a later commit:

| claim | ledger `reported_at` | evidence | agree |
| --- | --- | --- | --- |
| #564, 302 | 2026-10-12T22:17:00Z | comment 6133625109 created 22:17:00Z announces the refined certificate; GraphQL edit 22:16:43Z | yes (edit 17 s earlier; m3) |
| #566, 146 | 2026-10-12T23:41:41Z | comment 6134736610 created 23:41:41Z; edit 23:41:36Z | yes (m3) |
| #567, 261 | 2026-10-12T23:45:41Z | comment 6134779741 created 23:45:41Z; edit 23:45:35Z | yes (m3) |
| #575, 304 | 2026-10-13T04:13:31Z | comment 6138078023 created 04:13:31Z “added s(304) ≤ 17.929427758076”; edit 04:13:29Z; the n0304.sqcert first commit b909e1b 03:03:29Z | yes (m3) |
| PR #574, 153 | 2026-10-13T01:29:11Z | commit a006c4525 “bind exact N153 and N302 certificates” committed 01:29:11Z (lane: 00:29:11Z, a timezone slip) | yes |
| PR #574, 302 | 2026-10-13T01:29:11Z | same commit | yes |
| PR #574, 86 rational claims | 2026-10-13T00:24:05Z | commit 0ab26a794 “bind verified v2 certificate archives” 00:24:05Z, after the PR opened 00:13:11Z | yes (m9 for 51 of them) |
| PR #574, 60 algebraic claims | 2026-10-13T01:58:06Z | commit 48f063d84 “register the exact certificate archive” 01:58:06Z | yes |

Fifteen claims drawn at random (seed 20261014) from the 306:

| # | report, n | ledger: printed (rounding) / exact? / first_committed / reported_at | source read here | match |
| ---: | --- | --- | --- | --- |
| 1 | #593, 269 | 16.9015135821891320 (binary64) / yes / 2026-10-13T21:38:18Z / 2026-10-14T01:40:32Z | mishapolk lane claims.json at d4c198d0d + issue #593 table | exact==lane exact_side; printed==issue table; first_committed==lane; reported_at as expected |
| 2 | PR #574, 105 | 10.7893037837481588309… (up) / yes / 2026-10-13T00:24:05Z / 2026-10-13T00:24:05Z | pr574 lane claims.json at f817bf191 + PR commit dates | exact==lane exact_side; printed==lane offered_side; first_committed==lane; reported_at as expected |
| 3 | PR #574, 71 | 8.94407155757031550656… (up) / yes / 2026-10-13T00:24:05Z / 2026-10-13T00:24:05Z | pr574 lane claims.json at f817bf191 + PR commit dates | exact==lane exact_side; printed==lane offered_side; first_committed==lane; reported_at as expected |
| 4 | #593, 156 | 12.9791658538342762 (binary64) / yes / 2026-10-13T15:51:54Z / 2026-10-14T01:40:32Z | mishapolk lane claims.json at d4c198d0d + issue #593 table | exact==lane exact_side; printed==issue table; first_committed==lane; reported_at as expected |
| 5 | franciscouzo/square-packing@4596670, 375 | 19.893906534236 (up) / yes / 2026-10-13T13:53:57Z / 2026-10-13T13:53:57Z | couzo lane claims.json at f8ecf2173 + commit 4596670 date | exact==lane exact_side; printed==lane offered_side; first_committed==lane; reported_at as expected |
| 6 | #593, 209 | 14.9462232264464507 (binary64) / yes / 2026-10-14T01:24:10Z / 2026-10-14T01:40:32Z | mishapolk lane claims.json at d4c198d0d + issue #593 table | exact==lane exact_side; printed==issue table; first_committed==lane; reported_at as expected |
| 7 | PR #574, 265 | 16.7781745930520227684… (unstated) / no / 2026-10-13T01:58:06Z / 2026-10-13T01:58:06Z | pr574 lane algebraic-claims.json at f817bf191 + PR commit dates | printed==lane side_decimal; first_committed==lane; reported_at as expected |
| 8 | PR #574, 295 | 17.7042327907360303578… (up) / yes / 2026-10-13T00:24:05Z / 2026-10-13T00:24:05Z | pr574 lane claims.json at f817bf191 + PR commit dates | exact==lane exact_side; printed==lane offered_side; first_committed==lane; reported_at as expected |
| 9 | PR #574, 259 | 16.5913781454976981594… (up) / yes / 2026-10-13T00:24:05Z / 2026-10-13T00:24:05Z | pr574 lane claims.json at f817bf191 + PR commit dates | exact==lane exact_side; printed==lane offered_side; first_committed==lane; reported_at as expected |
| 10 | #593, 240 | 15.9696853375307803 (binary64) / yes / 2026-10-13T21:38:16Z / 2026-10-14T01:40:32Z | mishapolk lane claims.json at d4c198d0d + issue #593 table | exact==lane exact_side; printed==issue table; first_committed==lane; reported_at as expected |
| 11 | PR #574, 293 | 17.6341463414634146341… (up) / yes / 2026-10-13T00:24:05Z / 2026-10-13T00:24:05Z | pr574 lane claims.json at f817bf191 + PR commit dates | exact==lane exact_side; printed==lane offered_side; first_committed==lane; reported_at as expected |
| 12 | PR #574, 82 | 9.53553390593273762200… (unstated) / no / 2026-10-13T01:58:06Z / 2026-10-13T01:58:06Z | pr574 lane algebraic-claims.json at f817bf191 + PR commit dates | printed==lane side_decimal; first_committed==lane; reported_at as expected |
| 13 | #593, 68 | 8.7987952372182843 (binary64) / yes / 2026-10-13T21:38:13Z / 2026-10-14T01:40:32Z | mishapolk lane claims.json at d4c198d0d + issue #593 table | exact==lane exact_side; printed==issue table; first_committed==lane; reported_at as expected |
| 14 | PR #574, 239 | 15.9484433273004999050… (up) / yes / 2026-10-13T00:24:05Z / 2026-10-13T00:24:05Z | pr574 lane claims.json at f817bf191 + PR commit dates | exact==lane exact_side; printed==lane offered_side; first_committed==lane; reported_at as expected |
| 15 | #593, 86 | 9.8205354074967417 (binary64) / yes / 2026-10-13T16:39:57Z / 2026-10-14T01:40:32Z | mishapolk lane claims.json at d4c198d0d + issue #593 table | exact==lane exact_side; printed==issue table; first_committed==lane; reported_at as expected |

## Refinement and new-packing samples

| claim | mark in the ledger | what the cited source says | agrees |
| --- | --- | --- | --- |
| PR #574, 68 | refines T-118 (Couzo) | pr574 lane README: “At 73 counts the margin is padding … below a certificate of the same packing”; the submission says padding reductions “not 148 new nominal constructions” | yes |
| PR #574, 153 | refines T-148 (PingYou) | lane README: “N153 (degree 7) is 2.6e-12 below T-148’s ceiling … PingYou’s own constructions attained exactly” | yes |
| PR #574, 176 | refines #575 (Ostashev) | lane README: “a tighter copy of a newer packing that another open report holds … N176 (1.7e-2, Ostashev’s #575)” | yes; note #575 reached the repository after the PR’s claim (owner table) |
| #566, 146 | refines T-150 (Ryan Xu) | issue: “Ryan Xu: original layout. Robert Barnett: preceding refinement. PingYou Ltd: this further refinement”; lane measured it the same packing as T-150’s | yes |
| #568, 105 | refines T-130 (Ryan Xu) | issue: “exact contact refinement”, seeded from Couzo’s T-130 certificate; lane measured “the same packing” (no centre moved more than 1e-19) | yes |
| #569, 272 | refines T-151 (SQUISH) | issue: “Decode the pinned SQUISH centers … No … topology change is used” | yes |
| #504 comment, 153 | refines T-148 | comment: “A refined certificate for the same N153 construction” | yes |
| #528, 155/156/211 | refines T-149 (Ostashev’s own) | issue: “the same commit stores those three at the exact optima of their contact topologies … with the same arrangements” | yes |
| #586, 211/241 | refines #583 (Couzo’s own) | issue: “precision refinements at 211 and 241 … these tighter certificates continue the refinements reported in #583” | yes |
| #528, 175/232/264 | new packing | issue: “All three are new arrangements, not refinements of the previous packings” | yes |
| #562, 129/204/303 | new packing | issue: “204 and 303 are new arrangements. 129 … is a different local optimum, not a refinement of Xu’s” | yes |
| #575, 176/211/241/304 | new packing | issue: “All four are new arrangements. 211 updates our T-149 entry with a different packing” | yes |
| #552, 154 | new packing | issue: “a different local minimum from T-136’s packing” (RMS 0.319) | yes |
| #561, 156/176 | new packing, continuing Ostashev’s arrangement | couzo lane README “Credit and Licence”: “At 156 and 176 they are Daniil Ostashev’s arrangements, continued with the author’s basin hopping and refinement” | yes (the judgement call) |
| #561, 237 | new packing, continuing SQUISH’s arrangement (T-140) | lane README: “continued with the author’s basin hopping and Evan Daniel’s fq refinement”; but the issue’s own word is “237 is my refinement of SQUISH from #488” | the lane, yes; the issue calls it a refinement |
| #583/#586, 380/381/382 | new packing, continuing Kevin Fang’s published arrangement | #583: “continued Kevin Fang’s published arrangements through browser and native searches. Please retain his construction credit”; #586: “further browser fq refinements of Kevin Fang’s arrangements” | yes; the sources ask that Fang’s construction credit be retained |
| #584, 339/364/375; #596, 365/370/460 | new packing | issues: two-piece compositions, “new arrangements of known pieces, not new local structure” | yes |
| TheSnakeFang@e646c47, 380/381 | new packing | commit message “Direct packings for n = 380, 381, ...” | yes (a commit message is thin as a source) |
| #573, 153/207 | new packing | issue: “new arrangement discovered using basin hopping”; measured otherwise at 207 (M5) | the word, yes; the geometry, no |

The judgement call ("continued X’s arrangement" with search = a new packing that
continues X, not a refinement).
Against result-import.md Stage 3 and epistemics.md, a regularization is “a certificate
that rearranges a packing the record already credits, for display or after solving it to
an exact side”: the same packing, tightened.
A continued search that lowers the side by 1e-6 to 1e-2 (156: 6.8e-6; 176: 1.0e-3; 380:
1.5e-2) is a different local optimum seeded from X, so calling it a new packing that
continues X, with the lineage carried in `continues`, is the right default and matches
“the source says who did what” (the credit line becomes “Couzo after Fang”). Two
caveats.
First, where the source’s own word is “refinement” (#561 at 237, #586 at 380/382
“further refinements”, and #583’s “please retain his construction credit”), the mark
overrides the source’s word, which the ledger’s contract says it must not; the mark
should quote the word and let the register decide between `regularizations` and
`builds_on`. Second, the distinction is measurable (the lanes measured it for PingYou’s
refinements), and the policy’s `identity.basis:
measured` exists for exactly this; a continued packing whose squares all lie within 1e-3
of the seed (as #573’s 207 does of T-147) is a refinement whatever the author called it.

## Code quality for a records reviewer

- Error paths: no silent claim loss in the walk; `_entries` lists unknown-time claims;
  `git_show` and `gather` raise.
  The silent paths are `_selected` (m4) and `lowered` (M4).
- Determinism: `walk`’s sort key is total; rendering writes no timestamps; `json.dumps`
  and `yaml.safe_dump` orders are fixed; `render --check` is a byte comparison of both
  rendered files. Nondeterminism enters only through the tree (M3) and the network
  (`gather` without `--snapshot`).
- The `render --check` drift contract compares against the tree, not against
  `read_at_main` (M3); the README’s provenance sentence is true only by coincidence of
  the branch and its merge base.
- `_difference` prints distances from `value`, the print’s value for a printed side, so
  a “below by” against a printed side is approximate; fine for display, and every “by”
  in the owner tables I checked (153: 1.57e-14; 207: 2.42e-12; 51: 7.69e-20 in my
  computation) is right.

## Questions for the owner

1. Should the standing side at a count be the stronger of the case’s two lanes (M1)? At
   11 that makes PR #574’s certificate “not recorded” against the proved optimum.
2. May the ledger decide closed forms with `sqrt` by interval arithmetic and read an
   exact side a lane README states from a pinned certificate (M2)? That settles #593 at
   51\.
3. Do #573’s 153 and 207 enter as Mishapolk’s new packings, on the author’s word, or as
   refinements of PingYou’s T-148 and T-147, on the measurement (M5)? The same question,
   in the other direction, for #561’s 237 and #586’s 380/382, whose authors say
   “refinement” and whose ledger mark is “new packing”.
4. For a claim added or replaced by an edit, is the report’s time at the count the
   issue’s creation (the original, weaker claim) or the edit (m3)?
5. Should the directory freeze the starts it was decided against (M3), so that the
   record of this intake survives the merge that acts on it?
6. Is a commit message ("Direct packings for n = 380, 381, ...") enough of a source for
   a `new_packing` mark on a publication no issue reports?

## Tree state at hand-off

The checkout moved under this review: the reflog shows commits and merges by another
session from 10:05Z (b55524607, cb1ece1e9, c5ed6c3a6, 9f1aa645c), and at hand-off HEAD
is 9f1aa645c with a merge of a87dec6ef in progress (`.git/MERGE_HEAD`; `UU` conflicts in
`packing/resources/README.md` and `packing/resources/bibliography.yaml`). This review
ran only read-only git commands (`show`, `cat-file`, `ls-tree`, `diff --stat`, `log`,
`merge-base`, `branch`, `rev-parse`, `status`, `reflog`) and wrote only under its
scratch directory. The reviewed files are identical between 1dc253e5e and HEAD and
unmodified in the working tree, and `packing/frontier/` at HEAD still equals main
f73e9de13, so every statement above stands at both commits.

## Addendum: what the fix round changed

Written by the coordinator’s writer for session squares-43 on 2026-10-14, after this
review. The review above is the reviewer’s text as the repository’s Markdown formatter
reflows it, with straight quotes and three-dot ellipses retyped.
Its programs, with the outputs that need pinned bytes, are in
[`packing/campaign/issue-intake/upper-bounds-20261014/review/`](../../../packing/campaign/issue-intake/upper-bounds-20261014/review/README.md),
whose README says what each one reads.
The “scratch README” this review cites is that README’s source.

Fixed:

- **M1.** The start at n ≤ 324 is the set of both upper lanes of the case record, and
  the walk is seeded with every member.
  A lane is its exact form where that is rational, a rigorous interval where it has
  square roots, an enclosure by exact sign change where it is `root(...)` with the
  case’s minimal polynomial, and otherwise its print within one unit.
  Two lanes with one span are one member.
  Frozen lane relations name their lane, and each applies only while that lane still
  reads the frozen value and form.
- **M2.** Closed forms with `sqrt` are evaluated as 90-digit `mpmath` intervals, with
  endpoints converted to rationals exactly.
  #593’s exact side at 51, `7690355937288491748079718099723/10^30`, is filled from
  `certificates/n51.cert` at Mishapolk/square-packing-records@46f638c, as the mishapolk
  lane’s README at d4c198d0d states it.
- **M3.** `gather` freezes every count’s start in `starts.yaml` (format
  `intake-ledger-starts-v1`), keyed to `read_at_main` f73e9de13, with both lanes, the
  pending-adoption bounds and the beyond-horizon rows.
  It refuses to write one while `packing/frontier/` differs from that commit.
  `render` and `render --check` read only the snapshot and refuse one keyed to another
  commit. `check --tree` reports the counts where today’s tree would give another start,
  and gates nothing; at 7c672f5be it reports 0.
- **M4.** `lowered` is gone.
  The start keeps every member that nothing else in it is decidably below (`minimal`).
  The case from `bug_demos.py` is a test.
- **M5 and m8.** A claim may carry a measured-identity note.
  #573’s 153 and 207 carry this review’s measurements, and the ledger’s README lists
  both under “Measured Identity Against the Source’s Word” as an owner decision.
  #593’s 103, 153, 207 and 258 are marked as restating #573’s bytes.
- **m1.** `compare` reads a frozen relation in both argument orders.
- **m4.** `gather` refuses a lane row that no report takes and that is not named in a
  `not_ours` list.
- **m5.** The cross-check warnings are kept in `ledger.yaml` and `ledger.json`, and the
  ledger’s README shows them under “Lane Cross-Check” (15 warnings).
- **m7.** `nearest` spans half a unit.

Also changed at the coordinator’s request: `ledger.json` is written in the retained-JSON
layout; the input holds a list of key-reason candidates, rendered beside the rule’s
verdict and under Owner Decisions, with one entry, #529 at 102 (layer 6,
jlevy/squares#598 at bd2ae5869, registers it as T-159, an S2 entry that moves no case;
the rule’s verdict stays “not recorded, above T-146 by 2.43e-11”); and Fang’s exact
sides at 380, 381 and 382 come from
`packing/resources/web/fang-direct-certificates-2026-10-13/acquisition/claims.json` at
`main` 7c672f5be.

Left as notes: m2 (the `binary64` span is an empirical envelope, not a bound), m3
(claims added by an edit are dated by the announcing comment), m6 (#562’s 176) and m9
(PR #574’s times for its 51 retained v1 certificates).

Two verdicts changed, and both are the review’s:

| n | Report | Before | After |
| ---: | --- | --- | --- |
| 11 | PR #574 | undecided (record T-011) | not recorded: above the verified lane, the root of `P_trump11`, by at least 1.71e-95 (M1) |
| 51 | #593 | undecided (record T-126) | not recorded: above record T-126, `(16+5*sqrt(2))/3`, by at least 7.69e-20 (M2) |

The counts are now 128 recorded (46 new packings, of which 24 continue an arrangement;
76 refinements; 6 unclassified), 0 by exception, 157 not recorded and 21 undecided,
against 155 and 23 before.
Another 115 steps keep their verdicts and change only in what they show: the members
decided against, what would decide them, the separation, or a restates, measured,
key-reason or packing mark.

`recompute.py` was run again against the new ledger (`review/recompute-rerun.txt`): 306
steps, 305 agree, and 51 now agrees.
The one disagreement is 11. The program’s walk has a 2.0e-90 enclosure of the root and
leaves it undecided, while its own exact sign test puts PR #574’s side above the root,
which is the ledger’s verdict now.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
