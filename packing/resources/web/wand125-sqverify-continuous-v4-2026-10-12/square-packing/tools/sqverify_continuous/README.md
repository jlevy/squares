# sqverify_continuous: rectangle-density certificates at every angle

`sqverify-fast --continuous` checks a rectangle-density certificate for `s(n)` over **every
orientation and every centre**, not over a net of directions.

- It is `sqverify_fast`, the clean-room interval verifier from
  [jlevy/squares](https://github.com/jlevy/squares), with one new mode.
- The new code is `sqverify_fast/src/slab.rs`.
- The proof obligations are lemmas C1 to C6 in
  [`sqverify_fast/CONTINUOUS.md`](sqverify_fast/CONTINUOUS.md).
- Version **v4**, `source_sha256` `619b3c00bd918b329b4141c24ee30b027af7f88b86bcf2886e3c18855a61c7f5` (v4 adds `--resume`; see `PROVENANCE.md`).

## What it proves

Inputs:

- a measure μ: the certificate's rectangles, each one's mass spread uniformly over its eight
  images under the symmetries of K = [0, L]², with total mass M;
- a core side B;
- a threshold τ.

The run proves:

> every closed square of side B lying in K, at any centre and any angle, has μ(P) ≥ τ.

The run also checks nτ > M exactly. Together these give **s(n) > L/B**. If n unit squares
fit in a square of side L/B, scaling by B gives n interior-disjoint squares of side B in K.
Their captures would sum to at least nτ > M, which is impossible. The endpoint L/B itself is
excluded by attainment.

The net verifier (`tools/fine_net_verifier/`) proves `s(n) ≥ L` from a net of directions and
pays for the gaps between net directions with the core B. This mode needs no net, so the
same kind of measure gives L/B.

## Method

Lemma C1 reduces the problem by symmetry:
- the angle to θ ∈ [0, π/4], with t = tan(θ/2);
- the centre to the north-east quadrant, x = L/2 + uE(t) and y = L/2 + vE(t), where
  E(t) = L/2 − (B/2)(cos θ + sin θ) and (u, v) ∈ [0, 1]².

**For t ∈ [ε, T]** (T² + 2T − 1 > 0, so T > tan(π/8)), the mode runs an interval branch and
bound over boxes in (u, v, t). For each box:

- **Angle enclosures** (C2): cos θ, sin θ and cos θ + sin θ are enclosed over the box's t
  range by monotonicity.
- **Classification** (C4): every rectangle is classified as inside every square of the box,
  outside every one, or neither. These are interval comparisons only; no floating-point
  screen decides anything.
- **Lower bound for every angle** (C3): the capture at the path centre
  (L/2 + u₀E(t), L/2 + v₀E(t)) is bounded below for every t of the box at once. Concave
  sections are integrated by trapezoids, and each section value is bounded over the whole
  (cos, sin) box.
- **Extension to the box** (C5): translation-derivative bounds extend that to every pose of
  the box.

A box closes when the downward-rounded bound reaches τ. Otherwise one of u, v or t is
halved. The choice of which to halve affects only the running time.

**For t ∈ [0, ε]** (C6): each such square of side B contains the concentric axis-aligned
square of side A, where A·W(ε) ≤ B is checked exactly. The upstream exact event sweep
(`src/axis.rs`) checks that square.

All arithmetic is outward-rounded binary64, using the upstream `src/interval.rs`.

## What it reuses, and from where

- **From jlevy/squares `packing/sqverify_fast`**, unchanged: the interval arithmetic
  (`interval.rs`), admission and D4 expansion (`certificate.rs`, `exact.rs`), the exact
  axis sweep (`axis.rs`) and the exact oracle (`oracle.rs`). The concave-section lower
  bound and the derivative enclosures in `slab.rs` follow the same lemmas (R2 to R5 of
  `SOUNDNESS.md`), extended from one direction to an interval of directions.
- **Guzhou0806/n40-square-packing** (MIT) proved the first all-angle n = 40 bound with its
  own kernel `verifier/continuous_pose.cpp`.
  - This mode shares no code with it. Its author read that kernel while reviewing it
    (jlevy/squares#485) before writing this mode, and the two have the same outline.
  - This mode differs in these details:
    - interval-only classification;
    - each section term bounded from the sign of its numerator;
    - knots taken from both end angles of a box;
    - 86 root ranges of t;
    - near-axis range ε = 10⁻⁷, checked by the exact rational event sweep;
    - a split rule that also weighs the derivative losses at the middle angle.

  It is independent code, not an independent method. See `PROVENANCE.md`.

## Input

A candidate in the upstream verifier's rectangle format: a JSON object with
- `n`
- `L`
- `B` (used only for the upstream admission checks; the core side of this mode is `--core`)
- `rectangles`: rows `[x1, y1, x2, y2]`
- `weights`: one per row

Numbers may be JSON decimals or strings `"p/q"`, and all are read as exact rationals. Each
row's weight is spread uniformly over the eight D4 images of its rectangle.
`examples/n40/prepare.py` shows the conversion from other layouts.

## Use

```sh
cd sqverify_fast && cargo build --release --locked && cd ..
sqverify_fast/target/release/sqverify-fast --candidate CAND.json --n N \
    --continuous --core P/Q --tau P/Q [--threads K] [--max-nodes N] \
    [--eps P/Q] [--last-t P/Q] [--axis-core P/Q] [--cuts t1,t2,...] [--roots a-b] \
    [--resume PREVIOUS.jsonl]
```

| option | meaning | default |
|---|---|---|
| `--core` | the side B of the squares that must capture τ | required |
| `--tau` | the threshold τ; nτ > M is checked exactly | required |
| `--eps` | upper end of the near-axis range [0, ε] | `1/10000000` |
| `--last-t` | T, the upper end of t | `83/200` |
| `--axis-core` | side A of the near-axis square | B/W(ε) rounded down to 10⁻⁹ |
| `--cuts` | interior ends of the root ranges of t | 10⁻⁵, 10⁻⁴, 10⁻³, then steps of 1/200 |
| `--max-nodes` | node budget per root range | 50,000,000 |
| `--roots a-b` | run only these root ranges (diagnostic; never `VERIFIED`) | all |
| `--resume` | take over the verified root ranges of an earlier run's output (below) | none |

The output is one JSON object per line:

- `premises`: the exact premises, including the counting margin nτ − M, X = L/B and the
  axis containment margin;
- `axis-patch`: the near-axis check;
- one `root` line per root range, written as soon as that range ends;
- `sqverify-fast-continuous-summary/v1`, the summary. Its `status` is `VERIFIED` only when
  every root range and the axis patch are verified. Its `build` field names the
  `source_sha256` of the build.

Every `premises`, `root` and summary line carries `run_key`. This is a SHA-256 over:
- the input's SHA-256, `n` and `L`;
- the build's `source_sha256`;
- `--core`, `--tau`, `--eps`, `--last-t`, the axis side A, the root cuts and `--max-nodes`.

The exit status is 0 for `VERIFIED`, 1 for `REFUSED` and 2 for an admission or premise
error.

A refused root reports the box where it stopped and the exact rational capture at a pose
in that box (`exact_capture`, `exact_below_threshold`, `exact_pose` = (x, y, t)). When
`exact_below_threshold` is `true`, check that the pose is legal (|x − L/2|, |y − L/2| ≤
L/2 − (B/2)W(t)); the claim is then refuted there. When it is `false`, the search ran out of budget
or resolution first, which is not a refutation.

## Resuming an interrupted run

`--resume PREVIOUS.jsonl` reads an earlier run's standard output (complete or cut off). It
takes over a `root` line only when all of these hold:
- the verdict is `verified`;
- its `run_key` equals this run's;
- its `index` and `t` range match a root range of this run.

Malformed lines (a line cut off by the interruption, for example) and every other line are
ignored. The axis patch is always recomputed (it takes about a second).

Every taken-over line is copied to the new output with `inherited_from` set to the SHA-256
of the file it came from. The new output is therefore a complete record on its own, and a
run can be resumed from it again.

The summary reports `inherited_roots`, `resumed_from` and `missing_roots`. Its status is
`VERIFIED` only when every root range, taken over or searched now, and the axis patch are
verified.

Trusting a taken-over line means trusting the earlier run's output. That earlier output is
the same receipt a complete run would have printed.

## Controls

A claim should be accepted only together with a control that is refused. Two kinds are used
in the examples:

- every weight multiplied by 985/1000 (total mass rescaled): the claim must be `REFUSED`, and
  the summary's refused roots should show `exact_below_threshold: true`;
- a slightly smaller `--core` (a larger X): it should be refused if the claimed B is near
  the edge.

## Examples: n = 40

`examples/n40/run.sh OUT_DIR [THREADS]` downloads the two densities (see `prepare.py` for the
commits and SHA-256 values), writes the candidates and controls, and runs five checks:

| check | candidate | B | τ | expected |
|---|---|---|---|---|
| `c6715` | rect_n40_L67 (480 orbits), via Guzhou0806/n40-square-packing `71c97d0` | 199529/200000 | 4999/5000 | `VERIFIED`: s(40) > 1340000/199529 = 6.71581… |
| `c6715_control` | same, every weight × 0.985 | 199529/200000 | 4999/5000 | `REFUSED` |
| `c6718` | Guzhou0806/n40-square-packing `6a65957e` (685 orbits) | 3350/3359 | 4999/5000 | `VERIFIED`: s(40) > 3359/500 = 6.718 |
| `c6718_control` | same, every weight × 0.985 | 3350/3359 | 4999/5000 | `REFUSED` |
| `c6718_B3348` | same density | 3348/3359 | 4999/5000 | `REFUSED` |

Measured on Ubuntu 24.04 (x86_64, 6 threads, v3):

| check | status | nodes | least certified bound | axis patch (min) | least exact capture at a refused pose | seconds |
|---|---|---|---|---|---|---|
| `c6715` | `VERIFIED` (86/86 roots) | 110,877,174 | 0.9998000000016 | verified (0.99988) | — | 1,167 |
| `c6715_control` | `REFUSED` (86/86 roots) | 7,714 | — | refused (0.98488) | 0.98711 | 1 |
| `c6718` | `VERIFIED` (86/86 roots) | 118,717,888 | 0.9998000000076 | verified (1.00150) | — | 1,355 |
| `c6718_control` | `REFUSED` (86/86 roots) | 5,979 | — | refused (0.98648) | 0.98648 | 1 |
| `c6718_B3348` | `REFUSED` (86/86 roots) | 12,364,148 | — | refused (0.98421) | 0.99856 | 97 |

The whole script took 44 minutes. Each root range is searched by one thread in a fixed order, so the node counts do not depend
on the thread count (the same counts were obtained with 2 threads on another machine).

The minimum certified bounds lie just above τ, because a box is accepted as soon as its bound
reaches τ. They do not measure how much slack the claim has.

## Tests

```sh
cd sqverify_fast
cargo fmt --check && cargo clippy --locked --all-targets && cargo test --locked --release
```

The continuous mode adds three property tests in `src/slab_tests.rs`. They compare against
the exact rational oracle at random boxes and poses:
- angle enclosures;
- inside and outside verdicts;
- the area bound;
- the derivative enclosure against exact difference quotients;
- the whole box bound;
- classification of small rectangles within 3% of a square's edge.

`CONTINUOUS.md` lists the deliberate mutations these tests catch.

## Limits

- Points and segments in a candidate are not counted in the capture. The bound stays valid,
  because the counting uses the full mass, but such a candidate loses that mass.
- The running time is set by how thin the slack is and by thin, heavy rectangles (large
  translation derivatives), more than by n or the number of rectangles. The n = 40 examples
  take 10 to 20 minutes on 6 threads.
- A certificate built for a net of directions need not hold at every angle with the same B.
  The net only guarantees capture at net directions. Choose B with some slack, and check it
  with the controls.
- The trust base is the stated lemmas, the Rust compiler and IEEE 754 binary64 hardware. The
  mode has not been formally verified.
