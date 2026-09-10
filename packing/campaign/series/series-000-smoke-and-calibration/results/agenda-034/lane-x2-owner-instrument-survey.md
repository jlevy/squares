# Agenda 034, lane X2: what the single-corner conditional argument already has

Retained survey-lane report for
[X-024](../../../../explorations/X-024-two-lines-at-eleven.md), written by an Opus
sub-agent on 2026-09-09, read-only on the repository at
`claude/n-11-stronger-result-d730ds` (PR 137 merged in at `787cf1c9`). The report is
reproduced as delivered, with its own tables and its own numbers; only its file
references were rewritten to say where each file now is.
X-024 carries the coordinator’s reading.

This lane is an inventory, not a measurement of the mathematics: it says what the
conditional line’s machinery is, what it is parameterised by, and what would have to be
built. [Lane X1](lane-x1-corner-conditioning-is-mass-neutral.md) is the lane that says
the object is not worth building; this one is why that verdict is about sufficiency
rather than about missing tooling.
**Every item below was verified present or absent in the tree.** All paths are
repository-relative.
No tracked file was edited.

Nothing is retained beside this report: it cites the repository throughout and produced
no receipts of its own.
Not retained (scratch only): the `--estimate-only` sizing dumps for the sixteen classes,
the in-process replay calibration of exp-144, and the four exact-replay timing runs
tabulated in §6.

Labels: **RECORD** = read from a file in the repository; **CHECKED** = a timing on this
container; **EXACT** = a rational decision re-run here; **OPEN** = not measured.

## 1. The theorem

### Where it is written

| Document | What it states | Label |
| --- | --- | --- |
| [`agenda-030/bc-303-first-wave-selection.md`](../agenda-030/bc-303-first-wave-selection.md) §3 | the corner-pair ownership theorem, independently replayed | RECORD |
| [`agenda-031/proofs/corner-owner-sector-footprints.md`](../agenda-031/proofs/corner-owner-sector-footprints.md) | the sector lemma: sixteen classes per corner, each with a guaranteed footprint | RECORD |
| [`agenda-032/proofs/owner-footprint-contract.md`](../agenda-032/proofs/owner-footprint-contract.md) | the enlarged endpoint footprint and the LP/banking contract | RECORD |

Registered result: `T-023` in
[`packing/frontier/results.yaml`](../../../../../frontier/results.yaml).
Reader-facing writeup: [`agenda-032/sprint-report.md`](../agenda-032/sprint-report.md).

### The exact statement

`bc-303-first-wave-selection.md` §3, verdict:

> **Verdict: agrees.** Every packing of eleven unit squares in `[0, 96/25]²` has four
> distinct squares, one per corner, each containing in its interior at least one of its
> corner’s two marks `(3152/3175, 2336/3175)` and `(2336/3175, 3152/3175)` (and their
> images under the container’s symmetries).
> Since `[0, s]² ⊂ [0, 96/25]²`, the same holds of every packing at side at most `96/25`
> read in the `96/25` frame.

`corner-owner-sector-footprints.md`, ownership premise (the version the footprint
machinery uses; careful about closure):

> [BC-303’s corner-pair replay] establishes four distinct selected core owners in every
> hypothetical eleven-square packing.
> Each owner’s closed $B$-core contains at least one mark of its corner pair.
> […] Mark containment in a core may be on its boundary; no positive clearance is
> assumed.

and for the class structure:

> Two possible owned marks and eight sector bins give sixteen classes per corner.
> Choosing one class at each corner gives $16^4=65,536$ raw branches.
> Every packing belongs to at least one branch; no enumeration or feasibility pruning
> has been run. Owning both marks does not create a second owner.
> **The four distinct owners come from the premise, not from the sector construction.**

### Is the single-corner version standalone? Yes.

The four owners are NOT produced jointly.
The sentence that settles it is in `bc-303-first-wave-selection.md` §3, immediately
before the verdict:

> The argument needs exactly three facts and no more: a valid measure of mass `11 + ε`
> (so the eleven pairwise disjoint cores of a packing, each of mass at least one by
> Condition 5, leave at most `ε` outside them); a set of atoms of mass above `ε` **per
> corner** (so one of its atoms is in some core); and a cross-corner distance above the
> core’s diameter `B√2` (so no core holds atoms of two corners).

The second fact is per-corner and self-contained.
The third is used only to make the four per-corner owners distinct from each other; it
is not needed when conditioning on one corner.
The sector lemma then splits that one owner into sixteen closed classes without
reference to the other corners.

The single-corner discriminator is stated explicitly, with the threshold ten, as the
intended next step of the sector lemma (`corner-owner-sector-footprints.md`, final
section):

> The smallest next discriminator fixes only the bottom-left corner and tests its
> sixteen classes. Each class seeks complete residual-core coverage with
> $\mu(K)-\mu(T_j(m))<10$. All sixteen must pass or be exactly excluded to close that
> partition globally; one success excludes only its class.
> Failure to find a measure is inconclusive.
> This unrun test measures whether guaranteed triangles provide useful gain before
> funding the four-corner branch family.

`owner-footprint-contract.md` puts the four-corner family strictly after it: “Only then
consider `16^4` four-corner branches; their required residual threshold is seven.”

Two consequences the documents also record:

- **Eight solves, not sixteen.** The diagonal reflection sends `(m1, j)` to
  `(m2, 7 - j mod 8)`; `owner-footprint-contract.md`: “with reflected full directions
  and a reflection-invariant support/grouping, eight representative solves can cover all
  sixteen by explicitly transforming certificates.”
  Exposed as `OwnerClass.reflected_class_id` (verified: `m1:j0 <-> m2:j7`,
  `m1:j1 <-> m2:j6`, …).
- **No pruning is available at one corner.** `owner-footprint-contract.md`: “Cheap
  pose-emptiness pruning does not appear useful here: each mark can itself be the centre
  of a contained `B`-core at every orientation… At centre equality, either signed ray
  can be chosen, so all sectors are represented.”
  All sixteen must be run or excluded.

## 2. The instruments

Everything below is a promoted `devtools` module with tests unless marked otherwise.

### Owner footprints (guaranteed occupied patch)

- **[`packing/devtools/owner_footprints.py`](../../../../../devtools/owner_footprints.py)**
  (668 lines). Library, no CLI. Tests: `packing/tests/test_owner_footprints.py` (276
  lines).
  - `full_owner_direction_manifest()` -> 181 folded / 361 canonical square orientations.
  - `owner_branch_manifest(...)` -> `OwnerBranchManifest` with 16 `OwnerClass` entries
    (`class_id` = `bottom-left:m{1,2}:j{0..7}`, `mark`, `sector`, `reflected_class_id`).
  - `point_footprint(mark)`, `triangle_footprint(mark, sector)` (the `h²/4` sector
    triangle), `endpoint_footprint(...)` (enlarged anchored-square intersection),
    `owner_class_footprints(owner_class, directions)` -> all three as exact rational
    polygons.
  - `strict_residual_domain(outer_side, square_side, direction, footprint)` ->
    `StrictResidualDomain.components`: exact rational polygon pieces of the residual
    centre domain, one footprint, one direction.
  - `container_centre_polygon`, `forbidden_centre_polygon` (Minkowski collision
    polygon), exact convex-polygon utilities.
  - Constants `OUTER_SIDE = 96/25`, `CORE_SIDE = 9977/10000`, `HALF_CORE`,
    `ANGLE_LIMIT = 207107/500000`, `DIRECTION_STEPS = 180`, `BOTTOM_LEFT_MARKS`.
  - Carries `ENDPOINT_FOOTPRINT_STATUS = "provisional exact geometry; no authoritative
    endpoint-footprint certificate"`. Its analytic proof is
    [`agenda-032/proofs/endpoint-footprint-review.md`](../agenda-032/proofs/endpoint-footprint-review.md)
    (verdict: correct; a second derivation by the same agent family, not an
    independent-agent review).

- **[`packing/devtools/multi_owner_domains.py`](../../../../../devtools/multi_owner_domains.py)**
  (373 lines). Library, no CLI. Tests: `packing/tests/test_multi_owner_domains.py` (259
  lines).
  - `multi_footprint_domain(outer_side, square_side, direction, footprints)` -> exact
    vertical decomposition of the residual domain for several footprints at one
    direction.
  - `centre_in_strict_multi_footprint_domain(...)` exact membership predicate.
  - `compatible_m1_j0_footprints(kind)` -> the four reflected `m1:j0` footprints.
    Hardcoded: the only four-corner combination the tooling can build.

### Cover / piercing value on a residual domain

- **[`packing/devtools/run_owner_footprint_cover.py`](../../../../../devtools/run_owner_footprint_cover.py)**
  (975 lines). CLI `python -m devtools.run_owner_footprint_cover`. Tests:
  `packing/tests/test_run_owner_footprint_cover.py` (314 lines).
  - Flags: `--output`, `--class-id` (default `bottom-left:m1:j0`), `--owner-count {1,4}`
    (default 1), `--grid-count` (19), `--inset` (1/2), `--folded-indices` (default
    `0,45,90,135,180`), `--rows-per-direction` (3), `--max-rounds` (60),
    `--deadline-seconds-per-arm` (120), `--max-event-cells` (5e6), `--max-round-cells`
    (3e7), `--scale` (4e6), `--estimate-only`.
  - Four matched covering LPs on one support and one direction subset: `unrestricted`,
    `point`, `triangle`, `endpoint`. Float SciPy HiGHS row generation over exact
    rational event cells; weights rationalised at `--scale`.
  - Sets `settings.residual_square_count = 11 - owner_count` (10 at `--owner-count 1`, 7
    at 4) and reports `comparison.endpoint_below_residual_count` against it.
    **The single-corner threshold is already implemented.**
  - `--owner-count 4` refuses any `--class-id` but `bottom-left:m1:j0` (“the four-owner
    pilot is frozen to reflected m1/j0 classes”); `--owner-count 1` accepts all sixteen.
  - Exports
    `exact_minimum_covered_mass_on_pieces(atoms, direction, square_side, pieces)` ->
    `ExactMinimum(mass, reachable_cells)`, the exact rational reader.

- **[`packing/devtools/replay_owner_footprint_cover.py`](../../../../../devtools/replay_owner_footprint_cover.py)**
  (457 lines). CLI `python -m devtools.replay_owner_footprint_cover RECEIPT.json`. Tests:
  `packing/tests/test_replay_owner_footprint_cover.py` (177 lines).
  - Flags: `--expect-receipt-blob`, `--scope {source,full}`, `--max-atoms`,
    `--max-event-cells`, `--max-total-event-cells`, `--deadline-seconds`, `--output`.
  - Source-bound exact replay: rebuilds geometry from the receipt’s declared settings,
    refuses any mismatch, re-decides the endpoint arm’s rationalised atoms on all 361
    canonical orientations in `Fraction`. Works for `owner_count` 1 as well as 4.
  - Hard side gate: refuses a receipt whose `outer_side != 96/25` or
    `square_side != 9977/10000` (lines 111-114).

- **`packing/devtools/run_residual_cover_pilot.py`** (1298 lines) and
  **`packing/devtools/verify_residual_cover_pilot.py`**. CLIs.
  Tests `test_run_residual_cover_pilot.py`, `test_verify_residual_cover_pilot.py`. The
  predecessor instrument: four literal flush corner unit squares, not generic owner
  classes; a six-piece residual-domain formula that `owner-footprint-contract.md`
  explicitly says not to reuse (“Do not use the fixed-corner pilot’s six-piece
  formula”). Both bake in `OUTER_SIDE = 96/25`, `SQUARE_SIDE = 9977/10000`, and
  `RETAINED_INDICES = (0, 23, 45, 68, 90, 113, 135, 158, 180)`.

- **`packing/devtools/pierce_pilot.py`** (163 lines).
  CLI `python -m devtools.pierce_pilot --side 3.83 | --ladder`. Fractional piercing
  value `tau*` of the unrestricted unit-square pose family in `[0, t]²`. Float,
  grid-restricted, “neither an upper nor a lower bound on `tau*` by itself”.
  Not residual-domain aware: it has no owner or footprint input.
  Not usable per class.

### Dual / obstruction side on a residual domain

- **[`packing/devtools/screen_corner_dual_salvage.py`](../../../../../devtools/screen_corner_dual_salvage.py)**.
  CLI. Tests `packing/tests/test_screen_corner_dual_salvage.py` (248 lines).
  Deletes from a retained depth-one family every placement meeting a class’s footprint,
  per class. Constants `ONE_CORNER_THRESHOLD = Fraction(10)`,
  `FOUR_CORNER_THRESHOLD = Fraction(7)`. Output: per-class survivor mask, count, weight,
  `obstructs` flag. **Its source predicate is [`D-489`](../../../../../../defects.md)**:
  `_source_receipt` requires the source receipt’s `failures` to be exactly
  `["K3 total weight at least n"]`, so it accepts only a family that falls short of mass
  `n` and can never accept a proved ceiling family.
  That is what makes the exp-137 and exp-138 readings in §5 artifacts of their source.
- **`packing/devtools/audit_corner_dual_salvage.py`**. CLI. Independent receipt audit.
  Tests `packing/tests/test_audit_corner_dual_salvage.py` (189 lines).
- **[`packing/devtools/transport_ceiling_family.py`](../../../../../devtools/transport_ceiling_family.py)**.
  CLI
  `python -m devtools.transport_ceiling_family SOURCE.json --scale … --side … --verify`.
  Scales and recentres a family to another side, preserving depth and weights.

### Compatibility / counterexample audits (not cover values)

- `packing/devtools/corner_ownership_audit.py` (tests `test_corner_ownership_audit.py`).
- `packing/devtools/outer_pair_corner_audit.py` (tests
  `test_outer_pair_corner_audit.py`).
- `packing/devtools/render_owner_five_dot_figure.py` (tests
  `test_owner_five_dot_figure.py`).

### Unpromoted script retained beside a lane document

- [`agenda-032/unrun-independent-audit/check_five_dot_cover.py.txt`](../agenda-032/unrun-independent-audit/check_five_dot_cover.py.txt)
  and `test_check_five_dot_cover.py.txt`, both prefixed “UNTESTED DRAFT: retained for
  think-yhw2; no controls or scientific target ran.
  Not an importable project module or supporting certificate evidence.”
  This is the independent five-dot union checker that `T-023`’s `next_rung` and the
  current handoff ask for, and the only unpromoted script in this area.

### Threshold-atom machinery (unjoined)

- `packing/src/sqpack/fractional/threshold.py`, `threshold_interval.py`, `sweep.py`,
  `certificate.py`, `ceiling.py`, `classcert.py`, `colgen.py`, `cutting.py`; drivers
  `packing/devtools/decide_threshold_certificate.py`,
  `packing/devtools/plateau_reader.py`. These decide point-and-threshold certificates on
  the full centre domain.
  No forbidden-region input.
  Joining them to a residual domain is `H-155`’s instrument, and
  [`H-155`](../../../../hypotheses/H-155-conditional-threshold-cover-on-an-owner-class.md)
  records `instrument_ready: false`.

## 3. The parameters PR 137’s certified class ran at

| Parameter | Value | Where |
| --- | --- | --- |
| Container side `q` | `96/25 = 3.84` | `owner_footprints.OUTER_SIDE` |
| Shrink `B` | `9977/10000` | `owner_footprints.CORE_SIDE`; `h = B/2` |
| Angular slack `D` | `207107/90000000`; `B(1 + D) < 1` | `bc-303`, `gaps-to-global-bound.md` |
| Full direction net | 181 folded half-tangents, step `D`, limit `207107/500000`; 361 canonical square orientations modulo quarter turns | `DIRECTION_STEPS = 180`, `ANGLE_LIMIT`; verified `folded 181 / full 361` |
| LP direction subset | `--folded-indices 0,45,90,135,180` -> 9 canonical orientations | exp-142/143 commands |
| Support | 19x19 grid, inset `1/2`, plus the mark’s D4 orbit = 369 sites, independent singleton weights | `--grid-count 19 --inset 1/2` |
| Bottom-left marks | `m1 = (3152/3175, 2336/3175)`, `m2 = (2336/3175, 3152/3175)` | `BOTTOM_LEFT_MARKS` |
| Exact replay net | all 361 orientations, no symmetry fold | exp-144 `--scope full` |

Footprints are always derived from the full 361-orientation manifest even when the LP
uses nine directions (`owner_footprints_derived_from_full_manifest: true`).

### Parameterised by side? No. `96/25` is baked in.

- `OUTER_SIDE = Fraction(96, 25)` and `CORE_SIDE = Fraction(9977, 10000)` are module
  constants in `packing/devtools/owner_footprints.py`.
- Several helpers take `outer_side` / `square_side` as keyword parameters defaulting to
  those constants (`singleton_site_set`, `build_arms`, `build_four_owner_arms`,
  `strict_residual_domain`, `multi_footprint_domain`, `compatible_m1_j0_footprints`), so
  the geometry layer would take another side.
- But `build_receipt` and `main` in `run_owner_footprint_cover.py` pass `OUTER_SIDE` and
  `CORE_SIDE` literally (lines 714, 736, 756-757, 828-833), and there is no `--side` or
  `--shrink` flag.
- `replay_owner_footprint_cover.py` lines 111-114 actively refuse a receipt whose
  `outer_side` or `square_side` differs from those constants.
- `verify_residual_cover_pilot.py` re-declares its own `OUTER_SIDE = Fraction(96, 25)`.
- `BOTTOM_LEFT_MARKS` is hardcoded and side-specific: the marks are T-018’s
  `(197/200, 73/100)` orbit scaled by `128/127` into the `96/25` frame, and their
  ownership property comes from the `96/25` measure
  [`agenda-030/bc-293-measure-free-96-25.json`](../agenda-030/bc-293-measure-free-96-25.json)
  of mass `22524199/2000000 = 11.2620995` with per-corner pair mass `106251/400000`
  exceeding `eps = 524199/2000000` by `441/125000`.

**There is no owner or corner-pair theorem in the tree at any side other than `96/25`.**
The project statement on changing side is
[`agenda-032/gaps-to-global-bound.md`](../agenda-032/gaps-to-global-bound.md):

> Changing sides requires valid transport and revalidation of the marks, owner theorem,
> patches, net containment, and dots.
> The five-versus-seven count alone proves neither robustness to changing the container
> nor coverage of other classes.

Two side-related facts bearing on “`191/50` and above”:

- `191/50 = 3.82` is already unconditionally closed by `T-025`
  ([`t-025-threshold-certificate-proof.md`](../../../../../cases/n11_threshold_certificate/t-025-threshold-certificate-proof.md)),
  so a conditional argument there proves nothing new; **the open window for the
  conditional programme was `(3.82, 3.84]` before lane X1 closed it on other grounds.**
- The only cross-side transport in this area runs the other way: the retained depth-one
  family at `191/50` is transported by `+1/100` in each coordinate into the `96/25`
  frame by `devtools/transport_ceiling_family.py` (exp-137’s receipt records
  `source_outer_side: 191/50`, `translation: [1/100, 1/100]`).

## 4. The one certified class

It is a four-corner class, not a single-corner one.

| Item | Value |
| --- | --- |
| Class | the four reflected images of `bottom-left:m1:j0` — `compatible_m1_j0_footprints("endpoint")`, one endpoint footprint per corner |
| Residual threshold | 7 (`11 - 4`) |
| Residual cover value | 5 (normalised). Five atoms of common weight `beta = 1000001/1000000`, total `1000001/200000`; exact minimum over all 361 directions is exactly `beta`, so dividing by `beta` gives five unit dots |
| Piercing points | 5: `(73/75, 187/90)`, `(793/450, 43/15)`, `(48/25, 48/25)`, `(187/90, 73/75)`, `(43/15, 793/450)` |
| Wall time | LP search (exp-143) 9.12 s (arm seconds 4.62 / 1.83 / 0.83 / 0.77); exact 361-direction replay (exp-144) 28.95 s external, 12.76 s inside the exact loop, 589,549 dense event cells, max 2,457 per direction |
| Registered as | `T-023`, V3/C3, significance S3, `packing/frontier/results.yaml` |

Artifacts:
[`agenda-032/exp-143-four-owner-footprint-cover.json`](../agenda-032/exp-143-four-owner-footprint-cover.json)
(Git blob `cc66f06ddd3f7cc52d8a06d30a3920ba8e992c19`),
[`agenda-032/exp-144-four-owner-endpoint-full-net-replay.json`](../agenda-032/exp-144-four-owner-endpoint-full-net-replay.json),
the two experiment pages, the two proofs under `agenda-032/proofs/`, and the sprint
report with `four-owner-five-dot.svg` / `.png`.

## 5. The census

### There is no covered/uncovered class ledger. Not present.

X-024 §6: “PR 137’s class count after symmetry and pruning is unmeasured, and so is
whether any class other than the certified one admits a five-dot or a threshold cover.”
`gaps-to-global-bound.md`, on certificate reuse across classes: “Their class coverage is
unmeasured.” Building the ledger is X-024 slice B1 and step 2 of the handoff in
[`SYNOPSIS.md`](../../../../../../SYNOPSIS.md).
`H-155` lists “a declared uncovered class from PR 137’s covered/uncovered ledger, with
its rows-complete point value” among its unmet prereqs.

### Cover values that do exist

Exactly one single-corner class has ever been solved, and it failed the threshold:

| Run | Arm | Value | Converged | Rounds / rows / atoms | Arm seconds |
| --- | --- | --- | --- | --- | --- |
| exp-142, `bottom-left:m1:j0`, `--owner-count 1` | `unrestricted` (M0) | 11.884615384615364 | yes | 34 / 1254 / 83 | 4.61 |
|  | `point` (Mm) | 11.574514991181658 | yes | 50 / 1710 / 103 | 10.59 |
|  | `triangle` (MT) | 10.555555555555555 | yes | 21 / 1267 / 39 | 4.17 |
|  | `endpoint` (MP) | **10.38888888888889** | yes | 23 / 1416 / 41 | 4.46 |

Receipt
[`agenda-032/exp-142-owner-footprint-cover.json`](../agenda-032/exp-142-owner-footprint-cover.json);
`comparison.endpoint_below_residual_count: false` against `residual_square_count: 10`.
Wall 24.54 s. Scope: nine directions, 369 sites, float.
Nothing exact, nothing full-net.

Other conditional cover values, none of them owner classes:

| Run | Conditioning | Value | Scope |
| --- | --- | --- | --- |
| exp-136 | four literal flush corner unit squares | 7.804878 | numerical, 9 orientations, threshold 7 |
| exp-139 | same | `31219612/3804895 ~= 8.205118` (weakest core `760979/800000`) | exact, full net, threshold 7 |
| exp-143 | four `m1:j0` endpoint footprints | 5.0 | numerical, 9 orientations |
| exp-144 | same | 5 (exact) | exact, 361 directions |

### The one per-class table that exists: the dual side, all sixteen classes

`agenda-032/exp-137-corner-dual-salvage.json.gz`, produced by
`devtools/screen_corner_dual_salvage.py` (exp-137, 53.38 s) and independently audited by
`devtools/audit_corner_dual_salvage.py` (exp-141, 55.70 s, 147,456 exact SAT checks).

Source: the retained depth-one family
[`agenda-025/bc-232-leg-01-family.json`](../agenda-025/bc-232-leg-01-family.json), 768
closed `B`-squares at `191/50`, total weight `21342289572/2055263195 ~= 10.384212`,
transported `+1/100` into the `96/25` frame.
Deleting the members meeting a class’s footprint leaves a depth-one family of admissible
residual cores, so the survivor weight is a weak-duality LOWER BOUND on that class’s
residual cover value on any site set.
All sixteen bottom-left classes, threshold 10:

| Class | point | triangle | endpoint | endpoint survivors |
| --- | ---: | ---: | ---: | ---: |
| `m1:j0` | 9.417433 | 7.994638 | **7.987929** | 606 |
| `m1:j1` | 9.417433 | 8.495207 | 8.482323 | 644 |
| `m1:j2` | 9.417433 | 9.409494 | 9.030961 | 709 |
| `m1:j3` | 9.417433 | 9.417433 | **9.417433** | 734 |
| `m1:j4` | 9.417433 | 9.408579 | 9.408579 | 731 |
| `m1:j5` | 9.417433 | 8.969297 | 8.969297 | 705 |
| `m1:j6` | 9.417433 | 8.635910 | 8.635910 | 664 |
| `m1:j7` | 9.417433 | 8.468259 | 8.391376 | 628 |
| `m2:j0` | 9.417433 | 8.468259 | 8.391376 | 628 |
| `m2:j1` | 9.417433 | 8.635910 | 8.635910 | 664 |
| `m2:j2` | 9.417433 | 8.969297 | 8.969297 | 705 |
| `m2:j3` | 9.417433 | 9.408579 | 9.408579 | 731 |
| `m2:j4` | 9.417433 | 9.417433 | **9.417433** | 734 |
| `m2:j5` | 9.417433 | 9.409494 | 9.030961 | 732 |
| `m2:j6` | 9.417433 | 8.495207 | 8.482323 | 644 |
| `m2:j7` | 9.417433 | 7.994638 | **7.987929** | 606 |

Exact fractions are in the receipt: `m1:j0` endpoint is `65669186303/8221052780`;
`m1:j3` endpoint is `77421212793/8221052780`. `obstructs` is false for all 48 rows —
none reaches 10.

> **Correction, [`D-489`](../../../../../../defects.md).** Every absolute level in this
> table is an artifact of its source.
> The screen ran on a family of mass `10.384212`, `0.6158` short of eleven, because
> `screen_corner_dual_salvage._source_receipt` accepts only a receipt whose `failures`
> are exactly `["K3 total weight at least n"]` — that is, only a family that fell short
> of mass `n`. [Lane X1](lane-x1-corner-conditioning-is-mass-neutral.md) re-ran the same
> `screen_footprint` on the mass-eleven ceiling family and read survivor weight
> **exactly 10** at `m1:j3`, `m1:j4`, `m2:j3` and `m2:j4`. The *shape* of the table —
> which classes gain from the footprint and which do not — survives; the conclusion “no
> class reaches 10” does not.

The spread is NOT uniform:

- The point footprint deletes the same `10.384212 - 9.417433 = 0.966779` from every
  class, consistent with the point-extension lemma’s cap of 1
  ([`agenda-032/proofs/point-extension-lemma.md`](../agenda-032/proofs/point-extension-lemma.md)).
- The endpoint footprint’s extra deletion beyond the mark ranges from 0.000000 (`m1:j3`,
  `m2:j4`: survivor count identical to the point arm at 734, i.e. no placement in the
  retained family meets that footprint without already containing the mark) to 1.429504
  (`m1:j0`, `m2:j7`).
- The class PR 137 certified, `m1:j0`, is the single best class on this measure, tied
  only with its reflection `m2:j7`. `m1:j3` / `m2:j4` are the worst and gain nothing
  from the footprint at all — which is exactly the zero-gain lane X1 then measured
  against the mass-eleven family.
- Corresponding four-corner figures (same receipt, `four_corner` block, 65,536
  combinations): point min = max = `13394344077/2055263195 = 6.517094`; triangle min
  0.825915, max 6.517094; endpoint min 0.799079, max 6.517094; `obstructed_count: 0` in
  all three.

Interpretation limits: these are lower bounds from one retained family, not cover
values, and `gaps-to-global-bound.md` records the deletion route as exhausted (“Stop
unchanged- weight deletion filters”; “Further unchanged-weight filters of that family
therefore cannot recover those thresholds”).

The one genuine cover value, exp-142’s 10.388889 for `m1:j0`, sits ABOVE the threshold
on the easiest class, on a nine-direction, 369-site support.
Full-net values can only be larger for the same support.

## 6. The cost of sixteen single-corner classes at one side

### Recorded basis

| Stage | Recorded measurement | Host |
| --- | --- | --- |
| Four matched LP arms, one owner class, 9 directions, 369 sites | exp-142: 24.54 s wall, 23.83 s summed arm time (4.61 / 10.59 / 4.17 / 4.46) | Darwin 25.5.0 arm64, 10 logical CPUs, Python 3.14.7, one process, sequential arms |
| Same, four-owner | exp-143: 9.12 s wall, 8.05 s arm time | same |
| Exact 361-direction replay, 5 atoms | exp-144: 28.95 s external, 12.76 s exact loop, 589,549 dense cells | Darwin arm64, one process |
| Dual screen, 16 classes x 3 kinds + 65,536 joint | exp-137: 53.38 s; audit exp-141: 55.70 s | Darwin arm64, one process |
| Partial one-owner run that exhausted rounds | exp-140: 15.98 s, stopped_by timebox (point arm exhausted 60 rounds in 9.62 s, area arms never ran) | Darwin arm64 |

### Measurements taken on this container (one core, `packing/.venv/bin/python3`)

Calibration: exp-144’s exact inner loop was re-run in process (same 5 atoms, same
four-owner domain, all 361 directions), reproducing its exact minimum `1000001/1000000`
in 23.79 s against the receipt’s 12.76 s. **This container is about 1.9x slower per core
than the recorded host.** Figures below are this container’s. — CHECKED

Per-class geometry and LP sizing (`--estimate-only`, all sixteen classes, 3.27 s total
in-process; about 0.8 s each as a standalone process):

- Endpoint arm dense cells per direction: 542,432 to 554,280 across the sixteen classes;
  one-round totals 4,333,823 to 4,426,288. Retained singleton variables 362-367.
  Residual-domain components 5-6 per direction.
- The endpoint footprint has identical area in every class (0.10307770, against the
  triangle’s 0.06221283) — it is one shape rotated — so the sixteen classes are within
  2% of each other in LP cost.
  The certified class is not cheaper than the rest.
- `strict_residual_domain`: 1.6 ms per direction, so 0.6 s for the full 361-direction
  net.

Exact replay cost for a single-corner class (`m1:j0` endpoint domain), by atom count,
extrapolated across 361 directions:

| Atoms | ms / direction | reachable cells / direction | 361 directions |
| ---: | ---: | ---: | ---: |
| 5 | 10.4 | 193 | 3.8 s |
| 41 | 43.3 | 3,504 | 15.6 s |
| 120 | 110.2 | 24,578 | 39.8 s |
| 300 | 253.5 | 149,161 | 91.5 s |

The reader builds a dense `(2A + p) x (2A + p)` event grid per direction, so cells grow
quadratically in atom count while wall time grows closer to linearly over this range.

### The estimate

At the parameters PR 137 actually used — nine directions, 19x19 plus mark orbit, 120 s
and 300 rounds per arm — sixteen single-corner classes cost about 6.5 core-minutes, so
roughly 3 to 4 minutes on two cores.
Basis: 16 x 24.54 s = 393 s of recorded single-process work, split over two cores; the
sixteen classes are within 2% of each other in dense-cell count, so the exp-142 timing
transfers directly. Using the eight reflection representatives halves it to about 100 s
of core time, under 2 minutes on two cores.
On this container multiply by about 1.9 (about 12 core-minutes for sixteen, about 6
minutes on two cores).

Adding an exact 361-direction replay for each class that produces a candidate: about 16
s per class at exp-142’s 41-atom scale, about 40 s at 120 atoms, about 90 s at 300 atoms
on this container (roughly half that on the recorded host).
Sixteen replays at the 41-atom scale is about 4 core-minutes here.

**Two things the estimate does not cover, and they dominate any real attempt:**

1. **Nine directions is not a certificate.** A single-corner exclusion needs coverage on
   all 361 orientations.
   Row generation at 361 directions would need about 550,000 cells x 361 ~= 200M dense
   cells per round against the tool’s `--max-round-cells` default of 30M — a 6.6x breach
   of a guard that exists because the arrays are materialised.
   PR 137 got around this only because its four-owner candidate had five atoms and
   survived the full net unchanged; there is no recorded case of a nine-direction
   candidate for a single-corner class surviving the full net.
2. **The measured value is above the threshold.** exp-142 converged at 10.388889 on the
   easiest of the sixteen classes with the target below 10. A run at these parameters is
   priced at minutes, but its expected outcome is “all sixteen above ten”, not a
   certificate. Getting below 10 requires a larger site set and/or more directions, whose
   cost is not recorded anywhere in the tree.

## 7. The gap — what would have to be built

Each item verified absent:

1. **A full-net row-generation path for the LP.** `run_owner_footprint_cover.py`
   materialises a dense event grid per direction; at 361 directions the one-round total
   is about 200M cells against a 30M guard.
   Nothing in the tree runs a residual-domain covering LP on the full net.
   Needed: a sparse or incremental cell reader, or a two-stage screen (few directions,
   then exact full-net replay of the candidate) with a documented failure path.
2. **Enough site and direction resolution to get below 10**, or an obstruction proof
   that it is impossible.
   The only measurement, 10.388889, is above the threshold.
   There is no recorded run at a larger grid than 19x19 or at more than nine directions
   for any owner class, and no recorded scaling for that.
   [Lane X1](lane-x1-corner-conditioning-is-mass-neutral.md) is the obstruction proof
   for four of the sixteen classes, and it is exact.
3. **A per-class ledger and its driver.** No census tool exists for owner classes
   (`devtools/census_*.py` are about chunks and tight cells).
   X-024 slice B1 and handoff step 2 both name it; `H-155` lists it as an unmet prereq.
4. **Certificate transport between classes.** `OwnerClass.reflected_class_id` exists,
   but there is no tool that transforms a frozen dot set plus footprint under a
   container symmetry and re-decides it, nor one that decides exact union-containment
   `A subset A'` to reuse a certificate.
5. **Side parameterisation.** `OUTER_SIDE` / `CORE_SIDE` are module constants; there is
   no `--side` flag; `replay_owner_footprint_cover.py` refuses any other side; the marks
   are hardcoded to the `96/25` measure.
   Running at any side in `(3.82, 3.84)` additionally needs a new ownership theorem at
   that side — a valid measure of mass `11 + eps` there with a corner atom orbit of mass
   above `eps` and cross-corner distance above `B sqrt 2`. None exists in the tree for
   any side but `96/25`.
6. **The threshold-atom join**, only if point covers stay above 10.
   `sqpack.fractional.threshold` / `threshold_interval` take no forbidden region;
   `owner_footprints` / `multi_owner_domains` produce one.
   `H-155` `instrument_ready:
   false`; X-024 slice E1.
7. **The independent five-dot / union checker**, retained as an untested draft.
   Step 1 of the handoff and `T-023`’s `next_rung`; it blocks reusing the certified
   geometry to exclude further cases.

Not gaps: the single-corner threshold (`residual_square_count = 11 - owner_count = 10`
and `ONE_CORNER_THRESHOLD = Fraction(10)` are already wired), the sixteen-class
manifest, the per-class footprint geometry, the per-class residual polygons, the exact
replay for `owner_count = 1`, and the reflection pairing.

## What this lane does not establish

Nothing here is a statement about `s(11)`, and nothing here decides whether a
conditional certificate is worth building.
That decision is [lane X1](lane-x1-corner-conditioning-is-mass-neutral.md)’s, and it is
negative on grounds this survey cannot see: the tooling is present and adequate, and the
mass arithmetic is neutral anyway.

## Files

Nothing is retained beside this report.
Not retained (scratch only): the `--estimate-only` sizing output for the sixteen
classes, the in-process exp-144 replay calibration, and the four exact-replay timing
runs behind §6’s table.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
