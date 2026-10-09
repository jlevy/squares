# Fine inward hull proposals

The producer now tries an inward pull of `2^-18` before `2^-12` in both hull compression
and kernel-point proposal.
Each routine retains its own original coarser fallbacks.
This addresses the primitive limitation recorded in
[R9](review-2026-10-05-n17-capture-r9.md) and tracked by `think-juy9`. Exact
convex-combination witnesses and exact half-plane checks still decide which proposed
grid points are accepted; floating-point clipping proposes points.
No checker, admission rule, row policy or capture experiment changes.

## Fixed fixture

The synthetic source hull is the unit square `[1/3, 4/3]^2`, on the producer’s `2^20`
grid, with its four exact axis bounding halfplanes.
The frame side is 2. The single forbidden-region link is `K - Q`, with the fixed
centered square `Q = [-1/4, 1/4]^2`. This fixture was registered before measurement.

For normals `(+x, -x, +y, -y)`, compression, the kernel hull and the link all give the
following exact face recession.
The baseline restores the old first pull through the named constant; the duplicate
`2^-12` entry is immaterial to first-valid compression and deduplicated kernel
candidates.

| Policy | Four face recessions | Maximum |
| --- | --- | --- |
| Original | `[385, 383, 385, 383] / 3145728` | `0.0001223882039` |
| Fine proposal first | `[7, 5, 7, 5] / 3145728` | `0.0000022252401` |

The fine maximum meets the preregistered `1/100000` fixture threshold.
The factor 55 reduction includes grid rounding; it is not a runtime improvement.
An independent exact derivation predicted these four values before the output was read.
The one fixture measurement took 0.3595 s and reported a lifetime process peak of
46,120,960 bytes, under a 512 MiB worker guard and a 150 s owned Job timeout.
Available memory remained above the local 8 GiB floor.

## Regression and reporting boundary

From `packing/`, using the pinned Python 3.14 environment:

```bash
python -m pytest tests/test_hull_kernel_hull_pull.py tests/test_hull_kernel_sequential.py -q -k 'hull_pull or a_pair_closer or declared_closure_must or removed_residual'
python -m pytest tests/test_hull_kernel_sequential.py -q -k endpoint_sub_pattern
```

The first command passed 9 tests, with 14 deselected; the endpoint control passed 1
test, with 16 deselected, and retained its stalled, nonclosing outcome.
The new controls reconstruct non-grid compression through the unchanged checker, refuse
tampered witnesses, retain grid vertices, exercise near-boundary rounding rejection and
coarse fallback, and directly check that every old raw kernel candidate remains in the
new candidate set. Ruff and focused types passed.

The original local measurement receipt mislabeled a comparison of hull-vertex sets as
candidate retention: polygon encoding had removed interior candidates.
Its exact geometric values remain valid.
The derived correction renames these sets as kernel hulls, labels their vertex-set
inclusion as false, and cites the passing raw-candidate control separately.
No geometry was rerun to repair that reporting label; the local driver was corrected to
preserve raw candidates.

## What remains unknown

This establishes smaller face recession on one fixed unit-scale fixture.
R9’s pilot-node residual prediction remains unverified.
Adding kernel candidates does not guarantee monotonic improvement of the complete
producer after its vertex limits and subsequent hull operations.
No capture run, new exclusion, global radius result, or held-certificate admission
follows from this change.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
