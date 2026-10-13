# Plan: A Kind for Every Registered Result

**Date:** 2026-10-01

**Author:** Claude (agent), for the repository owner

**Status:** Implemented and merged in PR #270 at `7f1ad844e`. The ten medium-confidence
classifications and standing derivation remain owner decisions, listed under
`think-cv22`.

**Workflow:** W7 pipeline improvement

**Beads:** `think-69j0`

## Summary

The results register holds 61 results, and they are not all the same sort of thing.
Most are lower bounds on $s(n)$. Some are upper bounds, some settle an exact value, and
a few are neither: a rigidity proof, the exclusion of one branch of a case analysis, an
erratum to a published lemma.
Until now the record had one label for a result whose evidence claims no bound.
Its standing read “not a bound”, which says what the result is not.

The owner asked for every result to be classified by what it is, starting from four
kinds: lower bound, upper bound, optimality and simplification.
This plan proposes ten kinds, the owner’s four and six more, and assigns one to each of
the 61 results. Each result carries its kind in a required `kind` field, the checker
cross-checks the field against the claim and the evidence where it can, and every view
shows the kind, with a standing only where the result is a bound.

## The Vocabulary

Each kind is named for what a result of that kind establishes.
The first four are the owner’s.

| Kind | Stored as | A result of this kind | Results |
| --- | --- | --- | ---: |
| lower bound | `lower-bound` | proves $s(n) \ge v$ or $s(n) > v$: no packing of $n$ unit squares fits in a smaller square | 37 |
| upper bound | `upper-bound` | proves $s(n) \le v$ by a packing of $n$ unit squares in a square of side $v$ | 4 |
| optimality | `optimality` | settles an exact value $s(n) = v$: a lower bound that meets an upper bound | 6 |
| simplification | `simplification` | proves again a result the record already holds, by a shorter, cleaner or more elementary route, and moves no bound | 2 |
| rigidity | `rigidity` | says whether one named packing can move at fixed side: its flexes, its rigidity at first or second order, the isolation of its pose | 3 |
| case exclusion | `case-exclusion` | shows that one named class of configurations (a branch, a corner class, a region of pose space) holds no packing at a stated side, and moves no bound by itself | 3 |
| restricted optimality | `restricted-optimality` | finds the best packing within a declared family, such as fixed orientation classes near one pose, and says nothing about $s(n)$ outside it | 1 |
| method limit | `method-limit` | says how far one proof method or construction can reach: a ceiling on what a point set or a certificate format can certify | 2 |
| correction | `correction` | shows that a published statement is false as printed, and gives the corrected statement that holds | 1 |
| audit | `audit` | checks an existing proof or certificate independently and finds it correct as published | 2 |

The field is named `kind`. No result-level field had that name; a review record inside a
result has its own `kind` (adversarial, oversight and so on), which is a different
object and is untouched.

## How One Kind Is Chosen

Every result gets exactly one kind.
Three rules settle the cases where two kinds fit.

1. **The kind is what the claim concludes.** Where a claim ends in a bound or a value of
   $s(n)$, the kind is that bound, however it was reached: by a repaired proof (T-010),
   by an exact check of a published packing (T-011), or by monotonicity from another
   result (T-002, T-016).
2. **A lower bound that meets a known upper bound is optimality.** The claim states the
   value, so the kind does.
   T-051 is a cover that proves $s(32) \ge 6$, and the grid gives $s(32) \le 6$; the
   result is $s(32) = 6$.
3. **A second proof of a value the record holds is a simplification, not a second
   optimality.** What such a result adds is the route.
   Its claim names the result it proves again.

One field is enough.
No result needed a secondary kind once these rules were applied: the claim text carries
the second reading where there is one (T-006, below).

## The Classification

The claim column is each result’s headline.
Confidence is high where the kind follows from the claim’s own relation or wording, and
medium where another kind was a reasonable choice; those ten are discussed in the next
section.

| id | n | claim | kind | why | confidence |
| --- | --- | --- | --- | --- | --- |
| T-001 | 17 | $s(17) \ge \frac{4426213}{1000000} = 4.426213$, from a sixteen-point unavoidable set | lower bound | the claim concludes $s(17) \ge$ | high |
| T-002 | 18 | `s(18) ≥ 4426213/1000000`, by monotonicity from T-001 | lower bound | T-001 carried to 18 by monotonicity | high |
| T-003 | 17, 18 | The sixteen-point set’s unavoidability ceiling lies in $[\frac{4426213}{1000000}, \frac{4427}{1000})$ | method limit | brackets what one point set can certify; its lower end is T-001 | medium |
| T-004 | 46 | Bentz 2010, Theorem 8 ($s(46) \ge 7$) is correct as printed, machine-audited in full | audit | the claim is that a printed proof is correct; T-008 carries the value | medium |
| T-005 | 13 | Bentz 2010, Lemma 10 is false as printed and true as corrected to $(1.74, 1)$ | correction | a printed lemma is false, and the corrected one is certified | high |
| T-006 | 13 | $s(13) = 4$ | optimality | an exact value; the case-free second proof is in the same entry | high |
| T-007 | 4–100 | $s(n) \ge \min(\lceil\sqrt{n}\rceil, \sqrt{n - 2\lfloor\sqrt{n}\rfloor + 1} + 1)$ for $4 \le n \le 100$ | lower bound | Nagamochi’s closed-form family | high |
| T-008 | 46 | $s(46) = 7$ | optimality | the audited lower half meets the grid | high |
| T-009 | 29 | $s(29) \le 5.933833\ldots$, by a Krawczyk interval certificate | upper bound | a packing, interval-certified | high |
| T-010 | 11 | $s(11) \ge 2 + 4/\sqrt{5}$, by a repair of Stromquist 2003’s Figure 14 point set | lower bound | the claim concludes the bound; the repair is how it is proved | medium |
| T-011 | 11 | Trump’s 1979 packing is exactly valid, so $s(11) \le 3.877083590022814\ldots$ | upper bound | the claim concludes $s(11) \le$; the exact check is how | medium |
| T-012 | 5 | Goebel’s $n = 5$ packing is second-order rigid at fixed side | rigidity | second-order rigidity of one packing | high |
| T-013 | 40 | Goebel’s $n = 40$ packing: seven verified first-order flexes, each refused at second order | rigidity | first-order flexes, each refused at second order | high |
| T-014 | 5 | Goebel’s $n = 5$ optimum is rigid at fixed side: its pose is an isolated feasible point | rigidity | the pose is an isolated feasible point | high |
| T-015 | 17 | $s(17) \ge \frac{22529}{5000} = 4.5058$ | lower bound | a published certificate, replayed | high |
| T-016 | 18, 19 | `s(n) ≥ 22529/5000` for $n = 18, 19$, by monotonicity from T-015 | lower bound | T-015 carried to 18 and 19 by monotonicity | high |
| T-017 | 12 | $s(12) \ge \frac{99}{25} = 3.96$ | lower bound | a fractional certificate | high |
| T-018 | 11 | $s(11) \ge \frac{381}{100} = 3.81$ | lower bound | a fractional certificate | high |
| T-019 | 17, 18, 19 | $s(n) \ge \frac{459}{100} = 4.59$ for $n = 17, 18, 19$ | lower bound | one certificate, three counts | high |
| T-020 | 19, 20, 21 | $s(n) \ge \frac{24}{5} = 4.80$ for $n = 19, 20, 21$ | lower bound | one certificate, three counts | high |
| T-021 | 20, 21 | $s(n) \ge \frac{97}{20} = 4.85$ for $n = 20, 21$ | lower bound | one certificate, two counts | high |
| T-022 | 11 | $s(11) \ge 38100\sqrt{8100042893309449}/899996306539 = 3.8100257\ldots$ | lower bound | a dilation-limit corollary of T-018 | high |
| T-023 | 11 | Conditional exclusion: no eleven-square packing in the four-owner branch at $q = \frac{96}{25}$ | case exclusion | one four-owner branch holds no packing; no bound moves | high |
| T-024 | 11 | $s(11) \ge 3175000\sqrt{518400042893309449}/598960960743657 = 3.8166095\ldots$ | lower bound | a dilation-limit corollary on a finer net | high |
| T-025 | 11 | $s(11) \ge \frac{191}{50} = 3.82$, by a threshold certificate | lower bound | a threshold certificate | high |
| T-026 | 11 | $s(11) \ge 955000\sqrt{518400042893309449}/179696714646249 = 3.8264474\ldots$ | lower bound | a dilation-limit corollary of T-025 | high |
| T-027 | 18 | $s(18) \ge \frac{467}{100} = 4.67$ | lower bound | a fractional certificate | high |
| T-028 | 18 | $s(18) \ge \frac{187}{40} = 4.675$ | lower bound | a fractional certificate | high |
| T-029 | 18 | $s(18) \ge \frac{1871}{400} = 4.6775$ | lower bound | a fractional certificate | high |
| T-030 | 18 | $s(18) \ge \frac{4679}{1000} = 4.679$ | lower bound | a fractional certificate | high |
| T-031 | 11 | The octagon corner class (threshold $\frac{1}{2}$) holds no eleven-square packing at side $\frac{96}{25}$ | case exclusion | one corner class holds no packing at $\frac{96}{25}$; no bound moves | high |
| T-032 | 17 | $s(17) \ge \frac{461300}{99999} = 4.61304613\ldots$, and beneath it Mira’s $s(17) \ge \frac{4613}{1000}$ | lower bound | two published certificates, replayed | high |
| T-033 | 11 | $s(11) \ge 955000\sqrt{2073600042893309449}/359341754646249 = 3.8269975\ldots$ | lower bound | a dilation-limit corollary on the 2880-step net | high |
| T-034 | 21 | $s(21) \ge \frac{122}{25} = 4.88$ | lower bound | a fractional certificate | high |
| T-035 | 11 | Six-plus-five packings near Trump’s tilt with side $\le U_{hi}$ lie within `rho` of his pose | case exclusion | excludes the family’s small packings away from Trump’s pose | medium |
| T-036 | 11 | Trump’s pose is optimal among six-plus-five packings near its tilt, unique up to symmetry | restricted optimality | best within one orientation family; says nothing about $s(11)$ | medium |
| T-037 | 11 | $s(11) > \frac{31}{8} = 3.875$ | lower bound | a published certificate, replayed | high |
| T-038 | 17 | $s(17) > \frac{461300}{99853} = 4.6197910929\ldots$ | lower bound | a published certificate, replayed | high |
| T-039 | 17 | $s(17) > \frac{231001}{50000} = 4.62002$ | lower bound | a published certificate, replayed | high |
| T-040 | 17 | $s(17) > \frac{232001}{50000} = 4.64002$ | lower bound | a published certificate, replayed | high |
| T-041 | 17 | $s(17) > \frac{466001}{100000} = 4.66001$ | lower bound | a published certificate, replayed | high |
| T-042 | 17 | $s(17) > \frac{233009}{50000} = 4.66018$ | lower bound | a published certificate, replayed; never held the case | high |
| T-043 | 17 | $s(17) > \frac{116511}{25000} = 4.66044$ | lower bound | a published certificate, replayed | high |
| T-044 | 26–72 (14 counts) | Weighted point lower bounds for ten counts in $n = 26\ldots72$, plus four from the same files | lower bound | fourteen bounds from ten published certificates | high |
| T-045 | 27, 28, 31, 32 | $s(27), s(28) \ge \frac{28}{5}$, $s(31) \ge \frac{148}{25}$ and $s(32) \ge \frac{119}{20}$ | lower bound | three published certificates, replayed | high |
| T-046 | 18–95 (48 counts) | Rectangle-density lower bounds reported for 48 counts in $n = 18\ldots95$ | lower bound | 48 reported bounds, not yet replayed | high |
| T-047 | 11, 26, 27, 28, 29, 30, 31 | $s(11) \ge \frac{381}{100}$; $s(n) \ge \frac{1377}{250}$ for $n = 26\ldots28$; $s(n) \ge \frac{571}{100}$ for $n = 29\ldots31$ | lower bound | three published certificates, replayed | high |
| T-048 | 50 | $s(50) \ge \frac{37}{5} = 7.4$, reported | lower bound | a reported bound, not yet replayed | high |
| T-049 | 12 | $s(12) \ge \frac{15680}{3951} = 3.9686155\ldots$ | lower bound | a published certificate, replayed | high |
| T-050 | 21 | $s(21) \ge \frac{5000}{1001} = 4.995004995\ldots$ | lower bound | a published certificate, replayed | high |
| T-051 | 32 | $s(32) = 6$ | optimality | a closed cover at the grid side meets the grid | high |
| T-052 | 21 | $s(21) = 5$, by a mixed cover of points and grid-line segments | optimality | a mixed cover at the grid side meets the grid | high |
| T-053 | 45 | $s(45) = 7$, by a mixed cover of points and grid-line segments | optimality | a mixed cover at the grid side meets the grid | high |
| T-054 | 45 | $s(45) = 7$ by a second, point-only route | simplification | re-proves T-053’s value with points alone | medium |
| T-055 | 21 | $s(21) = 5$ by a point-only route, reported | simplification | re-proves T-052’s value with points alone, at a positive margin | medium |
| T-056 | 68–307 (49 counts) | Smaller packings for 49 counts from $n = 68$ to $307$, each certified two independent ways | upper bound | 49 packings, each certified | high |
| T-057 | 211 | $s(211) \le 14.99796070496771500150 < 15$, the first packing of 211 squares below the grid on record | upper bound | a packing below the grid | high |
| T-058 | 1–100 | Reported `B·UB(n)` rectangle-certificate ceiling has unresolved premises | method limit | a claimed ceiling on one certificate format; premises disputed | medium |
| T-059 | 11 | Reported equality of 12028 n11 row minima awaits a complete bound replay | audit | a second checker reproduces T-037’s row minima; no new bound | medium |
| T-060 | 11 | Trump’s eleven-square packing is globally optimal | optimality | the exact value of $s(11)$ | high |
| T-061 | 11 | $s(11) > \frac{3875000000}{999999999} = 3.875000003875\ldots$, 3.9e-9 above $\frac{31}{8}$ | lower bound | a published certificate, replayed | high |

Counts: 37 lower bounds, 6 optimality results, 4 upper bounds, 3 rigidity results, 3
case exclusions, 2 simplifications, 2 method limits, 2 audits, 1 correction and 1
restricted optimality.

## Where the Choice Was Not Obvious

- **T-054 and T-055: simplification or optimality.** Both claim an exact value,
  $s(45) = 7$ and $s(21) = 5$, that T-053 and T-052 already hold, and both sources say
  so and claim no priority.
  What they add is a certificate in a narrower language: weighted points alone, where
  the first proofs needed mass on grid-line segments, and for T-055 a positive margin
  where the first proof had none.
  They are proposed as simplifications.
  The alternative is to call them optimality and let the derived standing, *second
  certificate*, carry the rest.
  The weakness of the proposal is that “simpler” is a judgment and “second” is a fact; a
  second route that is different without being simpler would need the same kind or a new
  one.
- **T-006: one entry, two things.** The entry is $s(13) = 4$, Bentz’s theorem of 2010,
  and it also records Evan Daniel’s proof of the same value without a case analysis,
  checked in Lean. The value is primary, so the kind is optimality.
  The second proof is a simplification that has no entry of its own.
  Splitting the entry is outside this change.
- **T-004: audit or lower bound.** The claim is that Bentz’s printed proof of
  $s(46) \ge 7$ is correct, and T-008 carries the value $s(46) = 7$ built on it.
  By rule 1 the kind is audit, since the conclusion is about the proof.
  The alternative reading is that the entry is Bentz’s lower bound, with the audit
  recorded by its `V` and `C` rungs as it is for every other replayed result by others.
- **T-011: upper bound or audit.** The claim is that Trump’s 1979 packing is exactly
  valid, “so $s(11) \le$ that side”.
  The conclusion is a bound, so the kind is upper bound.
  T-004 and T-011 are close, and the owner may prefer to treat them alike.
- **T-010: lower bound or correction.** Stromquist’s printed argument for
  $s(11) \ge 2 + 4/\sqrt{5}$ does not close, and this result proves the bound with a
  repaired point set. The claim concludes the bound, so it is a lower bound.
  T-005 is the correction proper: its claim is that a printed lemma is false.
- **T-003 and T-058: method limit.** T-003 brackets the largest side one sixteen-point
  set can certify; its lower end is T-001’s bound and its upper end is an escaping pose.
  T-058 is a source’s claim that rectangle certificates with one core side cannot pass a
  stated side. Neither bounds $s(n)$. T-058 is reported and disputed, and its kind says
  what is claimed, as a reported lower bound’s does.
- **T-035: case exclusion or a reduction.** It shows that every small packing in one
  orientation family lies near Trump’s pose, which excludes the rest of that family’s
  pose space. It is proposed as a case exclusion, the kind read broadly.
  A separate kind for reductions would hold this one entry.
- **T-036: restricted optimality.** It proves that Trump’s pose is the best packing in
  one orientation family, with the equality case.
  It is not optimality, because it says nothing about $s(11)$, and calling it a case
  exclusion would hide what it concludes.
  It is the only result of its kind.
- **T-059: audit.** A source reports that its own checker reproduces every row minimum
  of the certificate behind T-037. It proves no bound and is not a second proof of the
  theorem, so it is an audit of a certificate, as T-004 is of a printed proof.

## What the Checker Derives and What It Takes on Declaration

`devtools.check_results` requires the field and its vocabulary, as the schema does, and
cross-checks the declared kind against three things the record already holds.

| Source | What it settles |
| --- | --- |
| The headline’s opening relation | A headline that opens with a relation on $s(n)$ states its kind: `≥` or `>` is a lower bound, `≤` or `<` an upper bound and `=` optimality; only a simplification may open with one under another kind. 44 of the 61 headlines open this way |
| The relations written elsewhere | A bound’s headline writes no relation of the other direction, and its claim writes one of its own if it writes any. An optimality result writes $s(n) = v$. A rigidity, a case exclusion and a restricted optimality write no relation on $s(n)$ in their headline |
| The cited evidence’s `claim` | A lower bound cites lower-bound evidence, an upper bound upper-bound evidence, and optimality an exact value or both halves. A rigidity, a case exclusion and a restricted optimality cite `derived-structure` evidence |
| The results the claim names | A simplification’s claim names a registered result that shares one of its cases |

Method limit, correction and audit are declared and reviewed, not derived: nothing in
the record distinguishes them from each other.
The checker’s tuple, the schema’s enum and the table in `epistemics.md` are held to the
same list by a test.

## What Replaces “Not a Bound”

A result’s standing is derived from the case records: *current best*, *superseded*,
*second certificate*. It is a statement about bounds.
Nine results cite no bound evidence, and their standing read “not a bound” on the site
and a dash in `RESULTS.md`: T-012, T-013, T-014, T-023, T-031, T-035, T-036, T-058 and
T-059. They now have no standing, and every view shows their kind instead: rigidity,
case exclusion, restricted optimality, method limit or audit.

Every view shows the kind of every result.
`RESULTS.md` has a kind column in both tables, and a dash in the standing column of a
result that has no standing.
On the site every row of both result tables draws its kind as a chip under its rungs,
above any standing chip, the result popover’s head and each step of its chain show it
beside the rungs, and the filter bar has a Kind select beside Standing.

## Decisions for the Owner

1. **The vocabulary.** Ten kinds, with one result each in `correction` and
   `restricted-optimality`. Merging `correction` into `audit` would give nine; the
   proposal keeps them apart because an erratum tells a reader that a printed statement
   is wrong.
2. **Simplification.** Whether T-054 and T-055 are simplifications, as proposed, or
   optimality results whose standing says they are second certificates; and whether a
   second route that is not simpler should share the kind.
3. **Audits of published work.** Whether T-004 is an audit, as proposed, or Bentz’s
   lower bound; and whether T-011 should follow it.
4. **T-035.** Case exclusion read broadly, as proposed, or a kind of its own.
5. **Which results have a standing.** Standing is still derived from the evidence an
   entry cites, so five results whose kind is no bound keep one: T-003 (method limit)
   reads *superseded*, T-004 (audit) and T-005 (correction) *current best*, and T-054
   and T-055 (simplification) *second certificate*. Deriving it from the kind instead
   would leave those five with their kind alone, as the nine above are, and no result
   would then be a second certificate while the two second proofs are simplifications.
   The derivation is unchanged here.

## What Is Left for the Site

The result tables, the result popover and the filter bar show the kind.
The case pages list each case’s results with their rungs and no kind chip; that list was
not changed.

## References

- [`results.yaml`](../../../../packing/frontier/results.yaml) and its
  [schema](../../../../packing/frontier/results.schema.yaml)
- [`epistemics.md`](../../../../epistemics.md), Result Kinds
- [`check_results.py`](../../../../packing/devtools/check_results.py)
- [Plan: others’ results in the register](../active/plan-2026-09-29-third-party-results-register.md)

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
