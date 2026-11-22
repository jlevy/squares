# Independent review of the later degree-seven 228-square packing

The independent checker accepts the exact degree-seven certificate supplied in the
[20 November follow-up](https://github.com/jlevy/squares/issues/1038#issuecomment-7046716722).
It proves finite feasibility of 228 unit squares in a closed square of side
(15+t), where the submission specifies (t) by an isolating interval and the
polynomial with high-first coefficients (1,11,-153,-1433,-1250,4706,-6839,2861).
A Rabin test establishes irreducibility modulo 3. An exact rational Sturm
sequence counts one root in the submitted interval.

All 228 units and 3,648 corner-wall inequalities passed. The checker evaluated
all four axes for each of the 25,878 unordered pairs. Exactly 66 wall
inequalities and 302 best separating-axis gaps were equalities. All eleven
predeclared controls behaved as expected. A separate roster audit matched each
receipt pair to the full unordered roster and bound the original source digest.

The author wrote the quotient arithmetic and separation predicates separately
from the maintained and contributor implementations. The frozen preparation
discloses exposure to the earlier independent rational implementation, the
maintained verdict and field metadata, and a small portion of the original
encoding. The full-corpus successor preserves all 32 arithmetic, geometry and
control definitions from the successful sample. Only the declared coverage
driver and reporting changed. The coordinator verified both digests and executed
the unchanged frozen successor on the original mathematical input.

The full run took 40.49 seconds in the checker and 41.05 seconds under
supervision. The guard observed pressure 1 and a maximum sampled process-tree
footprint of 0.14 GiB. Both processes exited zero. No root-interval refinement
was needed after the initial isolation.

[Frozen plan](frozen-plan.md), [freeze record](freeze.json), [frozen checker](checker.py.txt),
[complete compressed receipt](full-1.receipt.json.gz),
[admission audit](full-1-admission.json), [sample-to-full delta](successor-delta-audit.json)

The result supports exact finite feasibility. The stronger side belongs to the
same dated contribution as the independently verified rational witness.
Registration, credit and the published drawing will use the separate project
intake records.

## Compressed Files

| File | Origin | Git blob of original bytes | SHA-256 of original bytes |
| --- | --- | --- | --- |
| `full-1.receipt.json.gz` | receipt | `e5b5d2ef0db7d735499b77cbb0f0033535e8c967` | `85aec431826e5b1fb7717b9e2a92d1e2450c4ca8a3b59f7918d9fb52b3df6158` |

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
