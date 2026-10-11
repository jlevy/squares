---
title: H-272 — re-optimizing the 68 symmetric Kingbird-derived records without a symmetry constraint lowers one in ten and breaks their symmetry
softschema:
  contract: packing.squares:Hypothesis/v1
  schema: ../schemas/hypothesis.schema.yaml
  envelope: hypothesis
  status: enforced
hypothesis:
  id: H-272
  kind: hypothesis
  claim: >-
    Of the 68 non-grid known-best records whose witness derives from Kingbird's catalogue
    and whose pose is symmetric under a non-trivial subgroup of D4 at the family census's
    tight band (centres and angles within 1e-6), at least 7, one in ten, admit a packing,
    reached by a local re-optimization seeded from the retained witness with no symmetry
    imposed, whose independently verified side is below the retained side by more than
    1e-9 and whose tight-band symmetry group is strictly smaller than the record's. The
    symmetry of those families is then partly a property of who drew them, not of the
    optimum.
  lane: search
  derived_from: [X-049]
  strategy_refs: ['search:13', 'search:19', 'search:20']
  criterion:
    shape: conditions
    metric: >-
      The count of the 68 records (listed by n in the notes) for which the re-optimized
      pose, verified by sqpack.verify.verify_packing and
      devtools.check_rational_witness_independent at a rational side, has side below the
      retained reported_side by more than 1e-9 and a strictly smaller tight-band symmetry
      group under the family census's symmetry test; reported beside it, the count with a
      lowered side regardless of symmetry.
    direction: >-
      At least 7 of 68. Rejected when fewer than 7 after the full declared budget on every
      record, provided the positive control passes: the same optimizer, seeded from the
      44 pre-Couzo Kingbird-derived witnesses at Couzo's counts (git af33edf6e^,
      packing/witnesses/known-best/), where T-056 proves an improvement of 3e-8 to 0.022
      exists, lowers at least 9 of the 44, one in five. If the control fails the round
      is unresolved: the instrument cannot see improvements known to exist. The two
      proved-optimal members, n = 5 and n = 10, stay in the denominator as negative
      controls; a lowered side there is a verifier failure, never a result. Every
      lowered side, however few, is a candidate upper bound that enters promotion
      separately and never moves the frontier from this round.
    threshold: 7
  instrument: >-
    A seeded re-optimizer that reads Witness/v2, not yet written. The parts exist:
    sqpack.research.quench.quench_bracket, the LP-in-cell quench that
    devtools.polish_sweep_archive runs on annealer poses, re-minimizes the side from
    given centres and angles (the motion lab's interactive form is capped at 20
    squares); the family census's symmetry test and the two verifiers are retained. The
    Rust engine sqsearch starts from random placements and takes no seed pose, so it is
    not the instrument. The build: load a witness, apply a declared small random kick
    so the pose can leave the symmetric point, quench to a local optimum, repeat over
    seeds within the timebox, keep the best verified pose, report its census symmetry;
    byte-identical replay under --check.
  instrument_ready: false
  regime: >-
    Numerical, double precision, local optimization seeded from the retained witness
    with no global search; the atlas corpus frozen at the X-049 family census
    (campaign/explorations/X049-families-data/family-census.json over
    atlas/known-best/manifest.json); verification exact over Q or by outward-rounded
    intervals; the symmetry test the census's tight band at 1e-6; an equal per-record
    budget, timebox and seed count declared before the round, for the 68 targets and the
    44 controls alike
  instance: {axis: corpus, point: atlas-known-best-symmetric-kingbird-derived-68}
  priority: 3
  cost_estimate: >-
    Half a day of agent time for the tool; runs of minutes per record over 68 targets and
    44 controls, about 19 CPU-hours at a 10-minute timebox; wall time is the budget here,
    not pair-tests
  prereqs:
    - a seeded Witness/v2 re-optimizer with a --check replay
    - the 44 pre-Couzo control witnesses recovered from git history as a frozen file set with digests
  replication: true
  registered: '2026-10-02'
  notes: >-
    Premises recomputed 2026-10-02 from family-census.json: 97 Kingbird-derived records,
    all with non-integer sides, 68 symmetric at the tight band (D1-diagonal 23,
    D2-diagonal 19, D4 13, C2 8, D1-axis 4, C4 1), 53 of them with an a + b sqrt(2) side,
    3 rational, 12 with no closed form; 50 packet-derived records, none symmetric. The
    68, by n: 5, 10, 18, 19, 26, 27, 28, 37, 38, 40, 50, 52, 54, 65, 66, 67, 70, 82, 84,
    85, 88, 89, 101, 104, 107, 109, 122, 124, 125, 145, 146, 147, 148, 149, 150, 153,
    170, 171, 173, 174, 175, 178, 197, 198, 200, 201, 202, 203, 226, 227, 229, 230, 231,
    232, 233, 257, 258, 260, 262, 264, 265, 267, 290, 291, 294, 295, 296, 298. X-049's
    wording "the packet sources' optimizer" has no instrument behind it: Couzo's
    repository states no method, no tolerance and no checker, so the repository's own
    quench stands in. The control: of the 49 counts T-056 superseded, 44 had
    Kingbird-derived witnesses before commit af33edf6e and five had UnitSquare
    renderings. Relation to H-030 and H-051: those calibrate a surgery grammar on
    held-out UnitSquare children and reuse the same held-out design; this measures a
    population property of the catalogue's symmetric records. Relation to H-025: that
    permits refitting to few angle classes at a side cost, this permits any local motion
    and asks for a side gain. The threshold of one in ten is the registrant's choice of
    what "a measurable fraction" means; X-049's own falsifier was no move at all, which
    this criterion includes.
---
# H-272: Is the Symmetry of the Catalogue’s Records Drawn or Found?

X-049’s census found that symmetry follows the source, not the family: 68 of the 97
Kingbird-derived records are symmetric at $10^{-6}$, and none of the 50
optimizer-derived packets.

The 68 targets and the dated premises above remain the 2026-10-02 baseline, recoverable
from the family census at commit `69ddc7d988ba689cf887bdd0cb7fd64fdcf8c103`. The linked
census file is a live generated view; later atlas refreshes do not change this
hypothesis’s target population or thresholds.
Two readings fit. Optimizers stop short of symmetric optima, which the packets’ 2,400
slack squares make plausible, or the catalogue’s drawings impose a symmetry the optimum
does not have.
Re-optimizing the 68 without a symmetry constraint separates the readings:
a verified lower side with a smaller symmetry group says the drawn symmetry was not the
optimum’s.

A positive means construction families and optimum families are distinct, the symmetric
look of the $k^2+1$ column is partly the drawer’s, and each moved record is a candidate
upper bound for promotion.
A negative with a passing control means the symmetric records are local optima and the
difference between packets and drawings is the optimizers’ looseness, so the census’s
source confound is about packets, not about the catalogue.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
