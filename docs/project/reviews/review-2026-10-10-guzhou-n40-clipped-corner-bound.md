# Guzhou0806’s `s(40) > 335427/50000`: Review of the Clipped-Corner Transfer on wand125’s `rect_n40_L67`

**Verdict: no blocking defect in the mathematics.** The argument from wand125’s
rectangle density to the strict bound $s(40) > 335427/50000 = 6.70854$ is correct as
written in the release’s `PROOF.md`, every exact premise it states holds, and every
number in it was recomputed here in exact rationals with code written for this review.
The weaker full-core bound $s(40) > 67000\sqrt{6400006889}/798988091 > 6.70848908$ rests
on fewer hypotheses and is correct too.
The one machine step that is not finite, that every side-$9977/10000$ square at each of
401 net directions captures mass at least $10001/10000$, was decided by this
repository’s own verifier `sqverify-fast`, vendored byte for byte, and six of its 401
directions, including the tightest, reproduced the release’s receipts here field for
field on the reviewed build.
The bound stands as the source’s report until the records lane’s complete replay passes;
this review names what that replay must show.

Seven findings are recorded, none blocking for the claim.
One, GN-5, blocks the census route only: the census driver and its control evaluator do
not read a format T certificate’s metadata net, so until a small tooling change lands
the records lane runs the binary directly and evaluates the control apart from the
crate, as this review did.
The draft significance `S3` is suggested by the precedent of `T-099`, with the note that
the transfer is a technique new to this record.

This is the mathematical lane of stage 4 of the result import for issue 485
(`think-3oi5`), written on 2026-10-10 by an AI agent (Claude, model Fable 5.1, maximum
thinking effort), prompted separately from the records lane, before any replay here and
before retention.
It registers nothing and moves no bound; the register entry is `T-NNN`,
to be assigned.

## Scope and Evidence

The subject is the claim of
[jlevy/squares#485](https://github.com/jlevy/squares/issues/485) (Guzhou0806, opened
2026-10-10T07:28Z): source
[Guzhou0806/n40-square-packing](https://github.com/Guzhou0806/n40-square-packing) at
`e5abeb4d078a5c5b35df6204dd9b93378e5a7880`, committed 2026-10-10T06:47:01Z, which the
tag `n40-670854-20261010` names; release ZIP `n40-670854.zip`, 203,095 bytes, SHA-256
`dbefee8658dc8f7d2e4a6ed21b0c3cd29f36ae393405a218f6bbfdce54465bc5`, published
2026-10-10T06:50:59Z.

**Read in full.** The issue and wand125’s review comment on it (07:53Z); the release’s
`README.md`, `PROOF.md`, `VERIFICATION.md`, `REPRODUCIBILITY.md`, `SOURCES.md`,
`certificate/parameters.json`, `verifier/finite.py`, `verifier/run.py`,
`verifier/prepare.py`, `verifier/release.py`, `tests/test_finite.py`, the workflow,
`results/verification.json` and `results/nodes.jsonl`, in both the tree at the pin and
the ZIP; this repository’s `packing/frontier/n-040.md`, `T-068`,
`E-n040-wand125-rect-67-sqverify-fast-replay`, `E-wand125-rectangle-2026-10-01-report`,
the 2026-10-01 packet README, `epistemics.md`, `result-import.md` (the intake pass, the
sequence and stage 1), `SOUNDNESS.md` in full, the
[2 October review of T-068](review-2026-10-02-wand125-rectangle-bounds-t068.md), the
[6 October soundness re-review](review-2026-10-06-sqverify-fast-declared-net-soundness.md),
the [format T route review](review-2026-10-06-sqverify-fast-format-t-route.md) and the
[finer-net review of T-099 and T-100](review-2026-10-06-wand125-finer-net-n18-n19.md);
and, in the crate, `certificate.rs` (`admit`, `declared_net`, `domain_upper`,
`direction`) with every use of `cert.step` and `cert.angle_count` in `main.rs`, `lib.rs`
and `rotated.rs`, found by grep; `devtools/sqverify_fast_census.py` (`net_directions`,
`run`, `exact_capture`, `tightest_centre`, `rectangle_control`) and
`check_sqverify_fast.net_step`.

**Not opened.** No checker of wand125’s or Tokoharu’s. The GitHub Actions log of run
38032128403; only the run’s conclusion was read through the API.

**Ran.** Everything in a scratch directory outside the tree, with the untrusted
downloads in directories of their own and every script written here under `python3 -I`
(3.13 for stdlib scripts, the project’s 3.14.7 for `sqpack`); the Rust steps at two
threads. Scripts: `exact_checks.py`, `break_it.py`, `captures400.py`, `mutants.py`,
`net201.py`, `run_controls.sh`.

| # | Command | Result |
| --- | --- | --- |
| 1 | `gh release download`, `sha256sum` | the ZIP’s digest and size are the issue’s |
| 2 | `gh repo clone`, `checkout --detach e5abeb4d` | the tag resolves to the commit; the tree has 36 files |
| 3 | `diff -r` ZIP against tree; `sha256sum -c SHA256SUMS` in both | identical except `results/verification.json`, `results/nodes.jsonl` and their `SHA256SUMS` lines (GN-3); every listed digest holds in each |
| 4 | `cmp` of the 15 vendored crate files against `git archive ef79288a4 packing/sqverify_fast` | all identical; the repository holds six more non-code files; `git diff ef79288a4 HEAD -- packing/sqverify_fast` is empty |
| 5 | `gh api` on run 38032128403, the release and the tag | run `success`, `head_sha` `e5abeb4d`, started 06:47:00Z; two assets; tag → commit |
| 6 | `exact_checks.py` (below) | every line below holds |
| 7 | `break_it.py` (below) | no failure in 600,401 orientations, 100,001 angles, 200,001 corner placements |
| 8 | `captures400.py`: `sqpack.rectangle_density.coverage_at_point` at the 400 oblique least-bound leaf centres | all at least $10001/10000$; least $1.0013165658$ at $r = 220$ |
| 9 | `rustup toolchain install 1.98.0`, `cargo build --release -j 2` on `packing/sqverify_fast` | binary SHA-256 `567a0fd58f7ae4e9…`, the 6 October review’s; embeds `d97758bb…` |
| 10 | the binary on the regenerated 401-node input, directions 0, 1, 73, 220, 383, 400, `--threads 2 --confirm` | every row identical to the release’s receipt apart from timing; summary premises `format T`, `net_origin metadata`, `angle_count 401`; 2.4 s |
| 11 | four controls (below) | each refused or re-netted as expected |
| 12 | `--probe` at the $r = 220$ control centre and the $r = 73$ leaf centre | exact captures equal to the first-party evaluator’s |
| 13 | `net201.py` | the transfer on the 201 net and at the next side, both refused |
| 14 | a script comparing the release’s even-index rows with the retained census rows of `rect_n40_L67` | identical apart from timing at all 201 indices; 16,505,592 boxes on each side |

What failed along the way: a sign error in the review’s own polygon clipper made its
first adversarial pass vacuous (negative “exact” areas); it was fixed and the pass
rerun, and the numbers below are from the rerun.
Several commands were refused by the session’s sandbox as too complex to verify and were
split or moved into script files.
Nothing the brief asked for went unestablished.

## The Claim

Let $s(40)$ be the least side of a square that holds forty closed unit squares with
pairwise disjoint interiors, any rotations, boundary contacts allowed.
The release claims

$$
s(40) > X = \frac{335427}{50000} = 6.70854,
$$

an increase of exactly $427/50000 = 0.00854$ over the case’s reported and verified
$67/10$ (`T-068`, wand125’s `rect_n40_L67`), and separately

$$
s(40) > \frac{67000\sqrt{6400006889}}{798988091} = 6.708489081\ldots > 6.70848908,
$$

which needs no density-peak estimate.
Neither is a packing, an optimality claim or a priority claim; the release says so.
The density is wand125’s, unchanged: the retained
`rect_n40_L67/certified_candidate.json` of the 2026-10-01 packet decompresses to the
SHA-256 `71011d03…` the release pins, so this is an extension of a certificate the
record already holds, not a new density.

Nobody else holds either value.
The register’s strongest lower bound at $n = 40$ is $67/10$; wand125’s later packets (3
to 6 October) have no $n = 40$ certificate; the Kingbird catalogue lists packings, not
lower bounds. wand125’s comment on the issue reports a third run of the release’s entry
point and an independent exact check of the transfer; that is a third party’s evidence
on the issue, not retained here.

## The Argument From Certificate to Bound

Notation, all exact rationals: $L = 67/10$, $K = [0, L]^2$, $B = 9977/10000$,
$M = 3999/100$, $D = 83/80000$, net half-angle tangents $t_j = jD$ and angles
$\theta_j = 2\arctan t_j$ for $j = 0, \ldots, 400$, threshold $\tau = 10001/10000$,
$X = 335427/50000$, parent side $q = L/X = 335000/335427$, $h = 514946944479/10^{15}$,
$H = 2818711359413/10^{9}$.

**1. The density.** The 480 positive-weight rows of the certificate, read as exact
decimals and fractions, expand through the eight symmetries of $K$ with density
$w/(8|R|)$ per image into 3,840 terms, 3,792 distinct rectangles after merging, a
$D_4$-invariant $g \ge 0$ on $K$ with $\int g = M = 3999/100$. Recomputed here with an
expansion written from the eight maps on points (item 6): 480 rows, $M$ exact, 3,840
terms, 3,792 distinct, the merged density invariant under each map, and $\int g = M$
from the merged terms.
The release’s derived 401-node input is these 480 rows with the net declared in the
file’s `certificate` metadata (`D = 83/80000`, `angle_count = 401`) and
`coverage_lower_bound_exact = 10001/10000`; regenerated here from the retained candidate
by the construction `PROOF.md` and `finite.py` describe, its SHA-256 is
`49f696a4533ded9532b879bf69706da35bc03a49db79718573760adc08cd458e`, the digest both
receipts name as `input_sha256`. So the measure the crate decided is the retained
certificate’s, and nothing else.

**2. The nodal statement.** For every $j = 0, \ldots, 400$ and every centre $c$ with the
closed square $Q_j(c)$ of side $B$ and angle $\theta_j$ inside $K$ (Tokoharu’s domain,
$c \in [a_j, L - a_j]^2$ with $a_j = B(\cos\theta_j + \sin\theta_j)/2$),

$$
\int_{Q_j(c)} g \ \ge\ \tau .
$$

This is SOUNDNESS.md’s coverage premise for format T on the net $D = 83/80000$,
$N_\theta = 401$, which the crate admits from the metadata under the same premises lemma
N0 states for a declared net: $D > 0$, $2 \le N_\theta \le 2^{16}$,
$B(1 + D) = 798988091/800000000 < 1$, $t_{400} = 83/200$ with
$t_{400}^2 + 2t_{400} - 1 = 89/40000 > 0$, $t_{400} \le 1/2$; the tangent-form premise
(e) is format M’s and is not needed for Tokoharu’s domain (it holds anyway).
The 401 directions are the 201 standard ones at the even indices and their midpoints at
the odd ones. The crate decided all 401 at $\tau$: every row `verified`, none refused,
least certified bound $1.000100000471634$ at $r = 73$ (an odd, new direction),
32,970,910 boxes, of which 16,505,592 at the even indices, exactly the retained 3
October census rows of `rect_n40_L67`, row for row, and 16,465,318 at the odd ones.
The retained census row at $r = k$ and the release’s row at $r = 2k$ are identical apart
from timing at all 201 indices (item 14): the release ran this crate’s semantics on this
measure.

**3. The transfer.** Suppose forty unit squares pack in a square of side $X$. Scale by
$L/X$: forty closed squares of side $q = 335000/335427 = 0.99872699\ldots$, pairwise
interior-disjoint, in $K$. Fix one parent $P$ with centre $p$ and orientation $\alpha$
modulo $\pi/2$. Since $g$ is $D_4$-invariant and the diagonal reflection $\sigma$
preserves $K$, $\int_P g = \int_{\sigma P} g$, and $\sigma$ sends $\alpha$ to
$\pi/2 - \alpha$; so each parent’s integral may be bounded with $\alpha \in [0, \pi/4]$,
one parent at a time, without the reflected parents forming a packing.
Since $\theta_0 = 0$ and $\theta_{400} = 2\arctan(83/200) > \pi/4$ (because
$(1 + 83/200)^2 = 80089/40000 > 2$), $\alpha \in [\theta_j, \theta_{j+1}]$ for some
$j \le 399$. The gap is $\theta_{j+1} - \theta_j = 2\arctan\big(D/(1 + j(j+1)D^2)\big)
\le 2\arctan D$. Put $\delta_0 = 2\arctan h$ and $\beta = 2\arctan b$ with
$b = (D - h)/(1 + Dh)$, so that $2\arctan D - \delta_0 = \beta$ by the subtraction
formula.

- *Upper node.* If $\theta_{j+1} - \alpha \le \delta_0$, take the reference
  $R = Q_{j+1}(p)$, concentric with $P$. Its extent along either axis of $P$ is
  $B(\cos\delta + \sin\delta)$ with $\delta = \theta_{j+1} - \alpha$, nondecreasing in
  $\delta$ on $[0, \pi/4]$, and $B(\cos\delta_0 + \sin\delta_0) \le q$ holds in exact
  rationals (with $\cos\delta_0 = (1 - h^2)/(1 + h^2)$, $\sin\delta_0 = 2h/(1 + h^2)$;
  the slack is $1.63 \times 10^{-15}$). So $R \subseteq P \subseteq K$: $R$ is legal,
  and $\int_P g \ge \int_R g \ge \tau$. That $\theta_{400}$ exceeds $\pi/4$ does not
  matter here, since containment is relative to $P$.

- *Lower node.* Otherwise $\theta_{j+1} - \alpha > \delta_0$, so
  $\delta = \alpha - \theta_j < 2\arctan D - \delta_0 = \beta$. Take $R = Q_j(p)$. It is
  legal: $\theta_j \le \alpha \le \pi/4$, $\cos + \sin$ is increasing on $[0, \pi/4]$
  and $B \le q$, so $R$’s axis-aligned bounding box, concentric with $P$’s, has
  half-extent $B(\cos\theta_j + \sin\theta_j)/2 \le q(\cos\alpha + \sin\alpha)/2$, and
  $P$’s bounding box lies in $K$ because $P$ does.
  Hence $\int_R g \ge \tau$, and with $g \ge 0$ and $g \le H$ almost everywhere,

  $$
  \int_P g \ \ge\ \int_{R \cap P} g \ =\ \int_R g - \int_{R \setminus P} g
  \ \ge\ \tau - H\,|R \setminus P| .
  $$

**4. The clipped corners.** In $P$’s frame, $R$ is the side-$B$ square rotated by
$\delta$; put $c = \cos\delta$, $s = \sin\delta$, $e = \max(0, B(c + s) - q)$. When
$e > 0$ exactly one corner of $R$ lies beyond each side of $P$, by $e/2$. The part of
$R$ beyond the top side lies in the cone at that corner spanned by $R$’s two edges, and
the cone’s part above the side is the right triangle with legs $e/(2s)$ and $e/(2c)$
(the edges descend at rates $s$ and $c$), of area $e^2/(8cs)$. Summing the four sides,
$|R \setminus P| \le e^2/(2cs)$ by subadditivity, whatever the pieces’ shapes and
whether they overlap.
`PROOF.md` states the pieces as four interior-disjoint right triangles, which is true
here with room to spare (the legs are $7.3 \times 10^{-3}$ and $7.6 \times 10^{-6}$ at
$\delta = \beta$, against side $B$) but is not needed (GN-1). With $z = c + s$ and
$a = q/B \ge 1$, $2cs = z^2 - 1$ and $e = B(z - a)$, so the bound is
$B^2 (z - a)^2/(z^2 - 1)$, whose derivative in $z$ is
$2(z - a)(az - 1)/(z^2 - 1)^2 \ge 0$ for $z > a$; and $z = \sqrt2 \sin(\delta + \pi/4)$
increases on $[0, \pi/4]$. So over $0 \le \delta < \beta \le \pi/4$ the loss is at most
$A = e^2/(2cs)$ evaluated at $\beta$, with $\cos\beta, \sin\beta$ exact from $b$. Here
$\beta = 1.0451 \times 10^{-3}$, $e = 1.5161 \times 10^{-5}$,
$A = 1.09967 \times 10^{-7}$, and $HA = 3.0996 \times 10^{-4}$.

**5. The density peak.** $g \le H$ almost everywhere, where $H$ is the greatest sum of
densities over any open cell of the arrangement, each density rounded up to a multiple
of $10^{-9}$. Recomputed here by a different method (the half-open stack at every
lower-left corner, integer arithmetic after scaling by the common denominator): the
exact essential supremum is

$$
\operatorname{ess\,sup} g = \frac{744157113224753949201233200959491557948628550000000000000000000000000000000}{264006142643866310314006500845084529851262768737056316088338267454599309} = 2818.71135941178\ldots,
$$

attained on a cell whose lower-left corner is $(0.87567\ldots, 2.71307\ldots)$ where two
terms overlap, so $\operatorname{ess\,sup} g \le H$ with $H - \operatorname{ess\,sup} g
= 1.215 \times 10^{-9}$; and with the release’s rounding the same method returns $H$
exactly. wand125’s comment reports the same value.
Cell boundaries have area zero, so the bound on $\int_{R \setminus P} g$ stands.

**6. Counting and the endpoint.** Every parent captures at least
$\chi = \tau - HA = 0.99979003557\ldots \ge 99979/100000$ (margin
$3.56 \times 10^{-8}$). The parents have disjoint interiors and $g$ is absolutely
continuous, so $40\chi \le \sum_i \int_{P_i} g \le \int_K g = M$, while
$40 \cdot 99979/100000 - 3999/100 = 1/625 > 0$: no forty squares of side $q$ pack in
$K$, that is, no forty unit squares pack in a square of side exactly $X$. Strictness:
with sides in $[1, 7]$, centres in $[0, 7]^2$ and angles in $[0, \pi/2]$, the feasible
set is compact (vertex containment is closed; interior disjointness is a finite union of
closed non-strict separating-axis conditions) and nonempty (the $7 \times 7$ grid), so
the least side is attained; a packing at side $s(40) \le X$ would sit in a container of
side exactly $X$. Hence $s(40) > X$. Correct.

**7. The full-core bound.** The nearest node to $\alpha$ is within half a gap,
$\arctan\big(D/(1 + j(j+1)D^2)\big) \le \arctan D$, so the concentric side-$B$ square at
that node has extent at most $B(\cos + \sin)(\arctan D) = B(1 + D)/\sqrt{1 + D^2}
= \gamma$ in the parent’s frame: a parent of side $\gamma$ contains a legal reference
and captures at least $\tau$, and $40\tau - M = 7/500 > 0$. With the endpoint argument,
$s(40) > L/\gamma$, and $(L/\gamma)^2 = 28729630924721000000/638381969559824281
= (67000/798988091)^2 \cdot 6400006889$ exactly, so $L/\gamma$ is the closed form
claimed; $6.70848908^2 < (L/\gamma)^2 < 6.70848909^2$. Correct, and it uses only item 2.

**What the finer net buys.** The same transfer on the standard 201 net, with the same
$h$, gives $\beta = 3.12 \times 10^{-3}$, $A = 6.94 \times 10^{-4}$ and $HA = 1.96$:
$\chi < 0$, refused.
At the next side on the release’s grid, $X' = 335428/50000$, no $h$ works: at the
largest $h$ the containment allows, $40\chi - M = -0.00998$. The release’s $h$ is
$8 \times 10^{-16}$ below its own limit.
The full-core argument on the retained 201-direction census row alone gives
$s(40) > 6.70155\ldots$, a consequence of `T-068`’s certificate and the crate’s theorem
that nobody has claimed; it is noted, not proposed.

## Hypotheses Each Checker Assumes

The nodal verifier (the crate, items 2 and 7):

1. The input is the retained measure: admission recomputes the expansion, the merge and
   $M$ from the file, and the regenerated input’s digest ties the file to the retained
   certificate. Discharged here (item 1).
2. The net premises, checked at admission in exact rationals; discharged here as well.
3. SOUNDNESS.md’s theorem and lemmas for format T on an admitted net, with Tokoharu’s
   domain: reviewed on 3 and 6 October; lemma N0 covers every net admission accepts, and
   `domain_upper`, `direction` and every search path read the admitted `cert.step` and
   `cert.angle_count` (the reading list above).
   Trusted on those reviews; this review re-read the admission path only (GN-6).
4. Binary64 with IEEE-754 semantics, the Rust compiler at 1.98.0 and the pinned
   dependencies. Trusted.
5. All 401 directions finish `verified`: the receipts show it, and six directions
   reproduced here. The complete run is the records lane’s.

The finite checks (`finite.py` in the release; `exact_checks.py` here, written
independently of it, items 1, 4 to 7):

6. JSON decimals are their literal values, read as fractions; Python’s unbounded
   integers and `Fraction` are exact.
   Trusted.
7. The essential supremum of a finite sum of indicator densities is attained on an open
   cell of the arrangement and equals the maximum over lower-left corners of half-open
   stacks. Proved above; both implementations agree, and the release’s two sweeps agree
   with each other.
8. The scalar chain as item 3 to 6 state it.
   Every inequality recomputed here holds, and every fraction in the receipt’s `finite`
   block equals the value recomputed here: `parent_side`, `b`, `density_upper`,
   `cap_area_upper`, `charge_lower`, `counting_margin`, `simple_counting_margin`,
   `uncut_side_squared`.

The prose (`PROOF.md`, items 3, 4 and 6): the fold, the case split, the legality of both
references, the cone bound and its monotonicity, the counting and the attainment.
Re-derived above; nothing is assumed beyond measure theory.
`finite.py`’s `validate_nodes` reads the receipts and checks their shape and values; it
decides nothing about coverage, and `release.py --check` is not a replay, as the release
says.

## Trust Boundaries and What the Checkers Share

The Rust nodal verifier **is** `sqverify-fast`: the fifteen vendored files are byte for
byte the crate at `ef79288a4`, which is the crate at `origin/main` today, source digest
`d97758bb…`, the build the 6 October review accepted.
It decides the 401 coverage statements and nothing else.
With Tokoharu’s `verify.cpp` and wand125’s `mixed_rotated_verify.cpp` it shares no code;
it shares the theorem (net and shrink), the measure, the $D_4$ reduction, the rational
net, Tokoharu’s domain and the threshold, so a defect in that mathematics would reach
all of them, as the 2 October review said of the base certificate.
The release’s label `CODE_DISTINCT_FULL` means distinct from Tokoharu’s C++ route its
author used during research, which the release does not ship; it does not mean distinct
from this repository’s crate, and a replay here with the crate reproduces the producer’s
nodal run with the producer’s code (GN-4).

The Python finite checks share no code with either verifier and no code with this
review’s scripts; they share the definition of the density and its $D_4$ expansion with
everything. Their refusal tests (`tests/test_finite.py`) cover mutated parameters, a
false peak, missing or duplicated nodes, a wrong net or domain, a weak threshold and
fault injection, as the release says; they test `validate_nodes` against synthetic
receipts, which is bookkeeping, not coverage.

Independent of all of them here: `sqpack.rectangle_density`, written before the crate,
evaluated the exact capture at the 400 oblique least-bound leaf centres and at the
control centre, where the crate’s `--probe` returns the same rational.

## Findings

### GN-1 — Non-blocking, proof text: the triangle statement is unconditional in `PROOF.md`

`PROOF.md` says the reference outside its parent “consists of four interior-disjoint
right triangles with legs $e/(2c)$, $e/(2s)$” and that “$q \ge B$ prevents overlap”.
The pieces are triangles only while both legs are at most $B$, and disjointness follows
from $B \ge q(c + s)$ failing, which $q \ge B$ gives for $\delta > 0$; neither condition
is stated. The bound $e^2/(2cs)$ holds without them, by the cone and subadditivity (item
4), and for these parameters the clipped area equals the formula at every one of 100,001
angles in $[0, \pi/4]$ (ratio at most $1 + 2 \times 10^{-10}$, rounding).
No change to the claim.

### GN-2 — Non-blocking, robustness: $h$ is at the containment limit

$B(\cos\delta_0 + \sin\delta_0) \le q$ holds with slack $1.63 \times 10^{-15}$, and the
largest admissible $h$ is $8.2 \times 10^{-16}$ above the chosen one.
Any decimal restatement of $h$ or $q$ breaks the first branch; the chain is sound only
in exact rationals, which the release and this review use.
A replay must not round.

### GN-3 — Non-blocking, record: the release ZIP is not the pinned tree

The ZIP’s `results/` holds the GitHub Actions receipt (`source_commit` `e5abeb4d…`,
binary `f167c16b…`, 72.35 s wall, Python 3.12.3) where the tree holds the local one
(`source_commit` null, binary `75a14053…`, 60.06 s, Python 3.14.4); `SHA256SUMS` differs
in those two lines, and `release.py --package` writes it so.
The 401 rows are identical apart from timing, both name the same input digest and the
same crate source digest, and the issue describes the ZIP correctly.
The packet should retain both receipts and say which is which.

### GN-4 — Non-blocking, classification: the producer’s nodal code is this repository’s

For the nodal step, `relationship_to_generator` of a replay here with `sqverify-fast` is
`same-implementation` with respect to the release’s verification, since the release ran
this crate; it is `independent-implementation` only with respect to wand125’s and
Tokoharu’s checkers, which decided the base certificate at 201 directions and never ran
at 401. The finite step re-derived by a first-party exact script is independently
re-implemented with respect to `finite.py`. The register’s wording must say which; the
coordinator decides how the two parts compose.

### GN-5 — Blocking for the census route only: the tooling does not read a format T metadata net

`sqverify_fast_census.net_directions` returns 201 for any file without `proof_net`,
`check_sqverify_fast.net_step` returns $83/40000$ for a format T file, and
`rectangle_control` then exits with “the row’s net step 83/80000 is not the file’s
83/40000; the control would evaluate another net”; `--check` would compare 401 rows with
201\. The crate admits the net, reports `net_origin: metadata` and decides on it (items
10 and 11). Until the driver and the control evaluator read a format T metadata net as
admission does, with a test, the records lane runs the binary directly and evaluates the
control apart from the crate at the explicit angle, as item 8 did; the contract below is
written that way. This is DR-1 of the 6 October review again, for format T.

### GN-6 — Non-blocking, scope of the crate’s reviews: the format T metadata-net path has no retained review of its own

`admit` lets format T’s metadata set the net (“format T’s metadata may change it”) and
checks premises (a) to (d) on whatever net results; lemma N0 is stated for every net
admission accepts, and the 6 October verdict named format T on the standard net and
format M on a declared net.
`V-sqverify-fast`’s registry entry describes “the standard 201, or the net a format M
file declares”.
This review read the path and found the admitted step used everywhere the
net enters; the evidence entry and the registry note should name the path, and control D
below shows admission refusing a metadata net that stops short of $\pi/4$.

### GN-7 — Non-blocking, our record: `n-040.md`’s body still says 6.695

The issue notes it. The case record’s frontmatter carries $67/10$ and its “Open”
paragraph still states endpoints $6.695$ and $1339/200$ and credits `T-045`; the lane
that updates the case record on registration should correct the paragraph.

## The Replay Contract

What the records lane must run, and what each run must show, for the status to move from
reported. Every number is from the release’s receipts and was reproduced here where the
row says so.

**0. Retention.** The tree at `e5abeb4d` (36 files, `SHA256SUMS` holding) and the ZIP
`dbefee86…` with its CI receipt, both receipts named for what they are (GN-3); wand125’s
comment cited or retained as text.
The density is already retained in the 2026-10-01 packet.

**1. The derived input,** regenerated first-party from the retained
`rect_n40_L67/certified_candidate.json.gz`: the 480 positive-weight rows in file order,
coordinates and weights as exact fractions written `num/den` (or `num` when integral),
top-level `n`, `L`, `B`, `coverage_lower_bound_exact` `"10001/10000"`, and `certificate`
`{"L": "67/10", "B": "9977/10000", "D": "83/80000", "angle_count": 401}`, serialised
with sorted keys, no spaces and a trailing newline.
Its SHA-256 must be `49f696a4533ded9532b879bf69706da35bc03a49db79718573760adc08cd458e`;
the digest, not the construction, is the binding to the receipts.

**2. The nodal run,** on a build of reviewed crate source (`--source-digest`
`d97758bb…`; `567a0fd5…` is such a binary at rustc 1.98.0):

```text
sqverify-fast --candidate derived-401.json --n 40 --side 67/10 --directions all \
    --threshold 10001/10000 --threads 2 --confirm --receipts DIR
```

Expected: 401 rows `verified`, summary `VERIFIED`, `refused_directions: []`,
`fault_injected_at_box: null`, exit 0; premises `format T`, `net_origin metadata`,
`angle_count 401`, `D 83/80000`, `L 67/10`, `B 9977/10000`, `mass_exact 3999/100`,
`mass_below_n 1/100`, `centre_domain tokoharu`, `source_rectangles 480`,
`expanded_rectangles 3792`, `net_last_tangent 83/200`,
`shrink_bound 798988091/800000000`, `input_sha256 49f696a4…`; $r = 0$ by
`axis-vertex-sweep` over 4,879,681 vertices (2,209 events on each axis), bound
$1.0012141064171602$; the other 400 by `interval-branch-and-bound`, 32,970,910 boxes in
all, greatest depth 30, least certified bound $1.000100000471634$ at $r = 73$. On the
same source and toolchain the box counts are deterministic and the even rows equal the
retained census rows; a different toolchain may change counts and not verdicts.
The source measured 60 s of wall time at four threads (235 CPU-seconds); expect two to
three minutes at two threads.

**3. The finite checks,** by a first-party exact script (OR-1: the review’s
`exact_checks.py` is the measurement; the tool belongs in `devtools`): the values of
items 1 and 5 above, and the scalar chain of items 3, 4, 6 and 7, each equal to the
receipt’s `finite` block.
At least: 480 rows, $M = 3999/100$, 3,840 terms and 3,792 distinct,
$\operatorname{ess\,sup} g \le H$ with $H$ reproduced by the rounded-up method,
$q \ge B$, $B(\cos\delta_0 + \sin\delta_0) \le q$,
$b = 41804244441680000/80000042740596391757$, $\chi \ge 99979/100000$,
$40 \cdot 99979/100000 - M = 1/625$, and $6.70848908^2 < (L/\gamma)^2$.

**4. Controls,** each of which must refuse:

| Control | Expected |
| --- | --- |
| A. weights $\times 99/100$, metadata kept, directions 73 and 220 | `counterexample-candidate` at both, with exact witnesses below $\tau$ ($0.99932$ and $0.99923$ centre bounds); summary `REFUSED`; exit 1 (reproduced here) |
| B. weights $\times 499392017517921/500000000000000$ at direction 220, the census rule’s near-threshold factor at the centre of least exact capture $(3.353931795732347, 5.09801085267264)$, capture $1.0013165658$ | refused with an exact witness $1.00009999\ldots < \tau$ (reproduced here) |
| C. the `certificate` block removed | admitted on the standard net, `angle_count 201`, `net_origin standard`: a run of another claim, not this one (reproduced here) |
| D. `angle_count 201` with `D 83/80000` | admission refuses, “the net does not reach past pi/4”, exit 2 (reproduced here) |
| E. $H$ replaced by $H - 2 \times 10^{-9}$ | the exact script reports $\operatorname{ess\,sup} g$ above it |
| F. $X = 335428/50000$ | $40\chi - M < 0$ for every admissible $h$ ($-0.00998$ at the best) |
| G. $h + 10^{-15}$ | the first-branch containment fails |
| H. the 201 net, $D = 83/40000$ with last index 200, same $h$ | $\chi < 0$ |

The exact capture at B’s centre by `sqpack.rectangle_density` is the crate’s probe value
there, numerator beginning `964919800254432…`.

**5. The census route** carries once GN-5 is fixed: a census row at all 401 directions
and a control receipt at the tightest centre ($r = 220$, index 110 of the standard net,
the same centre the retained `rect_n40_L67.control.json` used).

What a complete replay here does and does not give: the nodal statement reproduced with
the producer’s code, which is first-party and reviewed, and the finite steps decided
again by other code; no second method decides the nodal statement.
Tokoharu’s `verify.cpp` at 401 angles would be one, at roughly twice its 201-angle cost
on this certificate (6,521 s of wall time upstream), given an input generator for a
finer net, which is a W7 slice and a budget the owner sets.

## Where the Issue, the Release and the Record Differ

- The issue, the release and the receipts agree at every number read here: the two
  bounds, $427/50000$, $B$, $M$, $D$, $\tau$, $h$, $H$, $99979/100000$, $1/625$, the
  three digests, 401 of 401, 32,970,910 boxes, 60.06 s and 72.35 s, Rust 1.98.0.
- The issue says the ZIP “contains the separate CI receipt”; it contains it in place of
  the tree’s (GN-3).
- The release vendors the crate at `ef79288a4` and says so; the record’s reviewed source
  is the same bytes.
- The issue’s remark about 6.695 is right (GN-7).
- wand125’s comment reports a minimum certified capture of $1.000100000472$ and a
  density peak of $2818.71135941\ldots$; both match the receipts and the value computed
  here.

## Significance

`T-099` and `T-100`, single-count raises on a finer net with no new technique, were
scored `S3` as the strongest verified lower bound on record at their counts.
This claim raises $n = 40$ by $0.00854$ and brings a technique new to this record, a
continuous-angle transfer with a clipped-corner loss bound that applies, with a finer
net, to any retained format T certificate; it also depends on nothing but wand125’s
density, the crate and finite arithmetic.
`S3` is suggested on that precedent; the score is the registering lane’s.

## Disposition

No finding blocks registration as reported or, once the contract’s runs pass, the replay
evidence. GN-5 blocks a census-route receipt only, and names its fix.
GN-3, GN-4 and GN-6 are wording and retention obligations for the records lane; GN-7 is
a correction to the case record; GN-1 and GN-2 are notes for the author, of which GN-1
alone is worth a sentence in the reply.
The reviewer’s own checks are evidence and not a rung: what was proved here is the
transfer, the clipping bound and the endpoint; what was checked by computation here is
every finite quantity, the derived input’s identity, six of 401 directions and the eight
controls; what the source reports and this review did not run is the complete
401-direction run, which its receipts, its CI run and wand125’s comment each report.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
