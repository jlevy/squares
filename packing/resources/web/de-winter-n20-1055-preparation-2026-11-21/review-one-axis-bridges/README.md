# Independent local bridge review for the one-axis case

The independent checker excludes all 3,488 positive-cost local bridge profiles for
`0 < tan(theta/2) <= 1/24`. It checks every one of their 15,696 normal choices by exact
rational polynomial bounds, with 83 distinct bound polynomials.
All twelve predeclared controls pass.
This completes the local bridge obligation. The separate
[sign and symmetry census](../review-one-axis-sign-census/README.md) now completes
that finite roster; general-path and graph coverage remain open.

The complete roster consists of 32 rank profiles and 112 sign profiles, or 3,584
combinations. There are 992 exclusions without an aligned tile on the chain and 2,496
with one. The remaining 96 zero-cost profiles are undecided here, not asserted feasible.
The receipt retains every profile and normal choice, with a canonical roster digest,
exact polynomials and Bernstein coefficients.
It separately proves the favorable mixed-diagonal prerequisite `1 - 5d > Ht` throughout
the closed interval `[0,1/24]`.

The geometric implication assumes a five-tile chain with four forward separating-axis
relations, one transverse rank step of plus or minus one, the near-grid rank intervals,
and at most one aligned tile on the chain.
Multiplication by `2(1-t²)(1+t²)² > 0` converts its physical span bound to a
degree-at-most-six polynomial.
Nonnegative Bernstein coefficients prove span at least five.
The scalar bounds include `t=0`; the global chain reduction here is for positive angle.
The fully aligned endpoint is handled by grid counting.

The reviewer had read the source proof and path implementation.
The checker independently enumerates the roster, maximizes rank error over all 32 box
vertices, reconstructs polynomials from the physical formula by rational interpolation,
and checks Bernstein coefficients.
It imports no contributor program.
This is an independent implementation with disclosed exposure.

## Evidence and reproduction

The [source packet](../README.md) records the exact attachment, attribution and license
scope. The immutable [specification](bridge-spec.json) binds its statement and
path-formula members.
The [frozen plan](frozen-plan.md), [freeze](freeze.json), [checker](checker.py.txt), and
[complete receipt](bridge-verification.json.gz) retain the predeclared method and
completed result.

The freeze’s prepared-only status describes the moment before execution.
The checker bytes are retained under `checker.py.txt`; their original name was
`check_one_axis_bridges.py`. The prior-bank path inside the frozen input and the frozen
plan’s sibling link describe the original external evidence layout.
They are historical references, not execution dependencies.
The accepted [576-certificate bank](../review-one-axis-bank/README.md) is a separate
obligation.

With Python 3.14 and an external supervisor, from this directory:

```bash
"$PYTHON" -I -B checker.py.txt --spec bridge-spec.json \
  --output "$OUT/bridge-verification.json"
```

The output must be a new file.
Use one worker, a 60-second wall ceiling, 0.25 GiB sampled process-tree cost ceiling,
and stop at memory pressure level 2. Use external scratch/cache directories.

The completed checker took 0.727 seconds and measured 38,502,400 bytes peak RSS (36.7
MiB). The supervised worker took 1.792 seconds; worker and guard both exited zero.
The [supervisor result](execution.run.json), [preflight](execution.preflight.json) and
[guard journal](execution.jsonl) are retained separately from the mathematical receipt.
Peak RSS comes from worker process accounting, not a claim that the short job’s peak was
caught in a periodic guard sample.

## Remaining coverage

The standalone source replay for `--Q 24 --exact-paths` uses general five-tile path
clauses, including chains with zero or multiple transverse jumps.
Those clauses are not established by this single-jump bridge check.
The separate sign/vacancy and D4 census now checks all 120 vacancy permutations
and twenty aligned positions, retaining 29,368 assignments in 3,671 orbits.
It uses only the paired-bridge conditions, not general-path clauses.

General-path soundness must still be checked before using those clauses to prune
a graph enumeration. Complete separation-graph enumeration, rule extraction and
graph-to-bank coverage remain open. The source’s 273,584 graphs and 566 used
certificates remain producer reports.

No unrestricted lower bound, angular-diversity theorem, registry value or selected
drawing is accepted by this review.

## Compressed Files

| Stored path | Origin | Git blob of original bytes | SHA-256 of original bytes |
| --- | --- | --- | --- |
| `bridge-verification.json.gz` | receipt | `69f62be84b71b713500296344d8a6f8c629d8ccc` | `a8b48b5cff9b0b101174e3eb513bb3ed502c05bbfb825e1f8b376fb0c017d286` |

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
