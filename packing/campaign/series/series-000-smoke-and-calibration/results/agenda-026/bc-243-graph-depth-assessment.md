# BC-243: A Complete Graph Bound Before More Geometry

Session093 selects a bounded source-free weighted-graph certificate component under
`think-yzzi`, following read-only assessment `think-m8x7`. The assessment ran from
07:50:34 to08:03:20UTC on September7, using766seconds. No source control, target,
benchmark or new scientific input was evaluated.

This changes the sufficient completeness argument; it is not a fourth run of the
unchanged arrangement verifier.
It does not establish H099 or a packing bound.
The coordinator independently checked the implications below before funding the generic
component. Geometry, source binding and any scientific invocation need separate review
and a prospective allocation.

## The Mathematical Contract

For finitely many closed squares S_i with nonnegative weights w_i, write K_i=int(S_i).
The finite boundary union has area zero.
A nonempty intersection of these open interiors contains a small open disk, so

$$
\operatorname*{ess\,sup}_x\sum_i w_i\mathbf1_{S_i}(x)
=\max_{\bigcap_{i\in I}K_i\ne\varnothing}\sum_{i\in I}w_i.
$$

An essential supremum ignores exceptions confined to a set of area zero.
Closed intersections consisting only of an edge or point therefore do not raise this
depth. The empty set contributes weight zero.

Construct a graph containing every pair whose interiors intersect.
An edge means “possibly compatible”; retain every unclassified pair as an edge.
Every set with a common interior is then a clique, meaning a vertex set with every pair
joined. Consequently an independently verified maximum weighted clique bound at most one
proves complete almost-everywhere depth at most one.
Nonedges require exact geometric evidence; an omitted edge cannot be justified by a
failed or incomplete intersection test.

The graph bound is sufficient, not necessary.
Pairwise intersection need not give a common intersection.
An overweight graph clique is unresolved geometrically, not a positive-area violation.
Deleting an infeasible maximal clique and all its subsets is unsound: one of those
subsets may have a feasible overweight common interior.

A finite include/exclude proof tree can cover every candidate clique.
On inclusion of vertex v, restrict the remaining vertices to its neighbors and add w_v;
on exclusion, remove v without adding weight.
Every branch must be represented or discharged by a sound upper bound.
A proper coloring partitions remaining vertices into independent sets, so a clique takes
at most one member of each color; the sum of each color’s largest weight is an upper
bound. A reader must reconstruct the branch state, verify the whole coloring and reject
missing branches. Node exhaustion is unresolved.

## What Not to Build Yet

Selected higher-order conflicts could strengthen this later, but are not funded now.
For inward strict half-planes a_j x+b_j y+c_j>0, exact nonnegative multipliers with
positive total, zero summed normal and nonpositive summed constant certify empty common
interior: summing the strict inequalities would contradict that constant.
Equality is a valid obstruction to interior feasibility, even if the closures touch.
Any future use still needs an exhaustive weighted-subset certificate.
Collecting some triples or rejecting one maximal clique does not supply completeness.

The earlier
[complete-method assessment](bc-254-post-screen-next-discriminator.md#next-step-complete-face-verification-2026-09-06)
rejected another incomplete higher-order filter and selected arrangements.
It did not establish that every complete graph certificate is too costly.
Conversely, three separately reviewed sixty-second uniform-source timeouts in Session090
do not predict the graph method’s runtime.

## Why the Easy Decomposition Stops at Eleven

The uniform D4 average has a direct certificate: each of eight source packings has
pointwise interior depth at most one, and their average does too.
This can certify that baseline without building its full arrangement.

It cannot certify the retained mass56/5 candidate.
If copies of packings containing at most eleven squares dominate its weights with
nonnegative coefficients eta_g, then

$$
56/5=\sum_iw_i\le11\sum_g\eta_g.
$$

A depth-one bound from that decomposition needs sum_g eta_g<=1, a contradiction.
This limitation concerns the decomposition certificate, not the candidate’s actual depth
or all other certificate methods.

## Cost Gate and Control Cases

[Exp115](../../experiments/exp-115-h-105-fixed-candidate-pair-obstruction.md) retains134
exact pair-separation receipts.
With matching source binding, those isolate the four weight-one placements in the
retained candidate. Thirty-two positive-weight vertices remain:496pairs and at
most4,960triples. These are combinatorial counts from retained data, not new target
measurements. Even so, one weight pattern already yields binomial(8,2) times
binomial(16,5)=122,304minimal overweight subsets; blind enumeration is not a justified
plan.

The selected first component gets twenty-five source-free author minutes and a separate
independent reader/review allocation before any source use.
Controls must include:

- Four common-interior squares of weight3/10, overweight although every triple weighs
  below one; a pair/triple weight screen must not certify them.
- Pairwise-compatible graph data without a common geometric interior: no graph clique is
  promoted to a geometric witness.
- A rejected maximal clique with a potentially overweight feasible subclique.
- Boundary-only contacts at the later geometry boundary, and omitted branches or invalid
  color classes at the combinatorial boundary.

The generic graph components and their geometric adapters passed source-free controls
and independent reviews in Session093. The separately authored source-binding command is
under independent review; no scientific source graph has been evaluated.
Even complete H099 success would address the fixed-support density question at the Trump
side, not below-Trump density or a new packing lower bound.

## Prospective Graph Source Controls

This is a changed complete sufficient method, not a retry of the earlier arrangement or
slab controls. Commit this protocol, freeze the independently reviewed engine and pass
records before either source-control invocation.
No candidate follows unless both source controls pass independently.

Use the explicit producer and independent-reader modes of
`packing/devtools/run_full_size_density_graph.py`, always through the parent CLI. Each
call requires `--node-limit 10000` and an explicit process cap.
The parent bounds startup, source reconstruction, checking and output; the worker alarm
also refuses direct-worker overruns.

| Named control | Family | Producer cap | Conditional reader cap |
| --- | --- | --- | --- |
| `trump-original-control-v1` | The eleven original exact squares, each of weight one;55 pairs | 30seconds | 30seconds |
| `trump-uniform-control-v1` | The full deduplicated D4 roster with its accepted mass-eleven uniform weights;1,770 pairs | 60seconds | 60seconds |

Run each producer once, in that order, only from the frozen clean engine.
An actual zero exit and a well-formed packet whose nested adapter status is
`proved_graph_bound` permit one independent reader invocation with the same control name
and `--input` pointing to that packet.
A graph overweight, unresolved packet, malformed result, error or timeout ends this
control sequence without a reader, retry or candidate run.

Reader admission requires actual exit zero, `status=verified_density_bound`,
`bound_proved=true`, mass exactly eleven, complete source identity and containment, and
independent replay of every removed edge and the complete graph upper certificate.
The original control must bind eleven squares and the uniform control sixty.
The low-level family API assumes an already validated `PairFamily`; only the named
worker/CLI routes reconstruct and validate scientific containment themselves.

Retain each producer stdout as `packet.json`, stderr plus external process timing as
`producer.log`, and actual exit.
If admitted, retain reader stdout as `replay.json` and stderr plus timing as
`replay.log`, with actual exit.
Use new original and uniform subdirectories under
`results/agenda-026/graph-source-controls`; never overwrite an existing receipt or infer
a missing reader result.
No source-control launch may begin after09:20UTC in Session093.

These controls test instrument readiness.
They do not establish H099 or remeasure the accepted original packing.
Only after both succeed may a separate committed experiment fund the unchanged exp113
candidate at its own original cap.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
