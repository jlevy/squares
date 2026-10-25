# C1089 — recovered family proof with a simpler all-angle ending

**Mathematical handoff complete. No Lean work or upstream changes.**

This is the alternative mathematical route permitted by the first handoff. It
recovers the existing continuous C1089 sector argument, supplies the actual
singleton/auxiliary entrance, and replaces the last sector's terminal argument
by a new self-contained eight-point obstruction. It does **not** claim to have
recovered or compiled the missing `S12.Case1089To0Aux` module.

## 1. Exact theorem and physical model

There are no twelve open squares of common side `1<a<=1001/1000`, with arbitrary
independent orientations, pairwise disjoint interiors, and closures in `[0,4]²`,
whose exact original-marker family is

```
{1,12,48,192,256,512,1024,2048,4096,8192,16384,32768}.
```

Let Q0,...,Q11 be these actual squares in ascending-mask order. The literal
marker and F/G coordinate tables are retained in the task and in
[the local entrance rule](entrance/LOCAL-RULE.txt). In particular Q0 owns only
marker 0, `(1,.914)`. Marker 1, `(.914,1)`, is globally absent. It is never
assigned to Q0 or replaced by a paired-corner hypothesis.

The handoff identifies this family as original case C1089, row 573 of its
577-row table. The written family contradiction below is the mathematical
input needed by the proposed row adapter. This package does not report a
compiler check of that adapter or of the repository's `ExcludesCase1089` theorem.

## 2. Actual-packing entrance, not an empty-list assertion

[FOUNDATIONAL-ENTRANCE.md](entrance/FOUNDATIONAL-ENTRANCE.md) proves the following
facts in ordinary geometry, including every orientation and closed boundary tie.

The exact Q0 singleton signature forces `(1.12,1),(1.74,1),(1.87,.76)` strictly.
The proof uses corner and wall non-avoidance plus six-triangle center covers;
it does not use the erroneous transposed seed `(1,1.74)`. It also proves the
stronger missing-inner-corner seeds `(1.82,1),(1.96,.76)` when `(1,1)` is
explicitly excluded, as required by the recovered singleton-ending arguments.

A square avoiding all F points must own a complete pair from
`{0,1},{2,3},{4,5},{6,7},{8,11},{9,10}`. The transposed statement gives the G
pair list. Thus precisely the three paired-corner owners are exceptional in
C1089: each other owner takes one or two points from each auxiliary set, and
an exceptional owner takes zero or one.

The local convexity, four-point and five/six-point rules in `LOCAL-RULE.txt`
then yield component-list sizes

```
2, 3, 6, 6, 21, 21, 64, 64, 10, 3, 10, 11.
```

They sum to **221 labels**, whose pairwise-disjoint ordered choices are exactly
**506 assignments**. The independent integer replay regenerated and compared
all labels and all 506 rows of the recovered catalogue. Every actual packing
reaches this catalogue because every deletion is a proved necessary-condition
operation. Mere emptiness of an unexplained final list is not used.

## 3. The recovered continuous reduction

Use [C1089-CONTINUOUS-REDUCTION](reference/recovered-lemmas/C1089-CONTINUOUS-REDUCTION.md).
Its Proposition 1 proves, without choosing a wall-sign sector,

```
X9 > 2.04,  and  [2.26,2.8] x {1} lies strictly in Q9.
```

This uses the true Q0 seeds and the actual Q5 marker. Put

```
L = Y8,   R = Y10,   T = X11.
```

There are eight closed choices of the signs of `L-2,R-2,T-2`. Here `+` means
`>=0` and `-` means `<=0`; equality is deliberately covered on both sides.
These are signs of actual wall-center coordinates, not discrete square angles.

| Sector | Complete continuous exclusion used |
|---|---|
| +,+,+ | C1089-CONTINUOUS-REDUCTION, Theorem 5 |
| +,+,- | C1089-MMMP-SINGLETON-ENDING, Theorem |
| +,-,+ | Sections 4–5 below, replacing the old last-sector terminal |
| +,-,- | C1089-CONTINUOUS-REDUCTION, Theorem 4 |
| -,+,+ | C1089-NORTHEAST-INWARD-ENDING, Theorem |
| -,+,- | C1089-REVERSE-CYCLIC-ENDING, Theorem |
| -,-,+ | C1089-CONTINUOUS-REDUCTION, Proposition 2 |
| -,-,- | C1089-CONTINUOUS-REDUCTION, Proposition 2 |

All named chapters are included under `reference/recovered-lemmas/`, with their
shared continuous lemmas and the older continuous foundations they use. These
are recovered mathematical proofs, not newly authored proofs of all those
lemmas. The table recovers their eight-sector organization; it is not a claim
that this turn newly discovered the reduction from 506 assignments to sectors.

## 4. Upstream facts for the remaining sector

Assume `L>=2`, `R<=2`, `T>=2`. Write `A=Q4`, `S=Q5`, `E=Q6`, `N=Q7`.
The following chain is retained, with literal actual-owner maps:

1. `C1089-LAST-SECTOR-REDUCTION.md` and `C1089-LAST-SECTOR-POINTS.md` put the
   actual wall bars and central crosspoints in place. Q0's inner point `(1,1)`
   is proved by the missing-inner-corner contradiction, not assumed from the
   absent marker. `ORDINARY-BAR-CROSSPOINT.md` gives `(1.5,2)` in A from the
   genuine Q0 horizontal segment.
2. Sections 1–2 of `C1089-LAST-SECTOR-ENDING.md` rule out A's label 1025.
   Its remaining label is 9217, so A owns `F0,G0,G3` strictly. The two alternatives
   for N's ownership of F5 are excluded respectively by the full-bar duplicate
   point and the all-angle coupled-support lemma. No angle of N is assumed.
3. Section 3 of that chapter applies the reflected support-point theorem to S,
   using its own crosspoints and the two genuine foreign segments in Q9 and A.
   It proves the strict point

```
(2.73,1.96) in S=Q5.                                    (*)
```

For clarity, all terminal data following that chain are:

| Datum | Actual owner and source |
|---|---|
| (2.35,2.35), (3,2.26) | E's original NE marker and F9 |
| (3,2) | Q10's proved lower-bar endpoint |
| (2.5,2) | S's proved central crosspoint |
| (3,3) | Q2's paired inner-corner point |
| (2.73,1.96) | S, from (*) |
| (2.56,3), (2.26,3) | Both in Q11's proved strict bar `[2,2.56] x {3}` |

Every owner listed for an excluded point is distinct from E. Each such point is therefore
excluded from E's open interior. No segment is inferred by joining points of
different owners, and no omitted auxiliary is declared foreign without a named
strict owner.

## 5. New terminal: two interior points, six exterior points

Apply the isometry `(xi,eta)=(3-x,y-2)` to E and all the terminal points at once.
The resulting square strictly contains

```
M=(.65,.35), H=(0,.26),
```

and excludes

```
O=(0,0), D=(.5,0), K=(0,1), X=(.27,-.04),
T0=(.44,1), T1=(.74,1).
```

The [eight-point obstruction](proofs/EIGHT-POINT-OBSTRUCTION.md) proves that no
square of side `a>1` has these properties. Its proof covers both canonical signs
and includes axial/diagonal orientations and boundary exclusions.

The two final width contradictions in that proof are simply

```
positive canonical frame:
  2a <= 1.48c+1.27s <= sqrt(3.8033) < 2;

negative canonical frame:
  2a <= 1.54c+1.17s <= sqrt(3.7405) < 2.
```

The intermediate face eliminations and exact norm certificates are all written
out. This eliminates the old need to first prove `2/3<s/c<8/11` and then
optimize a function on that interval. It also drops the old local terminal's
excluded points `(-.086,0)` and `(.74,0)`. Those points may still be used
upstream to obtain (*); the claim is a reduction of the terminal lemma's inputs,
not their removal from the entire C1089 proof.

This excludes the whole closed `(+,-,+)` sector. Combining it with Section 3's
other seven sector exclusions contradicts every possible configuration after
the actual-packing entrance. The theorem of Section 1 follows. ∎

## 6. Checks, provenance, and verification boundary

Run the exact checks from this directory:

```sh
python3 checks/replay_entrance.py --receipt checks/entrance-receipt.json
python3 checks/check_foundation.py
python3 checks/check_new_obstruction.py
```

All three also passed under `python3 -O`. They use only the Python standard
library. Their receipts report: 221 component labels; 506 complete assignments;
13 closed rectangle covers; six positive polynomial identities; 25 projection
identities with cone-sign checks; and eight literal actual-owner coordinate maps.

The scripts audit the finite entrance and the new arithmetic. They do **not**
constitute a new proof-assistant verification of the recovered analytic sector
library. The old 506 terminal traces were not rerun and are not used as the
chosen ending. No missing Lean import has been reconstructed, no formal row
adapter compiled, and no claim about accepted axioms or module/line counts is
made. This result is the mathematical C1089 replacement, not a new standalone
verification of all seventeen handoffs or of the entire twelve-square theorem.

`PROVENANCE.json` and `reference/RECOVERY-MANIFEST.json` distinguish the supplied
inputs, unchanged recovered proofs, and newly written work. The working task is
marked `01_DONE_MATH_C1089.md`; all sixteen later tasks remain pending.
