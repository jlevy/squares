# Agenda 034, lane X4: sixteen sectors do not break neutrality, and no bin count can

Retained measurement-lane report for
[X-026](../../../../explorations/X-026-what-conditioning-does-and-does-not-buy.md) and
[`H-157`](../../../../hypotheses/H-157-refined-owner-sector-patch-breaks-neutrality.md),
run 2026-09-10 against `claude/n-11-stronger-result-d730ds` at `67ccd16b`, read-only on
the repository. The report is reproduced as delivered, with its own findings and status
labels; only its file references were rewritten to say where each file now is.
X-026 carries the coordinator’s reading, and states this lane’s two theorems — T1
(angular) and T2 (pose) — in the unconditional form, without the arc-width premise the
report uses as robustness.

All scripts and survivor families are retained beside this report; see
[Files](#costs-and-files).

**Every “closed” in the body below is narrowed to “patch refinement is ruled out as the
lever”. The corrected reading is
[X-026](../../../../explorations/X-026-what-conditioning-does-and-does-not-buy.md) §5,
escape 1.**

**Coordinator’s scope note, added on review (PR 139, finding R3).** The delivered text
concludes in several places that escape 1 of X-026 §5, and with it the conditional
point-cover line, is *closed*. That is stronger than what T1 and T2 support, and X-026
carries the corrected reading: both theorems are statements about **survivor weight on
the retained transported mass-eleven ceiling family and the screened endpoint patches**,
and what they establish is that **patch refinement is ruled out as the lever**, at every
angular resolution and at pose level.
They do not establish that the conditional strategy fails, because that strategy needs
one closed owner selection per packing rather than every class closed, and owner labels
and valid selections can overlap.
Escape 1 is therefore **narrowed, not closed**; whether the neutral classes are ever
*forced* is adjacent to escape 2 and is not settled here.
The delivered claim that Step 6’s rank-one cap `3.868983` is untouched is likewise left
as delivered and not endorsed: finding R2 holds that no conditional transfer of that cap
is established without a separate owner, class, patch and routing verification.
The measurements below — the survivor table, the reach identity, the 135 neutral rays
and the pose probe — are unaffected by either correction.

Labels: **EXACT** = a rational decision by repository primitives; **CHECKED** = a float
reading; **RECORD** = read from a file in the repository; **OPEN** = not measured.

## Verdict

**H-157 is refuted, and by more than it asked for.** Six of the eight refined subclasses
of the four neutral eight-sector classes still carry survivor weight **exactly 10**;
only two drop, and they drop to `19/2`, not to the predicted `79/8`. Step 3 of X-026
(`packing/campaign/explorations/X-026-what-conditioning-does-and-does-not-buy.md`)
stands at sixteen sectors exactly as it stands at eight.

The measurement also settles the question one resolution further out than it was asked.
Screening the **singleton limit** — one class per retained signed ray, the finest
angular conditioning that exists — leaves **135 classes per mark at exactly 10**, and
those 135 rays form a contiguous arc `34.40698` degrees wide.
Any closed angular bin that contains one of them has survivor weight exactly 10,
whatever the bin count.
**No angular refinement of the owner-sector conditioning can break neutrality**, so
escape 1 of X-026 §5 is closed at every resolution rather than only at sixteen.
**Narrowed, not closed: the lane’s “closed” means only that patch refinement is ruled
out as the lever.
[X-026](../../../../explorations/X-026-what-conditioning-does-and-does-not-buy.md) §5,
escape 1 carries the corrected reading.**

## The instrument

`packing/devtools/owner_footprints.py` hard-codes eight bins in four places
(`owner_branch_manifest` iterates `range(8)`; `_sector_contains`, `triangle_footprint`
and `endpoint_footprint` reject `sector >= 8`). The bin count was parametrised in a
scratch copy, [`lane-x4-nbins.py.txt`](lane-x4-nbins.py.txt); the tracked file was not
touched.

Sector `j` of `n` bins is the closed cone `[j*2pi/n, (j+1)*2pi/n]`. Its two boundary
rays are exact elements of `Q[sqrt 2]` for every `n` dividing 16, so membership is an
exact sign decision on `a + b sqrt 2` and no float enters any verdict.

**Control, EXACT.** At `bins = 8` the parametrised module reproduces the tracked
behaviour with zero disagreements:

| control | result |
| --- | --- |
| membership predicate, 1444 signed rays x 8 sectors | 0 disagreements with `_sector_contains` |
| `sector_endpoint_rays` over 8 sectors | 0 disagreements |
| `endpoint_footprint` polygons over all 16 classes | 0 disagreements, vertex for vertex |
| class ids and reflection pairing | identical |

**Control, EXACT.** The eight-bin screen reproduces lane X1’s recorded numbers: survivor
weight from `33/4` to exactly `10`, four classes at exactly 10 (`m1:j3`, `m1:j4`,
`m2:j3`, `m2:j4`), mean deletion `55/32`, nearest survivor to the `j3` patch at
Euclidean SAT gap `0.014978` (source index 55).

## The refinement is real, and it is sound

Refinement was not assumed to be meaningful; it was checked.
The retained signed rays span each 45-degree bin essentially in full (`delta = 44.99996`
degrees, CHECKED), so halving the bin genuinely halves the angular spread — at sixteen
bins the extreme retained rays are `22.36` to `22.39` degrees apart.

**EXACT, per refined subclass:**

- the parent patch is contained in the refined patch, vertex for vertex;
- the refined patch is **strictly** larger — 1.6165x to 1.6175x the area;
- the refined patch is contained in `Q_phi(m)`, the anchored quarter-core, for **every
  one** of the 87 to 94 retained signed rays in its closed bin, checked ray by ray.

That last check is the containment argument of the
[sector-footprint proof](../agenda-031/proofs/corner-owner-sector-footprints.md)
restated at sixteen bins and then verified rather than restated only.
The refined patches are legitimate guaranteed patches.
The mechanism the hypothesis proposed is present: the guaranteed wedge does widen from
`pi/4` to `3pi/8`, and the patch does grow by about 62 per cent in area.

## Survivor weight per refined subclass

Transported mass-eleven ceiling family
([`ceiling-family-191-50.json`](ceiling-family-191-50.json), 88 placements, weight `1/8`
each, total exactly 11, RECORD) moved to `96/25` by
`devtools.transport_ceiling_family.transport` at scale 1, then screened by
`devtools.screen_corner_dual_salvage.screen_footprint` imported verbatim — the same
orientation filter, the same strict positive SAT gap, the same container check that lane
X1 used. All 88 placements pass the orientation and containment filters, weight 11.

| refined subclass | parent | survivor weight | deletion | verdict |
| --- | --- | --- | --- | --- |
| `bottom-left:m1:J6/16` | `m1:j3` | **10** | 1 | neutral |
| `bottom-left:m1:J7/16` | `m1:j3` | **10** | 1 | neutral |
| `bottom-left:m1:J8/16` | `m1:j4` | **10** | 1 | neutral |
| `bottom-left:m1:J9/16` | `m1:j4` | `19/2` | `3/2` | broken |
| `bottom-left:m2:J6/16` | `m2:j3` | `19/2` | `3/2` | broken |
| `bottom-left:m2:J7/16` | `m2:j3` | **10** | 1 | neutral |
| `bottom-left:m2:J8/16` | `m2:j4` | **10** | 1 | neutral |
| `bottom-left:m2:J9/16` | `m2:j4` | **10** | 1 | neutral |

All EXACT. Over the full thirty-two-class sixteen-bin split the maximum survivor weight
is **exactly 10**, attained at six classes: `m1:J6`, `m1:J7`, `m1:J8`, `m2:J7`, `m2:J8`,
`m2:J9`. A case split needs every class closed, and six survive.

The two that do break delete four extra weight-`1/8` placements each — indices
`[7, 16, 29, 55]` for `m1:J9` and `[2, 22, 25, 50]` for `m2:J6` — reaching `19/2`, not
the `79/8` H-157 predicted for a patch that picks up one more placement.
The whole table is symmetric under the diagonal reflection `J -> 15 - J` with
`m1 <-> m2`, which is an internal consistency check the screen was not told to satisfy.

## Why the fatter patch bought nothing

The reach gain toward the critical survivor is **exactly zero**, and it is zero as a
rational identity, not as a float coincidence.
The squared distance from the patch to the nearest surviving core is

```
d^2 = 75308842465387162009/335694834731568400000000      d = 0.014977891
```

and that value is **bit-identical** for the eight-sector parent and for both of its
sixteen-sector children, at both marks (EXACT).

The reason is that **the closest point of the patch to that core is the mark itself**
(EXACT: the minimising vertex is `m`, and `d(m, core) = d(patch, core)` exactly).
Every patch at every bin count has the mark as a vertex, so the distance to that
placement is pinned by the mark and cannot be reduced by widening the wedge.
The patch grows only into directions that lead away from the obstruction.
H-157’s `0.015` was measured as a gap to the patch; it is really a gap to the mark, and
no angular conditioning moves the mark.

## The refinement limit: no bin count works

The finest angular conditioning available is one class per retained signed ray — the
class “`e_1` is exactly the ray `r`” — whose guaranteed patch is exactly the anchored
quarter-core `Q_r(m)`. That split is finite (1444 classes per mark) and exhaustive, and
every coarser angular partition is a coarsening of it.

**EXACT, 1444 classes per mark:**

| reading | `m1` | `m2` |
| --- | --- | --- |
| maximum survivor weight | **exactly 10** | **exactly 10** |
| classes attaining it | 135 | 135 |
| minimum survivor weight | `33/4` | `33/4` |
| angular span of the neutral rays | `[147.17510, 181.58208]` deg | `[178.41792, 212.82490]` deg |
| width of that arc | `34.40698` deg | `34.40698` deg |
| contiguous in the ray order | yes, all 135 | yes, all 135 |

That gives a general statement, EXACT and independent of bin count:

> **Every closed angular bin containing at least one of the 135 neutral rays has
> survivor weight exactly 10.**
> 
> Let `F` be the bin’s guaranteed patch and `r0` a neutral ray in the bin.
> `F` is the intersection of `Q_r` over the bin’s rays, so `F` is a subset of `Q_r0`, so
> `F` deletes a subset of what `Q_r0` deletes and `w(F) >= w(Q_r0) = 10`. And `m` lies
> in `F`, so `F` meets every core containing the mark; the mark clique weighs exactly 1
> (F3), so `w(F) <= 11 - 1 = 10`. Hence `w(F) = 10`.

The neutral arc has positive width, so **every** partition of the owner’s pose angle
into closed bins has at least one bin meeting it, and that bin is exactly neutral.
Escape 1 of X-026 §5 is therefore closed at every angular resolution, not refuted only
at sixteen.

**Narrowed, not closed: the lane’s “closed” means only that patch refinement is ruled
out as the lever.
[X-026](../../../../explorations/X-026-what-conditioning-does-and-does-not-buy.md) §5,
escape 1 carries the corrected reading.**

The prediction was then checked against the screen rather than left as an argument
(EXACT). The bins that meet the neutral arc, and their measured survivor weights:

| resolution | mark `m1` | mark `m2` |
| --- | --- | --- |
| 8 bins | `j3`, `j4` — both exactly 10 | `j3`, `j4` — both exactly 10 |
| 16 bins | `J6`, `J7`, `J8` — all exactly 10 | `J7`, `J8`, `J9` — all exactly 10 |

Those are precisely the six sixteen-bin classes the screen found at exactly 10, and
precisely the four eight-bin classes lane X1 found.
The arc predicts the neutral classes at both resolutions, and it predicts at least one
at every other resolution too.

## The obstruction is at pose level, not at sector level

One conditioning strictly stronger than any angular split was probed: fix the owner’s
whole core, not just its direction.
The eight members of the mark clique (indices `8, 14, 59, 60, 66, 71, 81, 85`, total
weight exactly 1, and each contains **both** bottom-left marks) are themselves
admissible net-oriented cores inside the container, so each is a candidate owner pose.
Deleting everything that meets one of them leaves, EXACT:

`#8: 71/8`, `#14: 71/8`, `#59: **10**`, `#60: **10**`, `#66: 73/8`, `#71: 73/8`,
`#81: 37/4`, `#85: 37/4`.

Two of the eight leave exactly 10. They are `#59` and `#60`, two distinct axis-aligned
corner cores of weight `1/8` each, centred at `(45133461/88696100, 25096071/49318700)`
and its diagonal mirror — a mirror pair, not one square counted twice; both sit inside
the container and both contain both marks (EXACT).

Any conditioning at all whose guaranteed patch lies inside the owner’s core — which is
what makes the patch guaranteed — has a class containing the pose of member `#59`, and
that class’s patch is a subset of `#59`’s core, so its survivor weight is at least 10
against a requirement strictly below 10. Refining the patch is therefore the wrong lever
at every level of the pose, not only at the angular level.
What would remove that class is a proof that the pose cannot occur in an eleven-square
packing, which is X-026’s escape 2 (emptiness) and not a covering argument at all.

## Cross-checks

Every headline number was read twice, by two unrelated algorithms.
The screen decides “meets the patch” by SAT over edge normals (`strict_separation`); the
cross-check decides it by exact Sutherland-Hodgman convex clipping
(`convex_polygon_intersection`), calling a placement deleted when the exact intersection
is nonempty.

| cross-check | result |
| --- | --- |
| the 4 neutral eight-bin classes and 8 sixteen-bin subclasses: weight and survivor set | identical under both, 12/12 AGREE |
| singleton-ray neutral classes, both marks | SAT 135, clipping 135, AGREE |
| pose probe `#59`, `#60` | identical under both |
| eight-bin mean deletion vs lane X1’s `55/32` | match |
| sixteen-bin table under the diagonal mirror `J -> 15 - J` | exact, all ten pairs |

One false start is worth recording so it is not repeated: an exact vertex-to-edge
polygon distance is **not** a disjointness test, because it misses containment — the
mark clique’s cores contain the patch’s mark vertex strictly, so every vertex-edge
distance is positive and the test reported weight 11 for all twelve classes.
It is correct only as a distance between polygons already known to be disjoint, which is
how it is used in the reach measurement above.
The false start is retained as [`lane-x4-crosscheck.py.txt`](lane-x4-crosscheck.py.txt)
so the trap stays on the record.

## What this means for X-026

- **Step 3 stands, and is stronger than it was stated.** X-026 §5 escape 1 said
  neutrality is a property of the current eight-sector patches.
  It is not: it is a property of the mark and the mass-eleven ceiling family, and it
  survives every angular refinement and the pose-level refinement sampled here.
- **Steps 4, 5 and 6 are untouched**, and Step 6’s rank-one cap of `3.868983` never used
  the patch in the first place.
  Not endorsed: PR 139 finding R2 holds that no conditional transfer of that cap is
  established without a separate owner, class, patch and routing verification.
- **Escape 1 can be marked closed.** Narrowed rather than closed: the lane’s “closed”
  means only that patch refinement is ruled out as the lever, and
  [X-026](../../../../explorations/X-026-what-conditioning-does-and-does-not-buy.md) §5,
  escape 1 carries the corrected reading.
  Escapes 2 (empty classes) and 3 (compatibility pruning) are untouched by this
  measurement and remain exactly as open as they were.
- The conditional **point-cover** line can now be closed in the record at every angular
  resolution — narrowed rather than closed, on the same reading as the bullet above.
  The conditional **threshold** line (H-155) is untouched: this lane measured deletions,
  not atoms.

## Costs and files

| step | wall time |
| --- | --- |
| eight-bin control + sixteen-bin screen, 32 classes ([`lane-x4-screen16.py.txt`](lane-x4-screen16.py.txt)) | 4.1 s |
| exact containment and reach audit ([`lane-x4-verify-geometry.py.txt`](lane-x4-verify-geometry.py.txt)) | 1.6 s |
| singleton-ray limit, 2888 classes + pose probe ([`lane-x4-limit.py.txt`](lane-x4-limit.py.txt)) | 93.8 s |
| independent clipping cross-check ([`lane-x4-crosscheck2.py.txt`](lane-x4-crosscheck2.py.txt)) | 91.2 s |
| consolidation, artefacts and the bin-theorem check ([`lane-x4-consolidate.py.txt`](lane-x4-consolidate.py.txt)) | 165.4 s |
| eight-bin equivalence control ([`lane-x4-verify-eight.py.txt`](lane-x4-verify-eight.py.txt)) | under 5 s |

Total compute under six minutes; the lane fits inside its estimate.

Retained beside this report:

- [`lane-x4-nbins.py.txt`](lane-x4-nbins.py.txt) — the bin-count-parametrised footprint
  module.
- [`lane-x4-verify-eight.py.txt`](lane-x4-verify-eight.py.txt) — the eight-bin
  equivalence control against the tracked module.
- [`lane-x4-screen16.py.txt`](lane-x4-screen16.py.txt) — the eight-bin control screen
  and the sixteen-bin refinement screen.
- [`lane-x4-verify-geometry.py.txt`](lane-x4-verify-geometry.py.txt) — exact
  containment, strict growth, and reach audit.
- [`lane-x4-limit.py.txt`](lane-x4-limit.py.txt) — the singleton-ray refinement limit
  and the pose probe.
- [`lane-x4-crosscheck.py.txt`](lane-x4-crosscheck.py.txt) — the false start, retained
  so the trap is on the record.
- [`lane-x4-crosscheck2.py.txt`](lane-x4-crosscheck2.py.txt) — the independent clipping
  cross-check.
- [`lane-x4-consolidate.py.txt`](lane-x4-consolidate.py.txt) — the pose detail, the
  bin-theorem check and the artefact dump.
- [`lane-x4-pose-detail.py.txt`](lane-x4-pose-detail.py.txt) — the exact poses of `#59`
  and `#60`.
- [`lane-x4-probe-rays.py.txt`](lane-x4-probe-rays.py.txt) — the angular distribution of
  the retained signed rays.
- [`lane-x4-survivors-16.json`](lane-x4-survivors-16.json) — the eight refined
  subclasses with full survivor lists.
- [`lane-x4-survivor-families.json`](lane-x4-survivor-families.json) — every survivor
  family computed here.

All ten scripts are retained with a `.py.txt` extension, as
[lane X3](lane-x3-containment-atoms-do-not-cut.md) and
`agenda-032/unrun-independent-audit/` already do: they are scratch measurement scripts,
not importable project modules, and the repository’s Python surface is held at zero Ruff
and BasedPyright findings over every tracked `.py` file.
Their bytes are as delivered; nothing was reformatted.

Nothing tracked was edited by the lane, and the lane committed nothing.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
