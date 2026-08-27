# Review: PR #44, Constructive Enumeration, and the Known-Best Atlas

**Date:** 2026-08-26

**Author:** Codex (agent), for the repository owner

**Status:** Complete factual-review record; the accepted infrastructure slices are
implemented on `codex/packing-atlas-overnight-review`

**Reviewed:** [PR #44](https://github.com/jlevy/thinking-scratchpad/pull/44), merged as
`9aecc97` from head `26ee2a0` (13 files, 1,309 additions, documentation and campaign
records only). Both merge checks passed; the PR had no submitted review or discussion.

## Verdict

Keep the constructive-enumeration lane, but change its order and narrow its claims.
The useful idea is a deterministic proposer over structured assemblies, backed by the
existing fixed-angle LP and quench.
The PR did not yet define the corpus, the minimal chunk partition, or the completeness
certificate needed to make the resulting ranks or coverage percentages meaningful.
Those are prerequisites, not implementation details.

The new evidence supports the owner’s broader observation more strongly than the PR’s
specific grammar. At the registered tolerances, 1,780 of the 1,860 squares in the 36
non-grid records participate in a same-angle, positive-edge-contact assembly.
That is 95.7 percent.
It does **not** follow that those assemblies partition into six or fewer bars, Ls, and
rectangles. A bounded exact-cover splitter now handles irregular maximal lattice
components. It certifies all 64 grid-derived records but only 2 of 36 non-grid records
within the narrow six-chunk/two-free budget.
Eight more non-grid records have a lattice partition using 7–12 chunks, 23 have none in
the implemented candidate universe, and three reach the declared 10,000-state cap.
This is strong calibration evidence that the rigid lattice grammar is too narrow for the
interesting corpus, not a W6 verdict.

The resulting recommendation is:

1. Treat `n = 1..100` as a complete descriptive and calibration atlas.
2. Keep the deterministic lattice-partition layer as a control, but expand the grammar
   to same-angle contact graphs with explicit sliding degrees of freedom.
3. Freeze the revised grammar and enumerator only after that layer has replay,
   complexity, and omission controls.
4. Use a genuinely unseen corpus above 100 for any later confirmatory coverage claim.

No H-044 through H-048 verdict is licensed by this review.

## What the Review Built

The branch now retains one normalized `Witness/v1` construction and one deterministic
house-rendered SVG for every `n = 1..100`, linked from the frontier records.
The atlas is regenerable and checks its own source hashes, witness semantics, numerical
receipts, renderings, manifest, and frontier links.

| Source stratum | Records | Assurance of stored construction |
| --- | ---: | --- |
| Canonical exact integer grid | 64 | Exact rational feasibility |
| Retained Kingbird SVG | 34 | Multiprecision numerical check |
| UnitSquare public SVG rendering | 2 | Rendering-derived numerical check |
| **Total** | **100** | No missing or guessed case |

The two UnitSquare witnesses, `n = 68` and `n = 69`, are intentionally weaker than the
other imports. Their public SVG polygons carry only six displayed decimals; the stored
witnesses verify those displayed polygons and do not pretend to replay the unavailable
interval boxes named in the source metadata.
The renderer for every case is the repository renderer, not the source site’s styling.

Videos and galleries remain useful as independent visual indices: they can reveal a
missing case, unexpected topology, or obvious import error.
They are not coordinate sources.
Video frames introduce scaling, antialiasing, cropping, and interpolation, so
coordinates recovered from them would be weaker than the retained vector assets and
would need a separately declared approximation contract.

## What the First Census Says

Three deliberately different views are retained in
[`chunk-components.json`](../../../atlas/known-best/chunk-components.json) and
[`chunk-partitions.json`](../../../atlas/known-best/chunk-partitions.json).

| View | Tolerances | Result | Interpretation |
| --- | --- | ---: | --- |
| Narrow maximal lattice components | angle `1e-6` rad; adjacency `1e-9` or `1e-3` | 21/100 certified | Sound certificates for those reported decompositions; 79 unresolved, not refuted |
| Bounded lattice partitions, non-grid | same; 10,000 states per free-square count | 2/36 inside budget; 8 outside; 23 absent; 3 capped | Exact-cover repair handles splits, but the narrow grammar still misses most interesting records |
| Broad contact assemblies | angle `1e-6` rad; contact `1e-3` | 4,969/5,050 squares assembled | Strong descriptive evidence, dominated in part by exact grids |
| Broad contact assemblies, non-grid only | same | 1,780/1,860 squares assembled | 95.7 percent of the relevant non-grid corpus |
| Broad contact assemblies, non-grid budget | same | 25/36 records have at most six components and three free squares | Close to the intuition, but one free-square looser and without the shape restriction |
| Regularized descriptive sweep, non-grid | angle `1e-3` rad; contact `1e-2` | 1,793/1,860 squares; 26/36 within the broad budget | Sensitivity result, not a registered test |

The regularized row uses fitted angle classes rather than transitive pairwise clusters.
An adversarial angle-chain control found that the first implementation joined a chain
whose endpoints did not fit one angle; correcting it reduced the `n = 68` regularized
structured count from 65 to 60 and the non-grid aggregate from 1,798 to 1,793.

The 169 multi-square non-grid contact components comprise 55 chains and 114 cyclic
patches. Their contact-normal equalities leave 859 internal slide degrees before overlap
intervals and wall contacts are applied; 792 squares touch at least one wall at the
registered contact tolerance.
These counts explain why “one connected component” cannot mean “one rigid chunk.”
A useful grammar must charge for internal freedom and seating, then let the LP resolve
the slides.

The source-stratified count matters.
Reporting only 4,969 of 5,050 would make the ansatz look almost tautological because 64
records are exact grids.
On the 36 non-grid cases, only `n = 5`, `n = 11`, and `n = 17` have less than 80 percent
of their squares in broad assemblies at the registered tolerances.
Those three are precisely the kind of small exceptional constructions that should guide
the next grammar, not be hidden in the aggregate.

The compact
[`chunk-evidence-profile.json`](../../../atlas/known-best/chunk-evidence-profile.json)
and its
[`house overview`](../../../atlas/known-best/evidence/non-grid-chunk-evidence-profile.svg)
make every non-grid case inspectable in one table.
Ten of 36 cases are fully covered by the registered contact census; 27 cover at least 90
percent, 33 cover at least 75 percent, and 35 cover at least half.
`n = 5` is the lone zero-contact outlier.
The 34 Kingbird normalizations account for 1,666 of 1,723 contact-covered squares, while
the two six-decimal UnitSquare imports account for 114 of 137 and carry most of the
detector sensitivity.
Only `n = 68`, `69`, and `71` change on the registered-to-regularized row metrics; only
`n = 69` crosses the broad `C <= 6, F <= 3` budget.
These source and sensitivity splits make the broad assembly case substantially more
credible without turning it into a rigidity or completeness claim.

The maximal-component detector is intentionally conservative.
A connected irregular polyomino may admit a valid split into a rectangle and a bar, and
a tilted assembly may be a sliding contact chain rather than an integer-lattice block.
The bounded partition layer now handles the first case and proves its value on every
grid-derived record.
It deliberately does not turn a sliding assembly into a lattice chunk or split a
tolerance-connected angle class.
Its negative and capped outcomes therefore remain “not established,” not
“non-expressible.”

## Findings and Dispositions

### Accept

- **The proposer/refiner separation.** Discrete structure should propose; the existing
  LP and quench should place and refine.
  This is the most promising part of X-003.
- **Stratum identity and counted work.** Replayable labels and LP-solve counts are
  better comparison units than floating-point endpoint keys and wall time.
- **The refusal to run W6 on new instruments.** The overnight work remains W2, W3, and
  W7. It produces corpus, tools, descriptive measurements, and amendments, not a
  scientific disposition.
- **The grammar-freeze principle.** A target-aware grammar cannot provide clean
  rediscovery evidence.
  The freeze must include code, enumeration bounds, symmetry rules, tie handling, and
  the corpus split.

### Revise

- **F1 — `K` conflates different quantities (high).** H-044 uses `K` for chunk count,
  while X-003 justifies six with the six angle classes measured at `n = 29`. Chunk count
  `C`, fitted-angle count `A`, and free-square count `F` are different variables.
  Exp-037 constrains `A`; it says nothing by itself about `C`.
- **F2 — the detector objective was incomplete (high; bounded repair implemented).**
  “Emit minimal `K`” did not specify candidate chunks, overlapping candidates, tie
  order, or how free squares trade against chunks.
  The retained bounded solver minimizes `F` first, then `C`, and uses maximum residual
  plus a declared deterministic minimum-remaining-values traversal for ties.
  A tempting global lexicographic tie search was rejected during review because it made
  dense-grid replay impractical; the retained traversal rule is explicit and
  regression-tested. It emits exact, near, no-partition, outside-budget, and search-limit
  outcomes. Its declared universe is contiguous bars, filled rectangles, and corner Ls
  inside maximal lattice components; it is not yet the complete grammar H-044 would
  need.
- **F3 — the original calibration split is no longer clean (high).** The full 1–100
  corpus has now been inspected while designing the instrument.
  It is valuable calibration evidence, but it cannot also be an unseen validation set.
  H-044 should remain undisposed, and H-045’s `n = 11` run can at most be a
  retrospective replay.
  A later confirmatory claim needs a prospectively frozen corpus, provisionally public
  cases `n = 101..324` if complete geometry can be retained and normalized.
- **F4 — “complete by construction” is conditional (high).** An atlas is complete only
  relative to finite, explicit bounds, and only after the label generator, symmetry
  quotient, and omission checks have their own completeness evidence.
  The rough `1e9` inter-chunk count before partitions is a feasibility warning, not yet
  a tractable design.
- **F5 — endpoint and cell semantics need canonicalization (medium).** H-045 needs
  deterministic tie rules and should rank returned candidates, not unproved “stratum
  optima.” H-046 needs canonical active-cell labels, tolerance hysteresis, and event
  deduplication; crossing few serialized cells alone does not establish nearness in
  arrangement space.
- **F6 — H-047 tests objective recovery, not pose invertibility (medium).** Its
  criterion compares only side values.
  Either add a pose-equivalence metric after symmetry and relabeling, or weaken the
  prose to objective recovery.
- **F7 — H-048 has only two small calibration populations (medium).** “Top decile” is
  unstable or trivial when the enumerated population is small or tied.
  Use recall at a declared solve budget, deterministic tie handling, and more than two
  calibration cells before treating the screen as a cost assumption.
- **F8 — imported annotations are derived data (medium).** Source geometry, normalized
  witnesses, derived chunk annotations, and evaluation splits must remain separate.
  Recomputing a detector must not rewrite source evidence or silently alter a grammar.
- **F9 — the operational plan contained stale local assumptions (low).** A plan should
  use the repository’s locked `uv` invocation and report the actual provenance failure
  if one occurs. It should not prescribe a global `pip install` or assert that every
  clone is shallow.
- **F10 — “a run that beats a record has a bug” is too absolute (low).** Such a result
  is suspect and must be independently replayed and formally or interval-verified before
  a record claim. The guard should not logically exclude a genuine improvement.

### Defer

- The stage-1 enumerator and its glued screen, until the partition contract and a
  measured complexity budget exist.
- H-045 through H-048 execution, until each instrument amendment is explicit and has
  focused negative controls.
- Any `n = 11` or `n = 17` rediscovery headline.
  The current work is infrastructure and retrospective calibration, not a clean target
  trial.

### Reject

- Treating six observed angle classes as evidence for six chunks.
- Counting maximal-component failures as H-044 refutations.
- Calling an enumeration exhaustive without finite bounds and an omission certificate.
- Recovering canonical coordinates from YouTube when source vector geometry exists.
- Promoting a numerical decimal import, a rendered polygon, or a stopped quench to an
  optimality statement.

## Recommended Build Order

1. **Preserve the 1–100 corpus — complete.** Keep retained source hashes, normalized
   witnesses, numerical receipts, and 100 house renderings.
   Treat every derived contact or chunk field as a separate, regenerable calibration
   annotation.
2. **Keep the rigid lattice grammar as a control — complete at the registered bounds.**
   Its exact-cover certificates and typed caps are useful precisely because the 2/36
   result falsifies the proposed grammar without rejecting the broader assembly idea.
3. **Use contact scaffolds as the proposer vocabulary — infrastructure complete through
   size five.** Signed contact labels, full relabeling-by-D4 canonicalization, a
   topology-first quotient, and independent Burnside counts now produce exactly 11,013
   abstract size-five orbits.
   The compact atlas stores all of them; no size-five LP has run.
4. **Retain local realization as a filter, not a packing certificate — implemented
   through size four.** The fixed-angle LP checks contact equalities and positive
   tangential overlap. It still omits walls, non-edge separation, container fit, and
   global packing feasibility.
5. **Use the prospective 101–324 map only for acquisition planning — safe seed
   complete.** Exact grids and four CC BY 4.0 UnitSquare cases are normalized and
   house-rendered. Kingbird cases above 100 remain metadata-only until their reuse terms
   are established. No prospective contact annotation has been computed.
6. **Freeze costs and omissions before a scientific run — next decision point.** Decide
   whether slide degrees, wall seats, largest assembly, and angle classes form a
   lexicographic or scalar cost.
   Then bound scaffold size, wall labels, inter-assembly relations, LP solves, and
   rejection receipts.
7. **Evaluate only after an untouched target split exists.** Rank candidates by the
   frozen cost, report solve-count budgets and typed indeterminacy, and keep objective
   recovery separate from pose recovery.
   Do not reuse the inspected 1–100 corpus as a holdout.

This order builds infrastructure the project needs even if the narrow bar/L/rectangle
ansatz fails. The source atlas, witness importers, renderer integration, partition
certificates, and evaluation split remain useful for other constructive grammars.

## Status Addendum — 2026-08-26

The review above is retained as the factual record for the heads it examined.
Its `2/8/23/3` partition distribution, first-solution selection description,
raw-Kingbird retention language, and co-committed hash claims are superseded by the PR
45 merge-readiness continuation in
[session 023](../../../campaign/agent-sessions/session-023-pr45-merge-readiness.md).

The five review follow-ups were dispositioned as follows:

1. **Partition classification corrected.** Every allowed exact free-square count is now
   evaluated. The selector first prefers any certificate within `C <= 6`, then minimizes
   `F`, `C`, residual, and the deterministic certificate key.
   The corrected non-grid aggregate is 3 established, 2 conclusively outside the
   registered budget, 23 without a partition in the registered universe, and 8
   search-capped and therefore indeterminate.
   `n = 26` is established at `F = 2, C = 6`; the later capped slices prevent conclusive
   outside-budget classifications at `n = 65,66,82,85,89`.
2. **Kingbird retention narrowed.** No express terms covering redistribution of the
   catalogue SVGs were located.
   The candidate working tree removes the 34 raw SVGs added for this atlas acquisition.
   The source inventory retains attribution, URLs, retrieval metadata, and normalized
   numerical center/angle facts in Witness/v1; deterministic house renderings and
   numerical receipts are regenerated from those facts.
   This conservative repository policy is not a legal conclusion, and raw retention
   still requires an applicable license or express permission.
   Publication remains blocked until the replacement PR branch has one clean base-parent
   commit and
   `git rev-list --objects origin/main..origin/codex/packing-atlas-overnight-review`
   reports no path below `resources/web/known-best-packings/kingbird/`.
3. **Durable state reconciled.** The synopsis, active plans, grammar, agenda, atlas
   guide, session handoff, and generated campaign views now describe the completed
   11,013-orbit abstract atlas and the next full-cell boundary rather than completed
   canonicalization as future work.
4. **Mixed angle classes rejected.** The public local realization prefilter fails with
   `unsupported-angle-classes` before spending an LP solve when vertex colors are not
   uniform. The retained size-five atlas has one angle class, so its abstract counts are
   unchanged.
5. **Hash policy aligned.** Integrity digests for co-committed sources, witnesses,
   manifests, renderings, profiles, and maps were removed.
   Git and deterministic full-content replay remain their integrity boundary.
   Hashes declared independently by the UnitSquare source remain explicit upstream trust
   evidence.

These corrections do not promote the evidence.
The `n = 1..100` corpus remains calibration-only, capped partition cases remain
indeterminate, the 11,013 scaffold records remain abstract and geometry-free, and local
contact realization establishes neither container fit, whole-packing feasibility, nor
optimality.
[Session 025](../../../campaign/agent-sessions/session-025-pr45-performance-continuation.md)
owns the current strict and cross-platform validation receipts.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
