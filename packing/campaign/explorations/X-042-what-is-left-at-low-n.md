---
title: X-042 — what is left at low n, after the n = 17 ladder merged
softschema:
  contract: packing.squares:Exploration/v1
  schema: ../schemas/exploration.schema.yaml
  envelope: exploration
  status: enforced
exploration:
  id: X-042
  title: What Is Left at Low n, After the n = 17 Ladder Merged
  date: '2026-09-22'
  author: Claude session-151 coordinator, with four Fable review lanes and an adversarial Fable validation lane
  campaign: packing.squares
  brief: >-
    Ask again what significant improvement is available at n = 11, n = 17 or another
    low n, now that T-031, T-032 and the Kleddamag retention have merged and the n = 17
    ladder carries five values. Four lanes with disjoint deliverables: the n = 11
    one-body ceiling and what provably escapes it; the n = 17 measure and where the
    remaining gap lives; the cross-n integer plateaus; and the upper-bound and search
    side, which no lower-bound lane covers. Each lane recomputes the arithmetic it
    relies on, because a review that only reads the record inherits the record's errors.
  sources:
  - AGENTS.md
  - operating-rules.md
  - epistemics.md
  - packing/campaign/explorations/X-040-lower-bound-mechanisms-beyond-the-one-body-ceiling.md
  - packing/campaign/explorations/X-041-after-the-n17-certified-bound.md
  - packing/campaign/explorations/X-037-n11-overnight-review-and-route-slate.md
  - packing/frontier/n-011.md
  - packing/frontier/n-017.md
  - packing/frontier/RESULTS.md
  - packing/frontier/CERTIFICATE-REACH.md
  - packing/frontier/covering-values.yaml
  - packing/resources/web/n17-kleddamag-certified-bound-2026-09-21/kleddamag-17-squares-certified-bound/global-certificate.json
  - docs/project/reviews/review-2026-09-20-n17-r012-and-mira-4613-proof-review.md
  - docs/project/reviews/review-2026-09-21-n17-kleddamag-461300-99853.md
  proposes: []
---
# X-042: What Is Left at Low n, After the `n = 17` Ladder Merged

**Status: a review and a ranked slate.** Two measurements were taken while it ran and
are reported here with their rungs; no bound moved and no hypothesis was decided by this
document. `X-041` is its predecessor and this report contradicts it in nine places, each
named below with the recomputation that settles it.

**Reconciliation note, 2026-09-22.** The later external-certificate intake verified
Kleddamag’s stronger `s(11) > 31/8 = 3.875` result.
The T-033 passages below retain the earlier first-party result and the review’s
sequence; they no longer describe the current Frontier lower bound.
The unchanged T-025/T-026/T-033 fixed-core family has ceiling `955000/249507 ≈ 3.82755`,
below `3.875`, so further net refinement alone cannot improve the current bound.
Changed weights, sites, parent domains, and charge atoms stay outside that conclusion.

## The Three Claims a Reader Should Carry Away

Stated first, with their evidence, because each one redirects work that `X-041` ranked
differently.

> **1. The `n = 17` ladder is not converging on `4.613`; it is climbing away from it,
> and the only invariant of a certificate in that language is `sigma = L/A`.** `A` moved
> *away* from 1 across the five values — `0.99999379`, `0.99999`, `0.99975`, `0.99951`,
> `0.99853` — and `L/A` rises as `A` falls.
> Under the scale invariance of the parent language, `L = 4613/1000` is a normalisation
> inherited from Mira’s atom coordinates, not a constraint, so “a larger `L`” is not a
> mechanism at all. The cap on the ladder is `s(17)`, not `4.613` and not `4.6755`.

> **2. The external `n = 17` measure has not been re-priced against its own final
> catalogue, and that — not the restriction, and not the atoms — is where its remaining
> headroom is.** Two-thirds of its 7,853 rows sit on a plateau at the identical minimum
> `1.00207034`; 2,631 rows lie below it, 26 within `1e-4` of the global minimum.
> The surplus the measure was priced to carry is `0.0368`; what survived is `1.13e-4`.
> Row generation is not converged.

> **3. At `n = 19` and `n = 26` the target itself is less defended than elsewhere in the
> low range** — but this claim was overstated in the draft that opened the block, and
> the block’s own measurements corrected it.
> `n = 26` has the largest gap below `n = 27` at `0.4982` and has been improved twice
> historically. `n = 19` is the low non-grid cell no search has ever *reached*, which is
> weaker than “worst served”: after the same polish, `n = 26` sits `8.58e-2` and
> `n = 27` `6.90e-2` from their records against `n = 19`’s `3.03e-2`.

The `0.073` figure the draft quoted for `n = 19` was **the annealer’s stopping point,
not the repository’s best**, and it is now superseded twice over.
Polishing `exp-202`’s own archived poses — no new search, the same bytes — reaches
`4.915912971524`, a gap of `3.029e-2`; a four-times-budget sweep then reaches
`4.888118685629`, a gap of **`2.501e-03`**. The lesson generalises and is worth more
than the number: where the annealer only just escapes the grid, its reported side is not
a local optimum and should not be quoted as the search’s result.
`n = 27` shows the same `5.37e-2` polish gain.

All three are `V0/C0`: each is a reading taken once, in one-off code, on retained bytes.
`OR-1` is explicit that a measurement left in one-off code is a missing tool, and the
three tools these readings show are worth building are named in the slate.

## The One Bound That Moved

Stated before the rest, because it is the only movement in the block and because it came
from the slate’s lowest-ranked row rather than its highest.

> **`s(11) >= 955000*sqrt(2073600042893309449)/359341754646249 = 3.826997548829543624`**,
> against `T-026`’s registered `3.826447410572939744`. A movement of
> **`+0.000550138257`**.

The frozen `T-025` threshold atoms were re-certified at the **2880-step net**. The
crossing shrink does not rise under refinement — the 1,440 directions the finer net adds
do not break them, least charge exactly 1 — so halving the net gap `D` moves the
dilation-limit supremum with no new mathematics.
`X-041` called this a rung to be run in an idle CPU slot and never as a block, and that
is exactly how it was run.

Two things make it trustworthy rather than merely arithmetic.
The same run’s 1440 leg is a control and reproduces `T-026`’s registered surd exactly.
And the retention gate accepts the frozen bytes by **both** routes: the interval route
returns a zero-width enclosure `(1, 1)` over 5,761 directions and 23,785,079 boxes with
no stalls, the exact route independently finds least cell charge 1 at direction 1828 and
re-evaluates it at its witness by membership counting, and the two agree — `RETAINABLE`,
`sha256 fefcf8ac…`.

The value sits below `L/B* = 3.827547924507` and below the point-certificate ceiling
`L* = 3.828806254385`, and neither comparison is an independent check of the run.
`S < L/B*` is an algebraic identity, since `sqrt(1 + D^2) < 1 + D` for `D > 0`, so a
value above it would have meant an arithmetic defect rather than a better result.
And `L*` is the ceiling on *point* certificates, which is precisely the bound threshold
atoms are built to pass: `S < L*` holds here because `B* > 9977/10000`, which the
refinement measured, not because a theorem forbids a threshold certificate above it.
The dilation-limit theorem establishes the bound as a supremum and **supplies no
individual certificate at that side**, so the strict inequality there is not claimed.
The register entry is a separate decision and is not written by this report.

## Evidence Boundary

Read in full by the lanes: `AGENTS.md`, `operating-rules.md`, `epistemics.md`, `X-040`,
`X-041`, `X-037`, `n-011.md`, `n-017.md`, the `T-025`, `T-026`, `T-030`, `T-031` and
`T-032` register entries, `CERTIFICATE-REACH.md`, `covering-values.yaml`, the `T-025`
and `T-026` proof packets, the lane-a2 finer-net record, the two `n = 17` proof reviews,
the Kleddamag artifact’s `PROOF.md`, `global-certificate.json` and release replay, and
the `ceiling`, `threshold`, `relational`, `certificate` and `sweep` modules.

Not done here: no gate was run by any review lane, no instrument was built or retained
by one, and the artifact’s own checkers were not re-run except as noted.
The two measurements this document reports as its own are the `A1` sweep row and the
environment repair, both below.

## Nine Corrections to `X-041`

Each was found by recomputation, not by reading.
Where a correction changes what should be run, the slate row says so.

| # | `X-041` says | Recomputed | Consequence |
| --- | --- | --- | --- |
| 1 | The covering-LP experiment tests “what the selector and the restriction are worth” | `A2` as specified also swaps the adaptive per-row selector (`t` within `0.006°`, `B_row` in `[0.998367, 0.998526]`) for fixed net directions and `B_min` | A plain fail confounds the restriction with the catalogue change and cannot be reported as the restriction’s worth |
| 2 | `A1`’s kill: a lock at `B = 0.9995` means the restriction carries at least `4.6142 − 4.6130` | The rigorous floor is `4.61415 − 4.61398 = 0.0002`, and it is a floor on restriction *plus* selector *plus* support difference | The kill rule as written overstates by 6× |
| 3 | The universal one-body ceiling is “`>= 4.6137` (Mira’s unrestricted point certificate)” | The certificate proves `4.61303`, its dilation endpoint; `4.6137 = L/B` is the `D -> 0` idealisation the lane-a2 record says does not hold for frozen atoms | Over by `6.6e-4` |
| 4 | “Exactly one row is tight … no other within `1e-6`” | Literally true and misleading as a headroom signal: 13 rows are within `1e-5`, 26 within `1e-4`, and two-thirds sit on a `1.00207` plateau | The tight-row count is not the quantity that carries information; the slack distribution is |
| 5 | “The restriction is worth at least `+0.0011` when priced for” | R038’s `+0.0011` over R012 is confounded with the selector *and* a doubling of the support (3,280 against 1,616 atoms) | “At least” is not established |
| 6 | `L*` “is exactly T-025’s own `L/B` on the 181 net” | True by construction — the family and T-025 share `(L, B)` — not by theorem; and `L/B` is not the theorem-bounded quantity | A point certificate’s `L/B` may exceed `L*` by `(1+D)/sqrt(1+D^2)`, up to `3.837607` on the 181 net |
| 7 | The `n = 17` atoms are virtual sites, the `n = 11` atoms encode relations | T-025 itself carries a D4 orbit of eight 2-of-3 atoms of diameter `0.0006`, 7.1% of its threshold budget, straddling `x = B` | Right in proportion (93% wide), wrong as a dichotomy: `n = 11` already uses the virtual-site trick |
| 8 | `n = 20, 21`: “what binds: integer endpoint” | The endpoint forbids reaching `5`, not improving `4.85`; on retained site sets the covering value binds (`19.81` at `4.85`), extrapolating to crossing `20` near `4.86`. Same conflation for `n = 12` | Two slate rows misdiagnosed; a `+0.005` to `+0.01` prize is mislabelled unreachable |
| 9 | `L/B = 3.833820` for `153/40` | `38250/9977 = 3.833818` | Sixth decimal |

A tenth item is an omission rather than an error.
The parent-centre envelope restriction is priced for `n = 17` throughout `X-041` and
never considered for `n = 11`, where the core-scale 88-family does not obstruct it at
`3.82`: its 40 axis-aligned placements have centres `0.498853` from the wall against the
envelope inset `0.5`. It cannot pass `L*`, but it is the cheapest unused lever inside
the last `0.0024` and a free tightening of every retained certificate.

## What the `n = 11` Ceiling Is, Exactly

The `L*` argument reconstructs without a gap.
Scale the 88-family by `1/B` into unit squares in `[0, L*]^2` with closed depth at most
1 and weights summing to 11; weak duality then forces `mu(K) >= 11` for any measure
charging at least 1 to each member; and T-025’s own selection step puts an admissible
core inside each member, so depth does not rise.
No point certificate exists at any side at or above `L* = 38200/9977`, for any shrink
and any net.

What a stronger method must violate is therefore exactly one of two hypotheses:
**additivity** — a charge that is not `mu(P)` for any measure — or **unconditionality**,
a hypothesis about the packing that removes poses of the family without removing count.
That is a sharper statement than the record had, and it settles four candidate routes
negatively at a stroke.
Angle-dependent measure families do not escape, because disjoint cores consume disjoint
sites and the pointwise maximum is a single one-body measure with the same guarantee.
Nor do per-direction shrinks, the unshrunk `B = 1` language, or the parent-centre
envelope. Only relational two-body atoms, `k`-of-`S` and floor atoms, structural
conditioning, the wall-wedge emptiness lemma and higher-rank compositions violate a
hypothesis.

Near-coincident triples sit precisely on the boundary, and the reason is now a
proposition rather than a histogram.
A 2-of-3 atom of diameter `eps` covers the median site’s capture square minus an
`eps`-collar, at a point atom’s budget — so it is a point atom at a
**direction-dependent** virtual site, which no single site can emulate, and which three
point atoms emulate only at budget `3w/2`. Its genuinely relational content is a
pinwheel cut, and a pinwheel needs three placement classes each containing exactly one
pair of the triple. At `eps = 0.014` that is a measure-zero coincidence against a finite
family; at `eps = 0.53` it is generic.
So the virtual-site mechanism is capped with the point language, and the wide-triple
language is not.

## What the `n = 17` Measure Is, Exactly

The sharpest new fact is the slack distribution, and it points somewhere `X-041` does
not. The measure was priced to carry a surplus of `0.0368` and retains `1.13e-4`.
Two-thirds of its rows share one plateau minimum; the 2,631 rows below it group into 24
contiguous angular clusters.
The binding is not the cap signature `X-014` predicts — that would need three tight rows
at the folded Bidwell classes at once, and the tight row at `38.06°` is `1.44°` and
`1.74°` from the two tilts.
It is an optimizer residual on a catalogue that moved under the measure after the
measure was priced.

The restriction, meanwhile, is load-bearing for this artifact and now has an exact
witness rather than an inference: at row 6512, `40.379°`, the core whose vertex touches
the wall sits outside the envelope by `5.5e-5`, captures 561 points, and charges
`199827543/200000000 = 0.999137715` against `M/17 = 0.999907492`. The restricted domain
is nonetheless a genuine relaxation of the unrestricted one, so a pass on the
unrestricted test would still be decisive; it is the *fail* that is confounded, and that
is why correction 1 matters.

## The Two Measurements This Document Reports

**The `A1` cell on our own support, at the external side.** One run at `n = 17`,
`L = 4613/1000`, `B = 9995/10000`, the 181-direction net, seeded from the retained
`n = 17` certificate with a five-per-window lattice: 7,253 sites, 40 rounds, deadline
reached, objective `17.177501`, least covered mass `0.968232`. Unconverged and above 17.
That is consistent with the register’s `17.195968` at `461/100` and says our own site
set does not reach the external side at this net.
`V1/C1`: one run, one instrument, recorded with its command and its round table, not
reproduced.

**The research loop did not run at all in a fresh clone.** Five preconditions no
document named: the image’s `uv` could not resolve the pinned interpreter, the clone was
shallow, a submodule was absent, node modules were missing, and the Rust engine was
unbuilt. After repair the edit tier passes at `124.4 s` against its `240 s` ceiling.
This is recorded because a review block that cannot run its own instruments is not a
review block, and because the next session should not rediscover it.

## What the Unrestricted Test Actually Returned

The `A2` cell is decided, and the number is not marginal.
Read through the gate’s own exact route at a stratified sample of the 1440 net, the
measure’s **least charge is `305414321/1000000000 = 0.305414321`, at direction 0**, the
axis-aligned one, with the witness core pushed into the container corner `1.4e-5` off
flush against both walls.
Nine of the seventeen sampled directions charge below 1. Direction 0 belongs to every
net this repository builds, so the refutation holds at 288, at 1440 and at every finer
net.

That is not a near miss, and it is the expected shape once the restricted domain is
understood: the parent-centre envelope is exactly what excludes corner-flush cores, and
a measure optimised against it has no reason to charge them at all.
The whole-net figure varies domain, selector and net together, so `0.305414321` is an
**upper bound on what the restriction alone costs and never a measurement of it**. The
measurement is the single-row witness above, which moves only the centre.

A `Condition 5'` decision is a conjunction over directions, so a sample can refuse and
can never accept.
Seventeen directions of 1,441 refute; they are not a complete decision,
and none was run.

## The Gate Cannot Reach These Artifacts, and That Is Structural

Found by running the `A2` cell rather than by reasoning about it, and it bounds the
whole external-intake programme rather than one experiment.

`decide_threshold_certificate` retains a record only when **both** routes accept it.
The interval route refuses any input above `MAX_INTERVAL_ATOMS = 4096`
(`src/sqpack/fractional/interval.py:145`), a deliberate memory guard whose own comment
sizes it against the repository’s experience: “the largest retained certificate has
2,260 atoms”. The external `n = 17` measure expands to **6,744 point atoms and 2,008
threshold atoms**, so the interval route refuses it outright and prints
`REFUSED: the interval verifier supports at most 4096 atoms`.

The consequence is not about this artifact.
**No external measure above 4,096 atoms can be retained by this repository’s gate as it
is built**, whatever its mathematics, because one of the two required routes will not
look at it. The `C4` rung is structurally out of reach for artifacts at the scale they
now arrive at, and the five-value ladder shows that scale is rising — 1,620 atoms, then
1,616, then 3,280, then 8,988 sites.

The cap is not confined to the interval route either.
`AtomData.of` is the point route’s loader as well, so an `A1` certificate that keeps
more than 4,096 atoms from this support meets the same wall: the ceiling binds the
first-party colgen route at this scale too, not only the intake of someone else’s
measure.

The guard is conservative rather than fundamental.
It exists to refuse an input-driven allocation in the hundreds of megabytes, and it does
that by capping the atom count because the boxes-by-atoms mask is materialised whole.
Batching over atoms as well as over boxes would keep the same memory ceiling at any atom
count: at `BATCH = 4096` and 6,744 atoms the full mask is about 27 MiB, which is the
size the cap was chosen to avoid and not a size the method requires.
Raising the cap without chunking would not be the fix; chunking is.

Until that is done, an external measure of this size can be replayed, reviewed and
retained as bytes — which is what `T-032` and the Kleddamag retention did — and cannot
be decided by this repository’s own two routes.
That is worth stating plainly next to every claim about what the intake programme can
verify.

## Two Findings That Change the Slate Itself

**`fold_ceiling_family` is one-sided, and the record’s own calibration proves it.** At
the one side where the truth is known — `n = 11` at `191/50`, where the true covering
value is exactly 11 and the 88-family verifies it — every fold ever produced from a
column-generation dual sits two to six units low: the session-139 cap-32 folds read
6.82, 6.50, 7.12, 6.84 and 5.21; `BC-200`’s at `1152/175` read 6.58 and 9.91 after eight
cutting iterations; a cap-64 rerun this session folded 6.94 raw and polished to exactly
9\. The 88-family did not come from folding a colgen dual at all — it came from a
threshold-enriched 13,721-site LP and a separate extraction.

So a fold at or above `n` proves a ceiling, and **a fold below `n` proves nothing**.
`X-041`’s `A6` row sets its kill as “total below 18 after polish — the lock is an
artefact”, and that inference is invalid.
Only the positive branch is a kill.
The two-sided instrument is the cutting-plane loop, which ends either with a restricted
optimum below `n` on an enlarged support (an artefact) or a folded total at or above `n`
(a ceiling), and which can stay undecided for a long time.

**The `25.000000` plateau at `n = 26` and `n = 27` is a real floor, not the unexplained
artefact the record calls it.** If `(m-1)B < L` then the `(m-1)^2` axis-parallel
`B`-squares on a lattice of pitch `B + g` are pairwise disjoint closed sets, so every
covering measure on every site set has mass at least `(m-1)^2`. At `L >= 5B = 4.9885`
that is 25, and the loop is not stuck on an artefact: it is sitting on a degenerate
primal face above a tight trivial dual.
`exp-215`’s metric text and `X-041`’s `A5` row both mislabel it.
The genuinely artefactual integer locks are a different mechanism — when `L < kB` the
`k` squares across `[0, L]` force total overlap into fixed windows, and an auto grid
with no site coordinate in those windows makes the `k^2` placements pairwise
site-disjoint. That was measured exactly here at `n = 12` (`L = 3.98`, `3.985`, `3.99`)
and at `n = 21` (`997/200`), and it is cheap to test: `L < kB` and an empty window per
axis.

## The `n = 27` and `n = 28` Candidate: Run, and Refused for a Reason Worth Recording

The retained `n = 29` candidate at `548/100` was taken up in this block as `exp-225`,
and the outcome is a clean negative with a precisely located cause.
**No bound moved.**

The premise holds exactly.
Across the whole decision path `n` is read only by Condition 2
(`certificate.py:253-259`), by an `int64` guard that is monotone and strictly safer at
lower `n`, and by string fields; `sweep.py`, which is Condition 5’s engine, never sees
`n` at all. `decide_certificate` prints `certifies every n >= 27` on the bytes itself.
And `n = 29` at this side is not registered either — it is a covering row with
`frozen_artifact: null` — so `5.48` would move that too.

Re-rationalising at bump `103/100` raises the mass to `107289303/4000000 = 26.822326`,
keeping `0.1777` of headroom below 27, and lifts the declared least cell mass to
`4120021/4000000 = 1.030005`. **At the theorem’s own threshold that clears the
obstruction completely**: run with `enclose = False`, Condition 5 *holds* over the full
363-direction doubled net, 2,707,989 boxes, **zero stalled**, against the un-bumped
baseline’s 272 stalled and `undecided`.

**The gate nevertheless refuses, and not for the same reason.** It runs the interval
route with `enclose = True`, where a box settles against the *exact minimum* rather than
against mass 1. That shortfall is **relative**, so reweighting moves both ends of the
enclosure together and buys essentially nothing: `0.3980737%` before the bump,
`0.3973038%` after. All 272 stalled boxes sit in **direction 0**, the axis-parallel one,
at the seam where one coverage region’s leave-edge at `x + B/2` lands exactly on
another’s enter-edge at `x' - B/2` — unsplittable below the `1e-12` resolution floor.
The other 362 directions certify.

Raising `BOX_BUDGET` would not help and was not tried: `budget_exhausted` is 0
everywhere, the budget being per direction.

So what exists is a candidate whose five conditions are established by the exact
event-cell sweep **and** by the interval route at the mass-1 threshold, refused by the
retention gate on its enclosure-agreement requirement.
**That is a finding about the gate, not a bound**, and nothing is registered on it.
Whether a recorded escape from the agreement requirement is sound policy is a question
for the gate’s owner, and `D-435` is exactly why acceptance is asked the same question
in both modes.

## The Re-Pricing Prize, Measured and Bounded

Claim 2 above says the external measure has not been re-priced against its own final
catalogue and that this is where its headroom is.
The block ran that as `exp-222`, and the result bounds the prize rather than collecting
it.

**The A2 discriminator fires “confirm” on its face, and that reading is wrong.** The LP
over 1,387 orbit variables on the 7,853 extracted cells optimises to `16.776137532`,
well under the `16.99` the slate set.
But that optimum is supported on **93 orbits of 1,387**, and put back into the sweep
over the whole continuum it charges `0.608365` at row 6042 and would need mass **27.58**
to be a certificate.
One cell per row is far too weak a relaxation for its value to say anything about a
certificate. The slate’s own discriminator was badly chosen, and the lane’s separation
probe is what caught it.

What the lane does produce is a **floor**, and a floor is the useful direction here:

| Quantity | Exact | Float |
| --- | --- | --- |
| The artifact’s own normalised mass | `16998427356/1000020517` | `16.998078606` |
| **Floor under any re-priced measure on this support at this `(L, A)`** | `33945829752/2000000005` | **`16.972914834`** |

Because a subset of constraints can only lower an optimum, that floor is valid
catalogue-wide. So **re-pricing at fixed `(L, A)` on this support is worth at most
`0.025163774` of mass**, and the floor had not converged when its deadline hit — it was
still climbing at `4e-4` a round — so the true figure is smaller.
Under a stated sensitivity heuristic that is at most about **`+0.0034`** in the bound,
no more than roughly `4.6232` against the artifact’s `4.619791`.

`H-233` is therefore neither killed nor confirmed; what replaces it is a quantified
ceiling on the prize.
**The consequence for the slate is direct: `A2`’s weight should move to the sites
side**, because the weights alone cannot carry more than that.

Two further readings from the same lane.
Every slack figure this report quotes reproduces from the lane’s own sweep of all 7,853
rows. And on `H-239`, the `X-014` cap signature is **not** present at `4.6198`: only
`24.6%` of dual mass sits within `0.5°` of a folded Bidwell class, against the `50%` the
signature would need, and almost all of that is at `0°` rather than at either tilt.
That last is the weakest measurement of the block — it is the dual of a primal the
separation probe has just refuted — and is recorded as a first look, not a decision.

## What the Upper-Bound Lane Measured, and Three Things It Corrected

**The grid escape is the null, and the null is total.** At `n = 12`, `20` and `21`, all
fifteen runs and all 120 individual chains behind them returned the grid exactly —
`4.000000000000`, `5.000000000000`, `5.000000000000`. The seed-to-seed spread is not
small, it is zero, and polishing all fifteen best poses returns the integer again, so
the grid is a fixed point of the LP-in-cell quench too and not merely where the annealer
stops. That is the first grid-capable search ever run at these three sizes.

**`n = 19` was not decided.** A four-times-budget sweep — not the ten declared, because
the host runs this arm at about an eighth of `exp-202`’s rate and five seeds at `5e9`
was chosen over two at `1.25e10`, the kill rule being written over five seeds — reached
`4.888118685629` on seed 4, `2.501e-03` from Wainwright.
Neither branch of `H-U2` fires: no seed is within `1e-4`, and not all five sit at or
above `4.8956`. Every kept pose has least pair separation and least wall margin exactly
`0.0`, rather than a small negative cleared by a tolerance.

**All six one-sided tilt slopes are positive**, so no sub-record packing exists in the
axis-plus-one-angle family at `n = 18`, `19` or `26`. The shapes differ in a way that
matters: `n = 19` and `n = 18` are smooth quadratic minima, while **`n = 26` is a
genuine kink**, its one-sided slopes tending to `+1/2` on both branches.
A central difference there returns 0 and reports a smooth stationary point that does not
exist, so taking the slopes branchwise was load-bearing rather than pedantic.

Three corrections follow, and the third is to this block’s own briefs.

1. The `n = 19` figure, above.
2. **`exp-202`’s escape-mechanism story does not survive more points.** Measured over
   six cells rather than three, single-square proposals lower `required_side` in 0 of
   144,000 draws at every cell and scale, *including the cells that do escape*, so the
   statistic is a fact about trivial grids and not a discriminator.
   The collective-lowered rate does not predict escape either: `n = 26` has rate
   `0.0000` and escapes by `0.253`, while `n = 12` has `0.0006`-`0.0011`, higher than
   both `n = 17` and `n = 26`, and does not escape.
   **Why `n = 12`, `20` and `21` keep the grid is therefore unexplained**, and the
   three-point reading should not be quoted as though it had survived.
3. **The `4.888109` Stromquist `n = 19` figure carried in this block’s briefs is not in
   the record at all.** A search of the frontier, the resources and the campaign finds
   no Stromquist `n = 19` entry; the only retained Stromquist source is the 2003
   `n = 10` and `n = 11` paper.
   Seed 4 lands `9.69e-06` above that value, striking at five decimals, but its angle
   classes are five rather than one common tilt and reflection does not send them to
   `23.944°`. The coincidence is recorded, the basin is not claimed, and the number
   should not be repeated as though this repository held it.

## Ranked Slate

Ranked by expected information per hour against instruments that exist.
Rows marked **redesigned** differ from `X-041`’s because of a correction above.

### Tier A: the instrument exists and the design is sound

| Rank | Item | First discriminator | Kill | Why it ranks here |
| --- | --- | --- | --- | --- |
| A1 | **Are the `n = 17` triples necessary at these weights?** Empty `threshold_orbits`, set the budget to the point budget, run the artifact’s own sweep | Least point-only charge against `0.861183` | At or above `0.861183` — the triples are decoration at this `A` and the next rung is purely a sites problem | Four minutes, on retained bytes, independent of every contested theorem. The highest value per CPU-second on the slate |
| A2 | **Re-price the measure on its own final catalogue** (H-233) | The LP value on 1,387 orbit variables against 16.99 | Mass at or above `16.998` — no headroom on this support at this `A` | The `#1` ranked mechanism once the slack distribution is read; it is the ladder’s own next step |
| A3 | **`n = 20, 21` are site-limited, not endpoint-limited** (H-F) — **redesigned** | A point certificate of mass below 20 at `243/50 = 4.86` | Converged at or above 20 on two site sets | Corrects a slate row and is worth `+0.01` on a stock instrument |
| A4 | **The grid escape at `n = 12, 20, 21`** (H-U5) | Arm B at the exp-202 budget returns exactly the grid on 5/5 seeds | Any seed below — a new record | The first grid-capable search ever run at these `n`; converts “nobody looked” into a measured negative |
| A5 | **`n = 19` reproduction at 10×** (H-U2) | Best polished seed against `4.885618` | All five at or above `4.8956` | The one low-`n` record no search has reached; any seed below is a record candidate |
| A6 | **T-026 at the 2880-step net** (H-G) | Least charge at `B*` against `M/11` | Least charge below `M/11` — `B*` rises and the `0.0011` is not all available | A rung, not a mechanism: an idle CPU slot, never a block |

### Tier B: a bounded instrument first

`H-234` (the restriction’s worth, censused over all 7,853 rows rather than inferred) and
`H-C` (the parent-envelope domain at `n = 11`) both need the one small domain parameter
the `T-032` note already asks for, and they share it.
`H-A` (is the universal family immune to near-coincident triples?)
needs a face scan over the transported family.
`H-E` (is the `n = 18` lock an exact unit gap?)
needs the fold and both readers.
`H-U8` (core rigidity at the flexible records) needs `cases/trump11/tangent_cones.py`
generalised off its hard-coded `n = 11` tables.

### Tier C: retired or corrected

`H-228` **stays blocked, and an earlier draft of this report was wrong about it.** That
draft called it refuted as stated, on the ground that at side exactly 4 the sixteen grid
squares are disjoint and force `mu >= 16`. That argument uses the **interior**
convention; `H-228` is stated for **closed** unit squares, and sixteen closed grid
squares share their edges and vertices, so `sum mu(Q_ij) >= 16` is perfectly compatible
with `mu(K) < 12` once mass sits on the grid lines — an interior-line point is counted
twice and an interior vertex four times.
The refutation does not touch the hypothesis as written, and the adversarial validation
lane caught it before it travelled.

The closed convention is moreover sound for what `H-228` claims, by a scaling argument
that needs no shrink: if twelve unit squares pack at side `L' < 4`, scale by `4/L' > 1`
to get twelve parents of side above 1 in `[0, 4]^2` with disjoint interiors, take the
closed concentric unit core strictly inside each, and those cores are pairwise disjoint
closed unit squares, so `12 <= sum mu(core_i) <= mu(K) < 12`.

What the episode leaves is a **specification constraint rather than a verdict**: the
`BC-365` verifier must decide **closed** cores, because an open-core verifier is dead at
every integer side. The record nowhere fixes the convention, which is how the confusion
arose, and that is the thing to fix.

Angle-dependent measure families are killed outright by the pointwise-maximum argument.
“A larger `L`” at `n = 17` is not a mechanism, by scale invariance.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
