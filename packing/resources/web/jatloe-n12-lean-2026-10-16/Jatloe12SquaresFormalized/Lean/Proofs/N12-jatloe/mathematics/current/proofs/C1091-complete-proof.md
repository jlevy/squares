# C1091 / task 03: complete mathematical exclusion

**Current status: MATH COMPLETE; FORMAL INTEGRATION PENDING.**

This chapter finishes the exact C1091 family. It joins the previously proved
seven-sector reduction to a complete exclusion of the remaining sector.
There are no remaining auxiliary or continuous angle branches in this
mathematical argument. The proof is a direct geometric ending, not an assertion
that a missing certificate exists.

The previous [progress report](C1091-PROGRESS.md) is preserved unchanged as a
historical checkpoint and as the detailed entrance proof. Its PARTIAL status
and its final open obligation are superseded by this chapter. The earlier
report's references, complete local proofs, and exact ownership reconstruction
are all included in this archive.

No Lean was written or compiled. In particular, this chapter is not a kernel
acceptance receipt for row575, and does not claim that the other sixteen tasks
or the whole twelve-square theorem have been integrated. The supplied
148-operation historical terminal is not needed and is not claimed replayed.

## 1. Exact theorem and conventions

**Theorem.** There do not exist twelve congruent open squares Q0,...,Q11 with
pairwise disjoint interiors, common side

    1<a<=1001/1000,

closures in [0,4]², and exact original-marker masks, in increasing order,

    (1,12,48,192,258,512,1024,2048,4096,8192,16384,32768).

Thus the exact normalized family specified in task03/C1091 is impossible.

Write A=Q4, S=Q5, E=Q6, N=Q7. The strict original points needed below are:

| Actual square | Original points, or retained paired inner point |
|---|---|
| Q0 | (1,.914); southwest singleton |
| Q1 | (3,.914),(3.086,1), and inner (3,1) |
| Q2 | (3,3.086),(3.086,3), and inner (3,3) |
| Q3 | (1,3.086),(.914,3), and inner (1,3) |
| A | **(.914,1),(1.65,1.65)** |
| S | (2.35,1.65) |
| E | (2.35,2.35) |
| N | (1.65,2.35) |
| Q8 | (.914,2) |
| Q9 | (2,.914) |
| Q10 | (3.086,2) |
| Q11 | (2,3.086) |

Every decimal in this chapter denotes its exact rational value. Owned points
are strictly inside their actual open square. Excluded points may be on the
boundary. Every segment used below lies strictly in one named actual owner;
we never join endpoints belonging to different squares.

Canonical square frames are u=cx+sy, v=-sx+cy or u=cx-sy, v=sx+cy, with
c>=s>=0 and c²+s²=1. These are choices of a square's face labels, not rotations
of individual squares. Actual symmetries below are applied to the whole
configuration. Weak separating supports are retained.

## 2. The established entrance, and precisely what is imported

The finite entrance and continuous reductions are proved in
[C1091-PROGRESS.md](C1091-PROGRESS.md), Sections 1–6, with their full sources
included under `../C1089/entrance/` and
`../C1089/reference/recovered-lemmas/`. The new merged-marker and inward-point
proofs are in `proofs/`. This completion imports the **point-level conclusions**
below, not the C1089 or C981 whole-family theorems.

Let L,R,T be the vertical center coordinates of Q8,Q10 and the horizontal
center coordinate of Q11. The earlier argument gives the following exhaustive
closed-sign ledger:

| Signs of (L-2,R-2,T-2) | Established contradiction |
|---|---|
| (-,*,*) — four sign patterns | Strict F0=(1,1.74) in both A and Q8 |
| (+,-,-) | Two distinct inward squares strictly own (2,2) |
| (+,+,+) | Retained MMMM support ending with actual owners |
| (+,+,-) | New five-point merged-marker obstruction |
| (+,-,+) | The residual finished below |

The proof and actual-owner maps for the first seven patterns are in the
progress report, Section 4. Because equality belongs to an excluded closed
pattern, any remaining packing would have the strict signs

    L>2, R<2, T>2.                                         (1)

The bottom center coordinate is >2.04. The further residual conclusions are:

| Actual square | Strict points or same-owner segments already proved |
|---|---|
| Q0 | (1,1), (1.12,1), (1.74,1), (1.87,.76) |
| A | (1,1.74),(1,1.6), (1.5,2),(1.58,2) |
| S | (2,1.74),(2.26,2), **(2,1.5),(2,2),(2.5,2)** |
| E | (3,2.26),(3,2.4) |
| N | **(1.6,3)** |
| Q8 | **{1} x [2.26,2.56]**, including (1,2.4) |
| Q9 | **[2.26,2.8] x {1}**, and (2,1) |
| Q10 | **{3} x [1.44,2]**, including (3,2) |
| Q11 | (2.26,3) |

All original markers and the three paired corner inner points remain strict.
In particular the central marker (1.65,1.65) is always strictly in A; it is
never globally absent.

The six residual N labels are

    8200,8232,16392,16424,24584,24616.                       (2)

After the proved point (1.6,3) is imposed, every residual Q11 label owns both

    (2.4,3)=F7, (2.26,3)=G7.                               (3)

For clarity, (3) follows already from Q11's complete local family: its members
which exclude F3=(1.6,3), a strict N point, all contain bits7 and17. It does
not require that N own G4=(1.74,3), and it does not assume the top-wall origin.
The possible residual Q11 labels are

    131200,131232,147584,147616.

These statements are literal consequences of the reconstructed local lists.
The original entrance has 259 joint auxiliary vectors; 36 survive all the
previously proved residual point facts. Those vectors encode memberships,
not finitely many physical packings. The proof below is continuous on every
configuration represented by them.

We divide only according to whether the actual top square Q11 contains
G4=(1.74,3). Failure of strict membership, including boundary contact, belongs
to the first branch.

## 3. First branch: Q11 excludes (1.74,3)

### 3.1. A genuine top-wall advance

Apply Theorem 1 of
[C974-C976-CONTINUOUS-REDUCTIONS.md](../C1089/reference/recovered-lemmas/C974-C976-CONTINUOUS-REDUCTIONS.md)
to Q11 in coordinates

    (xi,eta)=(4-y,x).

Its strict anchors and exclusions are exactly:

| Local datum in the wall theorem | Original physical datum |
|---|---|
| Owns (.914,2) | Q11 marker (2,3.086) |
| Owns (1,2.4) | Q11 point (2.4,3), from (3) |
| Excludes (1,1.74) | Q11 excludes (1.74,3), this branch hypothesis |
| Excludes (1.65,2.35) | E marker (2.35,2.35) |
| Closure in xi>=0 | Q11's actual top wall y<=4 |

The theorem concludes

    (2.56,3) strictly in Q11.                              (4)

Consequently (2.5,3) is strict there as well. No inward-auxiliary exclusion
from Q11 is required for this wall theorem.

### 3.2. The two central squares meet the common-cycle hypotheses

Transpose the whole physical configuration by

    tau(x,y)=(y,x),

and set C=tau(S), B=tau(E). In this paragraph only, coordinates are transposed.
Then C strictly owns

    (2,2),(1.5,2),(2,2.5),(1.65,2.35),                    (5)

and excludes (1.65,1.65), strictly in tau(A), and (2.35,2.35), strictly in B.
It excludes the entire segment

    {1} x [2.26,2.8],                                   (6)

which is strictly in tau(Q9), not in a fictitious wall.

The upper square B strictly owns

    (2.35,2.35),(2.26,3),(2.4,3),                        (7)

and excludes the five points required by Theorem 1 of
[C981-COMMON-CYCLE.md](../C1089/reference/recovered-lemmas/C981-COMMON-CYCLE.md):

| Transposed excluded point | Actual original source |
|---|---|
| (2,2.4) | S: (2.4,2), on its strict center-to-crosspoint segment |
| (2,3) | Q10: (3,2) |
| (3,2.4) | Q11: (2.4,3) |
| (3,3) | Q2: (3,3) |
| (3,2.56) | Q11: (2.56,3), proved in (4) |

Thus that theorem and its Corollary 4 prove

    X0=(2,2.62) strictly in B,                            (8)

exclude an axial B, and, if B has positive canonical frame (b,t), give

    t/(1+b)>7/18.                                        (9)

If C has nonnegative canonical angle, Theorem 5 of the same chapter applies
with (5), the two actual foreign central markers, and the actual segment (6).
It puts the same X0 strictly in C. This contradicts disjointness. Importantly,
Theorem 5 needs **no foreign diagonal segment** and no particular auxiliary
set for N or A. Therefore C must have strictly negative canonical angle.

### 3.3. Both orientations of B now contradict disjointness

Rotate the transposed configuration through a quarter turn. In original
physical coordinates this combined map is simply

    sigma(x,y)=(4-x,y).

A quarter turn preserves signed canonical orientation modulo the square's
quarter-turn face relabeling. The relevant squares sigma(S), sigma(E) satisfy:

    sigma(S) owns (2,2),(2,1.5),(1.5,2),(1.65,1.65);
    sigma(S) excludes (2.35,1.65), strictly in sigma(A);
    sigma(E) owns (1.65,2.35),(1,2.26),(1,2.4).

If B has positive canonical angle, apply Theorem 3 of
`C981-COMMON-CYCLE.md`. Its additional B exclusions are

    (1.5,3) <- Q11's original (2.5,3),
    (1,3)   <- Q2's original (3,3).

It gives t/(1+b)<=7/18, contradicting (9).

If B has strictly negative canonical angle, apply the complete
negative/negative theorem in Section B of
[C981-RETAINED-CONTINUOUS-LEMMAS.md](../C1089/reference/recovered-lemmas/C981-RETAINED-CONTINUOUS-LEMMAS.md).
Its three additional B exclusions have the literal original sources

    (1.6,3) <- Q11's (2.4,3),
    (1,3)   <- Q2's (3,3),
    (.914,2)<- Q10's (3.086,2).

This theorem gives a contradiction. Axial B was already excluded. All
canonical orientations, including diagonal representatives and weak support
contacts, are therefore impossible in the first branch.

This one point-level argument closes all **31** residual vectors for which
Q11 excludes G4. It does not assume A's auxiliary G3 membership, and so replaces
the need to handle that membership in a separate branch.

## 4. Second branch: Q11 strictly contains (1.74,3)

### 4.1. A mixed span forces the other northwest auxiliary

N excludes (1.74,3), since that point is strict in Q11. By (2), its only
possible labels are now

    8200={F3,G3},    8232={F3,F5,G3}.

In particular N strictly owns both (1.6,3) and (1.74,2).

Suppose N does not own F5=(2,2.26), i.e. it has label8200. Apply the complete
[MIXED-SPAN-FOUR-POINTS.md](../C1089/reference/recovered-lemmas/MIXED-SPAN-FOUR-POINTS.md)
theorem to tau(N). Its two strict anchors and four exclusions are:

| Point in that theorem | Original physical datum |
|---|---|
| Owns (2,1.74) | N owns (1.74,2)=G3 |
| Owns (3,1.6) | N owns (1.6,3)=F3 |
| Excludes (2.26,2) | N excludes (2,2.26)=F5, the current supposition |
| Excludes (3,1.74) | Q11 owns (1.74,3)=G4 |
| Excludes (2.26,1) | Q8 owns (1,2.26)=F1 |
| Excludes (2.4,1) | Q8 owns (1,2.4)=G1 |

The theorem is an all-angle contradiction using isolated excluded points;
no common owner of all four exclusions is required. It follows that

    N owns (1.6,3),(1.74,2),(2,2.26),                     (10)

and its label is8232. This removes four of the five residual vectors in the
second branch.

For reproducibility, the only remaining joint auxiliary vector is

    (4100,0,0,0,1025,65552,524800,8232,
     2050,32832,262400,147584).                           (11)

We do not infer a packing from this vector. Its entire continuous realization
set is excluded below.

### 4.2. The merged marker replaces the missing singleton seed

Since N owns (1.74,2), the actual merged square A excludes it. It also excludes
(1,1), strictly in Q0. A strictly owns **both** (.914,1) and (1.65,1.65).
The new [merged-marker corner-seed theorem](proofs/MERGED-MARKER-CORNER-SEED.md)
therefore gives

    Z=(.76,1.87) strictly in A.                           (12)

Here is the essential exact calculation. Translate by -(1,1). A owns
H=(-.086,0), M=(.65,.65), excludes O=(0,0), G=(.74,1). A nonpositive canonical
frame would put O strictly between H and M in both projections, so the frame
is necessarily positive. If U,V are its lower faces, O's exclusion gives
V>=0, while G's three other strict bands force U+a<=.74c+s. For
Z=(-.24,.87),

    u(G)-u(Z)=.98c+.13s <=sqrt(.9773)<1<a,
    v(Z)=.87c+.24s       <=sqrt(.8145)<1<V+a.

These give the lower u- and upper v-bands of Z; its remaining strict bands
follow from M and H because .89c-.22s>0 and .87c+.154s>0. Thus (12) is strict.
The linked lemma proves every band and both canonical signs explicitly.

Now apply Theorem 4 of
[C981-WALL-CYCLES.md](../C1089/reference/recovered-lemmas/C981-WALL-CYCLES.md)
to the actual Q8. It owns (.914,2),(1,2.4), lies in the real half-plane x>=0,
and excludes

    (1,1.74),(.76,1.87) in A,
    (1.65,2.35) in N.

It follows that

    {1} x [2.26,2.8] strictly in Q8.                      (13)

This is the missing long wall segment. The proof has not relabeled A as a
singleton, has not discarded its central marker, and has not applied a
whole-family C981 theorem to a different marker family.

## 5. Complete continuous ending of the exceptional vector

For clarity, we now state every actual point and wall used by the retained
angular lemmas. Apply the single isometry

    chi(x,y)=(2-x,y-2)

simultaneously to the entire configuration. It is the transposition and
quarter turn used above, followed by translation by -(2,2). Use the actual
squares

    C=chi(S),  B=chi(E),  D=chi(N),  W=chi(Q11).

D is a new local name for the northwest square; it is not the merged A.
The table below lists the full input geometry.

### 5.1. Strict points, actual excluded points, and whole segments

| Square / datum in chi coordinates | Actual original source |
|---|---|
| C owns O=(0,0) | S: (2,2) |
| C owns E0=(-.5,0) | S: (2.5,2) |
| C owns P0=(0,-.5) | S: (2,1.5) |
| C owns MC=(-.35,-.35) | S marker (2.35,1.65) |
| C excludes B0=(-.35,.35) | E marker (2.35,2.35) |
| C excludes G=(.35,-.35) | **A marker (1.65,1.65)** |
| B owns H1=(-1,.26), H2=(-1,.4) | E: (3,2.26),(3,2.4) |
| B owns MB=(-.35,.35) | E marker (2.35,2.35) |
| B excludes (-1,0) | Q10: (3,2) |
| B excludes (-.4,0) | S: (2.4,2), on its strict segment |
| B excludes (-1,1) | Q2: (3,3) |
| B excludes (-.4,1) | Q11: (2.4,3) |
| W owns (-.4,1),(.26,1) | Q11: (2.4,3),(1.74,3) |
| W excludes (.4,1) | N: (1.6,3) |
| W closure lies in y<=2 | Q11's actual top wall y<=4 |
| D owns P=(0,.26), Q=(.26,0), MD=(.35,.35) | N: (2,2.26),(1.74,2), its marker |
| D excludes O | S: (2,2) |
| D excludes (.26,1) | Q11: (1.74,3) |
| D excludes {1} x [.26,.8] | Q8's whole segment (13) |
| C excludes [-.8,-.26] x {-1} | Q9's whole [2.26,2.8] x {1} |
| C excludes {-1} x [-.56,0] | Q10's whole {3} x [1.44,2] |
| C excludes the whole segment from (0,.26) to (.26,0) | Both endpoints and entire segment strictly in D |
| C excludes (.26,-1) | Q0: (1.74,1) |

All four squares are actual congruent squares, and every named pair has
disjoint interiors. No additional geometric assumptions are hidden in this
table. In particular, the formerly missing southwest marker in the C981
application is now a **strict foreign A point**, which is all the local
angular theorems require.

### 5.2. B cannot have nonpositive canonical angle

Its two short chords, at x=-1 and x=-.4, have lengths at most one from the
four displayed excluded endpoints. The strict anchors make both chords
nonempty. An axial square of side a>1 cannot have either such chord, so B is
not axial.

Suppose B has negative canonical angle. First suppose C has nonnegative
canonical angle. In the transposed, untranslated coordinates used in Section
3, Theorem 2 of `C981-COMMON-CYCLE.md` applies to tau(S). Its strict center and
crosspoints are already proved; its whole left segment comes from Q9; its
whole diagonal excluded segment comes from N's strict G3,F5 in (10); and its
foreign southwest marker is strictly in A. It proves

    (2,2.65) strictly in tau(S),

or equivalently (-.65,0) strictly in C.

The negative-sign part of Theorem 1 of that chapter puts the same transposed
point (2,2.65) strictly in tau(E), hence (-.65,0) in B. That part of its proof
uses only the four short-chord exclusions; the fifth, farther wall exclusion
is used only for the **positive** orientation and is not imported here.
This is a duplicate strict point, impossible.

If C and B both have negative canonical angles, use the retained complete
negative/negative two-square theorem. Its C inputs are O,P0,MC and the actual
foreign marker G. Its three additional B exclusions, in chi coordinates, are

    (-.4,1),(-1,1),(-1.086,0).

They come from Q11's (2.4,3), Q2's (3,3), and Q10's (3.086,2), respectively.
This is exactly Section B of `C981-RETAINED-CONTINUOUS-LEMMAS.md`, translated
by -(2,2). It gives another contradiction.

Therefore B has strictly positive canonical frame (b,t).

### 5.3. The actual top wall forces t>1/2

Apply Theorem 1 of
[C981-LAST-TWO-CYCLES.md](../C1089/reference/recovered-lemmas/C981-LAST-TWO-CYCLES.md)
to the actual B,W. Its strict B points, four B exclusions, the two strict W
anchors, the excluded W point, and the real W wall are exactly those in the
table in Section 5.1. The theorem covers every orientation of W and all weak
separating supports. It yields

    t>1/2.                                                (14)

Here t is the sine component of B's positive canonical frame, not its
half-angle parameter.

### 5.4. A nonpositive C forces t<1/2

If C has nonpositive canonical frame, apply Theorem 2 of
`C981-LAST-TWO-CYCLES.md`. Its strict C anchors are O,E0,P0,MC; its three
C exclusions are

    G=(.35,-.35) in chi(A),
    (.26,0) in D,
    (.26,-1) in chi(Q0).

Its B inputs are the displayed MB,H1,H2 and exclusions (-.4,1),(-1,1).
Every premise is present, so the theorem gives t<1/2, contradicting (14).
This includes an axial C.

### 5.5. A positive C also forces t<1/2

Suppose C has positive canonical frame (d,r). Apply Theorems 1 and 2 of
[C981-OPPOSITE-CENTRAL-ANGLE.md](../C1089/reference/recovered-lemmas/C981-OPPOSITE-CENTRAL-ANGLE.md),
with the theorem's square named A replaced by our actual D=chi(N).

Theorem 1 uses D's three anchors, its exclusions O and (.26,1), and its whole
excluded segment {1} x [.26,.8]. It bounds the lower positive-face offset e
of D by

    0<=e<17/500.

Theorem 2 uses actual D,C disjointness, their common side
1<a<=1001/1000, C's four displayed anchors, its two foreign central markers,
and the two whole bottom/left segments in the table. It concludes

    0<=r<8/25.                                            (15)

The same positive-C point theorem used in Section 5.2 applies independently
of B's orientation and gives (-.65,0) strictly in C. The whole diagonal
segment from (0,.26) to (.26,0) lies strictly in the actual D.

Consequently every premise of Theorem 3 of `C981-LAST-TWO-CYCLES.md` holds:
C has the bound (15), owns O,(-.65,0),P0,MC, excludes the two actual foreign
central markers and the whole D segment, and B satisfies its strict-anchor
and four-exclusion hypotheses. That theorem gives

    t<1/2,

again contradicting (14).

Every canonical sign of both C and B has now been excluded. Thus (11) has
no continuous geometric realization. This completes the second branch.

## 6. Exhaustiveness and conclusion

Every putative realization of the exact C1091 family enters the previously
proved local catalogue. The first seven closed wall-sign patterns have the
contradictions in Section 2. Every remaining realization satisfies all the
strict residual points used here.

For such a realization, either G4=(1.74,3) is outside the open top square,
in which case Section 3 contradicts disjointness, or it is strictly inside
that square. In the latter case the mixed-span theorem forces (10), the new
merged-marker seed proves the missing long left-wall segment, and Section 5
excludes all its continuous angle possibilities.

Hence there is no realization of the exact family, proving the theorem. ∎

The residual arithmetic ledger is a check on this logical partition:

| Residual membership alternatives | Continuous ending | Count |
|---|---|---:|
| Q11 excludes G4 | Common-cycle point/support ending, Section 3 | 31 |
| Q11 owns G4 and N omits F5 | Mixed-span theorem, Section 4.1 | 4 |
| Q11 owns G4 and N owns F5 | Merged-marker seed and angular ending, Section 5 | 1 |
| Uncovered | None | **0** |

These are counts of joint auxiliary encodings, not a discretization of
positions or angles. Boundary contact is assigned to the exclusion branch;
the local lemmas explicitly retain weak face/support inequalities. The
positive-C exceptional ending is the only new terminal step using the
already permitted upper cap a<=1001/1000.

## 7. What is new and what is reused

The new mathematical work is the complete two-way residual split, the
four-point-to-corner-seed theorem, and the literal mapping of the resulting
actual squares into the existing continuous endings. In particular:

* The top-wall branch can close without first forcing N's G4 membership.
* The exceptional branch does **not** need a proof that the left-wall origin
  belongs to Q8. The long segment ending at (1,2.8) is enough.
* C1091's extra marker gives (.76,1.87) when G3 is foreign; that supplies the
  singleton-style wall input without incorrectly making A a singleton.
* The C981 local support theorems require the southwest central marker to be
  excluded from their participating central squares, not globally absent.
  Its genuine owner A supplies precisely those exclusions here.

The common-cycle, mixed-span, wall-advance, and angular support lemmas are
retained mathematical results, not newly claimed inventions. Their complete
proofs are included under `../C1089/reference/recovered-lemmas/`. The actual
input maps above, rather than similar case numbers or label patterns, justify
each use. The prior entrance and seven-sector proofs remain necessary parts
of the full theorem and are preserved in this package.

## 8. Reproduction and verification boundary

From `results/C1091`, run:

```sh
python3 checks/run_completion_checks.py
```

The runner repeats the original exact entrance/new-lemma suite, independently
checks the new rational norm and polynomial identities, checks the complete
31+4+1 partition, verifies coordinate/owner maps and whole-segment sources,
and performs deliberate-corruption rejection tests in both ordinary Python
and `python -O`. Its actual receipt is
`checks/completion-suite-receipt.json`.

These are exact arithmetic, finite membership, and source-map checks. They
are **not** a general proof checker for the retained continuous geometry.
The geometric theorem is established by the written proofs and their
explicitly checked premises. No sampled-angle feasibility search is used as
evidence of exclusion. No Lean compilation, historical 148-operation replay,
repository push, or formal row adapter is claimed.

The original task's mathematical family obligation is discharged. Its
separate Lean row575 adapter and trust/acceptance audit remain formalization
work for the downstream integration, not an unresolved geometric branch.
