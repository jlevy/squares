# Completed n68 Fine-Net Certificate: Mathematical Review

2026-10-19. Reviewer: Codex/OpenAI, strongest tier, maximum reasoning
(`tbd-strong-max`). Bead `think-r9eb`, child of `think-haaq`. Workflow: W2 factual
review, using `tbd shortcut review-code review-code-correctness`. Scope: the completed
`mixed_n68_L853` checkpoint only; local review, with no source, registry, or GitHub
change.

**Decision: accept this completed certificate’s mathematics and retained native
execution as support for the claimed $s(68) \ge 853/100$, within the previously reviewed
`sqverify-fast` trust boundary.** No new mathematical blocker was found.
All 201 capture directions verify, and exact recomputation confirms every one of the 197
saved whole-net control refusals, the selected positive point, and the near-threshold
witness. The four scaled-control directions that verify are valid under the maintained
control contract. The missing outer capture exit does not require another capture: the
native exit, full receipt, and subsequent check/control completion are retained and
consistent.

This is a local mathematical decision.
T-205 remains `V0/C0`, with reported evidence `E-wand125-fine-net-n68-853-report`, until
a separate records lane registers and reviews the new evidence.
It accepts no other count, changes no standing bound, and authorizes no use of the
current Mac evidence renderer.

## Exact Candidate and Evidence

The checkpoint is
`/Volumes/spud-ext1/agent-source/squares-fine-net-mac-haaq/first-subset/case-checkpoints/mixed_n68_L853-20261019T124003-1906fda3/`.
The
[audit result](../../../packing/resources/web/wand125-fine-net-lower-bounds-2026-10-16/review-mac/n68-certificate-math/audit-result.json.gz)
records the complete paths, all checkpoint file identities, exact fractions, and all 197
independently recomputed refusal captures.

| Item | Identity |
| --- | --- |
| Candidate | `packing/resources/web/wand125-fine-net-lower-bounds-2026-10-16/release/certificates/mixed_n68_L853/candidate.json.gz` |
| Stored candidate SHA-256 | `cbbf2808db82dc68446c84929436783a3ac9abd66425bff199022bd25d7363cf` |
| Decompressed candidate SHA-256 | `3c5521d6ce47688cc32c900f3e97fd4f0db01aa85b0217a7ed5f3eacfbd2be6a` |
| Capture JSONL gzip SHA-256 | `90a748165d2f821bcd59b8be10ebf06a201e69a41d1f6a51c10256fe10b87345` |
| Control JSON SHA-256 | `22f4310803ca31aea6fa873e18fbb796f49d235bc39e19228b699836061512f6` |
| Execution JSON SHA-256 | `4ec722d6516aba90e23d5c7798e633959f8ccc1b2c5c9c3f1febe5790c3e8c96` |
| Native binary SHA-256 | `e44f27eb8f3375d85c71e085fe7d04667d38f28c589beae267457573be4ae61d` |
| Native source digest | `d97758bbc9639edc70b8bd7dc83106d4e8d1be034bacb3e88f8c539b88091c88` |
| Native build | `release`, `aarch64-apple-darwin`, `rustc 1.98.0 (88d9e12ae 2026-08-18)` |

The candidate is a single complete gzip member: 38,858 stored bytes and 202,022
uncompressed bytes. Its numeric geometry and masses are exact strings; the candidate
contains no floating-point JSON token.
Its stored bytes match the Git object on pinned main
`0ee05f4f3d0863f75c1036757839985e75655677`, and its raw identity matches the retained
acquisition manifest and `receipts/premises-n68.json`. The source’s `e2ab1b5b…`
candidate digest is its semantic JSON digest; it is a different identity from either
file hash above, as `audit_wand125_declared_net.py:450–458` defines.

The active source tree was read at `.worktrees/review-668-math-20261018`, HEAD
`461e20b939c7635e65fcb5491ec39399b2177045`. The audit compared 15 files with pinned
main: the 12 files in `build.rs`’s source-digest rule, the census driver, the maintained
exact audit helper, and this candidate.
All were byte-identical.
Recomputing the crate’s ordered filename/NUL/content/NUL digest and the preserved
executable’s digest gave the identities above.
Scoped `git diff` was empty; tracked status was clean before and after the audit.
The build’s arithmetic qualification remains the separate
[Mac review](../../../docs/project/reviews/review-2026-10-19-fine-net-mac-arithmetic.md).

## Mathematical Implication

The independent exact calculation expanded each listed rectangle into its eight $D_4$
images, assigning each image one eighth of the listed mass and merging coincident
rectangles by adding their rational densities.
Every weight is nonnegative and every positive-weight rectangle lies in $[0,853/100]^2$.
There are 726 source rectangles, 5,796 distinct expanded rectangles, and no points or
segments. The expanded density integrates exactly to the sum of the listed masses.
The admission density bounds also hold.

| Premise | Independently recomputed value |
| --- | --- |
| Total mass $M$ | $6799999/100000 = 68-1/100000$ |
| Core side $B$ | $9977/10000$ |
| Half-angle tangent step $D$ | $83/40000$ |
| Declared indices | $0,\ldots,200$ |
| Last tangent $t_{200}$ | $83/200$ |
| Endpoint polynomial $t_{200}^2+2t_{200}-1$ | $89/40000>0$ |
| Last-bin lower endpoint polynomial | $-4544311/6400000000<0$ |
| Core extent bound $B(1+D)$ | $399908091/400000000<1$ |
| Strict extent margin $1-B(1+D)$ | $91909/400000000$ |
| Stronger tangent bound $B(1+D/(1-D^2/4))$ | $63985225828447/63999931110000<1$ |

For each unit square separately, a $D_4$ reflection can fold its orientation; pulling
the certified core back preserves both its measure and strict containment.

The declared uniform net therefore covers every folded orientation $\varphi\in[0,\pi/4]$
with a node whose half-angle tangent differs by at most $D/2$. For the angular error
$\delta$, $z=\tan(\delta/2)\le D/2$, and the corresponding concentric core’s extent in
the unit square’s axes is $B(1+2z-z^2)/(1+z^2)\le B(1+D)<1$. Each core lies strictly
inside its parent unit square.

For node $r$, put $a_r=\max(0,rD-D/2)$ and $\rho(a)=(1+2a-a^2)/(2(1+a^2))$. A unit
square assigned to that node has its centre in $[\rho(a_r),L-\rho(a_r)]^2$. Quarter-turn
invariance of the density and square reduces this to $[L/2,L-\rho(a_r)]^2$, the admitted
`per-bin` domain. The orientation fold is at $\pi/4$; it is not moved to the last node
beyond $\pi/4$. Every saved refusal and both selected points pass the exact, stricter
quadrant-domain check.

The retained native run certifies capture at least one throughout every such domain,
under the previously reviewed axis sweep and interval branch-and-bound arguments.
If 68 unit squares packed in the container, their strictly interior cores would be
pairwise disjoint, so positivity of the measure would give
$68\le\sum_i\mu(Q_i)\le M=67.99999$, a contradiction.
This is the claimed lower-bound argument; it requires the universal native coverage, not
merely the exact point checks below.
The applicable source arguments are N0–N4, C1 and D in
[`SOUNDNESS.md`](../../../packing/sqverify_fast/SOUNDNESS.md).

## Capture, Controls, and Invariants

The saved JSONL has exactly 201 direction rows followed by one native summary.
Indices are exactly `0..200`, each verdict is `verified`, every threshold is one, every
certified lower bound is at least one, and no fault was injected.
The census and summary agree on every premise, build, direction count, node total and
refusal list. Their node total is 104,110,078; the axis sweep examined 23,941,449
vertices, which equals $4893^2$. Every rotated row has the completed binary-tree
relation `nodes = 2 * leaves - 1`.

The minimum recorded certified bound is $2251799813885651/2251799813685248$,
approximately `1.0000000000889968`, at direction 99. The census’s selected leaf is the
same leaf in that row, at binary64 coordinates
`(6.213950969710545, 5.3963078865770076)`. The reviewer-written exact integrator
recomputes its capture as approximately `1.084025519789846`, with its full rational
value equal to all three saved exact values: the census probe and the control’s crate
and independent values.
The original control also re-verifies direction 99 with the same bound and node count.
A least certified bound need not be the least true centre capture; the difference here
is consistent with conservative bounds over a box.

The `99/100` control has a complete partition of all 201 indices: 197 coverage refusals
and verified directions `[46,47,48,49]`. The summary reports `REFUSED`, native exit 1,
no fault, and the same refusal list.
The independently reconstructed scaled input bytes match its saved mutant digest
`6915644f11ed30f6d3537342ffad7ef2c166530cdf2c718ea4dd51b1bf69545f`. All 197 saved poses
lie in the exact domain; each original capture is at least one, and each scaled capture
is strictly below one and equals the receipt’s exact fraction.
The axis refusal also meets the reviewed lower-bound slack of at most $10^{-9}$. The 196
rotated refusals are `counterexample-candidate` with exact-below-threshold flags; none
is unresolved, non-finite, or an audit error.

The original captures at those poses range approximately from `1.0072762685079342` to
`1.010101010098987`; after scaling they range from `0.9972035058228549` to
`0.9999999999979972`. Those comparisons were made as fractions, including the refusal
only about $2\times10^{-12}$ below one.
The control predicate in `sqverify_fast_census.py:776–794` requires a complete sweep, at
least one valid coverage refusal, and valid coverage refusals for every direction that
did not verify. It does not require all directions to refuse.
The four verified directions therefore expose no defect.
The all-directions-refuse special case in `audit_fine_net_receipt.check_controls` was
not used for the final audit.

The near-threshold factor is `184497317036201/200000000000000`, exactly the driver’s
specified rounded-down factor computed from the selected positive capture.
At that centre it produces capture at most $1-10^{-6}$. Its separate witness at
`(6.069453700708498, 6.069453700708498)` is in-domain and has exact scaled capture
approximately `0.9543436150506317`, equal to both saved fractions.
The original capture at that witness is at least one.
The near run has exit 1 and an exact coverage refusal.
“Near-threshold” describes the selected-centre construction, not the global minimum of
the scaled measure.

## Recovery and Timing

**Accept the recovered capture with its outer exit explicitly unknown.** The driver
obtains the native exit from `os.wait4`, saves all direction rows and their summary,
evaluates the selected exact probe, and records the native exit separately
(`sqverify_fast_census.py:375–482`). Here that exit is zero, the complete saved result
is `VERIFIED`, and the captured completion line gives the matching 201 directions and
104,110,078 nodes. The later maintained `--check` reports
`1 of 1 retained certificates VERIFIED` with exit zero.
The later full control command exits zero and reports the actual 197-of-201 refusal
count.

The recovery source adopts the existing wrapper, checks the completed capture before
advancing, and saves `returncode: null` with `native_returncode: 0`; it does not
synthesize a successful outer exit or rerun the capture.
The retained recovery identity names supervisor 66537 and adopted wrapper 51164. The
reviewed local runner and recovery source copies match the external orchestration copies
byte for byte. This audit invoked neither script and changed no live process.
The checkpoint’s per-command receipts match `execution.json` exactly, and their timing
numbers match the retained `/usr/bin/time -lp` output.
A complete native result and a later exact audit establish the needed computation even
though the original outer process’s exit was not observed.

| Command | Aggregate CPU seconds | Command wall seconds |
| --- | ---: | ---: |
| Capture driver and descendants | 856.53 | 438.00 |
| Maintained check | 0.18 | 0.19 |
| Control driver and descendants | 346.81 | 186.31 |
| Sum | 1203.52 | 624.50 |

The census additionally retains `855.891151` native capture-process CPU seconds from
`wait4`. The `624.50` total is summed command wall time, not the elapsed time between
the case’s initial and final timestamps.
Native per-direction CPU measurements are unavailable on Mac: the direction map is empty
and the native summary’s `-0.0` is preserved with that explicit interpretation.
No per-direction CPU or cross-host speed claim follows.

## Trust Boundary, Findings, and Records Requirements

There are no new Blocker, High, Medium or Low mathematical findings for this case.
The existing Mac review’s **A1 (High)**, false Linux host prose, and **A2 (Medium)**,
unavailable per-direction CPU represented as zero, remain under `think-dazj`. Keep
`--evidence` and `--report` off until the renderer correction is reviewed; keep both the
native timing bytes and the unavailable annotation.
The unknown outer exit and the four verified mutant directions are confirmed benign
under the evidence and predicates above.

Universal coverage still relies on the reviewed Rust algorithm, its outward binary64
arithmetic, compiler, hardware, and truthful retained execution.
The saved summary rows are not a proof-assistant certificate or a second replay of every
search leaf. The final exact audit uses only the standard library and reviewer-written
code, with square-to-rectangle clipping rather than the maintained auditor’s reverse
clipping. It checks points and bindings; it is not another universal verifier.
The first-party soundness and platform reviews were read before this case’s findings, as
were the maintained driver and audit helper.
No claim of clean-room independence is made.
The producer adapted this repository’s crate, so the eventual evidence must state the
shared components with its generator; these point checks do not turn that route into a
wholly independent implementation.
The unlicensed adapted source archive was neither opened nor executed.

Before a rung or published assurance changes, the separate records lane still must:

1. Retain this exact capture, control and execution checkpoint through the project’s
   retention mechanism, preserving the existing candidate and source-author receipts.
   The checkpoint census contains other cases; only the n68 entry belongs to this
   acceptance. Keep unknown outer exit and unavailable CPU semantics intact.
2. Register a mapped mathematical review and this audit’s source, receipts and
   independence record under the stage-4 contract.
   This local `.codex` report supplies the findings; it is not yet that registered
   review.
3. Record the actual Mac target and compiler, the reviewed source and declared-net
   route, complete whole-net controls with 197 refusals and four verified directions,
   and the relationship to the producer.
   Resolve `think-dazj` before using the current evidence/report generator for this run.
4. Run the packet retention check, the relevant census contract test including exact
   saved-refusal checks, and the required records validation at the integration commit.
   Link the accepted review and complete replay evidence to T-205 under the normal rung
   rules; do not infer a new rung from this local report alone.

The design choice is to retain the authentic completed run and its incomplete outer exit
observation, then independently check its mathematical contents.
A duplicate full capture would not recover the missing historical exit and is not needed
for this scoped decision.

## Reproduction and Results

The reusable local audit and exact geometry are
[`audit_checkpoint.py`](../../../packing/resources/web/wand125-fine-net-lower-bounds-2026-10-16/review-mac/n68-certificate-math/audit_checkpoint.py.txt)
and
[`exact_geometry.py`](../../../packing/resources/web/wand125-fine-net-lower-bounds-2026-10-16/review-mac/n68-certificate-math/exact_geometry.py.txt).
The
[environment file](../../../packing/resources/web/wand125-fine-net-lower-bounds-2026-10-16/review-mac/n68-certificate-math/env.sh.txt)
uses the existing primary Python 3.14.7, the complete four-root `PYTHONPATH`, and the
read-only reviewed source tree.
The mounted APFS external volume was writable with 59 GiB free; `TMPDIR`,
`CARGO_TARGET_DIR` and `UV_CACHE_DIR` name this review’s external scratch directories,
bytecode is disabled, and pytest’s failed-only/count-one retention options are set.
No environment, build, optimizer, native replay, or broad test gate was created or run.

From the repository root:

```bash
source .codex/intake-resume-20261019/n68-certificate-math/env.sh
packing/.venv/bin/python3 \
  .codex/intake-resume-20261019/n68-certificate-math/audit_checkpoint.py \
  --tree "$N68_REVIEW_TREE" \
  --checkpoint /Volumes/spud-ext1/agent-source/squares-fine-net-mac-haaq/first-subset/case-checkpoints/mixed_n68_L853-20261019T124003-1906fda3 \
  --binary /Volumes/spud-ext1/agent-source/squares-fine-net-mac-haaq/sqverify-fast \
  --packet wand125-fine-net-lower-bounds-2026-10-16 \
  --certificate mixed_n68_L853 --n 68 --side 853/100 \
  --reference-ref 0ee05f4f3d0863f75c1036757839985e75655677 \
  --seconds 300 \
  --output .codex/intake-resume-20261019/n68-certificate-math/audit-result.json
```

Result: exit 0, `PASS`, 6.063 seconds; all 197 refusals, selected positive and
near-threshold witness exact matches.
The audit rejected three deliberate corruptions: a duplicate capture index, an
overlapping/missing control index, and an altered exact capture fraction.
These operate on in-memory copies.
The
[stdout](../../../packing/resources/web/wand125-fine-net-lower-bounds-2026-10-16/review-mac/n68-certificate-math/audit.stdout.log)
ends in the pass summary;
[stderr](../../../packing/resources/web/wand125-fine-net-lower-bounds-2026-10-16/review-mac/n68-certificate-math/audit.stderr.log)
is empty.

`packing/.venv/bin/python3
.codex/intake-resume-20261019/n68-certificate-math/check_geometry.py --output
.codex/intake-resume-20261019/n68-certificate-math/geometry-sanity.json` exited zero:
[12 analytical area checks passed](../../../packing/resources/web/wand125-fine-net-lower-bounds-2026-10-16/review-mac/n68-certificate-math/geometry-sanity.json),
covering full, half, quarter and zero intersections at three rational rotations.
The
[check’s source](../../../packing/resources/web/wand125-fine-net-lower-bounds-2026-10-16/review-mac/n68-certificate-math/check_geometry.py.txt)
is retained.

The initial diagnostic reused the maintained exact helper and reached all positive and
negative point comparisons, then stopped at a reviewer-script conversion of a rational
timing string with `float()` instead of `float(Fraction(...))`. Its
[source](../../../packing/resources/web/wand125-fine-net-lower-bounds-2026-10-16/review-mac/n68-certificate-math/attempt-1-audit_checkpoint.py.txt),
[stdout](../../../packing/resources/web/wand125-fine-net-lower-bounds-2026-10-16/review-mac/n68-certificate-math/attempt-1.stdout.log)
and
[traceback](../../../packing/resources/web/wand125-fine-net-lower-bounds-2026-10-16/review-mac/n68-certificate-math/attempt-1.stderr.log)
are retained.
The final audit corrects that harness error and uses the separately written
geometry module. The failed diagnostic produced no acceptance receipt.

`tbd prime`, the review shortcuts, child create/start/sync, `git show` byte comparisons,
scoped `git diff`, `git status`, and the two orchestration `cmp` checks completed.
The first sandboxed bead write and external-writability probe failed; authorized calls
succeeded.
There was no code commit, push, GitHub publication, or modification of another
bead’s owner.

## Records Preparation Addendum, 19 October 2026

The records lane retains this earlier local decision as the mapped stage-4 review.
Its accepted computations and findings are unchanged; relative artifact links now name
the retained packet copies.
The verbatim local note is retained under the packet’s `review-mac/notes/` directory.
Historical commands and source comparisons describe the original run, not a rerun
against today’s tree.

The coordinator accepted the current fine-net reporter after the B1/B2 correction at
`e062abfacfef60aa160ccd7b177c5b29eb31c2f8`. Current-packet output retains actual Mac
build facts, unavailable direction CPU, shared verifier components and the distinct
per-case exit/control observations.
The historical no-run prose issue remains separately owned by `think-vxh5`; no
historical evidence was regenerated here.

The prepared records cover only the accepted n68, n84 and n85 checkpoints and preserve
the historical n108 result.
Integration validation, final review and publication remain with the coordinator.
Neither native computation nor exact audit was rerun by this records-preparation pass.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
