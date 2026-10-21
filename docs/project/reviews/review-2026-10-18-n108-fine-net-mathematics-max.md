<!-- tbd:review v=1 id=C kind=correctness pr=671 round=1 head=32d47d3214ec28f2a82b89689cd8bb8f63f98e02 base=804eff369193b698d497a9c06847059eb9de0470 -->
# Mathematical Review of the n = 108 Fine-Net Certificate

**Review C** (correctness review, round 1), at
`32d47d3214ec28f2a82b89689cd8bb8f63f98e02`, base `main` at
`804eff369193b698d497a9c06847059eb9de0470`. Reviewer: **Codex system family, strongest
tier, maximum reasoning**. Channel:
[formal GitHub Review C](https://github.com/jlevy/squares/pull/671#pullrequestreview-5562556726)
and retained review note.
Coverage: **1 of 18 imported certificates**, the n = 108 mathematical slice of the
230-file PR. The other certificates, publication code, and page rendering are outside
this delegated review.
Tests run: the newly written `review-max/n108_audit.py`, five exact pose calculations,
four analytic geometry controls, Ruff, and BasedPyright; all passed.
No source checker, maintained audit program, native replay, or project test suite was
executed in this review.

## Verdict for the Author

**The mathematical implication and the checked exact premises are accepted.
No blocking or major mathematical defect was found.** One minor documentation finding,
C1, affects discovery of the control log only.

The claim is that 108 unit squares with disjoint interiors cannot fit in the closed
square of side $L=531/50=10.62$. This implies the stated lower bound $s(108)\ge531/50$;
it does not establish optimality.
The certificate is `mixed_n108_L1062` in the
[source packet](../../../packing/resources/web/wand125-fine-net-lower-bounds-2026-10-16/square-packing/problems/square-lower-bounds/certificates/mixed_n108_L1062/README.md).

This is a mathematical audit with exact checks of the input and five poses.
Universal coverage is supported here by **retained replay records**, whose complete
index sets and input identities were checked.
I did not freshly run their verifier.
The separate native replay and this audit must retain their different coverage and
implementation relationships; this audit supplies no independent full confirmation.

The review remains pinned to the head above.
GitHub reported a later head, `1b2cf7cfe15c4eec90d447bf3977a683d96dec1d`, during setup.
That later diff is not covered.

## Argument From Certificate to Claim

Let $K=[0,L]^2$. Each of the 823 listed rectangles $R_j$ has rational coordinates,
positive area, and positive rational mass $w_j$. Define

$$
\mu(A)=\sum_{j=1}^{823}\frac{w_j}{8|R_j|}
\sum_{g\in D_4}|A\cap gR_j|,
$$

where $D_4$ acts by the eight symmetries of $K$. The formula preserves multiplicity when
a rectangle has a symmetry; one must not deduplicate its images and divide by eight
afterward. It defines a nonnegative, $D_4$-invariant measure supported on $K$.
Overlapping rectangles add density.
They need not be disjoint.

My independent expansion gives **6,524 distinct rectangles**, with exact integrated mass

$$
M=\sum_jw_j=\frac{10799999}{100000}=108-\frac1{100000}.
$$

There are no point or segment atoms in this candidate.
These are calculations from the candidate bytes, not acceptance of its `total_mass`
field: the program checks the field against the sum and checks the expanded integral
against that same sum.

A unit square’s orientation is defined modulo $\pi/2$. To establish the capture property
for one square, use a symmetry of $K$ to fold its orientation to $\varphi\in[0,\pi/4]$.
This may depend on the square: the argument is a universal statement about each square,
and the resulting core is transformed back before the packing count is taken.
It does not require one reflection that folds all packed squares simultaneously.

Put $u=\tan(\varphi/2)$. The net nodes are $t_r=rD$, $D=83/40000$, $r=0,\ldots,200$. Its
endpoint $t_{200}=83/200$ exceeds $\sqrt2-1$, since

$$
t_{200}^2+2t_{200}-1=\frac{89}{40000}>0.
$$

Thus some node satisfies $|u-t_r|\le D/2$. For the angular discrepancy
$\delta=|\varphi-2\arctan t_r|$,

$$
z=\tan(\delta/2)=\frac{|u-t_r|}{1+ut_r}\le\frac D2.
$$

A concentric core of side $B=9977/10000$ at the net angle has extent along either axis
of the unit square at most

$$
B(\cos\delta+\sin\delta)
=B\frac{1+2z-z^2}{1+z^2}
\le B(1+D)
=\frac{399908091}{400000000}<1.
$$

Therefore the **closed core lies strictly inside the open unit square**. The side margin
is $91909/400000000$, and each edge has half that guaranteed margin.
Touching unit squares consequently have disjoint closed cores.

The centre domain must use the orientation of the original unit square, not merely the
orientation of its core.
Write

$$
a_r=\max(0,rD-D/2),\qquad
\rho(t)=\frac{1+2t-t^2}{2(1+t^2)}.
$$

On $[0,\sqrt2-1]$, $\rho'(t)=(1-2t-t^2)/(1+t^2)^2\ge0$. A folded square assigned to node
$r$ has $u\ge a_r$ and must have its centre in $[\rho(a_r),L-\rho(a_r)]^2$. The last bin
is legitimate: its left endpoint is $33117/80000$, with

$$
a_{200}^2+2a_{200}-1=-\frac{4544311}{6400000000}<0.
$$

So the net’s slight overshoot beyond $\pi/4$ neither loses the last physical orientation
nor justifies treating $\rho$ as increasing beyond its true interval.
Quarter turns preserve the square’s orientation modulo $\pi/2$ and preserve $\mu$; they
reduce the centre domain to $[L/2,L-\rho(a_r)]^2$. A reflection alone would reverse a
non-axis net angle and cannot be used as an additional centre reduction at that fixed
angle.

The remaining computational premise is, for every $r$ and every centre in that quadrant,
$\mu(Q_r(c))\ge1$. If it holds, transform the chosen cores back to their original
squares. Their disjointness and nonnegative measure give

$$
108\le\sum_{i=1}^{108}\mu(Q_i)\le\mu(K)=M<108,
$$

a contradiction. No assumption about the numerical search or an optimal packing enters
this implication.

## Premises, Coverage, and Arithmetic

The retained
[audit receipt](../../../packing/resources/web/wand125-fine-net-lower-bounds-2026-10-16/review-max/audit.json)
records the fresh computations.
In addition to the identities above, the program checks containment and positivity of
all 823 representatives; exact multiplicity in the expansion; nonempty domains at all
201 indices; $t_{200}\le1/2$; the count, coordinate, and density caps; and the stronger
admitted tangent condition

$$
B\left(1+\frac D{1-D^2/4}\right)
=\frac{63985225828447}{63999931110000}<1.
$$

That last condition is conservative for the shrink proof just given.
It does not replace a coverage calculation.

The implementation’s existing mathematical route is appropriate for this input: at the
axis, rectangle overlap is bilinear between exact event coordinates, so its minimum is
attained at a grid vertex; at a non-axis direction, a certified centre capture minus a
bound on its translation derivatives is a lower bound over an entire centre box.
The partition must cover the quadrant, every accepted box must clear threshold 1 with
outward rounding, and unresolved or nonfinite boxes must refuse.
These obligations are stated in
[SOUNDNESS.md](../../../packing/sqverify_fast/SOUNDNESS.md), lines 175–209, 211–336, and
414–492. I checked the mathematical arguments in those ranges and the admission/domain
definitions in `src/certificate.rs`, lines 448–650. I did not repeat a line-by-line
audit of the numerical search implementation.

The source log and the native census log each contain exactly one `verified` row for
every index 0 through 200, a `VERIFIED` summary at threshold 1, no refused index, and no
injected fault. Each reports 136,113,602 branch-and-bound nodes.
The axis row reports 30,140,100 vertices.
The reported lower bounds clear 1. Those facts check receipt completeness and
consistency; a receipt is not a proof trace that this program independently replays.

I also wrote a rational half-plane polygon intersection calculation, importing no
project code. At the native 99/100 control witnesses for indices **1, 100, 157, and
200**, it confirms all of the following: the pose lies in the correct domain; the
original capture is at least 1; the scaled capture is below 1; and the scaled capture
agrees *exactly* with the retained rational value.
Binary64 poses were converted to exact binary rationals, not interpreted as their
printed decimal values.

At the source’s axis control pose, supplied as rational strings, the independently
computed original capture lies in $[1.004011114658670742,1.004011114658670743]$ and its
197/200 scaling lies in $[0.988950947938790681,0.988950947938790682]$. This explains the
source receipt’s distinction between 32 refusals and 31 explicitly marked exact
witnesses: its axis sweep row has an `argmin` rather than the oblique
`exact_below_threshold` field.
The fresh calculation verifies that axis refusal too.
It does not independently check the other 31 source control poses.

## Trust Boundary and Independence

The source’s `check2` receipt identifies the forked `sqverify-fast` source digest
`ab6e33e164dbc5c32b40349ba55981b58e630b5eef59534196a69d259404fd7c`. The native retained
replay identifies the maintained source digest
`d97758bbc9639edc70b8bd7dc83106d4e8d1be034bacb3e88f8c539b88091c88`. The source README,
lines 19–22 and 49–52, explicitly describes its copy of this repository’s verifier.
The native build is covered by the
[general declared-net soundness review](review-2026-10-06-sqverify-fast-declared-net-soundness.md)
and its [fix check](review-2026-10-06-sqverify-fast-declared-net-fix-check.md).
I read those earlier general reviews after writing the polygon audit; neither is an n =
108 review.

The source and native runs share the verifier lineage, geometry, interval arithmetic
approach, and dependencies.
Their matching node counts are consistent with that shared search.
A fresh machine or different source digest does not make these two runs independent
implementations. The native run can independently repeat an execution; it cannot remove
errors shared by the engine family.

The native route trusts exact parsing and rational enclosure; the D4 expansion and
per-bin domain; axis-event enumeration; the branch-and-bound partition and certified
bounds; IEEE binary64/compiler behaviour; the Rust dependencies; and the connection
between a receipt and the process that wrote it.
Earlier engine reviews support the numerical implementation; this review checks the new
certificate’s mathematical fit and selected exact calculations.

The raw candidate SHA-256 is
`4d72da64052667a3ebf057f7e78ea9d40f1521a0b86ddef210a2be319d27042a`. Its retained gzip
SHA-256 is `acaf27593b53c3472ab249805f672030e3cbd3323033641b1df1d8460ae8835b`. The
source receipt binds the raw bytes and the native receipt binds the gzip bytes; my
program checked both against the same decompressed candidate.
This is an explained representation difference, not an input mismatch.

My audit uses Python 3.14.7 standard-library `Fraction`, JSON, gzip, and hashing only.
Its geometry and symmetry expansion were written before I opened the maintained
`certificate.rs` source.
I subsequently read that file’s admission and domain code, so I make **no clean-room
claim** for this reviewer.
No producer code is imported, copied, or called.
The audit independently decides its exact premises and five poses; it does not decide
the continuum of centres.
Its own implementation, Python runtime, and interpretation of the shared mathematics
remain trusted.

## Findings and Questions

### C1 — Minor (Low): the README gives the wrong control-log filename

Source reference:
`packing/resources/web/wand125-fine-net-lower-bounds-2026-10-16/square-packing/problems/square-lower-bounds/certificates/mixed_n108_L1062/README.md:17`.

The list names `check2/control.jsonl.gz`. The actual file is
`check2/control-197_200.jsonl.gz`, also named in `files-sha256.json:5` and retained in
the release packet. A reader following the README’s filename cannot locate that file at
the advertised path.
The manifest supplies the right name and digest.

**Impact:** discoverability only.
The candidate, receipt, mathematics, and correct control log are present; this does not
block acceptance of the mathematical argument.

**Fix:** correct the filename in the author’s living README. Preserve this repository’s
archived copy as source evidence and record the correction beside the review.
**Question for the author:** can the bundle inventory name
`check2/control-197_200.jsonl.gz` so it agrees with the manifest?

There are no additional suggestions requiring disposition.
For future reporting, the author and records maintainer should keep the phrase “second
system” tied to independence from the search, and identify the shared verifier when
comparing `check2` with this repository’s native run.
This is a scope clarification, not a second defect.

## False Positives Checked

- Rectangle overlap and stabilizer duplicates preserve total mass when all eight images
  carry their proper shares.
- The final node being beyond $\pi/4$ is allowed; the final bin still meets the folded
  orientation range.
- Reflection is valid for the per-square orientation argument, while quarter turns
  justify the fixed-angle centre reduction.
- Different compressed and decompressed input digests identify the same certificate
  through the recorded byte check.
- A tiny positive certified margin is not, by itself, a floating-point defect:
  acceptance relies on certified enclosures, not an ordinary approximate score.
- The 99/100 and 197/200 control factors are different declared experiments.
  A refusal under either factor does not prove the original universal coverage premise.

## Evidence and CI

The new program, its execution instructions and read log, and its receipt are retained
under
[review-max](../../../packing/resources/web/wand125-fine-net-lower-bounds-2026-10-16/review-max/README.md).
The command with the repository’s Python 3.14.7 interpreter exited 0 with
`EXACT_PREMISES_AND_FIVE_POSES_PASS`. Ruff format/check and BasedPyright on that file
passed with no findings.
The first development runs failed on my receipt-shape assumptions (the axis uses
`vertices`, and the control array is `sweep.refused`); they produced no passing receipt
and were corrected before the retained run.

At the reviewed commit, the GitHub checks API reported failed
[`packing-required`](https://github.com/jlevy/squares/actions/runs/39058628244/job/117474630168),
[`pages-required`](https://github.com/jlevy/squares/actions/runs/39058628178/job/117473081903),
and
[`overview`](https://github.com/jlevy/squares/actions/runs/39058628178/job/117472167473).
Those are merge gates handled by the coordinating records and page lanes.
This bounded mathematical verdict is not a merge-ready verdict.

## Independence Sequence

The preceding derivation, findings, and computational verdict were written to this file
before reading any earlier review of this n = 108 result or any PR discussion.
The review began from a separate prompt and a separate worktree pinned to the stated
head. Prior n = 108 review content seen before writing these findings: **none**. The
first findings draft was saved at **2026-10-18T10:25:13Z**. Only after that save did I
read the earlier formal reviews and Review B’s retained note.
The following comparison was then appended; the audit code, output, and mathematical
findings were not revised to agree with the earlier review.

## Comparison With Earlier Reviews

[Review B](https://github.com/jlevy/squares/pull/671#pullrequestreview-5562495021)
accepts the same mathematical route and reports no findings.
Its derivation agrees with mine on the mass deficit, D4 multiplicity, shrink inequality,
per-bin centre domains, and the distinction between a fresh execution and an independent
verifier implementation.
I found no mathematical disagreement.

The checks have different scope.
Review B independently recomputes all 201 retained native 99/100 control captures, and
also checks selected least-leaf and near-threshold poses.
My audit recomputes four of those native control captures and the source’s axis 197/200
pose, spells out the last-bin polynomial check, and reports the README filename defect
C1. Neither reviewer freshly runs the full native coverage search.
The independently written programs both use exact polygon clipping; the shared method is
disclosed, and I did not read or reuse Review B’s audit code.

[Review A](https://github.com/jlevy/squares/pull/671#pullrequestreview-5562187918)
addresses retention, release metadata, rendering, fixtures, manifest atomicity, and
replay wording. Those engineering findings belong to the coordinating lanes.
This mathematical review neither duplicates nor disposes of them.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
