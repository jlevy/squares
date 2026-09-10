# H157 and Conditional-Claim Review at ee98c4ba

Retained review snapshot.
Findings and line references describe the reviewed source; the
[subsequent correction review](correction-review.md) records their disposition.
The maintained replay is `packing/devtools/replay_h157_geometry.py`. Archived Python
helpers here use `.py.txt` to preserve their original source as evidence.

W2 factual review for bead `think-9zc9`, performed read-only on repository head
`ee98c4baae876835ba44a5f127bfa73d4e838d45`. The coordinator owns bead changes and
integration. This review concerns published results, not a new research target.

The registered H157 rejection is supported: six refined subclasses retain weight ten,
and the maximum is ten.
Two mathematical explanations need correction before reuse: the claimed zero reach gain
is false for the two successful subclasses, and T2’s exact equality needs a
mark-containment premise.
The results establish obstructions on named relaxations; they do not rank all
conditional and unconditional proof strategies.

## Findings

### High: the reach calculation applies a disjoint-polygon formula to intersecting polygons

The source is [lane-x4-verify-geometry.py.txt:56](../lane-x4-verify-geometry.py.txt),
with the unconditional calls at lines 98–108. `poly_dist2` explicitly requires disjoint
polygons. Its caller always chooses source core 55 for mark m1 and core 50 for mark m2,
including children that delete those cores.

Exact SAT and convex clipping agree that `m1:J9/16` intersects core 55 and `m2:J6/16`
intersects core 50. Both intersections are triangles of strictly positive area.
Their true distance is therefore zero, while the published script prints

`75308842465387162009/335694834731568400000000 > 0`.

That number is a vertex-to-edge minimum with its disjointness precondition violated.
The actual nearest *remaining* survivor in either of these two classes has squared
distance

`154520421972020636842286626510179978387793755009897266163721/8274126656975111962857032162670705972822328494029059600000000`.

The six neutral children retain the reported positive distance to their selected
targets. The all-children identity is false.
A mark being a vertex also does not, by itself, prevent an enlarged patch from
approaching or intersecting a distant core.

The false conclusion is active in
[exp154:72](../../../experiments/exp-154-h157-sixteen-sector-refinement-limit.md),
[H157:97](../../../../../hypotheses/H-157-refined-owner-sector-patch-breaks-neutrality.md),
[H157:166](../../../../../hypotheses/H-157-refined-owner-sector-patch-breaks-neutrality.md),
and
[X026:243](../../../../../explorations/X-026-what-conditioning-does-and-does-not-buy.md).
The delivered report repeats it at lines 144–161 and wrongly says at lines 260–261 that
its distance calculation is used only for polygons already known disjoint.
Its coordinator note at lines 36–37 currently endorses the reach identity as unaffected.

**Correction:** preserve the delivered script and report, add a dated correction with
the intersecting cases and guarded receipt, and correct active mechanism summaries.
Any promoted distance tool must decide intersection first, returning zero when the
intersection is nonempty.
Distinguish distance to a fixed original target from distance to the nearest current
survivor. The H157 survivor-weight rejection remains valid.

### High: T2 infers mark containment in an arbitrary guaranteed patch without a premise

[X026:308–317](../../../../../explorations/X-026-what-conditioning-does-and-does-not-buy.md)
defines a guaranteed patch by containment in every owner core, then infers that the
patch contains a mark because every owner core contains that mark.
The inference reverses subset containment.
A chosen subset of a common intersection need not contain the mark.

There is a positive-area counterexample on the stated data.
Take the singleton pose class consisting of core 59 and let its patch be that core
scaled by `1/10000` about its bottom-left corner.
The patch lies inside core 59, contains neither bottom-left mark, and has area
`99540529/10000000000000000`. Its survivor weight is **43/4**, not ten.
Exact SAT and clipping agree.
Similar patches at two other corners leave `85/8`. The
[geometry receipt](geometry-receipt.json) preserves their rational vertices.

**Correction:** T2 can conclude `w(F) >= 10` from `F subset core59` alone.
This already suffices to obstruct a point cover of budget below ten on the declared
patch-only relaxation.
For equality, additionally require a fixed common mark `m in F`, for example by defining
`F` to be the full common intersection for a class sharing that mark.
Owning one of two corner marks is not itself a common-mark premise.

### High: the angular and pose statements need explicit domain contracts before supporting broad refinement language

[X026:292–304](../../../../../explorations/X-026-what-conditioning-does-and-does-not-buy.md)
has a valid elementary argument for the declared construction
`F_B = intersection of Q_r(m) over retained rays r in B`. For a neutral retained ray
`r0 in B`, one has `m in F_B subset Q_r0(m)`, hence survivor weight exactly ten.
Only one neutral ray is needed; the measured arc width is not a necessary premise.
This concerns the finite retained signed-ray universe and that patch construction.

T2 extends the subset obstruction to any class retained in the declared pose universe
that contains core 59, with `F subset core59`. It is not a statement about arbitrary
geometry-conditioned residual domains.
If a residual model adds wall, unit-parent, joint-compatibility, or other restrictions,
the surviving family must satisfy those restrictions before weak duality applies.
A guaranteed region inside a unit parent also need not lie inside the selected B-core.
The proof’s assertion that being guaranteed is *precisely* core containment is a
definition of this restricted model, not a characterization of every occupied-region
argument.

Therefore statements such as
[X026:257–259](../../../../../explorations/X-026-what-conditioning-does-and-does-not-buy.md),
[X026:319–322](../../../../../explorations/X-026-what-conditioning-does-and-does-not-buy.md),
and
[H157:190](../../../../../hypotheses/H-157-refined-owner-sector-patch-breaks-neutrality.md)
should name the fixed relaxation instead of saying patch refinement is ruled out
throughout pose space.
The report’s current scope note retains the same overbroad phrase.
The documents already acknowledge stronger residual domains and routing elsewhere; the
theorem statement should carry those premises itself.

Core admissibility must also be separated from physical completion.
I independently verified more than the delivered B-core containment check: cores 59 and
60 each have a concentric, same-angle unit parent inside the container, with minimum
wall margin `785411/88696100 > 0`. Thus these isolated poses are unit-parent realizable.
No receipt shows completion to eleven disjoint unit parents or a physical packing forced
to use only neutral selections.
This review does not claim that the isolated poses are nonrealizable.

**Correction:** state the fixed residual domain, finite angle/pose universe, surviving
family admissibility, and common-mark premise beside each theorem.
Retain the already correct sufficient routing condition: every hypothetical physical
packing must admit an excluded valid selection.
Do not turn the failure of the stronger all-labels plan into a negative result about
every conditional strategy.

### Medium: exp154 still records the wrong aggregate metric

[exp154:90–92](../../../experiments/exp-154-h157-sixteen-sector-refinement-limit.md)
says survivor weight is *minimised* over the subclasses.
H157’s corrected criterion and the actual rejection use the maximum.
The minimum is `19/2 < 10`, so the machine-readable text describes a criterion that
these data satisfy.

**Correction:** change this active field to *maximised*, retaining the correction
history. Two subclasses satisfy the registered `at most 79/8` survivor bound more
strongly, at `19/2`; six fail.
Do not describe `19/2` as a failure to attain an exact prediction of `79/8`, since H157
registered an upper bound.

### Medium: the active reading still draws a comparative allocation conclusion from unmatched measurements

[X026:328–331](../../../../../explorations/X-026-what-conditioning-does-and-does-not-buy.md)
says the results remove the reason to prefer the conditional route.
Matching two cut maxima on one family and a count of sixteen classes do not establish
comparative runtime, attainable bound, probability of success, or the value of routing
and pruning. Calling the inference an estimate at lines 220–224 and 346–348 makes its
uncertainty visible, but does not establish the asserted allocation conclusion.

**Correction:** report the two exact cut readings and the unmeasured class-cost
assumption. State that these results do not supply a measured comparative ranking.
Any retained branch allocation can be recorded as the owner’s allocation choice with its
date, without presenting it as a mathematical consequence.

X024 already makes this correction in its
[current overview:76–91](../../../../../explorations/X-024-two-lines-at-eleven.md).
Its entire account from line 113 is explicitly marked historical.
Consequently, the old assertions at lines 349–453 and 621–627—“priced at no reach”, “a
census cannot rescue a neutral ladder”, and “an emptiness proof would rescue the classes
but not the method”—should not be recategorized as current endorsed claims.
Preserve those bodies.
The useful correction is a dated local pointer from sections 5 and 6 to the current
overview, and consistency in current downstream summaries.
A census or emptiness argument can matter to the routing condition; neither is ruled out
by this screen.

### Low: tighten two descriptions of the verification and result

- [X026:229–231](../../../../../explorations/X-026-what-conditioning-does-and-does-not-buy.md)
  says Steps 4 and 5 “close every class”.
  They establish obstructions on the named neutral relaxations and explain why the
  proposed all-class closure has not been obtained.
  Replace the sentence accordingly.
- The report’s “every headline number was read twice” at
  [lane X4:242](../lane-x4-sixteen-sectors-and-the-refinement-limit.md) is too broad.
  The clipping script validates all twelve parent/child survivor sets, but for the
  singleton sweep it clips only rays already selected as neutral by SAT
  ([crosscheck2:93–100](../lane-x4-crosscheck2.py.txt)). It confirms those 135 neutral
  rays per mark; it does not independently count all neutral rays among the other 1309
  candidates. The geometric distance claim is not independently cross-checked there.
  Describe those actual scopes.

## Confirmed Results and Replay Limits

The retained [replay instrument](replay.py.txt) adapts only the published scripts’
hard-coded host paths and preserves stdout and a
[receipt](replayed/replay-receipt.json).
It uses project Python 3.14.7. The [source manifest](source-manifest.json) records the
engine and reviewed commit parents, retained Git source identities, and actual import
origins. The imported geometry, screen, transport, and fractional code has no Git diff
between the reported engine commit `67ccd16b` and this review head.
The repository was not modified.

| Reading | Independent review result |
| --- | --- |
| Eight-bin equivalence | Zero disagreements for membership, extreme rays, polygons, IDs, and reflection pairing |
| Eight refined subclasses | Six weights of ten, two of `19/2`; generated JSON exactly matches the published JSON |
| Full 32-class sixteen-bin screen | Maximum ten, attained by six classes |
| Patch construction | Parent containment, strict area increase, and containment in all 87–94 retained quarter-cores per bin reproduce |
| Singleton scan | 1444 rays per mark; maximum ten at 135 rays per mark; minimum `33/4` |
| Clipping control | Identical survivor sets for all twelve parent/child cases; confirms all 270 SAT-selected neutral rays |
| Whole-core pose probes | Cores 59 and 60 leave ten; SAT and clipping agree on their survivor sets |
| Unit-parent check for the two poses | Concentric same-angle unit parents fit with positive wall margin; no full packing or forced routing claim |
| Reach check | Six neutral children retain the selected positive distance; two intersect their selected target, so their true distance is zero |

The five replayed scripts took about 164 seconds on this host.
This is a local replay receipt, not a comparison of research strategies or a replacement
for the original lane’s cost record.
The original command description also needs to mention adapting the hard-coded `REPO`
constant, not only `SCRATCH`, when replaying on another host.

The baseline family-depth proof and physical ownership theorem were read as inputs to
this bounded review; the review did not rerun the entire project validation suite or
establish new physical realizability constraints for the survivor families.

## Readiness

The survivor-weight result is ready to retain with the maximum criterion corrected.
The geometry explanation and the universal exact form of T2 are not ready for promotion.
After their correction, T1 and the subset part of T2 provide useful local obstruction
statements with explicit domain assumptions.
They do not settle stronger domains, owner routing, joint compatibility, richer charges,
or comparative research productivity.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
