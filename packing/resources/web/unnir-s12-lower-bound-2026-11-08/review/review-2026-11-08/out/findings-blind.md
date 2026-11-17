# L58 Blind Findings: Issue #924, s(12) ≥ 9929/2500

Frozen before any comparison material was read.
Written 2026-11-08 by the L58 review lane: Claude (Anthropic), tier `tbd-strong-max`,
maximum reasoning.

**Disclosure.** The issue text, read as data, names T-095 and #363 as the prior n = 12
record and credits the framework to Burns and Massaccesi, Levy, Daniel and Ryu.
Beyond those names I had read nothing of T-095, its review, `packing/frontier/n-012.md`,
the squarepacker packets, or the L57 lane when this file was frozen.
To choose this folder’s path I listed directory names under `packing/resources/web/`
and the layout of two unrelated packets’ `review/` folders; I read no file in them.

## Source

- jlevy/squares issue #924, by unnir (Numaro).
  Packet https://github.com/unnir/s12-lower-bound-3.9716 at
  `064c2955670765321aaf1c0a2d5c778949daab6b`, cloned into scratch space.
- `certificate/s12_lower_3.9716.txt`: 103,946 bytes, SHA-256
  `833b76a179a420a40775cc76305ec9ffb7f6ea27472e587958c234c4c4712cbd`, which matches the
  issue. All 19 entries of the packet’s `SHA256SUMS` match.

## What I Read and What I Ran

Read as data: the issue; `README.md`; `verification/summary.json`, `logs/rust.log`,
`logs/cpp.log` and `controls/*`; and `verification/replay.py`.
After my own decider was written and its digest recorded (2026-11-08T15:08:21Z), I also
read `verifier/rust/src/main.rs` and `verifier/cpp/indep_scan.cpp`.
For the Rust I read the parser, the bin geometry, `main` and the plain-certificate path
of `min_cover_k`, and the clique, anchor and region branches only far enough to see
that they are inactive for a plain file. The C++ I read in full.

Ran: only programs I wrote, under CPython 3.14.7 with exact `int` and `Fraction`
arithmetic. numpy 2.3.3 `int64` arrays hold the weight counts and nothing else.
No producer code was built or run.

| Program | Role |
| --- | --- |
| `premises.py` | Parse; count; digest; positivity; containment; distinctness; D4 invariance of the weighted multiset; total and margin |
| `net_coverage.py` | Exact coverage of [0°, 45°] by the N = 96000 net |
| `decide_bins.py` | The bin decider (digest frozen at 15:08:21Z) |
| `run_bins.py` | Driver: bin lists, ranges, shards |
| `test_decider.py` | Differential test of the sweep against brute force |
| `mutation_check.py` | Shows the differential test has teeth |
| `controls.py` | Controls on the real certificate, and an emulation of the producer’s shrink (written after reading their sources; decides nothing) |
| `summarize.py` | Summarizes receipts |

SHA-256 of each program as run:

```text
bc3812179c7f13f4681769bf3f1f7df87d118adedfa5789b0f1a54ddb44d860c  premises.py
e39de359f2a9baa7edf2f794c5ac09370fbe462b86c06430db9be53efe9e0ab9  net_coverage.py
335101d848607c63cd4e12c7ec14305585b3cd1f4c88df8735b900b0b9b11540  decide_bins.py
a6aacfb29dea2c8e71232a7b4418d72504c963cfe9d8286871bd707637a73590  run_bins.py
9b150f97f1d4b53eb403dd1f2ef392fda9938177071549285ae0a1e8ee928404  test_decider.py
1300772c33086ec2d7014ca52a3abfb43fca8635493430e50432f896788824fe  mutation_check.py
9335d1b4a4ae114ac56bb53006cfc50d7851aa068aa09502c56565e493823655  controls.py
05c53df595809ead5e70ce34181477a44fe532c15b809ec334d54cb3dc65f687  summarize.py
```

## The Argument, Re-derived

Notation: s = 9929/2500; C = [0, s]²; W = 9985226; points p_i = (X_i, Y_i)/D with
weights w_i/W, where D = 4·10⁶. S(c, θ) is the closed unit square with centre c and
angle θ.

**R1. Reduction.** Assume three hypotheses:

- (H1) every w_i ≥ 0;
- (H2) Σ w_i < 12 W;
- (H3) every S(c, θ) ⊆ C contains points of total weight at least W.

Suppose 12 unit squares with pairwise disjoint interiors fit in a square of side t < s.
Scale the packing by s/t > 1 about the container’s centre. The 12 squares of side s/t
then have disjoint interiors inside C. The concentric closed unit squares lie in those
interiors, so they are pairwise disjoint closed sets in C. By (H3) each holds weight at
least W, so by disjointness and (H1) the total is at least 12 W. That contradicts (H2),
so s(12) ≥ s.

**R2. Strictness.** The packet claims only ≥. Each of the three deciders certifies (H3)
through a core K ⊆ S(c, θ), and K lies in the open square. For the producers this holds
for θ in the half-open bin [θ_k, θ_{k+1}); for mine it holds on the whole closed bin.
Now suppose a packing exists at side exactly s. Each square then holds a core of weight
at least W. For θ_i in (45°, 90°), reflect in the diagonal and use the D4 invariance of
the weights. The cores are pairwise disjoint, which gives the same contradiction.
s(12) is attained by compactness, so s(12) > s.
The packet does not make this argument, and it is not needed for the bound the packet
claims.

**R3. Angles.** A square’s orientation is defined mod 90°.
The diagonal reflection maps θ to 90° − θ and maps C onto itself, so with D4-invariant
weights the angles in [0°, 45°] suffice.
θ_k = 2 arctan(k/N) has cos θ_k = (N² − k²)/(N² + k²) and sin θ_k = 2kN/(N² + k²).
Also θ_k ≥ 45° exactly when (k + N)² ≥ 2N². For N = 96000 the first such k is 39765:
(39765 + N)² − 2N² = 135225 ≥ 0, while (39764 + N)² − 2N² = −136304 < 0.
So bins k = 0..39764 cover [0°, 45°], and the last bin ends 0.00051° past 45°.
θ_39764 + θ_39765 < 90°, so that overshoot reflects back into the same bin, and the
bin’s smallest half-extent is at θ_39764.

**R4. Shrink lemma.** For |φ| ≤ h ≤ π/4 and |q|_∞ ≤ a, |R(φ)q|_∞ ≤ (cos h + sin h)·a,
because cos φ + |sin φ| increases with |φ| on [0, π/4]. Hence the square of half-side
1/(2(cos h + sin h)) at a reference angle θ_r lies in S(c, θ) whenever |θ − θ_r| ≤ h.
It lies in the open square when the half-side is strictly smaller or |θ − θ_r| < h.

The producers take θ_r = θ_k and h = δ_k = θ_{k+1} − θ_k, so the core side is
σ_k = 1/(cos δ_k + sin δ_k), which is exactly rational.
The Rust rounds σ_k down to a multiple of 10⁻⁶ (`main.rs:1622`).
The C++ floors the half-side on a 10⁻¹⁵ grid and subtracts one unit
(`indep_scan.cpp:117`), and floors each position (`:130`).

Mine takes tan(θ_r/2) = (k + ½)/N and bounds h by
H = max over the two half-bins of 2Δt/(1 + t·t′), using arctan z ≤ z.
It then uses cos h + sin h ≤ B = 1 − H²/2 + H⁴/24 + H − H³/6 + H⁵/120, and the half-side
floor(QD/(2B))/(QD). At bin 39531 my shrink is 17.8 coordinate units per side; the
producers’ is about 35.6, plus up to 2 more in the Rust.

**R5. Centre domain.** S(c, θ) ⊆ C exactly when c ∈ [r(θ), s − r(θ)]², where
r(θ) = (cos θ + sin θ)/2 on [0°, 90°]. r is concave there, so over a bin the union of
the domains is [r_min, s − r_min]², with r_min the smaller of the two endpoint values.
All three deciders use this rule.
The Rust and the C++ round the domain outward (`main.rs:1626`, `indep_scan.cpp:123–124`).
The Rust also pads the V-projection in f64 by about 2 coordinate units (`main.rs:1049`).
Every rounding is in the sound direction.

**R6. Exact minimum.** For a fixed core angle, the captured weight is
Σ w_i·1[c ∈ B_i] over closed boxes B_i, so it is upper semicontinuous. Its minimum over
the compact convex domain therefore equals its minimum over the open cells of the box
arrangement that meet the domain’s interior. All three deciders compute this quantity:

- the Rust over closed cells with closed-window counts (`main.rs:1041–1042` and the
  cell loop), which gives the same quantity;
- the C++ over open elementary intervals, with the V-projection taken over the closed
  slab, a superset;
- mine over open cells meeting the open domain, with exact rational strip projections.

## Premises Recomputed (`premises.py`)

| Premise | Result |
| --- | --- |
| Layout | Header `15886400 4000000`, D = 4000000, W = 9985226, m = 4996, then 4996 lines `X Y w`. ASCII, LF line ends, no trailing data. A strict line parse and a whitespace-token parse agree. |
| Side | 15886400/4000000 = 9929/2500 exactly; s·D = 15886400 is an integer |
| Points | 4,996, all distinct; D4 orbits: 613 of size 8 and 23 of size 4, no centre point |
| Symmetry | The weighted multiset is invariant under all 8 maps of D4 about (s/2, s/2) |
| Containment | Every point strictly inside C; coordinates in [1343865, 14542535]/D |
| Weights | All positive; minimum 1, maximum 1381741, 364 distinct values; 1,976 points have weight 1 |
| Total | 119787760/9985226 = 11.996499628551222… |
| Margin below 12 | 34952/9985226 |

## Bin Decisions (`decide_bins.py` via `run_bins.py`)

**The sample.** 170 bins, chosen before any result was seen: 0, 1, 2; every 500th bin
from 500 to 39500; 39520–39545; 39760–39764; and 30 bins drawn with seed 924.
All 170 were decided at the first level, with no subdivision.
For each bin I also computed the true minimum, with no shrink, at three exact angles
(both endpoints and the reference angle): 510 exact angles, none below W, and 38
exactly W.
The run took 159.5 CPU-s.

**The tight band.** Bins 39532–39545 (θ from 44.7629° to 44.7772°) have core minimum
exactly W, and bins 39520–39531 have W + 1.
The true minimum is exactly W at 38 exact angles within bins 39533–39545.
Elsewhere the smallest margin in the sample is 10224/W (bin 8000), and most bins sit
near 14,860/W.
In the band the minimising centres are near (1.48682, 1.21931), together with their D4
images.

**Comparison with the producer’s logs.** Both producer checkers report minimum
9985226/9985226 at k = 39531. The Rust’s k is the smallest bin attaining the global
minimum (`main.rs:1667`), and the C++ adds the centre (1.486822, 1.219308).
I emulated the producer’s core in my own sweep: endpoint reference, σ_k rounded down to
10⁻⁶, and the domain from the rounded-down endpoint minimum, without the Rust’s V pad.
It gives W + 1 at every bin from 39518 to 39530 and exactly W at 39531 and 39532.
The minimising centre at 39531 is (1.4868216, 1.2193083).
That reproduces the logged value, the logged bin and the logged centre to six decimals,
with code that shares nothing with the producer’s.

**The full sweep.** A complete sweep over all 39,765 bins, with the same frozen decider
in two shards, started at about 15:12Z. Its result belongs to the review document, not
to this file.

**Controls of my own decider.**

- `test_decider.py`: in 2,000 random small instances, built on coarse grids to force
  ties, the sweep minimum equals a brute-force enumeration every time. The enumeration
  covers all open cells, uses a four-axis separating test against the domain and counts
  directly.
- `mutation_check.py`: moving the half-side or the domain by one scaled unit is caught
  in 7, 7, 4 and 2 of 600 instances.
- `controls.py`, on the real certificate:
  - (a) I removed the 8-point orbit of the heaviest point captured at the bin-39535
    minimum (weight 136132/W). The decider then refuses the bin, and the exact-angle
    mode returns a centre capturing 9607982 < W, confirmed by brute force.
  - (b) Enlarging the side by 1/D leaves the margins in the band unchanged: 1, 1, 0, 0
    and 0 at bins 39520, 39531, 39535, 39540 and 39545. The tight configuration is in
    the interior, not against a wall.

## Findings

**Blocking:** none. **Major:** none.

### Minor

- **B-m1. The C++ receipt does not evidence its own coverage.**
  `verifier/cpp/indep_scan.cpp:85–86` accept optional `kmax`/`kmin` arguments that
  restrict the loop at line 108. But line 103 prints “bins k = 0..N−1 covering [0,90]
  deg” unconditionally, and the verdict at line 209 does not check that the range swept
  was complete. A one-bin run of the original certificate would print that line and
  `VERIFIED`.
  `controls/double-denominator-cpp.log` shows the effect: it swept only bin 39531, yet
  prints the full-range line and “min captured weight over all bins”.
  So the 96,000-bin coverage claimed for `cpp.log` rests on the recorded invocation in
  the README and `replay.py`, not on the log.
  `kmax` is documented as being for D4-symmetric certificates, but the program never
  checks symmetry.
  This is not a defect of the bound; it limits what the receipt proves.
- **B-m2. The negative controls do not touch the geometry.** The double-W control
  (`verification/replay.py:60–95`) tests only that the minimum numerator is compared
  with W. Any checker that reports the right numerator passes it, whatever its shrink,
  domain or sweep. The truncation control tests only the parser.
  Neither would catch an unsound shrink, a centre domain that is too small, or an
  open/closed boundary error. Those are the failures that matter for a certificate with
  zero slack.
  Useful geometric controls: remove a point, or its orbit, captured at a minimising cell
  and require refusal (as in my control (a)); or move a critical weight-1 point by 1/D.

### Notes

- **B-n1. Zero slack.** The minimum is exactly 1 in three senses: under the producers’
  shrink (the logged value), under my sharper midpoint core (14 sampled bins), and as
  the true minimum at 38 exact angles in bins 39533–39545. That is valid for a claim of
  at least 1, and it has three consequences:
  - the bound depends on exact closed-boundary semantics throughout that band;
  - any replay whose core is smaller than Daniel’s endpoint core anywhere in bins
    39531–39545, or whose rounding is looser, will refuse the certificate there although
    the certificate is correct. This applies to approximate or interval replays,
    including a method-distinct parent-core replay;
  - no record should describe the result as having a margin.

  1,976 of the 4,996 points carry weight 1/W, 1976/W ≈ 2.0·10⁻⁴ in total. These
  weight-1 points are what bring the minimum to exactly W.
- **B-n2. The claim is ≥, and > also follows.** See R2. A record that states
  s(12) > 9929/2500 should cite the strict-core argument; the packet states and proves
  only the exclusion of sides below 9929/2500.
- **B-n3. The Rust log’s “bins=39766” and “k=0..39765”.** Confirmed from the source.
  `main.rs:1566` finds kk = 39765, and the loop sweeps kb = 0..kk−1 (partial flag at
  1574). The statistics line prints kk + 1 (1733–1734). The ten per-thread counts in
  `rust.log` sum to 39,765, so the issue’s explanation is correct.
- **B-n4. What the deciders share.** The two producer checkers share the theorem, the
  net, the endpoint shrink σ_k, the domain rule and the certificate. They are
  implementation-distinct, not method-distinct, as the packet says.
  Mine shares the theorem, the idea of a per-bin core and, deliberately, the producer’s
  bin boundaries. It differs in reference angle, shrink bound, domain rounding,
  arithmetic and data structures, and it was written before their sources were read.
- **B-n5. Not checked in this pass.** Whether the Rust source equals
  evand/square-packing@0e76d9fe `verify/src/main.rs`, and whether the C++ equals
  squarepacker/s12-lower-bound@7a96bec `tools/indep_scan.cpp` apart from the include
  lines. Building or running the producer’s code is L57’s lane.

## Blind Verdict

**Accept with findings.** The certificate’s premises hold exactly. The reduction, the
shrink lemma, the domain rule and the D4 reduction are sound as stated, and as
implemented on both producer checkers’ plain-certificate paths. Independent exact code
decides every sampled bin, and the sample contains no exact-angle counterexample.
No finding blocks registration. Confirmation of the complete cover property by my code
waits for the full sweep.

## Questions for the Author

1. Will you add a coverage check to `indep_scan` (B-m1) and a geometric negative control
   (B-m2)?
2. Was the exact tie at weight 1, reached through the 1,976 weight-1 points, a
   deliberate target of the construction?
3. Do you claim s(12) ≥ 9929/2500 or s(12) > 9929/2500? The packet states the former.
