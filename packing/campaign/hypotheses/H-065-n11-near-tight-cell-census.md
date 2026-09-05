---
title: H-065 — the near-tight set on the retained n = 11 certificate is a small fraction of the reachable cells
softschema:
  contract: packing.squares:Hypothesis/v1
  schema: ../schemas/hypothesis.schema.yaml
  envelope: hypothesis
  status: enforced
hypothesis:
  id: H-065
  kind: hypothesis
  claim: >-
    On the retained 381/100 certificate at n = 11 -- 1121 atoms, B = 9977/10000, total
    mass 434547/40000 = 10.863675, least cell mass 4001/4000 -- the reachable event cells
    whose covered mass is at most 1 + 1/20 are, summed over the 181 net directions, fewer
    than one fifth of the reachable cells, so the near-tight set is enumerable and
    Corollary 1a's exact-cover step is a check rather than a search.
  lane: proof
  derived_from: [X-014]
  strategy_refs: ['proof:10', 'proof:22', 'proof:23']
  criterion:
    shape: record
    metric: >-
      the count of reachable event cells with covered mass at most 1 + epsilon divided by
      the count of reachable cells, per direction and summed over the 181 directions, for
      epsilon in {0, 1/100, 1/20, 1/10}
    direction: >-
      accepted if the epsilon = 1/20 ratio, summed over the 181 directions, is strictly
      below 0.20; rejected if it is at or above 0.50, which is X-014's own kill line --
      the tight set covering most of the centre domain, so the mass gap constrains nothing
      enumerable; between 0.20 and 0.50 the round is inconclusive and reports the number
      rather than a verdict
    threshold: 0.20
  instrument: >-
    devtools/census_tight_cells.py, built in agenda-021's BC-201 with a test. It is a
    readout and not a new computation: sweep.minimum_covered_mass_integer already fills
    the mass grid before it takes the minimum, and sweep.reduce_to_spans already returns
    the reachable cells as one (i, j0, j1) span per column, so the census counts what the
    decision already touched. Per direction it emits the reachable-cell count, the count
    at each of the four margins, and the bounding box of the tight set in the rotated
    frame. Its test pins the counts on a small synthetic certificate where they can be
    computed by hand and on one direction of the retained rung.
    OR-1 is why this is a tool rather than a script: the same readout is wanted again at
    whatever side agenda-021's BC-200 finds the wall, and on the 3.82 atom set once it is
    regenerated.
  instrument_ready: false
  regime: >-
    The retained certificate's own net and shrink, read from
    cases/n11_fractional_certificate/certificate.json: angle_limit 207107/500000,
    direction_steps 180, so 181 directions, B = 9977/10000. Exact arithmetic on the
    weights' common scale -- every retained certificate's weights are multiples of
    1/200000, because rationalise rounds to that scale -- so the census is decided in the
    same integers the sweep decides in and no float chooses a cell.
    One bookkeeping point, easy to get backwards. On a retained certificate every
    reachable cell carries mass at least one, since that is what Condition 5 says, so
    epsilon here is a census margin and not the mass gap M - 11, which at 381/100 is
    negative. The mass gap of Lemma 1 exists only at a side where a certificate fails; the
    census measures how many cells sit barely above one on a certificate that succeeds,
    which is the same geometry seen from the other side.
  instance: {axis: n, point: 11}
  sweep:
    axis: census margin epsilon
    points: [0, 0.01, 0.05, 0.1]
  priority: 2
  cost_estimate: >-
    60 elapsed minutes inside agenda-021's BC-201; this certificate already decides in the
    fast tier and the census adds a count per reachable span rather than a second pass
  prereqs: []
  replication: false
  registered: '2026-09-05'
  notes: >-
    The 0.20 accept line is declared, not derived, and the record should say so plainly.
    X-014 states only the kill condition -- the tight set at epsilon = 0.05 covering most
    of the centre domain -- and no census of this kind has ever been run here, so there is
    nothing to estimate from. 0.20 is fixed before the tool runs so that the round can be
    wrong; 0.50 is X-014's "most" made numerical; and the honest outcome of a first
    census may well be the inconclusive band between them, which the criterion admits
    rather than hides.
    Why the answer matters in both directions. Covered mass is piecewise constant in a
    core's centre and changes only on the event grid, which is what makes the exact sweep
    finite, so the epsilon-tight placements at each direction are a union of event cells
    and the census is a readout of a grid the decision already filled. A small clustered
    tight set makes Corollary 1a's exact cover finite in practice and not only in
    principle: the atoms heavier than epsilon are partitioned into eleven groups, each
    inside a B-square at a net direction, and the assignment count is what the census
    bounds. A fat tight set says the mass gap constrains nothing worth enumerating -- and
    is also what an integrality gap looks like from the inside, since a fractional optimum
    far from any integral configuration is exactly a wide band of near-tight placements.
    That second reading is worth having whichever way the number falls.
    Scope. The claim is about one certificate at one side. It says nothing about the atom
    set at 3.82, which does not exist in frozen form, and nothing about the tight set at
    the wall agenda-021's BC-200 may find; both are declared in the sweep of the
    instrument rather than of this claim, and each would be its own round.
---
# H-065 — How Big Is the Near-Tight Set?

X-014’s Lemma 1 says that a certificate which has stopped proving infeasibility has not
stopped constraining packings: any eleven disjoint unit squares at side `L` carry cores
that are `ε`-tight against `μ` and together miss at most `ε` of `μ`’s mass.
In integer-programming terms it is reduced-cost fixing — a placement whose mass exceeds
`1 + ε` cannot appear in any integral solution, so the search may be restricted to the
`ε`-tight placements.

Whether that restriction is worth anything is an empirical question with one number in
it, and Corollary 1b says the number is already sitting in a grid the sweep fills.
If the tight set at the ladder’s top is a few hundred cells clustered around a few dozen
positions, the case analysis of Corollary 1a is finite in practice; if it is a fat
region, the mass gap constrains nothing enumerable and the chunking half of the owner’s
question is dead where it stands.

This claim measures it on the one artifact where the measurement costs nothing extra —
the retained `381/100` certificate, whose `1121` atoms already decide in the fast tier —
and declares the accept line before the tool exists.
The margin is a census margin: on a retained certificate every reachable cell already
carries mass at least one, and what is being counted is how many carry barely more.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
