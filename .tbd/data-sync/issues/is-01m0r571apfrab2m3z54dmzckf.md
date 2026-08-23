---
type: is
id: is-01m0r571apfrab2m3z54dmzckf
title: "Reconcile PR #14 with the codex review branch: colliding D-numbers, and regenerate the golden"
kind: task
status: closed
priority: 0
version: 4
spec_path: explorations/packing/docs/project/specs/active/plan-2026-08-23-overnight-cartography-run.md
labels:
  - focus-process
dependencies: []
parent_id: is-01m0pw7redm194km37gpb3cvmf
created_at: 2026-08-23T20:32:55.125Z
updated_at: 2026-08-23T21:32:17.426Z
closed_at: 2026-08-23T21:32:17.425Z
close_reason: "Resolved on the merged-main review stack: PR #14 source is an ancestor of this branch; colliding review defects were renumbered D-036/D-037; the source-built golden was regenerated and reviewed under corrected convergence semantics; strict/deep and later post-merge gates passed. Continuing golden-policy work is tracked separately as D-059 on think-zt29."
---
Recorded 2026-08-23 20:35 from the PR #14 check-in, so it survives whether or not anyone reads the PR body.

origin/codex/pr14-square-packing-review has REBASED onto c412b8c, so it now carries this branch's work up to that commit plus two of its own (a2e0b18 review, 889a3ac fix). Head at time of writing: 889a3ac. This branch has since added f9f119a, which that branch does not have.

1. COLLIDING DEFECT IDS. Both branches independently allocated D-034 and D-035, with count: 35 on each. They are four different defects:

   ours   D-034 outstanding tooling  soundness   basin identity ill-posed for non-rigid optima (flat basins)
   ours   D-035 outstanding tooling  robustness  interrupted negctl leaves its sabotage in the tree
   theirs D-034 fixed       quench   validity    a timed-out free sweep reported as a convergence certificate
   theirs D-035 fixed       tooling  bookkeeping the atlas checker counted its own synthetic re-offers as proposals

   D-032 and D-033 are the SAME entry on both branches -- they took ours in the rebase -- so only 034 and 035 collide.

   Whoever merges second renumbers, which is this repo's existing convention (see commit 0abd578, "renumber the colliding defect"). PR #14 is landing first, so THEIRS renumber to D-036 and D-037. Note our two are referenced by ID from SYNOPSIS.md, the overnight plan spec, the research doc, campaign/ideas.md, X-001, and beads think-1s0h and think-97pp; the negative control in tools/controls.yaml also anchors on the literal string "count: 35", so whichever way the renumber goes, that anchor has to move with it or negctl fails by name.

2. THEIR D-034 INVALIDATES OUR COMMITTED CONVERGENCE NUMBERS, and this is the part that is easy to miss.

   `_free_sweep` stopped iterating when its deadline expired and returned the same tuple it returns after checking every angle, so `quench_bracket` could label an incomplete pass converged=True with reason "free pass clean". Their fix raises out-of-time and converts it to converged=False with an explicit budget reason.

   Everything on this branch that counts convergence was measured BEFORE that fix and may therefore be overstated:
     - golden/basin-maps.yaml: the per-case `converged` totals AND the new per-basin `converged_frequency` field
     - the D-030 ablation table (8/8 converged, 6/6 at shrink 0.1)
     - the atlas convergence guard's threshold, which refuses a census where most quenches did not converge

   ACTION after the merge: regenerate the golden with `uv run python tools/golden_basins.py --update` under their fix and diff. If convergence counts drop, the D-030 ablation should be re-run too before its numbers are quoted again. Do NOT simply accept the regenerated file -- the point of the diff is to learn how much the old numbers were inflated.

3. Their D-034 does NOT explain our D-034. Ours is a five-dimensional optimal family at n = 5 whose two members have identical contact certificates and identical sides; a convergence-reporting bug cannot produce that. Both are real and both need to land.

## Notes

2026-08-23 20:38. PR #14 MERGED as 8926a7c. main now carries D-001..D-035 with count: 35, so the collision described above is live from this moment: the codex branch's own D-034 and D-035 now sit against main's different D-034 and D-035.

CORRECTION to the risk assessment, in the reassuring direction. The collision cannot land silently. tools/validate_schemas.py does not merely check that count == len(defects); it requires the ids to be EXACTLY contiguous from D-001:

    if ids != [f"D-{i:03d}" for i in range(1, len(ids) + 1)]:
        errs.append("defects: ids are not contiguous from D-001")

A merge that leaves two entries claiming D-034 breaks contiguity and fails by name in the gate. So this is a loud failure, not a quiet one, and no duplicate-id guard needs building. Renumbering theirs to D-036/D-037 is bookkeeping the gate will insist on rather than a trap.

What is still quiet, and remains the item to actually worry about, is point 2 above: their convergence fix changes what `converged` means, and NOTHING fails if the golden is left un-regenerated. The stale numbers stay green because they are internally consistent. That asymmetry is worth noticing on its own -- the id collision is trivial and loudly guarded, while the measurement invalidation is significant and has no guard at all, which is the same pattern the defect log keeps recording.
