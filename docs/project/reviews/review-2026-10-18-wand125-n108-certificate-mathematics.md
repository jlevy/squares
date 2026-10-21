# Mathematical Review of wand125’s n108 Measure Certificate

**Verdict: accepted for n108 on the retained, reviewed sqverify-fast replay route.** The
certificate `mixed_n108_L1062` supports the lower bound $s(108) \ge 531/50 = 10.62$
through the argument below and the retained complete replay.
No blocking mathematical defect was found.
The replay shares components with the producer’s checker; this review establishes no
independent full-verifier confirmation.

This is the certificate-specific mathematical lane of
[stage 4](../../../packing/campaign/result-import.md#stage-4-validate), reviewed on
2026-10-18 by a separately delegated Codex (OpenAI) agent, Astra family, strong tier at
`xhigh` reasoning.
The reviewed [PR #671](https://github.com/jlevy/squares/pull/671) head
is `32d47d3214ec28f2a82b89689cd8bb8f63f98e02`, based on
`804eff369193b698d497a9c06847059eb9de0470`. The claim has the stable evidence ID
`E-wand125-fine-net-n108-1062-report` in the
[result register](../../../packing/frontier/results.yaml) and
[evidence register](../../../packing/frontier/evidence.yaml).
The original review used the Astra system family at `xhigh` reasoning.
This is the provenance of Review B; it was not a maximum-reasoning review.
Integration identifies the claim by its stable evidence ID, because result numbers are
assigned in merge order.

## Scope and Evidence

The review covers one of the 18 certificates registered by #671. At the reviewed head,
n108 is the only retained maintained census: **1 of 14 first-batch cases and 1 of 18
overall**. The other 17 certificates have no mathematical verdict from this review.

The inputs are the retained
[candidate](../../../packing/resources/web/wand125-fine-net-lower-bounds-2026-10-16/release/certificates/mixed_n108_L1062/candidate.json.gz),
[source README](../../../packing/resources/web/wand125-fine-net-lower-bounds-2026-10-16/square-packing/problems/square-lower-bounds/certificates/mixed_n108_L1062/README.md),
[census row](../../../packing/benchmarks/measure-verifier/census-mixed/census.json),
[201-direction log](../../../packing/benchmarks/measure-verifier/census-mixed/wand125-fine-net-lower-bounds-2026-10-16/mixed_n108_L1062.jsonl.gz),
and
[whole-net control receipt](../../../packing/benchmarks/measure-verifier/census-mixed/wand125-fine-net-lower-bounds-2026-10-16/mixed_n108_L1062.control.json).
The candidate’s retained gzip SHA-256 is
`acaf27593b53c3472ab249805f672030e3cbd3323033641b1df1d8460ae8835b`; the census, log and
controls bind to those same bytes.

The review re-derived the geometric implication and independently recomputed all
certificate masses, net premises and 201 control-witness captures using Python exact
fractions and polygon clipping.
That evaluator imports no project code and invokes no native verifier.
It was written after reading the certificate semantics, the maintained admission and
control interfaces, and the published soundness arguments.
It is an independent check of particular captured masses, with the same mathematical
semantics and data as the maintained evaluator.
Its author is this separately prompted Codex review lane; the source’s disclosed AI
assistance does not identify every system family, so authorship overlap is unknown.
The audit copies and imports no producer code.
Because its author read the maintained admission and control code that overlaps the
producer’s checker, the tool does not claim a clean-room implementation.
It is a premise-and-point audit, with no universal coverage decision of its own.

The full native coverage run was **not repeated** in this review.
Its saved results were inspected against the accepted
[declared-net soundness review](review-2026-10-06-sqverify-fast-declared-net-soundness.md#for-the-records-lane),
[net fix check](review-2026-10-06-sqverify-fast-declared-net-fix-check.md), and
[control fix check](review-2026-10-06-sqverify-fast-census-control-fc1-recheck.md#for-the-records-lane).
Those reviews supply the audited interval arithmetic and exhaustive search argument.
Review A, read before this note, covered engineering findings rather than an earlier
mathematical verdict on n108. The native soundness and control reviews above were read
as dependencies before deriving this certificate-specific argument.
The adapted source archive remains pinned by digest only; it was neither fetched nor
opened here.

## From the Certificate to the Bound

Let $K=[0,L]^2$, with $L=531/50$. For each of the 823 source rectangles $R_j$, let $w_j$
be its recorded rational mass.
The certificate defines the nonnegative density

$$
g(x)=\sum_j\frac{w_j}{8|R_j|}\sum_{S\in D_4}\mathbf{1}_{S(R_j)}(x).
$$

Every positive-mass rectangle is nondegenerate and inside $K$. The eight container
symmetries preserve area, so the integral is

$$
M=\int_K g=\sum_j w_j=\frac{10799999}{100000}
=108-\frac{1}{100000}<108.
$$

Repeated images add their densities; they do not discard mass.
The independent expansion yields 6,524 distinct rectangles, whose integrals sum to the
same exact $M$. There are no points, segments, scaling factor or competing net metadata.
The declared core side is $B=9977/10000$, with half-angle nodes $t_r=rD$, $D=83/40000$,
$0\le r\le200$.

**Orientation and strict containment.** A square’s orientation is defined modulo
$\pi/2$. Using a container reflection when needed, its capture question reduces to an
angle $\varphi\in[0,\pi/4]$; the inverse reflection returns the chosen core to the
original square and preserves its mass under $g$. The endpoint $t_{200}=83/200$
satisfies $t_{200}^2+2t_{200}-1=89/40000>0$, so it exceeds $\tan(\pi/8)$. Every relevant
half-angle tangent $u$ has a node with $|u-t_r|\le D/2$. For the angle difference
$\delta$,

$$
z=\tan(\delta/2)=\frac{|u-t_r|}{1+ut_r}\le D/2,
\qquad
B(\cos\delta+\sin\delta)
=B\frac{1+2z-z^2}{1+z^2}\le B(1+D)<1.
$$

Here $B(1+D)=399908091/400000000$, with strict margin $91909/400000000$. Thus the closed
core lies inside the unit square’s open interior.
The additional admission inequality also holds:
$B(1+D/(1-D^2/4))=63985225828447/63999931110000<1$.

**Admissible centres.** Put $a_r=\max(0,t_r-D/2)$ and $\rho(a)=(1+2a-a^2)/(2(1+a^2))$.
For a folded square assigned to node $r$, $u\ge a_r$ and $\rho$ increases up to
$\tan(\pi/8)$. Its centre therefore lies in $[\rho(a_r),L-\rho(a_r)]^2$. The last bin’s
lower endpoint is also below $\tan(\pi/8)$. Quarter turns, which preserve both the
square at its fixed net orientation and the D4-invariant density, reduce this domain to
$[L/2,L-\rho(a_r)]^2$. No reflection of a centre alone is needed.
The maintained verifier checks an outward-rounded superset of that quadrant.

**Coverage and counting.** The complete native receipt records capture at least one
throughout that domain at each of the 201 directions, using the reviewed axis sweep and
interval branch-and-bound implementation.
Each packed unit square would therefore contain a closed core of mass at least one.
Their open interiors are disjoint, and strict containment makes their closed cores
pairwise disjoint. Nonnegativity gives

$$
108\le\sum_{i=1}^{108}\int_{Q_i}g\le\int_Kg=M<108,
$$

a contradiction. This proves the claimed lower-bound implication conditional on the
maintained verifier’s reviewed implementation, arithmetic environment and recorded
complete run. It makes no claim of optimality or of a new certificate technique.

## Checks Performed

All checks used CPython 3.14.7 and external scratch.
The retained [exact audit tool](../../../packing/devtools/audit_fine_net_receipt.py)
passed in 15.57 seconds, with a 300-second cooperative time budget checked during point
evaluation. Its [focused tests](../../../packing/tests/test_audit_fine_net_receipt.py)
exercise analytic areas, D4 multiplicities, binary64 coordinate semantics, altered
captures, missing or duplicate directions, invalid premises, identity mismatches, both
refusal routes with their required evidence, and failure under optimized Python: **48
passed in 0.34 seconds**. Ruff and BasedPyright reported no findings for the two new
files. The invocation appears below.

| Obligation | Independent result |
| --- | --- |
| Exact count, side and mass | $n=108$, $L=531/50$, all 823 masses nonnegative; exact total $10799999/100000$ |
| D4 expansion and density bounds | 6,524 distinct rectangles; integrated mass preserved; eight times the largest source-row density is about 2,408,874.62, below $2^{32}$; every merged density below $2^{96}$ |
| Net admission | All exact N0 premises hold; 201 nodes, endpoint $83/200$, $0<B<1$, nonempty domains and both strict shrink inequalities |
| Complete receipt | Exactly indices 0 through 200, each once and `verified`; threshold 1; summary `VERIFIED`; census exit 0; no refused direction or injected fault |
| Source identity | Recomputed `build.rs`’s digest over the maintained crate: `d97758bbc9639edc70b8bd7dc83106d4e8d1be034bacb3e88f8c539b88091c88`, the source accepted by the declared-net review; receipt profile `release`, Rust 1.98.0 |
| 99/100 controls | All 201 directions have coverage refusals; every pose is in the exact reduced centre domain; every captured mutant mass independently equals its saved exact fraction and is below 1; every corresponding original capture is at least 1 |
| Least-bound leaf | At index 157, independently evaluated capture exactly matches the census and control fractions, approximately 1.0475325246573444 |
| Near-threshold control | Factor `95462334243713/100000000000000`; selected-centre capture below 1; refusal witness in domain, independently matching exact capture approximately 0.9917532140279091 |
| Maintained regression checks | The two n108 instances of `test_each_control_refuses_both_mutants_where_the_original_verifies` and `test_each_scaled_sweep_refuses_its_mutant_somewhere_with_an_exact_witness`: **2 passed in 17.57 s** |

The pytest invocation used `-c /dev/null` to select only the exported test and produced
one harmless cache-location warning for `/dev/.pytest_cache`; neither test was skipped.
Future invocations should set `-o cache_dir="$TMPDIR/pytest-cache"`.

The native log records 136,113,602 branch-and-bound nodes and 30,140,100 axis vertices.
Its least certified lower bound is `1.0000000001765084`; its census row records
2,086.786 CPU seconds and 1,859.046 wall seconds.
These are **retained run measurements**, not times or search work repeated by this
reviewer. The independently evaluated original masses at the 201 mutant witnesses range
from approximately 1.0040111146586708 to 1.010101010099135. Point evaluations do not
establish coverage between those witnesses.

The least-bound leaf’s actual centre capture being about 1.0475, while its certified box
bound is near one, is not a contradiction: the latter bounds a whole box.
Likewise, the near-threshold factor is chosen from that centre’s capture and is not
required to equal 99/100.

## Trust Boundaries and Disposition

The complete coverage decision belongs to `V-sqverify-fast` at the reviewed source
identity above. This review relies on the prior soundness audit of its conservative
floating-point bounds and exact refusal checks; it does not re-prove every native
routine or audit a new compiler build.
The saved build identity, candidate identity, complete direction set and returned
premises agree. As with the existing census route, the log is evidence of execution of
the trusted verifier, rather than a separately checkable full search-tree certificate.

The producer’s adapted checker derives from this repository’s crate.
Its reported runs and the maintained replay therefore share components.
The producer’s 32-direction 197/200 control remains sampled, and neither its claim of
independence nor the separate point evaluator in this review changes the relationship of
the complete coverage implementations.
Use **re-implemented sharing the producer’s components** for this confirmation.

There are **no new mathematical findings** in this bounded n108 review.
The existing
[Review A](https://github.com/jlevy/squares/pull/671#pullrequestreview-5562187918)
engineering findings remain outside this verdict.
In particular, A6 already tracks the stale statement that n108 has no completed replay;
`think-5nvt` owns that correction and the publication gates.
`think-8iky` owns A1/A5’s retention safety fixes.

`think-f40c` owns the stage-4 integration: map this note, list it as the accepted review
of the n108 claim, add the replay evidence and `external_review` link, then update the
claim, notes, next rung, activity and case lane together under
[the stage-4 exit](../../../packing/campaign/result-import.md#stage-4-validate).
This note changes no registry field or rung by itself.
At the reviewed head the record remains V0/C0 until that integration is made.
The other 17 certificates still need their own complete replay receipts and mapped
mathematical reviews.

The draft **S3 significance score for n108 is confirmed**: the reviewed record’s
reported lower lane is approximately 10.484093855851, below 10.62, and this is an
improvement using an existing certificate kind and net, without an optimality or new
method claim. This assessment applies only to n108.

## Original Review B Invocation

The invocation below preserves the review’s original run.
For the current tool, use the command in the dated engineering correction below.

The retained tool accepts an evidence-tree path, packet, certificate, claimed count and
side, and the source identity accepted by the existing native soundness review.
It reads only the candidate, receipts and maintained crate source; it neither imports
project modules nor executes the verifier.
From `packing/` in a checkout containing the tool:

```bash
uv run --frozen --group dev python -m devtools.audit_fine_net_receipt \
  --root /path/to/evidence-tree \
  --packet wand125-fine-net-lower-bounds-2026-10-16 \
  --certificate mixed_n108_L1062 --n 108 --side 531/50 \
  --reviewed-source-sha256 d97758bbc9639edc70b8bd7dc83106d4e8d1be034bacb3e88f8c539b88091c88
```

Use `..` for the evidence-tree path when the checkout retains the reviewed data and
crate. This review ran the tool against an export of the reviewed PR head, with the
project’s existing Python 3.14.7 environment.
The emitted JSON returned `PASS`, exact mass `10799999/100000`, gap `1/100000`, 6,524
expanded rectangles and 201 independent refusal-point comparisons.
The exact shrink, endpoint and capture results are recorded in the table above.
JSON numeric centre coordinates are interpreted as the exact values of their binary64
parses, as in the retained control writer; rational strings are interpreted literally.

The tool intentionally handles only the rectangle-only declared-net shape and complete
all-direction refusal receipt used here.
A time-budget failure, unsupported input or mismatched receipt returns a nonzero exit.
The checks remain active under `python -O`. Its `PASS` confirms these premises and point
checks; it is not a new full verifier and does not establish coverage between points.
Run its focused tests from `packing/` with:

```bash
uv run --frozen --group dev pytest -q tests/test_audit_fine_net_receipt.py \
  -o cache_dir="$TMPDIR/pytest-cache" \
  -o tmp_path_retention_policy=failed -o tmp_path_retention_count=1
```

## Engineering Correction, 18 October 2026

The original invocation and source-digest comparison above record what Review B ran.
The integration push gate later identified that acceptance condition as an OR-16
violation: a saved-point audit must not refuse because this repository’s current
verifier source changed.
The current tool removes the source reader and `--reviewed-source-sha256` argument,
without substituting a Git-revision gate.
The formal Review B verdict remains pinned to its original reviewed head; this
engineering correction does not widen it.

The audit still binds the downloaded candidate bytes to the census, complete direction
log and control inputs, joins the generated binary identity across census and controls,
and requires their complete historical build objects to agree.
The output field `recorded_native_source_sha256` reports the build receipt’s historical
metadata; it does not check the current crate.
The reviewed implementation and revision remain identified in the retained mathematical
and soundness reviews.
No native replay was rerun and the mathematical result’s assurance is unchanged.

Current reproduction, from `packing/`:

```bash
uv run --frozen --group dev python -m devtools.audit_fine_net_receipt \
  --root .. --packet wand125-fine-net-lower-bounds-2026-10-16 \
  --certificate mixed_n108_L1062 --n 108 --side 531/50
```

The refreshed `review/n108-exact-audit.json` reports this engineering run.
Its historical pre-correction version remains in Git.
Focused controls also exercise an absent current crate, an unrelated edited crate, and
mismatched historical build objects.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
