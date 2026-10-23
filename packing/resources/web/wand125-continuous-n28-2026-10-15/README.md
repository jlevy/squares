# Reported Continuous-Pose Lower Bound for n = 28, 15 October

Commit `8530baf` of wand125/square-packing (15 October 2026) adds
`continuous_n28_L5745`, a rectangle measure reported to prove $s(28) > 1149/200 = 5.745$
by a cover at every angle rather than on a net of directions, and reported as decided by
two of the source’s programs.
No issue reports it; the intake sweep of 15 October found it (think-mq0k). The bound
remains unconfirmed here; no standing bound or rating changes.
The records lane of 15 October registered it as T-192 at V0/C0, after T-142, from
[`register-plan.yaml`](register-plan.yaml); T-142 and T-107 keep their claims.

| Item | Value |
| --- | --- |
| Source | [`continuous_n28_L5745`](https://github.com/wand125/square-packing/tree/8530bafb03d48444f30f241fbc1f29f01cd7c96c/problems/square-lower-bounds/certificates/continuous_n28_L5745) |
| Added by | `8530baf`, 2026-10-15T04:13:10Z; the same tree at the head `b57e667` |
| Release asset | `certificates__continuous_n28_L5745.tar.gz` of `square-lower-bounds-v1`, asset id 642628950, 912,977 bytes, SHA-256 `d7249d0d…9ab8` |
| Candidate | 884 positive rectangle rows in D4 orbits, no points, mass $2799999/100000$ on $[0, 573351/100000]^2$; SHA-256 `a2e47a39…cb8d` |
| Parameters | core $B = 499/500$, threshold $\tau = 1$, claim $X = L/B = 1149/200$ exactly |
| Standing bound | T-107’s $1147/200$, both lanes; $+1/100$ |
| Earlier report | T-142’s $2297/400$ (10 October, V0/C0, pending adoption); $+1/400$ |
| Upper bound | $5.82444461667406$ (T-101, T-155); gap about $0.0794$ |

Every closed square of side $B$ in $K = [0, L]^2$, at every centre and every angle, is
reported to capture mass at least 1. Since $28 \cdot 1 - M = 1/100000 > 0$, no 28
squares of side $B$ with disjoint interiors fit in $K$, and scaling by $1/B$ gives the
claim. The angle is covered in the half-angle tangent $t = \tan(\theta/2)$ over
$[\varepsilon, 83/200]$, with $83/200$ past $\tan(\pi/8)$, by outward-rounded interval
branch and bound, and the near-axis band $[0, \varepsilon]$ by an exact check of a
smaller axis-parallel square that every side-$B$ square there contains.
This is T-145’s method, on a new density at a new count.

## The Source’s Two Programs

|  | check1 | check2 |
| --- | --- | --- |
| Program | `sqverify_continuous` v4, wand125’s continuous-angle mode of this repository’s `sqverify-fast` crate | `contpose_check3` v1.2, a driver around Guzhou0806’s T-145 kernels |
| Source digest | `619b3c00…c7f5` (by `build.rs`) | `f3629c29…c86e` (by `VERSION.json`’s rule) |
| Partition | 86 root ranges of $t$ over $[10^{-7}, 83/200]$ | T-145’s 43 slabs over $[10^{-6}, 83/200]$ |
| Near-axis side $A$ | $4989999/5000000$ | $249499501/250000000$ |
| Result | VERIFIED, 1,265,052,068 nodes | VERIFIED, 1,912,948,689 nodes |
| Least certified bound | $1 + 4.7 \times 10^{-12}$ (root 72) | $1 + 2.4 \times 10^{-12}$ (slab 5) |
| Axis patch | least bound 1.00101 | exact minimum $1.0010083703…$ on a 5,789 × 5,789 grid |
| Run | 4,183 s at 10 threads; 38,949 CPU-s over the roots | 8,506 s at 16 workers; 109,538 CPU-s over the slabs |
| Second run | before publication, 3,714 s at 30 threads, same node count | none reported |
| Control (every mass × 985/1000) | REFUSED at all 86 roots and the axis patch | REFUSED at the axis |

The source says the two programs share no code.
Read against this record, check1 keeps this repository’s `interval.rs`, `exact.rs`,
`axis.rs`, `oracle.rs` and `rotated.rs` byte for byte (think-xzob), and its author read
Guzhou0806’s kernel before writing it; check2 runs that kernel with its caps raised.
Both follow T-145’s method.
check2’s `SPEC.md` is headed as a specification for Codex and forbids its implementer to
read check1 or `sqverify_fast`.

## What Is Retained

[`devtools.acquire_source`](../../../devtools/acquire_source.py) wrote the packet from
its [declaration](acquisition/declaration.json): the
[acquisition record](acquisition/sources.json) and the
[subtree manifest](acquisition/upstream-subtree.sha256) give the size and SHA-256 of all
21 files in scope, and `--check` re-derives them.
Nineteen are retained byte for byte under
[`square-packing/`](square-packing/problems/square-lower-bounds/certificates/continuous_n28_L5745/):
the directory’s documents, both summaries of check1, check2’s manifest, and check2’s
source, its driver, generator and two kernels with `identity.h`. Two are pinned by
digest only: the enclosing licence, byte-identical to the FN-1 packet’s copy, and the
kernels’ licence, byte-identical to the T-145 packet’s copy of Guzhou0806’s.

The release asset is not retained.
It holds the candidate, the control, check1’s run logs and source archive
`sqverify_continuous_v4.tgz`, check2’s receipts and both kernel inputs, the sealed inner
bundle and the pre-publication receipt.
It stays with its author, pinned here by size and digest, and the
[premises receipt](receipts/premises-n28.json) inventories every member.

## What Was Checked

**Custody.** The asset’s size and SHA-256 equal the release API’s digest, the release’s
`SHA256SUMS` (line 446) and the source’s `ASSET.json`. The sealed inner bundle,
`n28-L5.745-continuous-bundle.tar.gz`, holds 30 files and matches all 29 entries of
`files-sha256.json`. Its README is the edition before the pinned one added two sections,
the first program’s check command and the pre-publication run; every other document is
the pinned one byte for byte.
The source archive of check1 is byte for byte `tools/sqverify_continuous` at `d4a1981`,
all 28 files by Git blob, the v4 that the 12 October read recorded.

**Exact premises, with no program of the source run.**
[`devtools.continuous_pose_followup`](../../../devtools/continuous_pose_followup.py)
`premises` ([receipt](receipts/premises-n28.json), 1.3 s) holds every check below, and
returns `EXACT_PREMISES_HOLD`:

- the candidate: 884 positive rows inside $K$, masses summing to `total_mass`; $X = L/B$
  is the claim; $28 - M = 1/100000$; $L^2 - 2B^2 > 0$; $T^2 + 2T - 1 = 89/40000 > 0$;
  and the control is the candidate with every mass times $985/1000$, row by row;
- check1: its stated premises equal those recomputed here, including $A$ by its own
  rounding rule and the near-axis margin $B - A\,W(10^{-7}) =
  200029979999/500000000000005000000 > 0$; its 86 roots are its default cuts, every one
  verified, each a full binary cover ($\text{nodes} = 2\,\text{leaves} - 1$) with least
  bound at least 1; its summary sums them; and the same log checks hold for the control,
  every root refused;
- check2: both kernel inputs, regenerated here from the candidate with
  `devtools.audit_continuous_pose`’s pose builder and the dominated axis measure at the
  density scale $10^8$ the source’s guards force, have exactly the digests its manifest,
  its receipt and its shipped inputs name, and so do the control’s; its receipt runs
  every slab with T-145’s endpoints, on that input, each verified, a full binary cover
  and at least 1; its axis minimum is exact and at least 1; its build names the pinned
  kernels; and the near-axis margin
  $B - A\,W(10^{-6}) = 1496999501/250000000000250000000 > 0$;
- both source digests, recomputed by the rule each program states.

**check2’s kernels against the reviewed upstream.** The diff of check2’s two kernels
against the retained T-145 copies, `continuous_pose.cpp` `da06206b…` and
`axis_integer_grid.cpp` `f5bc3f60…`, is exactly the one `CHANGES.md` prints: the
rectangle and side caps, the axis grid cap raised from 15,000,000 to 90,000,000
vertices, the axis threshold denominator to $2 \times 10^6$, and an echo of the input’s
digest and the arguments.
No arithmetic changed.
The 33.5 million-vertex axis grid of this certificate is above the reviewed kernel’s
cap, so that kernel refuses it unchanged.

**The source’s own control, run here.** check2’s `check.py`, run from a scratch copy
under `python -I` on the control candidate as `REPRODUCE.md` says, built both kernels to
the very binaries its receipt names (`c028f0e3…`, `3d144a45…`, g++ 13.3.0) and refused
at the axis with every output equal to the source’s control receipt apart from timing.

**A diagnostic sample of both programs.** `continuous_pose_followup sample`
([receipt](receipts/sample-diagnostic-n28.json)) ran one program at a time at one
thread, on a four-core host at load 3.3 to 6.8, from 06:03 to 06:27 UTC on 15 October,
about 20 CPU-minutes in all:

| Run | Program | Result | CPU here (s) | Source (s) |
| --- | --- | --- | --- | --- |
| Roots 0, 1, 2 of check1 | `sqverify_continuous` v4, built here (`31936c4d…`) | verified; nodes, leaves, splits, depth and least bound equal to the source’s log | 87.0 | 70.8 |
| The published control | the same | REFUSED at all 86 roots and the axis patch, 5,478 nodes, as the source’s | 4.8 | 1.4 at 10 threads |
| Mutant, every mass × 9999/10000, root 7 | the same | axis patch held (1.00091); root 7 verified | 185.9 | none |
| Mutant, every mass × 999/1000, root 7 | the same | axis patch held (1.0000087); root 7 stopped at its 200,000,000-node budget, its exact capture at the stopping pose $1.0000089$, not below 1 | 351.5 | none |
| Slabs 0 and 14 | the reviewed T-145 pose kernel `da06206b`, built here from the T-145 packet into its CI binary `69bc9e64…`, on the input regenerated here | verified; nodes, leaves and least bound equal to check2’s receipt | 567.6 | 1,613.8 |
| Axis patch, main and control | check2’s axis kernel, built here (`3d144a45…`) | PROVED and REFUSED, each output equal to check2’s receipts | 4.5 | 4.3 |

Two things follow beyond the agreement.
First, check2’s slabs are T-145’s kernel at work, unchanged: its reviewed binary
reproduces the source’s receipt on the input this repository builds.
Second, the least certified bounds the source prints, $1 + 4.7 \times 10^{-12}$ and
$1 + 2.4 \times 10^{-12}$, are where each search stopped splitting, not the
certificate’s slack: the 9999/10000 mutant passes root 7, and the 999/1000 mutant leaves
a pose there whose exact capture is $1.0000089$, so the slack at that pose is about
$10^{-3}$. Neither mutant is a counted control: the first was not refused, and the
second was stopped by its budget rather than by an exact capture below $1$. The source’s
own control, every mass × 985/1000, fails everywhere: check1 refuses it at the axis
patch and at all 86 roots, each at a legal pose whose exact capture is below $1$ (least
0.98599, each re-evaluated by the
[soundness review of 23 October](../../../../docs/project/reviews/review-2026-10-23-wand125-sqverify-continuous-soundness.md)),
and check2 refuses it at the axis, as its receipt shows.

## The Price of a Complete Replay

The sample prices each route by the larger of two ratios to the source on what it ran,
the program’s own timing and the process CPU here:

| Route | What runs | Ratio | Source CPU (s) | Price here |
| --- | --- | --- | --- | --- |
| A, the producer’s code | `sqverify_continuous` v4, all 86 roots and the axis patch | 1.23 | 38,949 | 13.3 CPU-hours |
| B, the reviewed kernel | `da06206b` on the regenerated input, all 43 slabs; the axis patch by check2’s kernel and by `sqverify-fast`’s exact sweep | 0.42 | 109,538 | 12.7 CPU-hours |

Each is under the owner’s 40 CPU-hour cap for one item and over the 30-minute limit for
a run inside this intake, so neither was run.
The ratios rest on three early roots and two slabs, on a loaded host, and the source’s
slab seconds were taken at 16 workers.
The upper ends are about 16 CPU-hours for route A, the price with a fifth added, and
30.4 for route B, the source’s own CPU over the slabs.
A control whose refusal counts adds a run at a tight root or slab with a mutant that
keeps the axis patch and fails there by an exact capture below 1; its scale is not yet
known, and the 999/1000 mutant shows that a budget stop is what a weak mutant gets.

## Review and Remaining Work

A replay counts toward `C3` only with a review that reads this certificate.
For route A that is the
[soundness review of `sqverify_continuous`’s continuous mode](../../../../docs/project/reviews/review-2026-10-23-wand125-sqverify-continuous-soundness.md)
of 23 October (think-xzob, jlevy/squares#533), which read this certificate and found no
blocking defect; route A’s next step is its 86-root replay with a control whose refusal
counts, think-0arj.
Route B rests on the 10 October review of T-145’s kernel and needs a preparation slice:
a replay command that runs the 43 slabs at two workers and judges them as
`devtools.audit_continuous_pose` does for T-145, and the near-axis patch decided by
`sqverify-fast` at side $249499501/250000000$, since the reviewed axis kernel’s cap
refuses this grid. Either needs an owner budget.
The import’s bead holds the plan and the validation beads hold the commands.

## Sources and Notices

The nearest enclosing notice, `problems/square-lower-bounds/LICENSE`, is MIT, Copyright
2026 wand125, byte-identical to the notice the FN-1 packet retains.
check2’s `kernel/LICENSE` is Guzhou0806’s MIT notice for the reused kernels,
byte-identical to the T-145 packet’s. check1’s archive carries no notice of its own; its
`PROVENANCE.md` gives the crate code as MIT and the copied documentation as this
repository’s CC BY 4.0. The asset stays outside Git, as the fine-net assets do.

The source credits Hiroaki Hosono (GitHub: wand125), with code and formats credited to
Evan Daniel, tokoharu and jlevy/squares, and its site entry of `b57e667` names the first
verifier’s base as “sqverify_fast (Joshua Levy, jlevy/squares)” and the second’s kernel
as Guzhou0806’s. All three commits past `afdcaac` are authored by Hiroaki Hosono and
name Claude Opus 5.5 as co-author.
`problems/square-lower-bounds/README.md` says parts of the work were produced with AI
assistance under human direction.
check2’s `SPEC.md` is a specification written for Codex.

The other two commits past `afdcaac` hold nothing to import: `a070143` notes the tool
versions of the right isosceles n = 15 run’s second checker, a container outside this
record, and `b57e667` lists the result on the source’s site.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
