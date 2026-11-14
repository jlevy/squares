# Proof Review: Khalili and Gharabaghi’s `s(k² − 5) = k` for Every `k ≥ 7`

**Date:** 2026-11-14. **Lane:** stage 4 of the
[result import runbook](../../../packing/campaign/result-import.md#stage-4-validate) for
issue [973](https://github.com/jlevy/squares/issues/973), lane L144, bead `think-h10k`.
**Reviewer:** Claude (AI review), strong sub-agent tier (`tbd-strong`), reasoning
setting not recorded, the stage 4 mathematical lane, separately prompted.
It shared no context with the import lane (L145), whose branch and packet it did not
read, and it read no earlier record discussion of the issue; `main` at `0db247de7` held
none. It froze its verdicts and the digests of its programs and outputs
([`receipts/freeze.sha256`](../../../packing/resources/web/khalili-gharabaghi-k2m5-973-review-2026-11-14/receipts/freeze.sha256))
before reading the record’s own material on `k² − 3`, `k² − 4` and `k² − 5`, which §11
then compares.
It ran programs it wrote, and the source’s and Daniel’s code after reading
it. Its plan, programs and outputs are the packet
[`khalili-gharabaghi-k2m5-973-review-2026-11-14/`](../../../packing/resources/web/khalili-gharabaghi-k2m5-973-review-2026-11-14/README.md).
It is not a human oversight record.

## Summary

This summary is written for the authors, Mohsen Khalili and Sara Gharabaghi.

**The argument holds as written.** For every `k ≥ 10` the claim reduces, correctly, to
one finite statement: every closed unit square in `[0, 11]²` has mass at least 1 under
the board `μ₁₁`. The family’s mass is `k² − 4D` with `D = 1340566927759/10¹² > 5/4`,
exactly. Lemma 7 (locality) is a correct proof, and the Lean theorem `k2m5_of_valid11`
states the reduction with `Valid11` about the board file verbatim and `minSide` as
Daniel’s `S32.lean` defines it.
The four-part proof of Theorem 10 covers the pose space.
The Tight-Tile Lemma is a sound blow-up argument: I re-derived each step (the chart
covering, the cell certificate and its concavity, the Lebesgue transport bound and the
three corner constructions) and read its implementation in full against the report.
I found no mathematical defect and no blocking finding.

**What was checked here, and how.**

- **Re-implemented clean-room, and decided here in full:**
  - the board’s exact total and D, and its D4 invariance as a measure;
  - the family file built into `μ_k` by your Definition 3: equal to the board at k = 11,
    with total `k² − 4D` for k = 10 to 40;
  - the premises Lemma 7’s proof uses, and its window identity for six values of k;
  - the whole θ = 0 face, without symmetry: the least one-sided limit is exactly 1, at
    3,000 of 40,000 corners, and at 750 of 10,000 in the D4 region, as you report;
  - the coverage step: all 1,255,023 leftover boxes lie in the lemma’s domain, and every
    job the domain needs is certified chart by chart;
  - the closure step of root 9632.

- **Replayed with your and Daniel’s code, on samples stated before running:**
  - `zmx2` built at the pin; the print patch is the one line you describe;
  - `cert0`, both ways;
  - three whole columns of the first-order sweep, census equal to your logs;
  - 40 random certified roots, all certified;
  - root 9632 and three tight-tile roots, box for box equal to your dumps;
  - `qx2_zm.py` on the 9632 window, equal to your run;
  - 8 random Tight-Tile jobs and the wedge-corner rerun, chart for chart equal to your
    outputs.

- **Probed with exact arithmetic written here:**
  - 41,268 poses, among them 3,280 at tilts `10⁻⁵` and `10⁻⁷` beside the tight tiles;
  - `zmx2`’s certified bound against exact mass in 3,300 of its tightest leaves;
  - your Tight-Tile bound `T` against exact `μ − 1` at 7,548 vertices of 1,968 certified
    cells.

  No pose fell below 1 and no bound exceeded the exact mass.

- **Controls:** your controls refuse as reported, and so do five of mine, each a
  genuinely invalid measure or a planted bookkeeping error (§6).

**What is not established here.**

- **The full replays.** The first-order sweep (about 15 CPU-hours here), the 75 coverage
  dumps (about 14) and the 323 Tight-Tile jobs (about 115 to 150) were sampled, not
  replayed (§9).
- **The Lean build.** It was not run: this host lacks the memory the precedent needed.
- **Two trust gaps.** `zmx2`’s area-density lemmas and its first-order Lemmas U and V
  decide most of the pose space, and this record has never reviewed them; Daniel’s own
  notes call U and V the least reviewed part (F1). The Tight-Tile Lemma has one
  implementation and no full replay (F2).

**Questions, none blocking,** are in §12: the per-root `zmx2` logs, which revision of
`run_tt.py` produced the outputs, `run_cov.sh`, and your own independent review.

## 1. What Was Reviewed

| Item | Where |
| --- | --- |
| Claim | `s(k² − 5) = k` for every integer `k ≥ 7`; issue 973, opened 2026-11-14T01:33Z by `moh63-dev` |
| Source | [moh63-dev/k2m5-family](https://github.com/moh63-dev/k2m5-family) at `2c0b1b9979bcb67d92eb215366dc5ee19286c1d8` (tag v1.0, the only commit, 2026-11-13T15:50:51−08:00), 467 files; all 466 entries of `SHA256SUMS_ALL` verify. Licence: `LICENSE` is MIT; the README adds CC BY 4.0 for text and data |
| Board | `certificate/sol_exact_box11.txt`, SHA-256 `d259fed5c9d5eb02c6fed85f5d1070e86d48f5717305f9e056c9a88adbd12099`, the issue’s `d259fed5…12099` |
| Family | `certificate/sol_exact_family.txt` (`643c1734…`), `certificate/sol_exact.json` (`b873ca94…`) |
| Checkers | evand/square-packing at `659ee62e4a9d39542a1146e8b011cc3ab6407ede`: `zmx2.rs` `e2bb84e9…`, byte-identical to the 4 October evand packet’s copy, with its `Cargo.toml` and `Cargo.lock`; `qx2_zm.py` `6294052a…`, the `T-064` and `T-081` checker, with `zm_mixed.py` `1fd20346…`, `mixed_cover.py` `bb89de15…` and `search/zeromargin.py` `3cb95fb7…` |
| Lean | `lean/K2m5/` (Fam10, Grid10, Inst, InstData, InstFam, InstC1–C7), against Daniel’s `lean/` at the same pin; `S32.lean` there is `4a3efd69…`, byte-identical to all four copies the record retains |
| Read in full | `paper/k2m5.tex`, `paper/tight_tile_report.tex`, `docs/CHECKING.md`, the READMEs, `verification/*.py`, `verification/verify.sh`, the patch, `tight_tile/*.py` and `*.sh`, `lean/K2m5/Inst.lean` and `minSide_eq` and `fileCover` in `Fam10.lean`; from Daniel’s tree, `ZMX2_AREA.md` §§0–1, 6, 11.2, 11.7, 12–13, `zmx2.rs` `run_root`, `cmd_cert` and the root grid, and `qx2_zm.py`’s header and `main` |
| Not read | the source’s `search/` tools (not part of the proof), `stress_family.py` beyond its header, the bulk of `zmx2.rs`’s area and first-order code (F1) |

## 2. Verdict

**Accepted as reviewed, with two major gaps for the record (F1, F2) and no blocking
defect.**

| Part | Verdict | Basis here |
| --- | --- | --- |
| Base cases k = 7, 8, 9 | Stand at the record’s entries | Not re-examined; §11 |
| Mass and D | Holds | Clean-room exact |
| Locality (Lemma 7) | Holds | Proof read; premises and window identity checked clean-room |
| Lean statement | Says what the issue says | Statement, `minSide` and data link read and checked; not built |
| θ = 0 face | Holds | Clean-room exact over the whole face; `cert0` replayed |
| 12,024 `zmx2` roots | Reported, sampled | 3 columns and 40 roots replayed with census equal; leaf probe clean; F1 |
| Root 9632 | Holds, given `zmx2` and `qx2_zm.py` | Both replayed in full on the root; closure clean-room |
| Tight-Tile Lemma | Sound as an argument and as code read | Proof re-derived, code read; 9 jobs replayed exactly; vertex oracle clean; F2 |
| Coverage of the 75 roots | Holds | Clean-room exact over all 1,255,023 boxes; 3 dumps replayed box for box |
| Controls | Refuse as required | Yours replayed, one with different cell counts (F8); five of mine (§6) |

This is a reproduction with the producer’s code for the `zmx2`, `qx2_zm.py` and
Tight-Tile parts, and an independent re-implementation for the mass, the family, the
locality premises, the θ = 0 face and the two bookkeeping steps (coverage, closure).

## 3. From the Board to the Claim

### 3.1 The statement and its split

`s(n)` is the least side of a square holding `n` unit squares with pairwise disjoint
interiors, rotations allowed.
The upper bound `s(k² − 5) ≤ k` is the grid.
The lower bound is:

| k | n | Lower bound |
| --- | --- | --- |
| 7 | 44 | the authors’ earlier mixed cover (§11) |
| 8 | 59 | Hosono’s mixed cover (§11) |
| 9 | 76 | Greff’s mixed cover (§11) |
| ≥ 10 | 95, 116, 139, … | the family `μ_k` of this source, through `Valid11` |

### 3.2 The family and its mass

`μ_k` on `[0, k]²` has the corner module `ν` in each corner (`[0, 4]²` and its images),
the wall period `ω₀` repeated along each side between the corners at depth up to
`R = 4`, and Lebesgue measure on `U_k = [19/5, k − 19/5]²`. My own builder, written from
Definition 3 and reading only the family file, found:

- every piece of `ω₀` (586) and `ν` (1,518) is an elementary piece of the 1/10 grid, of
  positive weight; `ω₀` lies in `[0, 1] × [0, 4]` with start phases in `[0, 1)`; `ν`
  lies in `[0, 4]²` and is invariant under `(x, y) ↦ (y, x)`; the periodic extension of
  `ω₀` is invariant under `x ↦ −x`;
- `ω₀` has total exactly `19/5`, so the term linear in `k` cancels against the Lebesgue
  term `(k − 38/5)²`;
- the built `μ₁₁` equals the board as a measure (13,148 distinct pieces; the board lists
  96 of them twice, where the corner module meets the bands’ end lines), with the same
  Lebesgue square `[3.8, 7.2]²` at density 1;
- the total of `μ_k` is `k² − 4D` for every k from 10 to 40, and `μ_k` is D4-invariant
  for k = 10 to 20; the board’s total is `28909433072241/250000000000 = 121 − 4D` with
  `D = 1340566927759/10¹²`, equal to `sol_exact.json`;
- the slack below `k² − 5` is `4D − 5 = 90566927759/250000000000 ≈ 0.362` at every k.

The source’s four built boards (k = 10, 12, 13, 20) equal this builder’s `μ_k`.

### 3.3 Locality (Lemma 7)

The proof splits each axis by the pose’s shadow `[a, b]` (`b − a ≤ √2`): (L) `a ≤ 4`, no
shift; (M) `4 < a` and `b < k − 4`, shift `⌈a⌉ − 5`; (H) `b ≥ k − 4`, shift `k − 11`. I
checked each step:

- The three cases are exhaustive and (L), (H) exclusive for `k ≥ 10`, since
  `b − a ≤ √2 < k − 8`.
- In (M) the shadow lands in `(4, 6.42] ⊂ (4, 7)`, the band of `μ₁₁`.
- Per axis, no corner or side-attached piece of the far side reaches the shadow; the
  band is invariant under integer shifts; `U_k` is a product, so the x- and y-cases
  combine.

The one step that needs more than the text says is “every segment has its endpoints on
the grid, so no segment crosses `x = R`” (`paper/k2m5.tex` lines 187–188). Grid
endpoints alone do not give it: a piece from 3.9 to 4.1 has them.
It holds because every piece is elementary, length 1/10, which the paper does not state
and which I checked (F5). The same fact makes case (L)’s “segments of `ω` in
`4 ≤ x ≤ 5.42` are the same for every `k ≥ 10`” hold.

As a check beside the proof, my builder compared, for k = 10, 12, 13, 14, 20 and 25, the
restriction of `μ_k` to every pair of the lemma’s x- and y-windows with the translate of
`μ₁₁` on the shifted windows.
That is 9 to 324 window pairs a k, and 17,836 to 103,636 pieces compared, with no
mismatch. Doubling one band weight of `μ₁₂` makes exactly the three windows that contain
it mismatch. The source’s own `locality_check.py`, which tests a different sufficient
condition (every 1.6 × 1.6 window of `μ_k` has an integer translate in `μ₁₁`), passes on
k = 10, 12, 13, 20 and refuses its one-weight mutation (176 windows).

### 3.4 The Lean statement

`lean/K2m5/Inst.lean` proves
`k2m5_of_valid11 (h : Valid11) : ∀ k : ℕ, 10 ≤ k → minSide (k ^ 2 - 5) = k`, with
`Valid11 := ∀ c θ, sq c θ 1 ⊆ box 11 → 1 ≤ box11Cover.measure (sq c θ 1)`.

- `box11Cover` is `fileCover` of `InstData.boxSegs`, `boxPolyVerts` and `boxPolyW`. My
  parser finds them equal, in file order, to the board’s 13,244 segment lines, polygon
  and weight. So `Valid11` is the closed-square validity of this board.
- `minSide` is not redefined in `lean/K2m5/`. It is Daniel’s
  `minSide n = sInf {s | Packs
  n s}` from `S32.lean`, byte-identical to the record’s copies.
- `minSide_eq` (`Fam10.lean` line 802) takes validity on the box `2R + 3 = 11`,
  `k ≥ 2R +
  2 = 10`, `A ≤ 10R` (`38 ≤ 40`) and the total below `n`, and returns `minSide n = k`
  through Daniel’s `not_packs_of_measure` and `packs_grid`.
- No file of `lean/K2m5/` contains `sorry`, `native_decide`, `implemented_by`, `extern`,
  `unsafe`, `axiom` or `admit`. The source’s `build.log` prints the axioms
  `[propext, Classical.choice, Quot.sound]`.

The build was not run here (§9, F6). The statement says what the issue says, and the
hypothesis is no stronger than what the four parts of Theorem 10 assert.

### 3.5 Theorem 10’s four parts

The D4 fold to centres in `[0, 5.5]²` and `θ ∈ [0, 45°]` is the standard one; `zmx2`
checks the board’s D4 invariance exactly before a `--d4` run, and its roots (1/10 cells
of `[0, 5.5]²` times four u-bins of width 1/8, `u ≤ 1/2`, θ to 53.13°) cover the fold.
The parts:

1. **θ = 0.** Settled here independently (§5.1).
2. **12,024 roots by `zmx2 --first-order`.** Every leaf certified or empty; the source’s
   logs keep only per-column summaries (F4).
3. **Root 9632.** `zmx2` leaves 6,850 boxes, all in the window W; `qx2_zm.py`, run on a
   cropped sub-measure (632 segments in `[3.5, 7.5]²` and the full Lebesgue square,
   which I checked is at most `μ₁₁` piece by piece), certifies its one root
   `[4.3, 4.4]² × [0, 1/16]` except 83 boxes, all at `x ≥ 4.339`, while the 6,850 lie at
   `x ≤ 4.3264`.
4. **The 75 tight-tile roots.** Each root was re-run with every uncertified box printed
   (the main sweep stops a root at 200, and `run_root` then dumps the stack as
   uncertified, so nothing is lost; `zmx2.rs` lines 2318–2346). Every printed box lies
   in the Tight-Tile Lemma’s domain or has `u = 0`.

Every pose of the fold is in one part, so the parts together give `Valid11`.

## 4. The Tight-Tile Lemma

This is the new part, and nothing in the record has checked a lemma of its kind, so I
read it twice: the mathematics in the report against my own derivation, then the code
against the mathematics.

### 4.1 Statement and use

For `d₀ ∈ {3/2, 5/2, 7/2}`, both tilt signs and `y ∈ I(d₀)`, every pose with centre
`(d₀ + δ, y)`, `tan(θ/2) = σu`, `0 < u ≤ 1/4000`, `|δ| ≤ 1/1000` has mass at least 1;
and likewise with `u ≤ 1/2000`, `|δ| ≤ 1/500` on five further ranges widened by 1/500. A
bottom-wall box becomes a left-wall pose under `(x, y) ↦ (y, x)`, which preserves `μ₁₁`
and turns `θ` into `−θ`: hence `σ = −1` there.
I checked the sign by the frame map.

### 4.2 The charts cover the domain

Near a base line `y_b ∈ (1/10)ℤ`, split by `|δ|` against `Ku` and `|t|` against `Ku`
(`K = 4`): `C_u` (both small, face `(δ/u, t/u)`), `W_t^±`, `W_d^±`, `W_td^{±±}` in two
triangles, each with `h = u` below its slab.
Between lines, `S_u` and `S_d^±`. Every pose of the domain is in exactly one case, with
face coordinates in the stated ranges.
I checked each line of `charts_line` and `charts_strip` (`ttbox.py` lines 412–446)
against the table: the centre polynomials, the face polygons and the `high` functions
agree. Strip ends are `y_b + Ku₀` and `y_b + 1/10 − Ku₀` (`run_tt.py` `send`), so lines
and strips tile each range with overlap.

### 4.3 The cell certificate

On a cell `Z` (a convex polygon in the face times an affine slab in `h`), every
constraint `τA ≤ B` of every segment is classified on the box `Bx(Z) = bbox × [0, max
high]`:

- *regular*: `A` keeps its sign, `A(·, 0)` a nonzero constant, `B(·, 0)` affine;
- *inactive*: `B ≥ max(0, A)`;
- *empty*: `B < min(0, A)`;
- otherwise by the exact wedge substitution `h = ηξ`, with bisection of the auxiliary
  ranges only.

Dividing out powers of `h`, or of a wedge variable, is division by a positive quantity
on the poses claimed.
For regular constraints the limit `b(0) = B(·,0)/A(0)` is affine, and the mean value
theorem on the vertical segment `{(p,q)} × [0, h] ⊂ Bx(Z)` gives `b⁺(h) ≥ b⁺(0) + hα`,
`b⁻(h) ≤ b⁻(0) + hβ`.

Then `f(h) ≥ f(0) + φ` with `φ` a sum of two minima of affine functions.
That inequality holds for any fixed choice of the reference bounds `r*`; the split that
makes `r*` the true minimiser only sharpens it.
The two-case bound on `ℓ(h) − ℓ(0)` and its convex combinations are correct and concave.

`T` is concave on the convex polytope `Z`, whose vertices lie among `(v, low(v))` and
`(v, high(v))`, so `T ≥ 0` there implies `T ≥ 0` on `Z`; the code also requires `G ≥ 0`
at the face vertices.

The Lebesgue term, only at `d₀ = 7/2`, has two parts:

- **Its limit value** is the product of two clamped affine overlaps, split at their
  kinks, bounded below by one McCormick plane, which is valid and affine.
- **Its `h`-derivative** is the transport integral `∫_{∂P ∩ U} v·n`, with
  `v·n = c'·n + θ' ε s`. I re-derived the sign `ε = k` for each of the four edges
  (`ttarea.py` lines 41–42) and `θ' = 2a/(1 + a²h²)`. An edge that may miss `U` widens
  its interval to contain 0.

The area is Lipschitz in `h`, so the derivative bound integrates.

### 4.4 Corner, wedge-corner and ray zones

Each construction covers the region it replaces by a trichotomy on `X` (and `Y`) against
`Mh`, with the slab either implied by the zone’s inequality or kept.

- `charts_corner3` covers `Ω × [0, u₀]`.
- `charts_wcorner` covers `Ω × {h ≤ q/K}`.
- `charts_rayzoom` covers the whole far-below zone: near (`|Δ| ≤ M'h`, where
  `q ≤ λX + M'h` and `Kh ≤ q` give `h ≤ λX/(K − M')`), above 1 and 2 split at
  `Δ_c = λ/3`, below 1 and 2 split at `E_c = λ/5`.

The substitutions `x_w = ζ x_o` are used only where `x_w ≤ ζ_max x_o` holds on the zone.

`run_tt.py` takes refused `C_u` cells to a box of dyadic radius `ρ` around a rational
point with denominator at most 1000 that contains every assigned cell’s vertices, and
refuses if `ρ > M h₀`. Refused wedge cells go to a box around `(p*, 0)`, and a refused
far-below zone is re-covered whole by the five ray zones, not only along the ray.
Anything else stays a failure, and a cell cap ends as a failure, never a silent drop.

### 4.5 The implementation

Read against the report’s six soundness rules (§7 of the report), all hold in the code:

- polynomials, limits, splits and vertex values are exact `Fraction`s;
- the binary64 intervals round to nearest and then widen one ulp outward at every
  operation (`ttpoly.py` lines 58–95), which is a valid enclosure under IEEE round to
  nearest;
- only positive quantities are divided out;
- dropping segments can only lower the bound;
- every cell ends certified, split or refused;
- checks raise exceptions.

Two details differ from the report’s wording without effect.
The segment filter compares a `Fraction` with a binary64 `ccx[0] − 0.75` (`ttbox.py`
line 191), not exactly, but its slack against `√2/2` is 0.043 (F7). And `run_tt.py`
passes `minarea` `2⁻⁶⁰` while `run` applies a fixed `2⁻³⁰` floor (`ttbox.py` line 391),
as the report says.

### 4.6 Coverage

My `k2m5_coverage.py`, written from the lemma’s statement and the chart table, places
every one of the 1,255,023 boxes:

| Domain | Boxes |
| --- | --- |
| d₀ = 3/2, σ = +1 | 473,914 |
| d₀ = 3/2, σ = −1 | 473,643 |
| d₀ = 5/2, σ = +1 | 153,999 |
| d₀ = 5/2, σ = −1 | 153,356 |
| d₀ = 7/2, σ = +1 | 33 |
| the five `u₀ = 1/2000` ranges | 78 |

It finds the 308 main and 15 further jobs the domain needs, each with every chart of the
table at zero refused cells and `h₀ = u₀`. The source’s `cov_check.py` agrees
(`COVERAGE-OK`).

Of the 326 job outputs, 325 do not record `K`; the published `run_tt.py` prints it, so
they come from an earlier revision of the driver, and `cov_check.py` defaults the field
to 4 (F3). The exact replays of §4.7 reproduce nine of them at `K = 4`.

### 4.7 What ran here

- **T-A.** 8 jobs drawn uniformly from the 174 the source records at 120 s or less.
  All 8 are equal to the source’s outputs in every chart’s `ok`, `cells`, `fails`,
  `worst` and tile string.
  The draw includes one line job (13 charts) and a `d₀ = 7/2` strip with the Lebesgue
  term.

- **T-B.** The rerun `d3.5_s-1_line_3.5` with `SKIP=C_u`: all 12 charts and all 41
  corner-zone lines are equal to `out_fix/`. That covers the two wedge corners
  `p* = −1/5` (`ρ = 2⁻²⁷`) and `p* = 0` (`ρ = 2⁻²⁶`), each with its ray `λ = 1/2` and
  277 zone cells. The last line reads `PARTIAL-ALL-OK (skipped C_u)` here and `ALL-OK`
  there, as the report explains: the published driver marks a run with `SKIP` as
  partial.

- **Vertex oracle.** On five regions, every certified cell’s vertex with `h > 0` was
  mapped to a pose by my own chart formulas and its exact mass computed.
  The regions are:
  - the `C_u` face `[3/4, 5/4]²` at `(3/2, 9/2, +1)`, your control’s region;
  - the M-3 region `[15/4, 4] × [−1/4, 1/4]` at `(5/2, 9/2, −1)`;
  - all 13 charts of `d2.5 σ=−1 line 1.6`;
  - all 3 charts of `d2.5 σ=−1 strip 3.9+ 4.0−`;
  - the 12 `W` charts of `d3.5 σ=+1 line 4.4`, where the Lebesgue term is live.

  Over 1,968 certified cells and 7,548 vertices, no vertex has `μ − 1 < T`; the least
  margin is `1.2·10⁻⁷`.

- **Exact samples.** 3,280 poses at every base line of the lemma’s ranges, both signs,
  at `h = 10⁻⁵` and `10⁻⁷` with `(p, q)` uniform in `[−4, 4]²`: none below 1, least
  `(μ − 1)/h` 0.141 and 0.203. 15,988 exact evaluations at the centres and `u > 0`
  corners of 2,000 random leftover boxes: none below 1, least `μ − 1 = 1.27·10⁻⁶`.

## 5. `zmx2` and `qx2_zm.py`

### 5.1 The θ = 0 face

`k2m5_axis.py` uses that, on an open 1/10 cell of centres, the set of lines a closed
axis-parallel square counts is fixed and the mass is bilinear; at a cell boundary the
mass is upper semicontinuous.
So the least one-sided corner limit over all 10,000 cells of `[1/2, 21/2]²` is the
infimum over the whole face.
It is exactly 1, at 3,000 of 40,000 corner limits; in the D4 region at 750 of 10,000,
the source’s count. No symmetry and no code of the source or Daniel is used.
`zmx2 cert0 --d4` (2,500 roots) and `cert0 --full` (10,000) both verify.

### 5.2 The build and the patch

`zmx2.rs` at the pin is `e2bb84e9…`; the patch replaces line 4248’s `.take(40)` by a
count that is unlimited when `ZMX2_PRINT_ALL` is set, one line becoming two, output
only. Built with rustc 1.97.0, the unpatched binary is `d68a2e35…`, the digest the
record’s s44 review built; the patched one is `32cf67df…`.

### 5.3 The first-order sweep, sampled

| Run | Result |
| --- | --- |
| Columns 29, 30, 48 (drawn from the 26 columns recorded at 1 to 300 CPU-s) | census equal to `col29.out`, `col30.out`, `col48.out` (3,142,510, 4,056,282 and 2,722,119 boxes; column 48’s 471 uncertified boxes are its tight-tile roots, and its 80 printed lines equal the source’s) |
| 40 roots drawn from the 12,024 certified | all certified: 368,236 boxes, 8 empty roots, 7 certified at depth 0, 25 subdivided |
| Root 9632, all boxes printed | 6,850 uncertified boxes, the same set as `verification/r9632/dump.out`, census and header equal |
| Roots 3436, 3472, 5668 (drawn from the 13 tight-tile roots whose dump records at most 120 CPU-s) | 15, 90 and 59 boxes, the same sets as `cov/r3436.out`, `r3472.out`, `r5668.out` |

The logs keep only per-column census lines and at most 40 boxes a root, so a sampled
root can be checked for certification here but not compared root by root (F4).

### 5.4 The certified bound against exact mass

First, plain exact samples with `k2m5_exact.py`, none below 1:

- 20,000 uniform admissible poses over the whole container and `θ ∈ [0, 90°)`, the least
  exactly 1, in the Lebesgue middle;
- 2,000 uniform poses in the root-9632 window, the least exactly 1, at a pose inside the
  Lebesgue square near its corner.

`zmx2`’s main property is that a leaf’s bound is at most the mass at every admissible
pose of the leaf. `--dump-tight` wrote the 149,381 certified leaves of these runs with
bound below 1.001. For 3,000 of them drawn uniformly and the 300 of least bound, I
evaluated exact mass at every admissible corner, at two random interior poses and, for
leaves whose `u` range starts at 0, at the centre corners with `u = u₁·2⁻²⁰` and
`u₁·2⁻⁴⁰`. That is 32,476 evaluations, none below the bound.
Where the bound exceeds 1 the least margin is `4.7·10⁻⁷`, at a wall tile, also at
`u ≈ 10⁻¹⁷`. In the 300 tightest leaves, bounds down to `1 + 1.8·10⁻⁸`, it is
`3.4·10⁻⁶`. Where the bound is exactly 1 the mass is 1 at the poses inside the Lebesgue
square. This is a probe of the bound’s validity where it is tightest, not a proof of it.

### 5.5 What `zmx2` trusts here

As the s44 review found, `zmx2` encloses geometry in outward-rounded binary64 and
compares masses as exact integers.
That review could rely on the lemmas the record had derived for `6b7f0f79` because its
cover had no polygon and its run no `--first-order`. Here both are on the path, header
`atoms=grid+fo … area=1`:

- **The area-density lemmas.** Lemma 1 (containment), Lemma 2 (cap), Lemma 3 (corners),
  Lemma K and K (d), all in `ZMX2_AREA.md` §§2–5 and 11.7. They certify every box that
  meets the Lebesgue square.
- **Lemma U per base cell, with Lemma V.** These are the only certificate for
  `0 < θ < 0.014°` at every zero-limit germ: the walls, the column germs and the double
  germs.

`ZMX2_AREA.md` §12 calls U and V “the least mature part” and §13 is a self-audit by the
agent that wrote them.
It found one proof gap and closed it, and lists four refinements (cone width, pair
activity, sweep candidates, the `u = 0` form constraint) whose correctness “rests on the
written proofs alone”.
The record has not reviewed these lemmas (F1).

### 5.6 `qx2_zm.py` on root 9632

Staged at its pinned digests and run single-process on `c9632.txt` over W:

- 2,357 boxes, maximum depth 18;
- leaves `LEB 10 CAP 192 EXACT 85 EXACT0 3 PIECE 806 UNCERT 83`, the source’s census;
- the 83 uncertified boxes equal `zm_unc.txt` exactly.

`qx2_zm.py` is the checker whose method the record reviewed for `T-064` and `T-081`. My
`closure_9632.py` then checks that the 6,850 `zmx2` boxes lie in the one `qx2` root,
that `qx2` ran that root to the end, and that no closed `qx2` leftover box meets a
`zmx2` one. All three hold.

## 6. Controls

| Control | Checker | Expected | Result |
| --- | --- | --- | --- |
| Source: every segment × 0.999, × 0.993, root (15, 36) bin 0, depth 24, cap 2·10⁶ | `zmx2` | refuse; real cover certified | real: certified (55,283 boxes); × 0.999: 209 uncertified; × 0.993: 217; census equal to the source’s three logs. The scaled covers rebuilt here equal the source’s files |
| Source: every segment of the 9632 window cover × 0.999 (`c9632_scale0999.txt`, checked here to be exactly that) | `qx2_zm.py`, then the closure check | not closed | census equal to the source’s (2,405 boxes, the same 87 uncertified boxes); 3 of them meet `zmx2` leftover boxes (3,486 pairs), so `closure_9632.py` refuses |
| Source: “same limit, smaller growth” (`ctl_rise.txt`) | Tight-Tile checker | refuse on `C_u` `[3/4, 5/4]²` at `(3/2, 9/2, +1)`; certify `μ₁₁` there | `μ₁₁`: certified, 155 cells, as reported. Mutant: refused; 3,819 cells refused at the `2⁻³⁰` floor, 6 of them containing `(1, 1)` as reported, but over 20,083 cells, to the cap, not the reported 6,079 and 1,190 (F8). Exact mass here: `1 − 1.3356·10⁻⁷` on the mutant, `1 + 1.2205·10⁻⁷` on `μ₁₁` at `(3/2 + h, 9/2 + h, u = h)`, `h = 10⁻⁶`, so the mutant is genuinely invalid |
| Source: one weight of `μ₁₂` | `locality_check.py` | refuse | 176 windows fail |
| M-1: the Lebesgue weight × (1 − 10⁻⁶) | `zmx2` first-order, root 12096 (centre cell `[5.4, 5.5]²`) | refuse; real certified | real: certified at depth 0 (Lemma 1); mutant: 235 uncertified. Exact mass at 50 poses there: 1 on `μ₁₁`, 0.999999 on the mutant |
| M-2: every segment weight − 1/(2·10¹²) | `zmx2 cert0 --d4`; `k2m5_axis.py` | refuse | `cert0`: 200 uncertified, worst bound 0.999999999941; clean-room: least corner limit `999999999913/10¹²` |
| M-3: a first-order-only mutant at `(5/2, 9/2, −1)`: the segment `x ∈ [2.5, 2.6]`, `y = 5.0` deleted, which changes no limit value at that face point | Tight-Tile checker, `C_u` `[15/4, 4] × [−1/4, 1/4]` | refuse; `μ₁₁` certified | `μ₁₁`: certified, 3,049 cells, none refused. Mutant: refused, 4,805 of 20,073 cells within the 20,000-cell cap, among them cells refused at the `2⁻³⁰` size floor (reason `bound`); all refused cells lie in `[3.75, 4] × [−0.2, 0.25]`. The driver kept the set of reasons, not a count per reason. Exact mass at face point `(4, 0)`, `h = 10⁻⁶`: `1 − 5.42·10⁻⁷` on the mutant, `1 + 1.27·10⁻⁶` on `μ₁₁` |
| M-4: one leftover box widened to `u₁ = 1/4000 + 2⁻⁴⁰` | `cov_check.py`; `k2m5_coverage.py` | refuse | both report it outside |
| M-5: one `qx2` leftover box moved onto a `zmx2` leftover box | `check_9632.py`; `closure_9632.py` | refuse | both refuse |

M-3 was found by the procedure stated in the plan.
The first two tiles tried had no such segment; the third did.

M-4’s first pre-stated box (the first box of the first dump) lies in the further range
`[4.4, 4.5]` at `d₀ = 5/2`, where `u ≤ 1/2000` is certified.
There the widened box is genuinely covered, and both checkers correctly accepted it.
The control was then run on the first box outside the five further ranges.

## 7. Re-implemented and Replayed

| Part | Re-implemented here (clean-room) | Replayed with the producer’s code |
| --- | --- | --- |
| Total, D, D4, family = board | `k2m5_cover.py` | `sanity_k2m5.py` (`SANITY-OK`) |
| Locality | premises and window identity, `k2m5_cover.py` | `locality_check.py` (`LOCALITY OK`) |
| θ = 0 face | `k2m5_axis.py`, complete | `zmx2 cert0 --d4`, `--full` |
| Tilted validity, general position | — (exact sampling and leaf probe only) | `zmx2`: 3 columns, 40 roots |
| Root 9632 | closure step, `closure_9632.py` | `zmx2` on the root; `qx2_zm.py` on its window |
| Tight-Tile Lemma | — (vertex oracle and exact sampling only) | 8 jobs and the wedge-corner rerun |
| Coverage | `k2m5_coverage.py`, complete | `cov_check.py`, `audit_zmx2.py`; 3 of 75 dumps |
| Lean | data link and token scan | not built |

The vertex oracle runs the source’s `ttbox.run` and checks its output with this review’s
own exact evaluator and chart formulas: it shares the cell decomposition with the
source, and nothing of the mass computation.

## 8. Findings

**F1. `zmx2`’s area and first-order lemmas have no review in this record (major, for the
record).** They decide most of `μ₁₁`’s pose space (§5.5), and Daniel’s own notes
(`search/ZMX2_AREA.md` §§12–13 at `659ee62`) ask for a second reader first.
The samples, the leaf probe and the controls here found nothing wrong, and a sample
decides nothing.
Until a review reads Lemmas 1–3, K, K (d), U per base cell and V against
`zmx2.rs`, or an independent decider replaces them, the 12,024 roots rest on the
source’s self-audit.

**F2. The Tight-Tile Lemma has one implementation and no full replay (major, for the
record).** The argument is sound (§4) and 9 of 326 job runs reproduce exactly.
The other 317 runs, about 115 to 150 CPU-hours here, are the source’s. The source’s
“independent review” of the lemma (`docs/CHECKING.md`, paper §8) is by an agent of the
source and is not in the release.

**F3. The Tight-Tile outputs carry no code digest, and 325 of 326 lack `K` (minor, in
the source).** The chart lines of `out/`, `out_u2000/` and `out_fix/` have no `K` field,
which the published `run_tt.py` prints (line 113), and no output records the digest of
`ttbox.py`, `ttpoly.py`, `ttarea.py` or `run_tt.py`. `cov_check.py` line 45 defaults `K`
to `'4'`. `K` is load-bearing: `δ_max = K u₀`. The exact replays at `K = 4` are the
evidence here that the outputs were made with it.

**F4. The sweep’s per-root records are not retained (minor, in the source).** The
release keeps the column `.out` files, which hold a census per column and at most 40
boxes per root, but not the `--log` files with `ROOT` lines.
A replay can match columns, not roots.

**F5. Lemma 7 uses elementary pieces without saying so (note, in the paper).**
`paper/k2m5.tex` lines 187–188 infer “no segment crosses `x = R`” from grid endpoints;
the inference needs every piece to have length 1/10, which holds (§3.2).

**F6. The Lean reduction was not built here (note, for the record).** The precedent
(`Sqpack.Bentz` in the 3 October evand packet) needed about 13 GB resident plus 9.6 GB
of swap; this host has 15 GB and no swap.
The source reports the instance modules at about 6 GB each.

**F7. Small inaccuracies in the documentation, without effect (note, in the source).**

- `run_cov.sh` line 6 puts `B=` and `NP=` inside the comment after `Z=`, so the script
  cannot run as published.
- The report’s “the comparison is exact” for the segment filter (report line 455) holds
  only up to a binary64 subtraction with 0.043 of slack.
- `ctl_rise.py`’s docstring gives the moved weight as 0.0284007811; it is 0.0142, the
  file’s integer over `2·10¹²`, as the paper says.
- `LICENSE` holds the MIT text only, while the README adds CC BY 4.0 for text and data.

**F8. The Tight-Tile control’s cell counts do not reproduce (note, in the source).** The
“same limit, smaller growth” control behaves as reported where it matters: `μ₁₁` is
certified on 155 cells, and the mutant is refused at the size floor in cells containing
`(1, 1)`. But the replay went on to the 20,000-cell cap, while the report has the run
end at 6,079 cells with 1,190 refused.
No log of that run is in the release, and the floating LP that proposes the weights `λ`
(`ttbox.py` lines 311–323) can steer a different cell path under another `scipy`; the
versions are not recorded.
Soundness is untouched, since `λ` is verified exactly; the outputs are not reproducible
to the cell without the versions.

## 9. Cost

**Spent here:** about 3.1 CPU-hours, at `nice -n 19`, on a 4-core host shared with
another lane’s runs, so the times include contention.
Of it:

- `zmx2` runs, 1,405 CPU-s;
- `qx2_zm.py`, 1,302 CPU-s on the window and 1,669 on its ×0.999 control;
- Tight-Tile replays, oracle regions and controls, 6,243 CPU-s, of which the two capped
  mutant runs took 4,670;
- the clean-room programs, the source’s fast checks and the two builds, about 500 CPU-s.

**A full replay on this host,** priced from the timings here:

| Part | Source’s record | Ratio here | Priced here |
| --- | --- | --- | --- |
| `zmx2` first-order sweep, 55 columns | 45,366 CPU-s | 1.13–1.20 (3 columns) | about 52,000–55,000 CPU-s, 15 CPU-h |
| 75 coverage dumps | 65,802 CPU-s (6 in parallel) | 0.75–0.79 (3 roots) | about 50,000 CPU-s, 14 CPU-h |
| Root 9632: `zmx2` and `qx2_zm.py` | 182 + 1,652 CPU-s | measured | 228 + 1,301 CPU-s |
| `cert0`, both ways | under 1 s | measured | under 1 s |
| 323 Tight-Tile jobs and 3 reruns | 1,007,447 s recorded (8 in parallel) | 0.41–0.53 (8 jobs) | about 115–150 CPU-h |
| Lean (Daniel’s closure and the K2m5 instance) | not recorded in CPU | — | about 1–2 CPU-h on a host with at least 24 GB of memory or swap and 10 GB of disk |
| **Total** |  |  | **about 145–180 CPU-hours** |

## 10. Frozen Digests

The freeze was written at 2026-11-14T04:41:26Z, before anything of §11 was read, and
committed as `2e04440f` on this lane’s branch.
[`receipts/freeze.sha256`](../../../packing/resources/web/khalili-gharabaghi-k2m5-973-review-2026-11-14/receipts/freeze.sha256)
(SHA-256 `34624a421901ca271edd59403b2c0b418cafb4a7e5683131acea86cdaf57355d`) holds the
verdicts of §2 and the digests of the packet’s 284 files and of this review’s draft.
The plan’s own digest is `c2844104…`, recorded at 02:17:26Z, before any sample ran.

| File | SHA-256 |
| --- | --- |
| `programs/k2m5_exact.py` | `6fa4dc3d6070713324b27f42f61e76e79d2809f1199ec0290a0b90068ef0ab48` |
| `programs/k2m5_cover.py` | `82012d288121b61ecbe046f4aded87dddb1a8fbf0130d030dd9533f76eb92f16` |
| `programs/k2m5_axis.py` | `ea4d0802141415ec0e041c926cea35766f70db48539b5b9186bb3c42de6e6a21` |
| `programs/k2m5_coverage.py` | `415fcded1ca2488758fdd1cfb9897d435f9f6c320c565da2197a89b41e732e99` |
| `programs/closure_9632.py` | `513f2850ebd5559e6569fbfb59ccdf9ed49e5702a952c920224aeb7485ba8a77` |
| `programs/tt_region.py` | `cd3085bbca7c2dc202ba611ad1413a460069581a226afdba57bc876ae62c9bc1` |
| `programs/zmx2_leaf_probe.py` | `5be1cbe4a4ef332a44baaf31eb5dc09ff02e9ae153e756292f61821405306190` |
| `programs/m3_search.py` | `9318c48f45d4b278de43f5e900782e5ef8260365a43b5b9334e24031ffa5ba8d` |
| `outputs/cover.json` | `607e8d9bf72a6c46ad3b8b677a6c2340026453674dbc1f4299cac8809b8e2036` |
| `outputs/axis_mu11.json` | `bd7f17d8bdf5e7ddae3d0399bbea5a09c8da70bfcada81ab53686db0723da35f` |
| `outputs/coverage.json` | `67d5d42675e01f02c9b84d891dbd38e7aaef921d3bfb20d6e4c72259e6df53f3` |
| `outputs/closure_9632.json` | `17b8c8bbc5b036c7770632875b790b3a2026db26f7efc11c2c226d827c0cba10` |
| `outputs/samples_eval.json` | `8859f65d0bc6f0a8fbd2656137cf55d178e8c56c7f17292bb9bcdd86dc230da8` |
| `outputs/leaf_probe.json` | `c76f7fd917190db893867a6ee475852210311f81f7a4775ade3bbe46a3d8c1bb` |
| `outputs/comparisons.jsonl` | `3233e08d11fd67eaa3b1e16c80b1d0e63b0aaee1f27ae62715e083d7dd76840c` |

Bulk files are not kept.
`outputs/bulk_not_kept.json` gives each one’s digest and the program that remakes it:
the drawn samples, the tight-leaf dumps and the mutant covers.
Each `zmx2` output keeps its census and the digest of its sorted box strings.

## 11. Relation to the Record

Read after the freeze: the register entries of `T-064`, `T-066`, `T-081`, `T-184`,
`T-191` and `T-252` in `results.yaml`, `n-095.md`, the frontier records of the nine
counts, and the 16 October review of Greff’s `s(76)` and `s(95)` covers.

Read before it, as the brief’s models or for the checkers’ history:

- the 3 October claim-chain review of `T-081`, which is about `k² − 4`;
- the 31 October review of the authors’ `s(44)` cover (`T-252`), for `zmx2`’s state at
  `e2bb84e9`;
- the 3 November review of Özden’s `s(94)`, for form;
- the `evidence.yaml` note and the 4 October evand packet’s README on `ZMX2_AREA.md`.

**The base cases stand at their entries.**

| k | n | Entry | Rung |
| --- | --- | --- | --- |
| 7 | 44 | `T-252`: the authors’ own mixed cover | V3/C3 |
| 8 | 59 | `T-066`: Hosono’s | V3/C3 |
| 9 | 76 | `T-184`: Greff’s | V3/C3 |

The source’s table says the same.

**k = 10.** `s(95) = 10` is already `T-191`, Greff’s cover, at V3/C3, as the paper says.
The family is a second route there, through `Valid11`.

**The counts the family newly decides.** At `n ≤ 324` they are `n = 116, 139, 164, 191,
220, 251, 284` and `319` (k = 11 to 18). Each is open in the record.
`n-116.md`, for one, holds the grid’s upper bound 11 against Hosono’s counting lower
bound `10.9113`. With `n = 95` already proved, eight counts are new, not nine.

**Second routes by monotonicity.** Since `s` is nondecreasing, `s(k² − 5) = k` gives
`s(k² − a) = k` for `a = 1` to 4. At `k = 10` to 18 that is a second route to `T-081`’s
instances `n = 96, 117, …, 320`, which stand at V0/C1 until `ValidTilt9`’s full replay,
and a further route to `T-064`’s (V3/C3). These routes are only as good as `Valid11`’s
own replay and review.

**Against `T-081`’s method.** The structure is Daniel’s, at a finer grid:

|  | `T-081` (`k² − 4`) | This family (`k² − 5`) |
| --- | --- | --- |
| Corner module and band depth | `R = 3` | `R = 4` |
| Grid pitch | 1/5 | 1/10 |
| Lebesgue square starts at | 14/5 | 19/5 |
| Board | box 9 | box 11 |
| D | about 1.074 | about 1.341 |

The Lean is `BentzFam.lean`’s reduction ported to the 1/10 grid.
The difference is in the finite statement’s checker.
`T-081`’s `ValidTilt9` is decided by the exact `qx2_zm.py`; the 3 October review
recorded that `zmx2` left 4,844 tiny-tilt boxes on box 9 and so was not a second route
there. Here `zmx2` with `--first-order` and area densities decides 12,024 roots, and the
Tight-Tile Lemma closes what it leaves at the tight tiles.
That is the new step, and its two new trust points are F1 and F2.

**Against the 16 October review.** That review ran `zmx2` on covers with no polygon and
no `--first-order`. It trusted Lemmas P, C, M, S, Z, W, H, T, E, DP and R, the ones the
record re-derived for `6b7f0f79`. So it does not reach the area and first-order lemmas
this claim uses, and F1 stands after reading it.

Its framing section says Greff’s covers carry nothing to another k “without a lemma for
the inserted band”. This source supplies such a lemma for its own family, as Lemma 7 and
in Lean, and it holds (§3.3).

The 16 October review’s practice of exact poses at every uncertified box and germ, and
of mutants each shown invalid at an exhibited pose, is the one followed here (S4, M-1,
M-3).

**Earlier reviews of this claim.** None was on `main` when this lane started, so there
is none to compare.

## 12. Questions for the Authors

1. Can you publish the `zmx2 --log` files of the main sweep (the `ROOT` lines), so a
   replay can be compared root by root (F4)?
2. Which revision of `run_tt.py` produced the outputs without `K`? Would you add `K` and
   the digests of the four checker files to each output (F3)?
3. Was `run_cov.sh` run as published, with `B` set in the environment (F7)?
4. Is the report of the separate agent’s review of the Tight-Tile Lemma available (F2)?
5. Do you know of any review of Daniel’s Lemmas U and V, or of a second decider for the
   tilted part of `Valid11` (F1)?
6. Could the paper say that every piece of the family is an elementary 1/10 piece, where
   Lemma 7 uses it (F5)?
7. Which Python, `numpy` and `scipy` versions ran the Tight-Tile jobs and the controls,
   and is the log of the “same limit, smaller growth” run available (F8)?

## 13. For the Records Lane

*Records lane L145, 14 November 2026, on mapping this review:* this section, as the
review lane committed it at `f58b34b7b`, repeated §11 word for word and ended in a stray
token, `S-LANE`; the repetition is removed here, and nothing else in the review is
changed. The records lane mapped the review from §§2, 8, 9, 11 and 12: it is recorded as
the `external_review` of `T-298`’s three report entries and in `T-298`’s `reviews`, its
clean-room programs as `V-khalili-973-review-check`, and what they decide in full as
`E-khalili-973-review-partial-checks`. Its price (§9) and F1 are in `think-0h7r`.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
