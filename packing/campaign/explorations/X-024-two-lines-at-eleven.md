---
title: "X-024 — two lines at eleven: the unconditional certificate and the owner case split, and where to push next"
softschema:
  contract: packing.squares:Exploration/v1
  schema: ../schemas/exploration.schema.yaml
  envelope: exploration
  status: enforced
exploration:
  id: X-024
  title: "Two Lines at Eleven: The Unconditional Certificate and the Owner Case Split, and Where to Push Next"
  date: '2026-09-09'
  author: Claude coordinator (Fable), with one Opus agent for the read-only summary of PR 137
  campaign: packing.squares
  brief: >-
    Two branches reached partial results at n = 11 on the same day by different routes.
    This branch pushed the weighted fractional unavoidable-set certificate: a finer net
    and a larger shrink dilate the retained atoms to 3.816609502788862 (T-024), an
    exact ceiling family proves the one-body point-atom method cannot pass unit side
    3.8288, and a threshold certificate, rank-one Chvátal–Gomory cuts on the measure
    side, proves s(11) >= 191/50 = 3.82 unconditionally and past that ceiling, decided
    by two routes that fail differently and reviewed adversarially. PR 137 pushed
    ownership and conditional-owner case splits at q = 96/25 = 3.84: four unavoidable
    corner owners, sixteen exhaustive classes per corner, and one four-owner class
    excluded by five piercing dots (its T-023), with the feasibility of exhausting the
    65,536 raw class combinations stated as unknown. The owner asked for a strategic
    reading of the two lines together. This report says what each established, where
    they meet in the same objects, and which of three routes to push, with the cheap
    discriminating measurement for each.
  sources:
  - packing/campaign/explorations/X-023-three-losses-and-a-new-atom.md
  - packing/cases/n11_fractional_certificate/t-024-dilation-limit-proof.md
  - packing/cases/n11_threshold_certificate/t-025-threshold-certificate-proof.md
  - packing/campaign/series/series-000-smoke-and-calibration/results/agenda-033/lane-b-threshold-atoms-at-191-50.md
  - packing/campaign/series/series-000-smoke-and-calibration/results/agenda-033/lane-t-theory-cuts-and-routes.md
  - packing/campaign/series/series-000-smoke-and-calibration/results/agenda-033/lane-t2-cap-and-next-cuts.md
  - packing/campaign/series/series-000-smoke-and-calibration/results/agenda-033/lane-t2-plateau-reader.md
  - packing/campaign/series/series-000-smoke-and-calibration/results/agenda-033/ceiling-family-191-50.json
  - docs/project/reviews/review-2026-09-09-threshold-certificate-theorem.md
  - packing/campaign/series/series-000-smoke-and-calibration/results/agenda-032/gaps-to-global-bound.md
  - packing/campaign/series/series-000-smoke-and-calibration/results/agenda-032/sprint-report.md
  - packing/campaign/agendas/agenda-032-conditional-owner-sprint.md
  - packing/campaign/explorations/X-022-segment-ownership-continuation.md
  - packing/campaign/hypotheses/H-142-five-dot-full-net-cover.md
  - packing/campaign/series/series-000-smoke-and-calibration/results/agenda-032/proofs/five-dot-transfer-review.md
  - packing/campaign/series/series-000-smoke-and-calibration/results/agenda-031/proofs/corner-owner-sector-footprints.md
  - packing/frontier/results.yaml
  proposes: [H-146, H-147]
---
# X-024 — Two Lines at Eleven: The Unconditional Certificate and the Owner Case Split, and Where to Push Next

**Two branches moved on `n = 11` on the same day by different routes, and they meet in
the same objects.** This branch works on the unconditional side: one certificate, one
global bound. It re-certified the retained `T-018` atoms on a finer net and dilated them
to `3.816609502788862` (`T-024`); proved by an exact depth-one family that the one-body
point-atom method cannot pass unit side `3.8288`, however the net and shrink are chosen;
and then passed that ceiling with a new certificate language, threshold atoms, which
prove `s(11) >= 191/50 = 3.82` unconditionally and are decided by two routes that fail
differently. PR 137 works on the conditional side: split the packings of eleven squares
at `q = 96/25 = 3.84` by which squares own the four corners and how, and exclude each
class by a residual cover.
It proved the class structure (four owners, sixteen exhaustive classes per corner),
excluded one of the `16^4 = 65,536` raw combinations with five piercing dots (its
`T-023`), and wrote down what a complete exclusion would need while stating that its
feasibility is unknown.
The right next move is to push the unconditional threshold certificate up in side,
because each success there is a global bound in one certificate and the instruments are
in place, while running one cheap discriminator that tells whether threshold atoms also
unlock the conditional tree where point covers fail.
The two lines are not competitors: the conditional route is the fallback if the
unconditional LP stalls below `3.84`, and threshold atoms are the tool it would then
need.

## 1. What each line established

### The unconditional line (this branch)

| Result | Side | Status | Scope |
| --- | --- | --- | --- |
| `T-024`, the finer-net dilation limit of the frozen `T-018` atoms | `3.816609502788862` | registered, V4/C4 | unconditional weak limit; no endpoint certificate |
| The exact ceiling family at `191/50`: 88 closed `B`-squares at six net directions, weight `1/8` each, total exactly eleven, maximum depth one | `3.82` | EXACT, two verifiers and an independent reader | no D4-symmetric point-atom measure of mass below eleven satisfies Condition 5 at `(191/50, 9977/10000, any net containing its six directions)`; scaled to unit squares, no one-body point certificate passes unit side `3.8288` |
| The threshold certificate at `191/50`: 584 point atoms and 320 two-of-three atoms, budget `685457679/62500000 = 10.967322864` | `3.82` | accepted by the exact sweep and by the interval route, which agree at least charge `100000203/100000000`; theorem reviewed sound; registration in progress as `T-025` | unconditional endpoint certificate `s(11) >= 191/50`; the first result past the point-method ceiling |

The three losses of the point certificate that X-023 separated, the shrink tax, the site
restriction and the integrality gap, have now each been measured: the finer net recovers
about `0.0066` of the shrink tax on the frozen atoms and about `0.011` remains below the
cap; the site restriction is real but capped by the same ceiling; and the integrality
gap at `3.82` is what threshold atoms closed, since the ceiling family violates the
two-of-three cuts by `1/4` and the accepted certificate carries `2.29` of its budget in
them.

### The conditional line (PR 137)

| Result | Side | Status | Scope |
| --- | --- | --- | --- |
| `T-023` (PR 137): five dots exclude one four-owner branch | `96/25` | V3/C3/S3 | conditional on one of `65,536` raw owner-class combinations; “changes no global bound for `s(11)`” |
| The corner-pair theorem and the sector footprints: four distinct owners in every eleven-square packing at `q`, sixteen classes per corner, each guaranteeing a closed rational patch | `96/25` | proved, reviewed twice by the same agent family | the exhaustive class structure; “There is presently no evidence that full case exhaustion is feasible” |
| The deletion screens (exp-137, exp-138, exp-141): point-only filters of the retained depth-one family at `191/50`, translated to `q`, fall below ten for every one-owner class and below seven for every four-owner combination (maximum `13394344077/2055263195 = 6.517`) | `96/25` | exact, negative | “Stop unchanged-weight deletion filters”; the retained family obstructs no class |
| The residual covers: numerical four-arm programs on nine directions, then the exact five-dot replay on all 361 orientations | `96/25` | exact for one class | the certified class only |

Their transfer from the finite net to physical angles is analytic (the `V3` half): every
physical unit square contains a concentric `B`-square at a net direction, strictly
inside; every owner in its class contains its patch; every residual core avoids the
patches. That is the same core selection this branch’s certificates use, with the same
`B = 9977/10000`, the same net and the same `B(1 + D) < 1`.

## 2. Where the lines meet

They share their objects and their obstruction.

- **The same cores, the same sweep.** Both lines decide coverage over closed `B`-squares
  at net directions by exact event cells, transfer to arbitrary angles by the strict
  containment `B(1 + D) < 1`, and use the D4 fold or the doubled net.
  PR 137’s residual covers are point-atom certificates with two extra inputs: a
  forbidden region (the union of the guaranteed occupied patches, which no residual core
  may meet) and a budget threshold of `n - 4 = 7` instead of `11`.
- **The same obstruction.** PR 137 names its decisive stopping test: “an exact feasible
  fractional residual-core family of mass at least seven, with depth at most one
  everywhere”, which “would rule out every nonnegative point cover of mass below seven
  for that relaxed branch”.
  That is the weak-duality ceiling this branch proved at `191/50` for the unconditional
  problem, where the family of mass exactly eleven stops every point cover.
  The tutorial on their branch states the unconditional version of the same test.
  Both lines therefore run into the point method’s integrality gap; this branch is the
  one that has crossed it.
- **The tool each lacks.** Their negative results are point-only; threshold atoms are
  the cover language the ceiling family does not bound (X-023, lane T). Their owner
  structure supplies free deletions: a core meeting a guaranteed occupied patch needs no
  charge, which is why five dots suffice for one class where an unconditional cover
  needs a thousand atoms.
  Conditioning multiplies the number of certificates and lowers the bar for each;
  threshold atoms raise what any single certificate can reach.

## 3. Three routes

**A. Push the unconditional threshold certificate up in side.** Retain `3.82`, then run
the same loop at `383/100` and `96/25` from the accepted site and atom set: a rows-only
round costs about forty seconds and a full round with site and atom separation a few
minutes, so a bounded run of ninety minutes reads the LP value at the next side.
On top of whatever side the LP reaches, the finer-net mechanism of `T-024` adds its
shrink recovery at no cost in soundness, and it has not yet been measured on a threshold
certificate; on the frozen `3.82` certificate it would give about `3.8266` if the atoms
transfer to the 1440-step net at the larger shrink the way the point atoms did.
Every success is a global bound in one certificate, decided by the gate that exists.
The base case at `383/100` is a plateau, not a success: the point LP rose at least
`13.6` units of value per unit of side between `3.81` and `3.82`, the two-of-three
certificate has `0.0327` of budget to spare, and if the cut LP’s slope is comparable the
two-of-three family reaches eleven near side `3.822` to `3.825`, before `3.83`. What is
proved about the reach of any rank-one method at this shrink and net is only the bracket
`[3.82, 3.868983]`, the upper end being Trump’s packing shrunk and snapped.
So the loop at `383/100` is priced as a reading of the plateau, and the instrument that
turns a plateau into a theorem is an exact plateau reader on the symmetrised dual: its
depth, its exact maximum two-of-three charge over all point triples, its heaviest
cliques with fractional piercing number below two, its line chords, and a Chvátal–Gomory
separation program, each returning an exact violated atom or a certificate that none
exists. The next cut families, ranked by the theory lane’s analysis (lane T2): weighted
clique atoms (three-of-five with a doubled point, which already cut both retained optima
at `191/50` harder than two-of-three), floor two-of-five atoms, and exact vertex-set
separation in place of the sampled generator.
Three-of-four atoms are dominated by two-of-three and are not built; wall-line atoms are
tight at exactly three on the plateau family and gain nothing.

**B. Exhaust the owner classes at `3.84`.** PR 137’s own plan: an independent
implementation of the residual-domain union, transport of the certified patches and dots
under container symmetries with exact union containment, a covered/uncovered class
ledger, new dot patterns for uncovered classes, refinement of difficult classes.
Its value is that it targets `3.84` directly and may work beyond where any unconditional
fractional method stalls.
Its costs are the class count (up to `65,536` raw, fewer by symmetry and compatibility
pruning, unmeasured), the analytic transfer steps that keep the composed theorem at
`V3`, and the fact that a single uncovered class blocks the whole bound.

**C. Hybrid: threshold atoms inside the conditional tree, owner patches inside the
unconditional certificate.** A conditional threshold certificate is one object: a class
`c`, its forbidden region `F_c`, the threshold `n - 4`, and a family of point and
threshold atoms charging every admissible core that avoids `F_c`. The tools exist on
both branches and have not been joined: this branch’s threshold sweep and interval
route, and PR 137’s exact residual-domain polygons (`multi_owner_domains`,
`owner_footprints`). The cheap discriminator is one class PR 137 could not cover with
points. Positive: the class tree becomes an LP per class with a language proven stronger
than point covers, and route B’s feasibility question changes character.
Negative: threshold atoms do not help conditional covers either, and route A is the only
fractional route to `3.84`.

## 4. Why conditioning constrains so much

The owner asked to read the five dots as a symptom rather than the point, and the
numbers support that reading with one correction.
On PR 137’s nine-direction sample the unrestricted cover needed about `11.88` units of
mass and the exact full-net residual cover of the certified class `5`; but the first
figure is a restricted-site number on nine directions and the second an exact cover of
one favourable class, so they do not subtract.
The retained measure-free certificate at `96/25` (bc-293, mass `11.2620995`) bounds the
full-net covering value from above, so four conditioned squares bought at most
`(11.262 - 5)/4 = 1.566` units each, of which the mark itself accounts for at most one
(PR 137’s point-extension lemma); the rest is the occupied patch, and it is measured on
the one class that happened to be certified.
The reason it is large at all is where the mass goes: every dual read on either branch,
at `3.82` and at `3.84`, puts its weight on wall squares and corner-region intruders,
and the corner-pair theorem says four squares must be at the corners.
Conditioning removes the expensive part of the cover.

Read as an engine, the strategy is: find structure every packing must have, enumerate
its classes exhaustively, and in each class delete the guaranteed occupied region and
lower the threshold.
Its cost is the tree, not the leaves: each layer of forced structure multiplies the leaf
count (`16^4 = 65,536` raw at the first layer, unmeasured after symmetry and pruning)
while shrinking the residual by one square and a patch of area well below one, so
without bounding at internal nodes the case split does not converge toward the structure
of Trump’s packing on its own.
The sound form is branch and cut: a threshold certificate at an internal node (one patch
deleted, threshold ten) prunes the whole subtree under it, and a class-indexed threshold
certificate, one atom family per leaf, is the single object that a complete exclusion
would be (lane T2, C.2). Negative mark atoms, which would fold the owner theorem into an
unconditional certificate, are sound but worth exactly nothing at `191/50`: the ceiling
family already carries exactly one unit on every corner-mark clique.
The unconditional threshold certificate gives the quick global wins now; the conditional
engine is the way past the rank-one cap, and its bottlenecks are the tree, the cover
language at internal nodes, and the analytic transfer that keeps a composed result at
`V3` until it is mechanised.

## 5. Recommendation, the division of labour, and the next slices

Route A is the primary lane for movement now: the highest value per certificate, the
instruments in place, and two cheap decisive measurements, with the plateau at `383/100`
priced as the base case and the plateau reader (A4) as the instrument that turns it into
a theorem and names the next cut (A5). The conditional engine is the architecture for
`3.84` and beyond, and its decisive measurement is a class census (slice B1): how many
classes survive symmetry and pruning, and how their residual cover values are
distributed against seven.
If most classes are five-dot easy and the hard tail is small, the exhaustive program is
compute plus threshold atoms for the tail; if most sit near seven, the engine needs the
next layer of forced structure before it is affordable.
The unified certificate format (E1) is the piece both lanes need and moves up with it.

The owner set the division of labour on 2026-09-09: this branch follows the
unconditional line (slices A2 and A3, then the next atom families), and the conditional
line continues on PR 137’s branch with its own agent.
The conditional slices below (B1, E1, C1) are mapped here so that whichever branch takes
them starts from the same statement; this branch’s contribution to them is the threshold
sweep, the interval route and the two-route gate, which are general and take any centre
domain.

| Slice | Deliverable | Discriminator | Owner |
| --- | --- | --- | --- |
| A1 | `T-025` registered: case package, two evidence entries, the proof packet, the case page at `191/50` | the records tier and the gate on the frozen bytes | mechanical, Opus |
| A2 | the frozen threshold certificate on the 720- and 1440-step nets at their crossing shrinks, and its dilation records | the two-route gate at each net; the endpoint about `3.8266` if it holds (H-147’s first reading) | mechanical, Opus |
| A3 | the threshold loop at `383/100` from the accepted site and atom set, ninety minutes, rows complete or not | LP value below eleven with rows complete, frozen and decided; or a second plateau and its dual (H-147) | research, Fable |
| A4 | the exact plateau reader: vertex membership sets, the two-of-three triple search, maximal cliques with exact piercing LPs, line chords, the CG-separation program, each returning an exact violated atom or a certificate of none | run on the `383/100` dual: two-of-three feasible (the plateau is a theorem and the reader names the cut) or not (the generator, not the language, was the limit) | this branch |
| A5 | weighted clique atoms (three-of-five with a doubled point) and floor two-of-five atoms in the loop, with exact vertex-set separation | one atom round plus rows-only completion at `383/100`: below eleven, freeze and gate; at eleven, the reader’s next family | this branch |
| B1 | the owner-class census at `96/25`: combinations modulo the container symmetries, compatibility pruning by exact footprint separation, the nine-direction residual point LP on a sample of a few hundred classes | the class count and the distribution of residual values against seven | conditional line (PR 137’s branch) |
| E1 | one certificate format for both lines: point and threshold atoms, an optional forbidden region, a budget threshold, one two-route gate | PR 137’s `T-023` re-decided by the unified gate to the same verdict | either branch; efficiency block |
| C1 | a conditional threshold certificate on one uncovered owner class at `96/25`, decided by both routes on the residual domain | budget below seven where the point cover was above it (H-146) | research, Fable |

Two things must not be conflated when the lines are reported together.
PR 137’s `T-023` is conditional and does not move the bracket; `T-024` and the threshold
certificate are unconditional and do.
And their composed theorem is `V3` because its transfer is analytic, while the threshold
theorem has a written proof reviewed adversarially and a machine decision of every
condition; a hybrid certificate inherits the weaker of the two until the owner-class
transfer is mechanised.

Lane T2 is retained with this reading — the cap of the threshold method and the next cut
families in
[`lane-t2-cap-and-next-cuts.md`](../series/series-000-smoke-and-calibration/results/agenda-033/lane-t2-cap-and-next-cuts.md),
the instrument it asked for in
[`lane-t2-plateau-reader.md`](../series/series-000-smoke-and-calibration/results/agenda-033/lane-t2-plateau-reader.md)
— and slice A4 is done: the plateau reader is promoted as
`packing/devtools/plateau_reader.py` and its run on the `191/50` ceiling family is
retained beside the family, so what remains at `383/100` is to point it at that dual.

## 6. What this document does not establish

No bound moves here.
The `3.8266` figure is the shrink recovery the frozen threshold atoms would earn if they
transfer to the finer net, not a measurement.
The threshold LP’s cap is unknown beyond the proved bracket `[3.82, 3.868983]`, and the
`3.822` to `3.825` figure for the two-of-three family is slope arithmetic, not a
theorem.
PR 137’s class count after symmetry and pruning is unmeasured, and so is whether
any class other than the certified one admits a five-dot or a threshold cover; the
`1.566` units per conditioned square is an upper bound from one retained certificate on
one certified class, not a measurement of the tree.
The hybrid tool does not exist yet.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
