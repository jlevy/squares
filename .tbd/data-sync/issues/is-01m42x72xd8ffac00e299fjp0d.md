---
type: is
id: is-01m42x72xd8ffac00e299fjp0d
title: Adopt significance rules (a)-(d) in epistemics.md and rescore the register
kind: task
status: open
priority: 2
version: 3
labels: []
dependencies:
  - type: blocks
    target: is-01m42x73fcj164z21qmgmgbdyc
parent_id: is-01m42sq026mszrdm4fwf5r8g8y
created_at: 2026-10-04T07:31:52.365Z
updated_at: 2026-10-04T07:32:05.187Z
---
Owner decision 2026-10-04: adopt all four proposed rules from the think-3evx review — (a) families, (b) longstanding and much-attempted lift, (c) central-case rungs, (d) corrections/re-proofs/routine consequences — into epistemics.md (Significance and Novelty), fix the site's S4 short form (overview_sections.py RUNG_SHORT_MEANINGS: 'resolved disputed value'), then rescore per the review's table: T-064 S4->S5; T-084, T-086, T-085, T-083, T-007 S3->S4; T-053 S4->S3; T-019, T-020 S4->S3; T-002, T-016 S3->S1; T-011 S2->S3; T-022, T-024, T-026 S5->S4; T-081 stays S4 with history rationale; T-060 rationale records history. Also test T-006, T-008, T-049 against rule (b). Rescoring confirmed scores goes through an independent review lane (widen think-qh3s or do it here with by naming that review). Review text: think-3evx notes (scratchpad significance-review.md).

## Notes

# Significance Consistency Review

Bead `think-3evx`, 2026-10-04. Read-only on the repository.

**Sources.** The register is read from `origin/claude/ecstatic-archimedes-62hj6a` at
`f60987ea8` (PR #305), compared with `origin/main` at `e5a48b310`. They differ in
significance only by T-083 to T-087, which are new, and by rationale text on T-007,
T-048, T-069, T-070, T-074, T-076 and T-080. No score differs.
PR #305 does not change `epistemics.md`, and its edits to `packing/frontier/README.md`
and `results.schema.yaml` leave the significance lines as they were.
History comes from `packing/resources/` (DS7, Nagamochi 2005, Kingbird,
`bibliography.yaml`), the case records `packing/frontier/n-*.md` and the reviews under
`docs/project/reviews/`.

## Answer in Brief

- **T-064, `s(k²−3) = k` for every k ≥ 6, should be S5.** The literal anchors give it
  S4, but the history factor lifts it.
  The family had been open since at least 2000, and its members were proved one or two
  at a time (Stromquist 1984, Kearney–Shiu 2002, Bentz 2010 and 2016), with none at k ≥
  8 before October 2026.
- **T-081, `s(k²−4) = k`, should stay S4, with a new reason.** It has T-064’s claim
  shape but not its history: the archive holds one attempt dated before 2026 on a member
  with k ≥ 5, and its first members fell, mostly to the same author, the week before.
- **No re-proof or refutation reaches S5, but four S3s should be S4:** the restored
  families T-084 and T-086, the refutation T-085, and the general floor T-083.
- **T-053 should come down to S3**, to match T-062, T-066 and T-067.
- **The sharpest inconsistency** is a 2.6 × 10⁻⁵ rung at n = 11 (T-022, S5) outranking a
  theorem that settles a family worked on since 1984 (T-064, S4). Several older pairs
  are also out of line (§4).

## 1. The Rubric

`epistemics.md`, *Significance and Novelty*, verbatim:

> Significance is recorded as a score, rationale, date, and scorer.
> The score guides reading order and never changes validation behavior.

| Score | Anchor |
| --- | --- |
| `S1` | Bookkeeping or a routine consequence |
| `S2` | A citable detail that changes no theorem |
| `S3` | A substantive case result or machine audit |
| `S4` | A reusable technique, bound family, or resolved disputed value |
| `S5` | Movement on a central open case or broad external adoption |

> The `scored` field dates the current assessment; Git retains earlier values.
>
> Three rules govern scoring:
>
> - **The score is of the claim.** It says what the result establishes if it is correct;
>   `V` and `C` say whether it is.
>   A reported result and a confirmed one take the same score.
> - **The registering lane drafts and the reviewing lane confirms.** A score set when a
>   result is registered is a draft, and `by` says so.
>   The lane that reviews the result’s mathematics compares it with the entries nearest
>   to it, keeps or changes it, and `by` then names that review.
> - **A score follows the claim, not the frontier.** It is revisited when the entry’s
>   claim or scope changes.
>   A later result that supersedes the entry does not lower it.

The same section’s classification table says “Dated judgment; never gating”.
The schema says “S is a judged, anchored, dated score that never gates”, and the
frontier README says “`significance` is a `score` from 1 to 5 against the rubric, a
`rationale`, the date `scored`, and `by`; it never gates.”

**Ties to evidence and scope.** Rule 1 explicitly decouples S from V and C. No rule ties
S to scope, to the result kind, to authorship or to novelty, and none defines “central”
or “family”.

**What S does drive**, without gating validation:

- the reading order of the synopsis headline block and the pull-request presentation
  (`conventions.md`, “A registered result is presented”);
- the Stage 6 paper obligation in `packing/campaign/result-import.md`: “Write one when a
  result is confirmed and is scored `S5`, or is scored `S4` with a proof that cannot be
  followed from its source alone”.
  **Raising T-064, which is at V3/C3, to S5 creates that obligation.**

**Drift found.** The site’s short form in `packing/devtools/overview_sections.py`
(`RUNG_SHORT_MEANINGS`) renders S4 as “settled value”, not “resolved disputed value”.
Read that way, S4 would cover every exact value.
Three working rules live only in rationales: the T-020 calibration note, the T-015/T-032
precedent, and T-042/T-061 for a step that changes nothing visible.

## 2. Every Registered Result

The anchor column gives what the rationale cites, not what fits.
The history column is the owner’s added factor: the date of the previous value or of the
open status, and the earlier attempts.

| ID | Claim (short) | n | V/C | S | Anchor the rationale cites | History: prior value or open since; prior attempts |
| --- | --- | --- | --- | --- | --- | --- |
| T-001 | s(17) ≥ 4.426213, 16-point set | 17 | V3/C3 | S3 | none named; first verified movement since 2005 | floor Nagamochi 2005; Burns 4.4811 public 6 Aug 2026, so not first movement |
| T-002 | s(18) ≥ 4.426213, monotone from T-001 | 18 | V3/C3 | S3 | none; “frontier field moved” | routine corollary |
| T-003 | ceiling of T-001’s point set | 17, 18 | V3/C3 | S2 | none | — |
| T-004 | Bentz 2010 Thm 8 audited | 46 | V3/C3 | S3 | implicit “machine audit” | 2010 proof, unchecked by machine for 16 yrs |
| T-005 | Bentz 2010 Lemma 10 false, corrected | 13 | V3/C3 | S2 | “changes no theorem” (S2) | 2010 lemma |
| T-006 | s(13) = 4 | 13 | V3/C3 | S3 | none (“the theorem’s”) | open 1979–2010; Bentz 2010; case-free proof 2026 |
| T-007 | Nagamochi closed form, 4 ≤ n ≤ 100 | 4–100 | V0/C1 | S3 | none (usage count) | 2005; cited 21 yrs (DS7, Kingbird); proof gap found Sep 2026 |
| T-008 | s(46) = 7 | 46 | V3/C3 | S3 | none | Bentz 2010 |
| T-009 | s(29) ≤ 5.9338…, interval certificate | 29 | V3/C3 | S3 | none | Gensane–Ryckelynck packing 2004 |
| T-010 | s(11) ≥ 2 + 4/√5, Stromquist repaired | 11 | V3/C3 | S4 | “resolves the proof status” (≈ resolved disputed value) | printed proof cited 2003–2026 |
| T-011 | Trump’s packing exactly valid | 11 | V3/C3 | S2 | “changing no theorem” (S2) | packing 1979; never exactly certified |
| T-012 | n = 5 second-order rigid | 5 | V3/C3 | S3 | none | Göbel 1979; rigidity asserted, never argued |
| T-013 | n = 40 flexes refused | 40 | V3/C3 | S3 | none | catalogue packing |
| T-014 | n = 5 pose isolated | 5 | V3/C3 | S3 | case result | Göbel 1979 |
| T-015 | s(17) ≥ 4.5058 (Massaccesi) | 17 | V3/C3 | S3 | none (becomes “T-015 precedent”) | Burns 6 Aug, Massaccesi 21 Aug 2026 |
| T-016 | s(18), s(19) monotone from T-015 | 18, 19 | V3/C3 | S3 | none; n=19’s first movement since 2005 | routine corollary |
| T-017 | s(12) ≥ 3.96, eight-rung ladder | 12 | V3/C3 | S4 | technique; “bound family” | inherited s(11) floor 2003; T-049 earlier (25 Aug) |
| T-018 | s(11) ≥ 3.81 | 11 | V3/C3 | S5 | central open case | floor 1984/2003, 23 yrs; open since 1979 |
| T-019 | s(17..19) ≥ 4.59 | 17, 18, 19 | V3/C3 | S4 | S4 anchor via displacement | not first movement (Burns, T-001, T-015 before) |
| T-020 | s(19..21) ≥ 4.80 | 19, 20, 21 | V3/C3 | S4 | S4 via displacement; parity with T-019 | n = 20, 21 floor Nagamochi 2005 |
| T-021 | s(20, 21) ≥ 4.85 | 20, 21 | V3/C3 | S3 | T-020 calibration note | same campaign |
| T-022 | s(11) ≥ 3.8100257… | 11 | V3/C3 | S5 | central open case | 2 days after T-018; same certificate, +2.6e-5 |
| T-023 | four-owner branch excluded at 96/25 | 11 | V3/C3 | S3 | substantive case result | n = 11 programme |
| T-024 | s(11) ≥ 3.8166… | 11 | V3/C3 | S5 | central open case | T-018 atoms on a finer net |
| T-025 | s(11) ≥ 3.82, threshold certificate | 11 | V3/C3 | S5 | central; new architecture | first certificate of a new kind |
| T-026 | s(11) ≥ 3.8264… | 11 | V3/C3 | S5 | central open case | T-025 atoms on a finer net |
| T-027 | s(18) ≥ 4.67 | 18 | V3/C3 | S3 | T-020 note | n = 18 floor 2005; Sep 2026 rungs |
| T-028 | s(18) ≥ 4.675 | 18 | V3/C3 | S3 | T-020 note | rung |
| T-029 | s(18) ≥ 4.6775 | 18 | V3/C3 | S3 | T-020 note | rung |
| T-030 | s(18) ≥ 4.679 | 18 | V3/C3 | S3 | T-020 note | rung |
| T-031 | octagon corner class excluded | 11 | V3/C3 | S2 | none; “moves no bound” | n = 11 programme |
| T-032 | s(17) ≥ 4.6130… (Mira) | 17 | V3/C3 | S3 | T-015 precedent | rung |
| T-033 | s(11) ≥ 3.82700 | 11 | V3/C3 | S3 | case result or machine audit | below public 31/8 when made |
| T-034 | s(21) ≥ 4.88 | 21 | V3/C3 | S3 | T-020 note | rung |
| T-035 | six-plus-five near Trump localised | 11 | V3/C3 | S3 | case result / machine audit | n = 11 programme |
| T-036 | Trump optimal among six-plus-five | 11 | V3/C2 | S3 | case result / machine audit | n = 11 programme |
| T-037 | s(11) > 31/8 (Kleddamag) | 11 | V3/C3 | S5 | central open case | closes 96% of the 2026 gap |
| T-038 | s(17) > 4.61979… | 17 | V3/C3 | S3 | T-015/T-032 precedent | Bidwell upper 1998; ~12 rungs Aug–Sep 2026 |
| T-039 | s(17) > 4.62002 | 17 | V3/C3 | S3 | T-015/T-032 precedent | rung |
| T-040 | s(17) > 4.64002 | 17 | V3/C3 | S3 | T-015/T-032 precedent | rung |
| T-041 | s(17) > 4.66001 | 17 | V3/C3 | S3 | T-015/T-032 precedent | rung |
| T-042 | s(17) > 4.66018, superseded same day | 17 | V3/C3 | S2 | T-042 (citable intermediate) | rung |
| T-043 | s(17) > 4.66044 | 17 | V3/C3 | S3 | T-015/T-032 precedent | rung |
| T-044 | weighted point bounds, 17 counts | 17 counts, 26–73 | V3/C3 | S3 | substantive (family of case results) | Nagamochi 2005 / Green (DS7 2009) floors |
| T-045 | rectangle-density bounds, 15 counts | 15 counts, 18–78 | V3/C3 | S3 | substantive case results | same |
| T-046 | reported bounds, 48 counts | 48 counts, 18–95 | V0/C0 | S3 | scored as a claim, S3 | same |
| T-047 | Tokoharu’s rectangle-density bounds | 7 counts, 11–31 | V3/C3 | S4 | reusable technique | 2026 |
| T-048 | s(50) ≥ 7.4 | 50, 51 | V3/C3 | S3 | substantive case result | 2005/2009 floors |
| T-049 | s(12) ≥ 3.9686 (Daniel) | 12 | V3/C3 | S3 | substantive case result | first n = 12-specific bound, 25 Aug 2026 |
| T-050 | s(21) ≥ 4.995 | 21 | V3/C3 | S3 | substantive case result | DS7 Table 2 decimal; 2026 rungs |
| T-051 | s(32) = 6 | 32 | V3/C3 | S4 | reusable technique | open since 1979; first k²−4 (k ≥ 4) value; first new exact value since 2016/18 |
| T-052 | s(21) = 5 | 21 | V3/C3 | S4 | reusable technique (line mass) | open since 1979; DS7 decimal; Sep 2026 rungs |
| T-053 | s(45) = 7 | 45 | V3/C3 | S4 | “bound family”; case changes character | open since 1979; technique is T-052’s |
| T-054 | s(45) = 7, point-only | 45 | V3/C3 | S2 | citable detail | second route |
| T-055 | s(21) = 5, point-only | 21 | V3/C3 | S2 | citable detail | second route |
| T-056 | 49 smaller packings, n = 68..307 | 49 counts, 68–307 | V3/C3 | S3 | substantive case result | catalogue records 1979–2026 |
| T-057 | s(211) < 15 | 211 | V3/C3 | S3 | substantive case result | grid record |
| T-058 | rectangle-certificate ceiling | 1–100 | V3/C3 | S2 | none (tooling) | — |
| T-059 | n11 row minima reproduced | 11 | V3/C3 | S2 | none | audit of T-037’s certificate |
| T-060 | s(11) = Trump’s side | 11 | V3/C3 | S5 | central open case | open 1979–2026 (47 yrs); floor 1984/2003 stood 23 yrs; Göbel and Trump 1979, Stromquist 1984 and 2003, DS7; 16 earlier entries here |
| T-061 | s(11) > 31/8 + 3.9e-9 | 11 | V3/C3 | S2 | citable detail (T-042 precedent) | slack of T-037 |
| T-062 | s(60) = 8 | 60 | V3/C3 | S3 | substantive case result | open since 1979 |
| T-063 | s(61) = 8, monotone from T-062 | 61 | V3/C3 | S1 | routine consequence | k²−3 member; H-033 target |
| T-064 | s(k²−3) = k, every k ≥ 6 | 13 counts, 33–321 | V3/C3 | S4 | bound family | members 1984/2002 (k=3), 2010 (k=4,7), 2016 (k=5,6); Friedman Conj. 1 ≤ 2000; no k ≥ 8 before Oct 2026 |
| T-065 | Bidwell’s n = 17 packing exactly valid | 17 | V3/C3 | S3 | substantive / machine audit | packing 1998 |
| T-066 | s(59) = 8 | 59 | V3/C3 | S3 | substantive case result | open since 1979 |
| T-067 | s(77) = 9 | 77, 78 | V3/C3 | S3 | substantive case result | open since 1979 |
| T-068 | reported bounds, 34 counts | 34 counts, 19–95 | V0/C1 | S3 | T-020 note (further sizes) | 2005/2009 floors |
| T-069 | mixed bounds, 5 counts | 5 counts, 37–92 | V3/C3 | S3 | T-020 note | same |
| T-070 | rectangle bounds, 23 counts | 23 counts, 29–95 | V3/C3 | S3 | T-020 note | same |
| T-071 | mixed bounds, n = 84..87 | 4 counts, 84–87 | V3/C3 | S3 | T-020 note | same |
| T-072 | mixed bound, n = 76 | 76 | V3/C3 | S3 | T-020 note | same |
| T-073 | linear-measure bounds, 6 counts | 6 counts, 83–105 | V3/C3 | S3 | T-020 note | same |
| T-074 | rectangle bounds, 31 counts | 31 counts, 19–95 | V3/C3 | S3 | T-020 note | same |
| T-075 | mixed bounds, 9 counts | 9 counts, 83–96 | V3/C3 | S3 | T-020 note | same |
| T-076 | linear-measure bound, n = 82 | 82 | V3/C3 | S3 | T-020 note | same |
| T-077 | reported bounds, n = 20, 42, 70 | 20, 42, 70 | V0/C1 | S3 | T-020 note | same |
| T-078 | s(12) ≥ 3.96912, rescaled | 12 | V3/C3 | S2 | T-061 precedent | slack of T-049 |
| T-079 | s(12) ≥ 3.97020, re-weighted | 12 | V3/C3 | S3 | substantive; “not S5: central question at n = 12 does not move” | n = 12 programme, Aug–Oct 2026 |
| T-080 | linear-measure bounds, n = 101..105 | 5 counts, 101–105 | V3/C3 | S3 | T-020 note | same |
| T-081 | s(k²−4) = k, every k ≥ 5 | 14 counts, 21–320 | V0/C1 | S4 | bound family; “not central” | k = 3 fails (1979), k = 4 open; no k ≥ 5 member before 26 Sep 2026; DS7 n=21 decimal only |
| T-082 | reported mixed bounds, 22 counts | 22 counts, 51–96 | V0/C1 | S3 | T-020 note | same |
| T-083 | Karakuş general floor, nonsquare 8..324 | 8–324 | V3/C1 | S3 | substantive case result or machine audit | replaces Nagamochi 2005 floor |
| T-084 | s(k²−1) = k, every k ≥ 3 | 16 counts, 8–323 | V3/C1 | S3 | substantive case result or machine audit | El Moumni 1999 (k = 3, 4); Nagamochi 2005; gap found Sep 2026; restored 29 Sep |
| T-085 | Nagamochi 2005 Lemma 1 false | 10–324 | V3/C3 | S3 | substantive case result or machine audit | lemma relied on 21 yrs (DS7, Kingbird, 95 case records here) |
| T-086 | s(k²−2) = k, every k ≥ 2 | 16 counts, 7–322 | V3/C3 | S3 | substantive case result or machine audit | El Moumni 1999 / Kearney–Shiu 2002 (k = 3), DS7 (k = 4), Nagamochi 2005; Lean Sep 2026 |
| T-087 | s(37), s(61) by optimal piercing | 37, 61 | V3/C1 | S3 | substantive case result or machine audit | Bašić–Slivková 2018 |

## 3. Assessment

### n = 11 against the families

The register applies the anchors as written.
T-060 is “movement on a central open case”; T-064 and T-081 are “bound family”.
The inconsistency lies a level up, in two undefined terms.

- **“Central open case”.** S5 has gone to every visible step at n = 11, seven entries.
  By their own rationales, three of them re-derive or rescale an existing certificate:
  T-022 (+2.6 × 10⁻⁵), T-024 and T-026. At n = 17 to 21, T-020’s note puts such a step
  at S3.
- **“Family”.** It has been applied alike to a bound carried to three counts by
  monotonicity (T-019, T-020), to three sibling exact values (T-053) and to an infinite
  family of exact values (T-064).

**Is an infinite family at least as significant as one hard exact case?
Not by counting cases.** The near-square families are uniform: one periodic measure and
one finite check settle every k, and the optimum is the grid.
“Infinitely many” therefore measures reach, not difficulty.
s(11) needed a proof that an irrational tilted packing is optimal at the smallest open
n. The question had been open 47 years, and its lower bound had not moved for 23. What
separates the two families is the history factor:

- **k² − 3.** Proved for k = 3 in 1984 and 2002, for k = 4 and 7 in 2010, and for k = 5
  and 6 in 2016. The general statement was conjectured by 2000 (DS7, Conjecture 1,
  restated by Nagamochi 2005). It was a target of this project’s H-033 in August 2026.
  Nothing with k ≥ 8 had been proved.
- **k² − 4.** k = 3 fails (Göbel 1979), and k = 4 (n = 12) is open.
  No member with k ≥ 5 was proved before T-051 on 26 September 2026. The only attempt
  dated before 2026 in the archive is DS7 Table 2’s undocumented decimal at n = 21.
  Conjecture 1 had no known base case at this deficit until s(21) = 5 on 27 September.

On that factor T-064 sits in T-060’s tier and T-081 does not.

### Re-proofs, refutations and imports

The rubric does not separate new results, re-proofs and imports by score, and should
not. Rule 1 scores the claim, T-037 and T-060 are imports at S5, and novelty has its own
axis. The distinction it does draw runs through the result kind:

- **A second proof of something the record already proves** is a simplification, scored
  S2 (T-054, T-055).
- **T-084 and T-086 are not that.** On PR #305’s register the values rest on them alone.
  T-007 is withdrawn to V0, and the case records (n-007, n-008, n-014, n-015) now cite
  Karakuş’s and chelokot’s evidence as their verified lower bound.
  Their shared rationale, “every value was already held as proved”, is therefore false
  on the register it ships with.
- **T-010 is the precedent that fits** (S4): a value cited as proved, its printed
  argument falsified, restored by a source-distinct repair.
  T-084 and T-086 are T-010 for infinite families.
- **No history lift for them.** The families were open for weeks (chelokot’s gap note of
  4–6 September to 29 September 2026), not years.

**T-085, the refutation of Nagamochi’s Lemma 1.** The anchor its rationale cites, “a
substantive case result or machine audit”, does not fit: T-085 is a correction.
T-005, the other correction, holds S2 because it “changes no theorem”.
T-085 is the opposite case.
It removes the proof of Nagamochi’s Theorem 1 at full strength and of both exact
families in his Theorem 2. That proof was relied on for 21 years by DS7, by the Kingbird
catalogue, and by 95 of this record’s 100 case files.

It is not S5:

- it settles no value;
- the families it unsettled were restored within the month;
- Theorem 1 is unproved, not disproved.

S5’s second clause, broad external adoption, could reach it later, if the catalogue and
survey revise their “Proved by Hiroshi Nagamochi” lines.

### Single exact values

The register gives S3 to a single exact value without a new technique (T-006, T-008,
T-062, T-066, T-067) and S4 where the entry brought the technique (T-051’s zero-margin
closed cover, T-052’s line mass).
T-053 is the outlier.
Its rationale concedes that the technique is T-052’s, then lifts it because the case
“changes character”, which is true of every exact value, and because “with its two
siblings it is a bound family”, a claim that now belongs to T-081. The s(60) review
(2026-10-02, §8) already said that T-053 and T-062 must carry one score.

## 4. Recommended Changes

| ID | Now | Recommend | Confidence | Basis |
| --- | --- | --- | --- | --- |
| T-064 | S4 | **S5** | high | family + history lift (rule b) |
| T-084 | S3 | **S4** | high | resolved disputed value; T-010 |
| T-086 | S3 | **S4** | high | resolved disputed value; T-010 |
| T-053 | S4 | **S3** | high | T-020 note; parity with T-062 |
| T-085 | S3 | **S4** | medium | correction rule (d) |
| T-083 | S3 | **S4** | medium | bound family + technique |
| T-007 | S3 | **S4** | medium | bound family; rule 1 |
| T-011 | S2 | **S3** | medium | machine audit; T-065, T-004 |
| T-002, T-016 | S3 | **S1** | medium | routine consequence; T-063 |
| T-019, T-020 | S4 | **S3** | medium | monotone carry, not a family |
| T-022, T-024, T-026 | S5 | **S4** | if rule (c) is adopted | rescaled rungs at a central case |
| T-081 | S4 | S4, new rationale | medium | fails the much-attempted test |

**T-064 → S5.** The claim settles s(k²−3) = k for every k ≥ 6. Together with the proved
cases k = 3 to 7, it settles Friedman’s Conjecture 1 at deficit 3 outright.
The anchor gives S4 as a family, and rule (b) lifts it one step on the history above.
The current rationale is also stale.
It says V0/C1 and “would settle eleven open cases”; the entry now reads V3/C3, with nine
cases closed by it. Its `by` names the intake, not a review, so rule 2 has never been
met.

**T-084 and T-086 → S4.** They restore families whose only proof fell, the S4 anchor’s
“resolved disputed value”, as T-010 was scored (§3). T-084 is not a routine consequence
of T-083: both are corollaries of Karakuş’s Theorem 1.1. Replace the sentence “every
value was already held as proved”.

**T-053 → S3.** One more exact value by T-052’s technique, scored as T-062, T-066 and
T-067 are.

**T-085 → S4.** It removes the proof of S4 theorems, T-007 and both families, so under
rule (d) it scores as they do; T-005 at S2 marks the other end of the scale.

**T-083 → S4.** A closed-form lower bound for every nonsquare n, by a strip measure that
also yields T-084 and replaces Lemma 1: a bound family and a reusable technique, both
named by the S4 anchor.
Its S3 rationale, “replacing its proof at a weaker value”, describes the frontier, which
rule 3 sets aside.
Judgment could hold S3, since away from k²−1 the bound is barely above
area (0.003 at n = 82); 287 case floors fell back to it, which decides it for me.

**T-007 → S4.** Nagamochi’s closed form is the model bound family: one formula for every
n ≥ 4, and the strongest general lower bound for 21 years.
Its S3 rationale is a usage count, not an anchor.
Rule 1 means its withdrawal to V0 does not hold the score down.

**T-011 → S3.** Exact certification of a published record packing is the S3 anchor’s
“machine audit”. T-065 (Bidwell’s packing) and T-004 are scored that way.
T-011 is also the upper half of T-060.

**T-002 and T-016 → S1.** Each follows from its parent in one line of monotonicity, as
T-063 does from T-062, and S1’s anchor names “a routine consequence”.
Their S3 rests on the case’s frontier field moving, a basis rule 3 rejects.
The movement’s significance belongs to T-001 and T-015.

**T-019 and T-020 → S3.** Each carries one constant bound to three counts by
monotonicity, which is not a family.
Their S4 rests on displacing a published value, which no anchor names; T-020’s own note
says “the S4 anchor is being carried here by the displacement rather than by the
technique”. T-044, T-046 and T-056 displace published values at 17, 48 and 49 counts at
S3. Rule (b) does not apply: Burns moved n = 17 first, on 6 August, and at n = 21 T-020
has one earlier dated source, DS7.

**T-022, T-024, T-026 → S4, conditional on rule (c).** Each re-derives or rescales an
existing certificate, and none is the first movement or the settlement.
S4 still credits the central case without equating these rungs with T-018, T-025, T-037
and T-060.

**T-081 stays S4.** Drop “not S5, since no case it settles is central” and give the
history reason above, which holds up under the owner’s factor.
Name the 3 October claim-chain review in `by`; it agreed S4.

**Kept, with notes.** T-060 stays S5; its one-line rationale should record the history.
T-017 stays S4 on its technique ground, but its claim to the “first bound specific to n
= 12” belongs to T-049. T-059 (S2) against T-004 (S3) is defensible, because an audit of
another entry’s certificate is confirmation evidence for that entry, but no rationale
says so.

## 5. Proposed Rubric Wording

For `epistemics.md`, after the three rules:

> **(a) Families.** A family is one argument that gives a bound or a value depending on
> n across infinitely many n or a stated range: a closed form, or one certificate
> parametrized by n. A constant bound carried to larger n by monotonicity is not a
> family. Certificates at many separate n from one generator are further sizes, scored
> `S3`. A bound family or an infinite family of exact values scores `S4`, and `S5` only
> under (b).
>
> **(b) Longstanding and much-attempted.** A result that settles a question, or is the
> first to move it after a stall, rises one step, to at most `S5`, when the record shows
> both:
>
> - *Longstanding:* at the result’s date the question had been open, or its previous
>   best value had stood, for at least ten years.
>   The date comes from a source retained in `packing/resources/` or from a case
>   record’s history.
> - *Much-attempted:* at least two independent sources, each dated five or more years
>   before the result, attacked the question or stated it open.
>   A source counts if it is a published proof of a special case, a published partial
>   bound specific to the question, a survey or problem list naming it, or a recorded
>   computational campaign.
>   A general closed form covering every n is not an attempt on one case.
>
> The lift goes to the settling or first-moving result.
> Later rungs on the same question do not inherit it.
> The rationale names the dates and sources it relies on.
>
> **(c) Central and movement.** A central open case is the smallest open n at the
> result’s date, or a case the owner names here with a date.
> On a central case, the first movement after a stall, a new kind of certificate and the
> settlement score `S5`. A later rung that re-derives or rescales an existing
> certificate scores `S4`, and a step that changes no printed digit of the case’s
> bracket scores `S2`.
>
> **(d) Corrections, re-proofs and imports.** A correction that changes no theorem
> scores `S2`; one that removes the proof of a theorem scores as that theorem’s entry
> does. A second proof scores `S2` while the record holds another proof of the same
> claim. A proof that restores a value whose only proof has fallen scores `S4`, as a
> resolved disputed value.
> A routine consequence of another entry scores `S1`. Who produced a result does not
> enter its score; novelty records that.

These rules move the T-020, T-042/T-061 and T-010 precedents out of rationales and into
policy. Applied to the register, rule (b) lifts T-064 and confirms T-018 and T-060. The
lane should also test:

- **T-006 and T-008** (Bentz 2010), against DS7’s pre-2005 editions;
- **T-049**, the first n = 12-specific bound, which I judge to fall short on dated
  sources.

Rule (c) is separable from the rest.
Without it, T-022, T-024 and T-026 stay S5. Also change the site’s S4 short form to
“resolved disputed value”.

## 6. Process

- **These are recommendations; I reviewed no mathematics.** By rule 2, a change to a
  confirmed score has one stated path: `think-qh3s`’s “one rescoring pass … by an
  independent review lane”, with `by` naming that review.
- **`think-qh3s` needs a wider scope.** It covers the 23 drafts (T-037 to T-057, T-061,
  T-065), which contain only T-053 of these changes.
  The rest need it widened or a sibling bead: T-002, T-007, T-011, T-016, T-019, T-020,
  T-022, T-024, T-026, T-064, T-081 and T-083 to T-086, all but T-064 and T-081
  confirmed scores.
- **The rule comes first.** Rules (a) to (d) are policy for the owner, as `think-qh3s`
  already says of its working rules.
  Rescore after that decision and after #305 merges, since T-083 to T-087 exist only on
  its branch.
- **Downstream.** T-064 at S5 triggers the Stage 6 paper; the synopsis headline and the
  pull-request presentation re-render from `results.yaml`.
