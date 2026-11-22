# Minimum Moved Centers for the 305-Square Variants

Exactly nine centers must move to align the specified 36 near-axis squares while keeping
T-336’s exact container side, all other directions fixed, and each coordinate within
$2\times10^{-11}$ of its original value. The minimum holds separately with square 43
kept at its original direction and with square 43 snapped to the axis.

The prior exact geometry replays verify a nine-center witness for each orientation.
This [assembly audit](receipts/minimum-scope-audit-20261121.json.gz) binds both witnesses
to the exact original side, dimensions, directions, and movement limit. It rechecks
all 34 local exclusions. The [independent review](independent-review.md) checked
the relevant corner projections and replayed every exclusion with separate exact
arithmetic. A separate subset dynamic program also gives minimum nine.
Both checks use the retained full-packing feasibility receipts.

Every local cohort drops outside-square constraints. Within the cohort, both coordinates
remain free for every square outside the named fixed group. Restricting a feasible full
packing to the cohort therefore gives a solution of its local model if all centers in
that fixed group stay in place. An exact contradiction shows that at least one center
in each group must move. The fresh finite cover search checked all 17 groups and found
minimum nine, 1,581 minimizers and 10,991 search nodes.

The [first probe](receipts/probe.json.gz) checked 10 exclusions. The
[branching run](receipts/branch-resumed-20261121.json.gz) added 20. The last two cohorts
each appeared in both square-43 variants. Their final exact duals use only mandatory
rows, five in one and six in the other. The [mandatory-row replay](receipts/root-dual-closure-observed-20261121.json)
checks nonnegative multipliers, cancellation of all free coefficients and a strictly
negative weighted right side. The [earlier bounded search](receipts/completion-20261121.json.gz)
still records that its last traversal reached the time cap. The mandatory-row
certificates close both local models directly.

The [subset replay](receipts/verified-subsets-hitting-set-20261121.json) shows that
either of the last two exclusions on its own leaves the 16-group minimum at eight.
The bounded-motion result keeps T-336’s exact numerical upper bound and the same-side
variants. Unrestricted motion and rotation are outside its scope.

## Replay the Assembly

Use the project’s Python 3.14.7 environment and a fresh external scratch directory.
Copy this directory there and give each frozen program its original `.py` suffix.
Decompress `probe.json.gz`, `branch-resumed-20261121.json.gz`, and
`completion-20261121.json.gz` in the copy to restore the frozen input paths.
The original math and retained feasible witnesses stay in the repository. Start the
memory guard before permitting the worker to enter the audit; the audit reads its
sample journal from `N305_GUARD_JOURNAL`. Pass `--repo` the repository root,
`--followup` this packet’s parent source directory in the repository, and `--output`
a fresh scratch file.

```bash
PYTHONPATH="$REPLAY_PACKET:$REPO/packing:$REPO/packing/src" \
  "$PYTHON" -B -m programs.audit_minimum_scope \
  --repo "$REPO" \
  --followup "$REPO/packing/resources/web/de-winter-n305-1052-followup-2026-11-20" \
  --output "$TMPDIR/n305-minimum-replay.json"
```

The [assembly supervision receipt](receipts/minimum-scope-supervision-20261121.json)
records 8.87 seconds, 0.10 GiB peak footprint and memory pressure 1. The launcher path
field is omitted from the supervision reading copies. The deciding receipt files and
program bytes match the observed run.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
