# unnir’s Certificate for s(12) ≥ 9929/2500: Stage 4 Mathematical Review

This review was carried out on 2026-11-08 from the source packet
[unnir/s12-lower-bound-3.9716](https://github.com/unnir/s12-lower-bound-3.9716) pinned
at `064c2955670765321aaf1c0a2d5c778949daab6b`, cloned into scratch space, in a worktree
of this repository at `172d737be`. The reviewer is an AI agent: the separately prompted
mathematical review lane (L58) of stage 4 of the import of jlevy/squares#924. It shares
no context with the lane that replays the certificate (L57) and read none of that lane’s
files. The reviewer is Claude (Anthropic), at tier `tbd-strong-max` and maximum
reasoning.

The claim is jlevy/squares#924, opened on 2026-11-08 by unnir (Numaro):
$s(12) \ge 9929/2500 = 3.9716$, from `certificate/s12_lower_3.9716.txt`. If it holds, it
supersedes `T-095`, $s(12) \ge 7943/2000$, as the verified lower bound at n = 12, by
exactly $1/10000$. `T-095` stays true.
This review registers nothing and moves no bound.

**In one line:** No defect was found in the mathematics or the certificate.
Every premise was recomputed exactly and the argument re-derives.
This review’s own exact decider was written before either of the producer’s checkers was
read and shares no code with them.
It decided all 39,765 bins of the net: every closed unit square in $[0, 9929/2500]^2$,
at every angle, captures weight at least 1. The minimum is exactly 1, so the certificate
has no slack. Two minor findings concern what the packet’s receipts and controls show.
None blocks registration.

## Summary for the Author

- **The bound holds as far as an independent exact check can decide it.** Your premises
  hold exactly. The reduction, the shrink lemma, the centre box and the D4 fold
  re-derive. My decider shares no code with Daniel’s `verify` or Ryu’s `indep_scan`, and
  uses a different reference angle and a different shrink.
  It covers all 39,765 bins at N = 96000, with the minimum over every centre in each
  bin’s domain computed exactly.
- **Your minimum is exactly 1, and the tie is real, not an artefact of the shrink.** In
  the 24 bins 39532–39555 (about 44.763° to 44.787°), my sharper core captures exactly
  9985226/9985226. So does the true unit square, with no shrink at all, at the 38 exact
  angles I sampled there.
  Daniel’s core, as I emulate it without his padding, is at exactly 1 in bins
  39531–39556; your logs report the first of them.
  A claim of at least 1 is satisfied by a tie.
  But any replay with a smaller core or looser rounding than Daniel’s may refuse there
  without the certificate being wrong.
- **Two changes to the packet would make its evidence say what it means (F1, F2).**
  `indep_scan` prints “bins k = 0..95999” whatever range it actually swept, and
  `VERIFIED` whenever that range passes.
  And neither control touches the geometry: a checker with an unsound shrink or centre
  box would pass both.
- **The bound you claim is ≥, and the strict form also follows** (F5). You state only
  the exclusion of sides below 3.9716, which is right.
- **Three questions** are in §11.

## 1. What Was Reviewed

| Field | Value |
| --- | --- |
| Claim | $s(12) \ge 9929/2500 = 3.9716$, jlevy/squares#924 |
| Source | unnir/s12-lower-bound-3.9716 at `064c2955670765321aaf1c0a2d5c778949daab6b`; all 19 entries of its `SHA256SUMS` match |
| Certificate | `certificate/s12_lower_3.9716.txt`, 103,946 bytes, SHA-256 `833b76a1…2cbd` as the issue states |
| Header | `15886400 4000000 / 4000000 / 9985226 / 4996` |
| Total weight | $119787760/9985226 = 11.9964996…$, margin $34952/9985226$ below 12 |
| Reported least capture | $9985226/9985226$ at bin 39531, by both of the producer’s checkers |
| Producer’s checkers | Daniel’s `verify`, byte-identical to evand/square-packing@`0e76d9fe` `verify/` (`main.rs` `aca2fa6f…`); Ryu’s `indep_scan.cpp`, squarepacker/s12-lower-bound@`7a96bec` with the include line replaced (`74146d48…`) |
| Superseded if confirmed | `T-095`, $7943/2000$ |

**Read, in this order.**

1. Read as data: the issue; the packet’s `README.md`, `verification/summary.json`,
   `verification/logs/*`, `verification/controls/*` and `verification/replay.py`.
2. Then I wrote and tested my decider and recorded its digest (15:08:21Z).
3. Only after that did I read the producer’s checkers:
   - `verifier/rust/src/main.rs`: the parser, `bin_geometry`, `check_symmetry`, `main`
     and the plain-certificate path of `min_cover_k`, and the clique, anchor and region
     branches only far enough to see that a plain file never enters them;
   - `verifier/cpp/indep_scan.cpp`, line by line.

The blind findings were written and frozen at 15:20:50Z, before any comparison material
had been read. They are kept unchanged as
[`findings-blind.md`](../../../packing/resources/web/unnir-s12-lower-bound-3.9716-2026-11-08/review/review-2026-11-08/out/findings-blind.md),
SHA-256 `89e94ecae99d0048a77b538f95751115c74afcc5ca21367a0d3bbfe5011c6370`. Only then
did I read the comparison material:

- `T-095` in `packing/frontier/results.yaml`;
- its review,
  [review-2026-10-05-s12-v11-certificate.md](review-2026-10-05-s12-v11-certificate.md);
- `packing/frontier/n-012.md`, with what it says of #810;
- the squarepacker packets of 2 and 5 October under `packing/resources/web/`, including
  the retained `indep_check.cpp` and `indep_scan.cpp`;
- Daniel’s retained `verify` at `167d842c`;
- the upstream `verify/` at `0e76d9fe`, fetched as data to check provenance.

§7 is that comparison.
The complete sweep (§4) finished after the freeze, run by the decider whose digest was
recorded before it.

**Not read:** the L57 replay lane’s worktree, scratch files and pull requests.
**Not run:** any producer code.
This lane runs only code it writes.

## 2. The Argument, Re-Derived

Notation: $s = 9929/2500$, $C = [0, s]^2$, $W = 9985226$. The points are
$p_i = (X_i, Y_i)/D$ with weights $w_i/W$, where $D = 4 \cdot 10^6$, and $S(c, \theta)$
is the closed unit square with centre $c$ at angle $\theta$.

**The counting reduction.** Assume three things:

- every $w_i \ge 0$;
- $\sum w_i < 12W$;
- every $S(c, \theta) \subseteq C$ holds points of weight at least $W$.

Suppose twelve unit squares with disjoint interiors fit in a square of side $t < s$.
Dilate that square onto $C$ by $s/t > 1$. The concentric closed unit squares of the
images lie in their open interiors, so they are pairwise disjoint closed sets in $C$.
Each holds at least $W$, so together they hold at least $12W > \sum w_i$, which is a
contradiction. Hence $s(12) \ge s$. The hypotheses do not need the points to be inside
$C$. Weights must be nonnegative, because a negative weight placed where no square sees
it would lower the total for free.

**Strictness.** The packet claims only $\ge$, which is what the bare reduction gives.
Each decider, however, certifies the third hypothesis through a core
$K \subseteq S(c, \theta)$ that lies in the open square:

- for the producer’s checkers, whenever $\theta$ is in the half-open bin
  $[\theta_k, \theta_{k+1})$;
- for mine, on the whole closed bin.

So suppose a packing existed at side exactly $s$. Each of its squares would contain such
a core. For angles in $(45°, 90°)$, take the diagonal image of the square and use the D4
invariance of the weights.
Each core lies in the interior of its square, and the interiors are disjoint, so the
cores are pairwise disjoint and the same contradiction follows.
A packing in a smaller square is also one in $C$, so no side up to $s$ admits a packing.
$s(12)$ is attained by compactness, so $s(12) > s$ (F5).

**The fold.** $S(c, \theta + 90°) = S(c, \theta)$. The diagonal reflection maps $C$ to
itself and $S(c, \theta)$ to $S(\rho c, 90° - \theta)$, so with $\rho$-invariant weights
the angles in $[0°, 45°]$ suffice.

**The net.** $\theta_k = 2\arctan(k/N)$ has rational cosine $(N^2 - k^2)/(N^2 + k^2)$
and rational sine $2kN/(N^2 + k^2)$. Also $\theta_k \ge 45°$ exactly when
$(k + N)^2 \ge 2N^2$.

At $N = 96000$ that first holds at $k = 39765$: $(39765 + N)^2 - 2N^2 = 135225 \ge 0$,
while $(39764 + N)^2 - 2N^2 = -136304$. So bins 0 to 39764 cover $[0°, 45°]$, and the
last ends $0.00051°$ past it.
Since $\theta_{39764} + \theta_{39765} < 90°$, the overshoot reflects into the same bin.

**The shrink lemma.** Take $|\varphi| \le h \le \pi/4$ and $|q|_\infty \le a$. Then
$|R(\varphi) q|_\infty \le (\cos h + \sin h)\, a$, because $\cos\varphi + |\sin\varphi|$
increases with $|\varphi|$ on $[0, \pi/4]$. So a square of half-side at most
$1/(2(\cos h + \sin h))$ at angle $\theta_r$ lies in $S(c, \theta)$ whenever
$|\theta - \theta_r| \le h$. It lies in the open square when the inequality is strict.

The producer’s checkers take $\theta_r = \theta_k$, $h = \delta_k$, and
$\sigma_k = 1/(\cos\delta_k + \sin\delta_k)$, which is exactly rational:

- Daniel’s rounds it down to $10^{-6}$ (`main.rs:1622`);
- Ryu’s floors the half-side on a $10^{-15}$ grid, takes one more unit off, and floors
  every position (`indep_scan.cpp:117, 130`).

Mine takes $\tan(\theta_r/2) = (k + \tfrac12)/N$. It bounds $h$ by
$H = \max 2\Delta t/(1 + t t')$ over the two half-bins, using $\arctan z \le z$. It then
uses $\cos h + \sin h \le B = 1 - H^2/2 + H^4/24 + H - H^3/6 + H^5/120$, with half-side
$\lfloor QD/(2B)\rfloor/(QD)$. At bin 39531 its shrink is 17.8 coordinate units a side.
The producer’s is about 35.6, plus up to 2 more in the Rust.

**The centre box.** For $\theta \in [0°, 90°]$, $S(c, \theta) \subseteq C$ exactly when
$c \in [r, s - r]^2$, with $r(\theta) = (\cos\theta + \sin\theta)/2$, which is concave
there. Over a bin, then, the box is set by the smaller endpoint value of $r$. All three
deciders use this. Daniel’s and Ryu’s round it outward, and Daniel’s also widens each
strip’s V-range in `f64` by about 2 coordinate units (`main.rs:1049`).

**The cell-minimum lemma.** For a fixed core angle, the capture is
$\sum w_i\,1[c \in B_i]$ over closed boxes, which is upper semicontinuous.
Its minimum over the compact convex box is therefore its minimum over the open cells of
the arrangement that meet the box’s interior.
Daniel’s sweep counts closed windows on closed cells, which is the same number; Ryu’s
queries open elementary intervals against the closed slab’s V-projection, a superset;
mine queries open cells against the open domain’s exact projection.

**What a pass of `decide_bins.py` proves.** It proves that every closed unit square at
an angle in the bin, with its centre where the square fits in $C$, contains points of
weight at least $W$. It also proves that the core doing so lies in the open square.
Together with the premises and the fold, a pass over bins 0 to 39764 is the whole of the
third hypothesis.

## 3. The Certificate, Checked

`premises.py` recomputed every premise in exact integers, apart from any code of the
producer’s:

| Premise | Result |
| --- | --- |
| Layout | ASCII, LF line ends; the header lines above, then 4,996 lines `X Y w` and nothing after them. A strict line parse and a whitespace-token parse agree |
| Side | $15886400/4000000 = 9929/2500$ exactly; $sD = 15886400$, an integer |
| Points | 4,996, all distinct, strictly inside $C$, coordinates in $[1343865, 14542535]/D$ |
| Symmetry | The weighted multiset is invariant under all eight maps of D4; 613 orbits of 8, 23 of 4, no centre point |
| Weights | All positive: least 1, greatest 1381741, 364 values. 1,976 points carry weight $1/W$ |
| Total | $119787760/9985226$, which is $34952/9985226$ below 12 |

## 4. The Bins, Decided

**The tests of the decider.** Two tests check the sweep itself:

- `test_decider.py` compared the sweep with a brute-force enumeration of every open cell
  on 2,000 random small instances, on coarse grids that force ties.
  The enumeration uses a four-axis separating test against the domain and counts
  directly. There were no mismatches.
- `mutation_check.py` moved the half-side or the domain by one scaled unit; the test
  catches each mutant (7, 7, 4 and 2 of 600 instances).

**The sample.** 170 bins were fixed before any result was seen:

- bins 0, 1 and 2;
- every 500th bin;
- bins 39520 to 39545 and 39760 to 39764;
- 30 bins drawn with seed 924.

All were decided without subdivision.
For each, I also computed the true minimum at both endpoints and the reference angle,
with no shrink: 510 exact angles, none below $W$ and 38 at exactly $W$. That took 159.5
CPU-s.

**The complete sweep.** `decide_bins.py` decided all 39,765 bins, 0 to 39764, in two
shards, every bin at the first level with no subdivision.
It took 9,494 CPU-s (2.64 CPU-hours) on two cores at `nice -n 19`. The least core
minimum is exactly $W$, at the 24 bins 39532 to 39555. Another 55 bins are at $W + 1$:
39511 to 39531, 39556 to 39570, and 39629 to 39647. Every other bin is at least $2702/W$
above $W$. The per-bin table and its summary are retained (§12).

**The tight band.** All 79 bins within $1/W$ of the bound lie between 44.74° and 44.88°.
For bins 39511 to 39570 the minimising centres are near $(1.4868, 1.2193)$, and for
39629 to 39647 near $(1.2171, 1.4865)$, together with their D4 images.
Everywhere else the slack is at least $2702/W \approx 2.7 \cdot 10^{-4}$, and most bins
sit near $14{,}860/W$.

**The producer’s logs, reproduced.** Daniel’s `verify` reports the global minimum
$9985226/9985226$ at $k = 39531$, the smallest bin attaining it (`main.rs:1667`).
`indep_scan` reports the same value at bin 39531, near $(1.486822, 1.219308)$.

`controls.py` computes Daniel’s core with my sweep: endpoint reference, $\sigma_k$ and
the centre box rounded down to $10^{-6}$, without his `f64` padding.
It gives $W + 1$ at bins 39516 to 39530 and exactly $W$ at the 26 bins 39531 to 39556,
then $W + 1$ again from 39557 to 39572 (`emulate_band.py`). At bin 39531 the minimising
centre is $(1.4868216, 1.2193083)$. So the logged value, bin and centre are reproduced,
to six decimals, by code that shares nothing with the producer’s.

**Controls on the certificate.** Two controls checked the decider against the real
certificate:

- Removing the 8-point orbit of the heaviest point captured at bin 39535’s minimum
  (weight $136132/W$) makes the decider refuse that bin.
  The exact-angle mode then returns a centre capturing $9607982 < W$, confirmed by brute
  force.
- Enlarging the side by $1/D$ leaves the band’s margins unchanged: 1, 1, 0, 0 and 0 at
  bins 39520, 39531, 39535, 39540 and 39545. The tie sits in the interior, away from the
  walls.

## 5. The Checkers’ Trust Boundaries

| Checker | What it decides | What it trusts |
| --- | --- | --- |
| Daniel’s `verify` (`0e76d9fe`, `main.rs` `aca2fa6f`) | The file’s premises. Then bins 0 to 39764 through the fold, by an exact arrangement sweep in `i128`, with $\sigma_k$ and $\omega$ rounded down to $10^{-6}$ | The four lemmas; an overflow-checked build; `f64` padding of the V-range that only widens it |
| Ryu’s `indep_scan.cpp` (`74146d48`) | Run without range arguments, all 96,000 bins on $[0°, 90°]$ with no fold, $\sigma_k$ exact, a $10^{-15}$ grid with conservative rounding, and a segment tree | The same lemmas; the invocation, since range arguments restrict it silently (F1); the compiler |
| This review’s `decide_bins.py` (`335101d8`) | Each bin given: a core at the mid-tangent angle with a Taylor-bounded rational shrink, the exact centre box, and the exact minimum over open cells. Premises separately, by `premises.py` | The lemmas as re-derived in its docstring; CPython’s integers and `Fraction`; numpy’s `int64` add and minimum on counts below $1.2 \cdot 10^8$ |

**What the deciders share.**

- *Daniel and Ryu* share the framework: the net, the endpoint $\sigma_k$, the box rule
  and the cell-minimum lemma.
  They share no code.
- *Mine and either of theirs* share the theorem, the idea of a per-bin core, and, on
  purpose, the bins. Mine differs in reference angle, shrink bound, box arithmetic,
  number type and data structure, and shares no code.
- *All three* rest on the certificate bytes, the counting reduction with closed squares,
  and the 39,765 bins of $N = 96000$.

**How the weights were found is not stated.** The packet makes no claim about its
method, and its minimum is exactly $W$ under exactly Daniel’s core.
That is the trace of a linear program whose rows are that checker’s cells.
`T-095`’s rows were Daniel’s `TIGHT_DUMP` cells, and its search stopped when
`indep_scan` was silent (F3). This review’s decider did not exist when the certificate
was made, and its cores differ from Daniel’s. An error specific to the producer’s
checkers would not carry over to it.

## 6. Findings

**None is blocking, and none is major.** F1 and F2 are minor, for the author and the
replay lane. The rest are notes.
The blind-pass identifiers are kept in brackets.

### F1 — Minor: the C++ receipt does not show its own coverage [B-m1]

`verifier/cpp/indep_scan.cpp:85–86` read optional `kmax` and `kmin` arguments that
restrict the loop at line 108. Line 103 prints “bins k = 0..N−1 covering [0,90] deg”
unconditionally, and the verdict at line 209 does not check that the range was complete.
Read from the source, though not run here: a one-bin run of this certificate would print
that line and `VERIFIED`. `verification/controls/double-denominator-cpp.log` shows the
effect: it swept only bin 39531 and still prints the full-range line and “min captured
weight over all bins”.

So the 96,000-bin coverage of `verification/logs/cpp.log` rests on the invocation
recorded in the README and `replay.py`, not on the log.
`kmax` is documented for D4-symmetric certificates, but the program never checks
symmetry.

The precedent sharpens the point (§7). `indep_scan.cpp` is `indep_check.cpp` with these
range arguments added, and it was the stopping rule of `T-095`’s search.
This repository’s replay of `T-095` ran `indep_check.cpp`.

**Ask:** print the range swept, and refuse `VERIFIED` unless it is the whole net (or
check D4 when `kmax` stops at 45°). Alternatively, ship `indep_check.cpp`. For the
replay lane: name which file ran, and with which arguments.

### F2 — Minor: the negative controls do not touch the geometry [B-m2]

The double-W control (`verification/replay.py:60–95`) tests only that the minimum’s
numerator is compared with $W$. Any checker that reports the right numerator passes it,
whatever its shrink, centre box or sweep.
The truncation control tests the parser.

Neither would catch the failures that matter for a certificate with no slack: an unsound
shrink, a box that is too small, or an open/closed confusion at cell boundaries.
`T-095`’s controls were geometric and local: its heaviest orbit lowered at the
minimising square, and the same integers over a smaller $D$, which enlarges the
container.

**Ask:** add a control that removes, or lowers, a point captured at a minimising cell,
which must be refused, as `controls.py` (a) does here.
Add one that changes the container or the grid.

### F3 — Note, for the records lane: treat the producer’s two runs as producer evidence

The weights’ search is undisclosed, and the exact tie under Daniel’s core suggests it
was fitted to that checker’s cells.
`T-095`’s review (its F3) found the same for that search.
The two producer checkers should therefore be cited as the producer’s evidence.

Confirmation comes from deciders untouched by the search:

- this review’s complete sweep, an independent implementation that ran here;
- whatever the replay lane runs that the search could not have consulted, the native
  parent-core route among them.

For `T-095`, Daniel’s full sweep counted as a confirmation, because the search had never
used it as its stopping rule.
Here the packet does not say which checker stopped the search.
Until it does, a replay of either producer checker reproduces the producer’s evidence
with the producer’s code.
That is worth having for the build and the input digest, as `T-095`’s F2 asked, but it
should not be the method the confirmation rests on.

### F4 — Note: zero slack [B-n1]

The minimum is exactly 1 in three senses:

- under the producer’s core, which is the logged value;
- under this review’s sharper core, at the 24 bins 39532–39555 of the complete sweep;
- as the true minimum with no shrink at 38 exact angles in bins 39533–39545.

A tie satisfies a claim of at least 1. But the bound then depends on exact
closed-boundary semantics throughout the band, and no record should describe it as
having a margin. 1,976 points carry weight $1/W$, $1976/W \approx 2.0 \cdot 10^{-4}$ in
all. They are what brings the minimum to $W$ exactly.

For a replay with a core smaller than Daniel’s or looser rounding, a refusal in the band
is not a counterexample.
The native parent-core route certified `T-095` with its least row bound exactly at the
threshold (row 21524), so a tie does not in itself defeat it.
It does, however, meet this certificate’s tie head on, since it uses Daniel’s $\sigma_k$
by design (`T-095`’s F9).

### F5 — Note: the claim is $\ge$, and $>$ also follows [B-n2]

§2 gives the argument: the cores of all three deciders lie in the open unit square.
The packet states only the exclusion of sides below 9929/2500, and `T-095`’s review says
the bare reduction gives $\ge$ and not $>$. Both are right.
The strict form needs the strict-core property, which is how this record has stated it
before, through the native route, for `T-078` and `T-095`. If the record states
$s(12) > 9929/2500$, it should cite that property: this review’s sweep has it on every
closed bin, and the native route has it row by row.

### F6 — Note: the Rust log’s “bins=39766” and “k=0..39765” [B-n3]

`main.rs:1566` sets `kk = 39765`; the loop sweeps 0 to `kk − 1` (the partial flag is at
1574); the statistics line prints `kk + 1` (1733–1734). The ten per-thread counts in
`rust.log` sum to 39,765. The issue’s explanation is right, and `T-095`’s review reads
the `angles:` line the same way.

### F7 — Note: provenance of the two checkers [B-n5, resolved after the freeze]

**Rust.** `verifier/rust/src/main.rs`, `Cargo.toml` and `Cargo.lock` are byte-identical
to upstream evand/square-packing@`0e76d9fe` `verify/`, fetched here as data.
`main.rs` differs from the copy this repository replayed for `T-095` (`226ef3f1`) in two
places only:

- a doc comment, “interior” changed to “CLOSED”;
- the exit statuses 0, 1 and 4.

The checking logic `T-095`’s review read line by line is unchanged, and its remark that
`verify` exits 0 on `NOT VERIFIED` no longer holds.

**C++.** `verifier/cpp/indep_scan.cpp` equals the retained squarepacker v1.1
`tools/indep_scan.cpp` (`35465554…`) except for the include lines, as the packet says.

### F8 — Note: the logs bind no binary

As in `T-095` (its F2), the logs are plain output.
`summary.json` lists binary and source digests, but those are the producer’s statements.
The replay lane’s receipts should bind the binary, the build flags and the input digest.

### F9 — Note: the point set extends Daniel’s

`lineage.py` compares the point set with `T-095`’s, whose points are Daniel’s, already
dilated once. Every one of those 1,736 points has a point of this certificate within one
coordinate unit of its image under the further dilation $39716/39715$. The other 3,260
points are new. The kept points carry 59.1 % of the total weight, and Daniel’s row at
$x = (141/560)s$ is still there: 112 points at $x = 3999969/D$.

So the certificate is Daniel’s points, dilated as `T-095` did and once more, plus new
points, with new weights.
The issue’s credit, which builds on Levy, Daniel and Ryu, matches the file.
The new points are what `T-095`’s source said a higher bound would need.

## 7. Reconciliation With the Precedent

What the reading of `T-095`, its review, `n-012.md` and the squarepacker packets
changed:

- **Confirmed: the framework and Daniel’s checker.** The precedent re-derives the same
  four lemmas, and reads the same `verify` logic line by line.
  `T-095`’s review computed nothing (its F1), and this review supplies the computation
  it lacked: exact premises, and a decision of every bin by independent code.
- **Sharpened: F1.** I had not known in the blind pass that `indep_scan` is the
  range-restricted copy of `indep_check` that served as `T-095`’s stopping rule, nor
  that the record’s replay of `T-095` ran `indep_check`.
- **Sharpened: F2.** `T-095`’s controls were one local control (its heaviest orbit
  lowered at the minimising square) and one geometric (a regrid that enlarges the
  container). `T-078`’s included a further scaling of the container.
  This packet’s are neither: one lowers every weight at once, and the other is a parser
  test.
- **New: F3.** The precedent’s fitting finding applies here with more force, because the
  tie is exact.
- **Tempered: F4.** The blind pass expected interval replays to struggle with the tie.
  The native route has certified a row at the threshold before (`T-095`, row 21524), so
  a refusal is possible but not to be expected.
- **Reconciled: F5.** `T-095`’s review says the bare reduction gives $\ge$. Its register
  entry and `n-012.md` attribute the strict form to the native route’s strict
  containment, which is the argument of §2. There is no conflict.
- **Context: #810.** `n-012.md` records Jatloe’s Lean proof that $s(12) = 4$, as `T-245`
  and tracked in #810, as reported and not verified.
  The reported lower bound is 4. This result moves only the verified lower bound, from
  `T-095`’s 7943/2000, and the issue itself says it uses nothing of `T-245`.
- **Context: why a new point set was needed.** `T-095`’s source reports that its linear
  program over Daniel’s 1,736 points reaches 12.0758 at $s = 3.9716$ on $N = 96000$. Its
  review puts the geometric limit of those points at $560/141 = 3.97163$. The new bound
  is $11/352500 \approx 3.1 \cdot 10^{-5}$ below that limit, on 4,996 points (F9).

## 8. Significance

No draft score was in front of this lane.
I suggest **S3**.

The register’s own line at n = 12 scores a rescaling S2 (`T-078`) and new weights S3
(`T-079`, `T-095`). This result has new points and new weights, and it raises the
verified lower bound of a central open case.
Against that, the step is $1/10000$: the smallest of the new-weights steps at n = 12,
and about a thirteenth of `T-095`’s 0.0013. The packet claims no new technique, and the
method is capped below 3.99.

The rationale should say all of that.
It should also say that the bound lies within $3.1 \cdot 10^{-5}$ of $560/141$, the
limit `T-095`’s review identified for Daniel’s points, and that a reported proof of
$s(12) = 4$ (`T-245`) stands unverified.
S2 would need step size to outweigh the new points and weights.
Its nearest precedent, `T-093` at n = 17, added no orbit, weight or method, which is not
the case here. S4 is out: there is no new technique.

## 9. Verdict

**Accept with findings.** The argument from `s12_lower_3.9716.txt` to
$s(12) \ge 9929/2500$ re-derives, and so does the strict form through the cores.
The premises hold exactly.
Both producer checkers’ plain-certificate paths are sound as read.

Independent exact code decided the cover property over the whole net, and controls show
that it refuses a damaged certificate.
The producer’s logged minimum, bin and centre are reproduced.
No finding blocks registration.
F1 and F2 go to the author.
F3 and F8 are for the records and replay lanes.
F4 to F7 and F9 are notes.

**Re-derived here**, by argument or by this lane’s own code:

- the counting reduction, and the strict form through the cores;
- the D4 fold, and the exact D4 invariance of the weighted multiset;
- the net’s exact coverage of $[0°, 45°]$, and the last bin’s overshoot;
- the shrink lemma: the producer’s endpoint $\sigma_k$, and this review’s mid-tangent
  core with its rational bound;
- the centre box, and the cell-minimum lemma;
- every premise of the file;
- the coverage of all 39,765 bins;
- the true minimum, with no shrink, at 510 exact angles;
- the producer’s logged minimum, bin and centre, by emulating Daniel’s core;
- the provenance of both checkers against their upstreams.

## 10. For the Records Lane

These are drafts. The coordinator owns the identifiers and the packet path.

```yaml
reviews:
  - path: docs/project/reviews/review-2026-11-08-s12-unnir-3.9716.md
    kind: adversarial
    reviewer: AI agent, the separately prompted stage-4 review lane (L58) for #924, sharing no context with the registering and replay lanes, blind to the replay; Claude (Anthropic), tbd-strong-max tier, maximum reasoning
    reviewer_kind: ai
    relation: project
    date: '2026-11-08'
    scope: >-
      unnir's certificate for s(12) >= 9929/2500, pinned at 064c2955: the argument from certificate to bound with every hypothesis of Daniel's verify and Ryu's indep_scan; premises recomputed exactly; every one of the 39,765 bins at N = 96000 decided by an independent exact sweep written before the producer's checkers were read; the true minimum at 510 exact angles; the producer's minimum, bin and centre reproduced by emulating Daniel's core; controls; provenance of both checkers; the precedent of T-095 reconciled after a frozen blind pass.
    verdict: accepted
    covers: [NEW-T-NNN]
```

**`external_review` on the report evidence entry:** `state: informally-verified`,
`date: '2026-11-08'`, with this path.
Note: no defect; premises recomputed exactly; all 39,765 bins decided by the review’s
own exact code; zero slack (F4); F1 and F2 minor, to the author; F3 to F9 notes.

**Evidence entry for the review’s sweep** (suggested id
`E-n012-unnir-9929-2500-review-sweep`):

- `method: exact-algebraic`, `performed_by: repository`,
  `relationship_to_generator: independent-implementation`, `origin: replayed-here`,
  `replay_status: passed`.
- `independence.coverage`: `extent: full`, unit “angle bins of $N = 96000$ covering
  $[0°, 45°]$, each over its whole centre domain”, `checked: 39765`, `of: 39765`. The
  fold rests on `premises.py`’s exact D4 check.
- `verifiers: [V-unnir-924-review-premises, V-unnir-924-review-decider]`.
- `replay`: the commands in the review folder’s README.
- `limitations`: one implementation, Python with numpy integer counts, written by a
  Claude agent; the bins are the producer’s; 2.64 CPU-hours on a shared host.

**Verifier entries** (suggested):

- `V-unnir-924-review-decider`, `decide_bins.py` with `run_bins.py`, `role: decides`,
  `methods: [exact-algebraic]`. Its independence record:
  - `read: [mathematics, specification, certificate-format, producer-output]`;
  - `clean_room: true`, since the file’s digest was recorded before the producer’s
    checkers were read and the digest that ran is that one;
  - `shares: []`;
  - `written_by`: Claude (Anthropic), tbd-strong-max, maximum reasoning;
  - `overlaps_producer.extent: system-family`, since both checkers’ sources say Claude
    helped write them; `separate_prompt: true`; `separate_code: true`.
- `V-unnir-924-review-premises`, `premises.py` with `net_coverage.py`, `role: premises`,
  with the same record.
- `controls.py` is not clean-room: its emulation was written after reading the Rust.
  It decides nothing about the bound.

## 11. Questions for the Author

1. Will you make `indep_scan` refuse `VERIFIED` on a partial range, or ship
   `indep_check.cpp` for the full run (F1), and add a geometric negative control (F2)?
2. How were the points and weights found?
   In particular, was the exact tie at weight 1, reached through the 1,976 weight-$1/W$
   points, a target of the construction, and which checker stopped the search?
3. Do you claim $s(12) \ge 9929/2500$, as the packet says, or would you state
   $s(12) > 9929/2500$ (F5)?

## 12. Programs and Receipts

The programs and receipts are in
[`review-2026-11-08/`](../../../packing/resources/web/unnir-s12-lower-bound-3.9716-2026-11-08/review/review-2026-11-08/README.md),
staged for the replay lane’s packet.
Its README says what each program does, what it read, how to run it and what it printed.
The frozen blind findings are its `out/findings-blind.md`. The lane used about 2.7
CPU-hours: 2.64 for the complete sweep and minutes for the rest, at most two processes
at `nice -n 19`.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
