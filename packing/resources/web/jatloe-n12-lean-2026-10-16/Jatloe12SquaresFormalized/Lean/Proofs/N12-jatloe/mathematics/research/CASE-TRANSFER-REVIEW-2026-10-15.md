Current source follow-up: C896, C975 and C983 are now registered through
complete original-case source endings. The assembly has112/117, with
683,700,867,868,972 still pending. See [the follow-up argument](THREE-MORE-CASE-ENDINGS-2026-10-15.txt)
and [current continuation](../../handoff/THREE-MORE-CASES-2026-10-15.txt).
The dated analysis below is retained as historical mathematical context.

# Transfers from the four new case proofs

The C1089, C1090, C1091 and C1092 deliveries give useful reductions for the
other thirteen case handoffs. The strongest immediate findings are a common
wall-center reduction for all thirteen, a new unconditional C975 ownership
cut, and a compulsory C896 entrance. They do not by themselves exclude all
thirteen families.

C580 and C581 already have a complete matching entrance and terminal in the
current Lean source; their next step is composition. C974's local terminal
and C976's complementary angle endings have completed mathematical text,
while their original-family entrances and source joins still need integration.
C981 needs coverage and assembly of its existing representative proofs.
These should not be assigned as thirteen independent requests for new
terminal mathematics.

All coordinates below are exact rationals. Ownership is strict interior
membership. An exclusion includes boundary contact. Every segment used as a
foreign bar belongs to one named actual square.

## Scope and source state

This review covers C580, C581, C683, C700, C867, C868, C896, C972, C974,
C975, C976, C981 and C983 in `mathematical-gap-handoffs`. It compares the
dated handoffs with live source on branch
`codex/n12-initial-programs-2026-10-14`, based on commit `496092631bc2`
and the current source additions. In that source snapshot the original-case
registry still has 17 pending IDs. A mathematical deduction below does not
change that count until its actual-owner proof and case adapter are written.

The eight supplied documents are preserved unchanged under
`mathematics/current/proofs`. This review is a separate research note; it
does not revise the authors' text or adopt commands and reported receipts
inside those documents as instructions or verification results.

The geometric deductions use the completed continuous lemmas in the local
mathematical library. Their Lean translations are source-written and
uncompiled. No compiler, catalogue replay or numerical search was used for
this review.

## A common reduction for all thirteen cases

Every one of the thirteen families has separate actual singleton masks 1
and 2. Their exact singleton seeds give

```
Q_1 owns (1.74,1),
Q_2 owns (1,1.74).
```

Here subscripts are masks, not ascending owner indices. Each family also
has a bottom owner B with mask 8192, except C581 where its mask is 8196.
The left owner L has mask 4096, except C976 where its mask is 6144.

The wall-sign chord theorem says that a square W of side greater than one,
with its genuine wall x>=0, strict marker (.914,2), omitted marker
(1.65,2.35), and center height at least 2, strictly owns

```
{1} x [2.22,2.39].
```

It includes equality of the center sign. Its source entry is
`Compact/Geometry/WallSignChord.lean`, theorem `WallSignChord.chord`.

### The actual left center is strictly above 2

Suppose the actual L center has Y<=2. Apply the chord theorem to the
same square in coordinates `(x,y) -> (x,4-y)`. Its marker stays fixed,
its center height is 4-Y>=2, and its required omitted marker becomes
the original southwest central marker (1.65,1.65). That marker is omitted
by both masks 4096 and 6144, from their exact marker signatures.

At the chord parameter 2.26 the theorem gives original (1,1.74) strictly
in L. It is also strict in distinct actual Q_2, a contradiction. Therefore

```
centerY(L)>2.
```

For mask 4096 the original northwest central marker is omitted as well.
Applying the chord theorem without reflection now gives the entire strict
upper chord `{1} x [2.22,2.39]`, in particular F1=(1,2.26).
For C976, mask6144 actually owns that northwest marker. Its center
inequality still follows, but this second chord application does not.

### The actual bottom center is strictly right of 2

Suppose centerX(B)<=2. Use the chart with original coordinates
`(4-y,x)`. The bottom marker becomes (.914,2), the real bottom wall
becomes the real left wall, the center height becomes 4-centerX(B), and
the required omission again is the original southwest central marker.
Both bottom masks 8192 and 8196 omit that marker.

The parameter 2.26 gives original (1.74,1) strictly in B, contradicting
its strict ownership by Q_1. Hence centerX(B)>2.

Now transpose B, using original coordinates `(y,x)`. The required omitted
marker becomes the original southeast central marker (2.35,1.65), omitted
by both bottom masks. The theorem gives

```
[2.22,2.39] x {1} strictly in B,
G5=(2.26,1) strictly in B.
```

No F6 ownership premise was needed. If F6=(2.4,1) is subsequently forced,
the standard wall-advance theorem, with Q_1's off-row seed (1.87,.76),
gives (2.8,1). Convexity in that same B gives the longer bar
`[2.26,2.8] x {1}`.

These are statements about centers and actual physical pullbacks. They do
not assert canonical square-angle signs or identify different marker families.

## A new unconditional C975 cut

Use actual masks A=256, S=512, E=1024, T=34816, B=8192 and R=16384.
The existing `C975Entrance.compulsory` supplies A's F4/G3, S's F8 and
G6-or-G8 cover, E's F5-or-F7 and G6-or-G7 covers, B's F6/G5 and R's
F9/G9. T strictly owns the northwest central marker as part of its genuine
merged signature. It is a foreign point for A, S and E.

1. The actual mask2 singleton owns (1,1.5),(1,1.6) by its vertical
   seed segment. The actual mask1 singleton owns (1.5,1),(1.6,1) by its
   horizontal seed segment. The all-angle central-crosspoint theorem,
   under a half-turn and a swapped half-turn, therefore gives
   A(2,1.5) and A(1.5,2). The other omitted central markers belong to
   actual S and T. No missing-marker segment is assumed.
2. If S omitted G8, its cover would give G6. The elbow-point theorem
   applied to S's actual marker, F8 and G6, with G8 omitted and actual
   E/R markers foreign, gives S(2,1.5). This conflicts with step 1.
   Thus S strictly owns G8.
3. The bottom wall-advance theorem gives B(2.8,1). Together with its
   strict G5 it supplies the genuine whole bar `[2.26,2.8] x {1}`.
4. Apply the new northeast-selection lemma to the actual S,E. Its lower
   bar is in B; its two southeast corner points are in actual mask12;
   its right marker and F9/G9 are in actual R; its northwest marker is
   in actual T. These are distinct foreign owners wherever required.
   Its two covering alternatives are exactly those of the current
   C975 entrance. Consequently

```
E strictly owns G7,
E owning G6 implies E owns F7.
```

5. T therefore omits G7. The existing complete top G alternatives are
   `{G4}` and `{G4,G7}`, so its complete G set is now exactly `{G4}`.
   If T owned F7, its strict G4-to-F7 segment would strictly contain G7,
   contradicting E's ownership. Thus T also omits F7.

This removes a real optional top branch that remained live in the old
handoff. Two further direct consequences sharpen the result:

* E must also own F7. Otherwise its F cover forces F5. The quarter-turned
  elbow theorem gives E(2.5,2) and E(2.525,2.125). If S owns G6, the
  crossed-elbow obstruction at its closed parameter .8 uses the first
  point, actual A(2,1.5), and actual B(2.8,1) to contradict S's data.
  If S omits G6, the reflected outward-bar theorem puts the identical
  sharp point (2.525,2.125) in S. Both alternatives contradict disjointness.
  The elbow theorem's northwest and top marker exclusions both have the
  legitimate foreign source T; they need not have different foreign owners.
* E cannot own both F5 and G6. The existing
  `C975IncomingPair.incoming_forces_top_seven` would put G7 in T, already
  excluded by E's strict G7.

Thus E owns F7/G7; its extra F5 and G6 cannot occur together. This does
not yet exclude C975. The remaining actual S/E/T/R support configurations
still require an ending. The C1090 upper-point joins require an actual
T(2,3); their earlier producer used a separate northwest square. A direct
common-cycle assignment to T would require the west point (1.5,2), which
is actually in A, so that assignment cannot be used.
In particular the new C1092 squeeze cannot simply be inserted: its
southeast profile owns F4, whereas C975's F4 is already in distinct A.

Source interfaces: `FiniteCases/C975Entrance.lean`,
`FiniteCases/C975IncomingCut.lean`, `C981/Crosspoint.lean`,
`OtherCases/ElbowPoint.lean`, `C981/WallAdvance.lean`, and
`OtherCases/C1090/NESelection.lean`, under `Compact/Completion`.

## A compulsory C896 entrance

C896's ordinary F owners have exactly one F point; its G sets can have
two points. The existing domain soundness results and singleton seeds
make the conditional handoff cuts into the following actual-owner chain.

| Actual mask | Forced strict auxiliary points |
|---|---|
| 1 | F2, G2 |
| 2 | F0, G0 |
| 16 | F7, G7 |
| 8192 | F6, G5 |
| 4096 | F1, G1 |
| 32768 | F3, G4 |
| 2048 | F5, G3 |
| 1024 | F9 |
| 16384 | F8, G8 |
| 768 | F4 |

The first two rows are the genuine singleton seeds. The singleton16 is
the half-turn of singleton1, giving F7/G7. Foreign F2 forces the bottom
row through `bottom_forced`; foreign F0 forces the left row through
`left_forced`; foreign F7 forces the top row through `top_forced`.
The northwest square now omits F1,F3,G1,G4, all strictly in the named
foreign walls, so `northwest_forced` gives its F5/G3.
The northeast F domain has alternatives F5,F7,F9; the first two are
foreign, leaving F9. `right_forced` then gives the right wall F8/G8.
Finally the F2 census forces ordinary merged768 to own one F point.
All nine other F points have strict foreign owners in this table, so
that point is F4.

The domain source is `Compact/Completion/FiniteCases/C896Domains.lean`.
This is a completed entrance deduction, not a geometric contradiction.
Genuine bottom and left wall bars can now be supplied by the common
wall arguments. The remaining ending must couple the lower merged768
square to the two upper central squares and the real walls. The complete
two-point G alternatives must be preserved.

The right wall's elementary advance is to height 1.44, giving its lower
bar through 1.74; it is not the upper right bar used in C1090. A rotated
merged-near-point application would require merged768 to omit G6, which
the compulsory table does not prove. Northeast selection's southeast F8
anchor is also unavailable in merged768: that point is already strict in
actual right16384.

## What the terminal lemmas would still need

### A precise eight-point target for C983 F4

The remaining C983 branch has merged2304 exactly `{F4,G3}`. Its northeast
square E already owns F7,G7, so northeast selection alone adds no missing
terminal fact. Apply the eight-point obstruction in coordinates

```
(xi,eta)=(3-y,x-2).
```

Its two strict anchors are E's actual marker and G7. Four required
exclusions have genuine sources:

| Original excluded point | Actual source |
|---|---|
| (2,3) | top origin |
| (3,3) | paired northeast corner |
| (3,2.56) | right-wall advance |
| (3,2.26) | right F9 |

Precisely two further exclusions would finish this route:

```
E excludes (2,2.5),
E excludes (1.96,2.73).
```

Neither follows from the current merged-owner point APIs. In particular
the point (2,2), available under an additional singleton-corner premise,
does not establish either exclusion. This gives a small explicit target
for outside mathematical work without claiming it has been proved.

The C1092 squeeze also fails a literal input here: actual southeast512
omits F4 because that point is strict in merged2304. The C1090 residual
argument cannot treat the merged southwest/northwest square as two
distinct disjoint owners.

### Why the new squeeze is not a universal right-side ending

In the translated chart centered at (2,2), its southeast profile owns
I=(0,-.26) and has upper V face H<=0 and a coupled floor. Its northeast
profile has U_N>=.4t, a specific positive half-angle interval, and the
strict point (.47,.12). Its one actual right wall contains the whole
vertical bar from height 1.74 to 2.4 in original coordinates and has
center height at least 2. These are necessary inputs, not consequences
of merely possessing a wall marker.

For C700, southeast/northeast markers belong to the same actual1536.
The southeast cap H<=0 excludes that square's strict northeast marker,
whose V value is .35(c-s)>0. The northeast lower-V cap similarly excludes
its southeast marker. Also the actual right center is strictly below 2,
as forced by singleton32 and the reflected chord argument.

For C683, C867 and C868, candidate northeast3072 also contains the
northwest marker (-.35,.35). Its U_N value is .35(t-b)<=0, contradicting
the required U_N>=.4t>0. The original marker must be retained; canonical
face relabeling cannot remove it. C683 additionally lacks an ordinary
right-wall owner with the required lower bar.

For C972 the central squares are separate, but the new southeast angle
and coupled-floor profile, northeast angle/faces/sharp point, and full
right-wall profile still have no established entrance here. Its missing
top owner cannot be supplied by a top-wall argument from another family.

C868 does have one additional genuine right-wall deduction. Its merged
right16416 owns markers (3.086,2),(3.086,3). A normalized square's vertical
half-width is at most a*sqrt(2)/2<3/4, so these anchors force its center
height into (2.25,2.75). The reflected chord theorem gives its strict
`{3} x [2.22,2.39]`. Its existing same-owner wall-bridge seed supplies
`{3} x [2.25,2.75]`; the union is the whole strict
`{3} x [2.22,2.75]`. This does not supply the squeeze's lower endpoint
1.74. Ordinary right16384 in C867 does not have the extra marker5.

### Useful bars in C683

Its actual singleton32 has strict seeds (3,2.88),(3,2.26),(3.24,2.13).
Its actual singleton16 has strict seeds (2.88,3),(2.26,3),(2.13,3.24).
These are simultaneous transforms of the genuine singleton seed theorem.
Convexity in each same owner gives

```
{3} x [2.26,2.88] strictly in mask32,
[2.26,2.88] x {3} strictly in mask16.
```

Thus merged3072 omits F7/G7/F9/G9. These are valid outer bars even
though the ordinary right-wall mask is absent. They do not contain the
lower portion of the right bar required by the new squeeze.

## Disposition of every case

| Case | Finding | Work still required |
|---|---|---|
| C580 | Current three-square entrance matches the complete negative triple ending, including central disjointness. | Compose, supply row321 adapter, then eventual Lean acceptance. |
| C581 | Same complete composition with its own bottom mask8196. | Compose independently for row322 and eventual Lean acceptance. |
| C683 | Common wall-center cuts and genuine singleton upper/right bars transfer. | A merged-upper ending or authenticated missing proof source. |
| C700 | Common wall-center cuts transfer; top center<2 and right center<2 follow from its northeast singletons. | Ending with actual merged1536 and ordinary left4096; C702's extra NW marker is unavailable. |
| C867 | Common wall-center cuts and top center<2 transfer. | Actual merged-upper ending with ordinary right16384; C868's extra right marker is unavailable. |
| C868 | Common wall-center cuts, top center<2, and the genuine right bar [2.22,2.75] transfer. | Both surviving canonical-sign sectors, retaining the singleton corner alternative and merged3072. |
| C896 | The full compulsory entrance above follows from genuine seeds and current certified domains. | Coupled all-angle ending; preserve optional G memberships. |
| C972 | Common bottom/left center and chord cuts transfer. | Genuine family entrance and ending without an ordinary top32768. |
| C974 | The later THREE-SQUARE-ENDING chapter closes both local missing-corner roots; its local Lean translation is present. | Supply original-family coverage, stronger singleton-seed producers and actual-owner joins. |
| C975 | New SE G8, NE F7/G7, top exact G={G4}, no top F7, and no NE F5/G6 pair. | Exclude remaining actual support/ownership alternatives. |
| C976 | Common center cuts remain valid for6144. Later chapters already give both complementary angle endings. | Translate the negative actual-owner join and authenticate/assemble the finite entrance; no new terminal is currently localized. |
| C981 | Existing representative mathematics is supplied; common cuts may simplify its entrance. | Actual-assignment coverage, complete source integration and eventual replay. |
| C983 | F5 is already source-closed; F4 has the explicit two-exclusion eight-point target above. | Prove those exclusions or another full F4 ending, then original row514 assembly. |

The C580/C581 composition is exactly

```lean
obtain ⟨E,N,R,input,apartEN,_,_,_⟩ :=
  C580581TripleEntrance.entrance v p hf
exact C983.NegativeTripleEnd.impossible E N R input apartEN
```

with v=0 for C580 and v=1 for C581. This supplies no new assumption.
The ending dispatches all four surviving separating-face combinations.

C974's later `C974-THREE-SQUARE-ENDING.md`, especially its final original
applications, supersedes the older note that stopped after the second-root
midpoint. The local contradiction still needs the genuine strong singleton
seeds and original entrance. `OtherCases/C983/C974LocalEnding.lean` is a
generic local theorem; its C983 wrappers are not C974 family coverage.

C976's later `C974-C976-CONTINUOUS-REDUCTIONS.md` sections 5-6,
`C976-MERGED-LEFT-ENDING.md`, `C976-LEFT-TOP-ANGLE.md` and
`C976-NEGATIVE-NE-TOP-ENDING.md` explicitly complete its two necessary
central alternatives for every northeast/top angle sign. They retain
the northwest marker in the actual merged left6144. The existing
`C976MergedLeft.ActualOwners` nonnegative ending and `C976LeftTop.ActualOwners`
are partial source integration of those texts. The eleven old residual IDs
must still reach the genuine entrance; this review does not substitute a
count or a point-hull relaxation for that proof.

There is also a small source correction in C868's
`Compact/Cases/C868/NegativeCornerSector.lean`: the foreign point
(2,.914) was attributed to mask12 in the call to
`SouthwestNegativeCorner.point`. It is the original bottom-wall marker
of actual8192. Both the disjointness application and strict seed source
must use8192. This repairs owner provenance; it does not close either
remaining C868 sector.

## Formalization priorities after this review

Write the common wall-center/chord reduction once, with actual-owner adapters;
write the new C975 cut and C896 compulsory entrance; compose the existing
C580/C581 source endings. Resume the completed C1090 entrance and C1091
merged-marker seed translations alongside those small shared additions.
Keep C1092's newly supplied squeeze and its actual entrance as separate
formalization obligations. No enlarged proof forest or new certificate
generation is needed for these steps.

The whole-proof hard limit remains 10000 modules including libraries, with
8000 preferred. The previous complete selected source inventory was 8302;
it must be refreshed after the new source additions. Mathematical progress,
written Lean, static source review and eventual kernel acceptance remain
distinct statuses.

## Source work completed after the comparison

The requested formalization has resumed. The common reduction is now in
`CommonCases/WallSignFromSingleton.lean`; the C975 cuts are in the three
`FiniteCases/C975Selection*.lean` modules, and the C896 deductions are in
`FiniteCases/C896Entrance.lean` and `C896WallBars.lean`.

C580 and C581 now have unconditional case declarations and row adapters in
`FiniteCases/C580581Completion.lean`. A further source simplification also
closed C1090's complete entrance: `C1090/DirectDomains.lean` instantiates
the existing local right/top certificates with its own actual budgets;
`C1090/OriginalEntrance.lean` derives all thirteen original entrance fields
and the unconditional row574 case contract. No outside catalogue is assumed.

The source registry therefore now has 103 of 117 original case contracts
and 14 pending, including the still-open cases identified above. The new
C1091 merged-marker seed and actual-wall application are also source-written.
All these additions remain uncompiled. The refreshed selected source
inventory is 8331 modules including libraries and 455965 project source lines,
with complete source-header closure. These figures do not include unwritten
future proof work or certify kernel acceptance.

## Current source disposition after the six-case translation

The earlier snapshot counts and composition tasks above are historical. All
six requested original cases C974, C976, C981, C1089, C1091 and C1092 now
have unconditional source contracts and are registered. C580/C581 and C1090
remain registered. C1092 includes every whole-packing branch, the actual
inward-to-Ordinary reduction and the full Ordinary sign-state contradiction.
No scalar profile or unavailable mathematical certificate is assumed by its
original row576 source root. These source terms have not been compiled.

The assembly now has109 of117 original contracts. The eight remaining
mathematical targets are C683, C700, C867, C868, C896, C972, C975 and C983,
listed precisely in `../REMAINING-EIGHT.txt`. The literal owner/profile
obstructions to transferring the new squeeze, described above, still apply.
No completed ending for those eight has been inferred from a conditional
local lemma, a source-reported receipt or a foreign family's entrance.

The complete selected source-header inventory is now8609 modules including
libraries; the assembly alone has8342. Both remain below the hard10000 cap
and above the preferred8000. Future unwritten obligations are excluded from
those counts. All259 recorded mathematical source files retain their exact
hashes and sizes. Source review and preservation are not compiler acceptance
or a proof of the unrestricted global theorem.
