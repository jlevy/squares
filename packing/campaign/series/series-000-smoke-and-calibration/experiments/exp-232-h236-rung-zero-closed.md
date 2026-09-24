---
title: exp-232 — rung 0 closes, Trump is globally optimal at its own angle
softschema:
  contract: packing.squares:Experiment/v2
  schema: ../../../schemas/experiment.schema.yaml
  envelope: experiment
  status: enforced
experiment:
  id: exp-232
  series: series-000
  title: Rung 0 closes, Trump is globally optimal at its own angle
  date: '2026-09-24'
  hypotheses: [H-236]
  tier: confirmatory
  subject:
    label: >-
      The rung-0 cell tree of exp-231 completed: the 58 wall-cap subtrees rerun from
      scratch with the unchanged Amendment 1 bytes, then the independent reader over the
      complete tree of 256 subtrees
    engine: >-
      packing/cases/trump11/fixed_angle_tree.py at Amendment 1 (9c92406) with the
      independent reader fixed_angle_tree_check.py (c4ae4e48); digests checked before
      the run
    assurance: verified
    method: exact-algebraic
    host_system: macOS, Claude Session 157; project Python 3.14.7; 9 workers, then a 10-worker reader
  instance: {axis: n, point: 11, role: target}
  method:
    control: >-
      The exp-231 controls, reader-checked except the producer-level n=11 negative
      controls, and the W2 contract review of 2026-09-23
    candidate: >-
      The H-236 box. Confirm only when the reader closes the complete tree with at least
      one Trump-degenerate leaf, the declared half-tangent box covering the registered
      box and the target at least U; kill with a verified non-degenerate leaf below U.
    runs_per_condition: 1
    interleaved: false
    operator: Claude Session 157 coordinator
    entry_point: packing/cases/trump11/fixed_angle_tree.py
    command: >-
      cd packing && .venv/bin/python3 -m cases.trump11.fixed_angle_tree h236 --strong 6
      --node-cap 20000000 --workers 9 --resume-subtrees <the 58 wall-cap indices, heavy
      partials first> --stop-launching-at 2026-09-24T12:00:00+00:00 --stop-at
      2026-09-24T12:45:00+00:00 (exp-232-h236-frozen.txt, R4); then python3 -m
      cases.trump11.fixed_angle_tree_check ../attic/rung0/h236.jsonl.gz --workers 10
    budget: One night of wall on 9 workers, then the reader.
    record: packing/campaign/series/series-000-smoke-and-calibration/results/agenda-042/
  effort:
    timebox: Launch cutoff 12:00Z, hard stop 12:45Z
    wall_seconds: 16764
    stopped_by: criterion
  results:
  - shape: determination
    role: outcome
    question: >-
      Does the independent reader close the complete rung-0 tree with at least one
      Trump-degenerate leaf, on the registered box, at a target of at least U?
    outcome: criterion_met
    checked_by: >-
      All 58 remaining subtrees completed (5.12e7 nodes, 2.62e8 LP solves, 14,350 s; the
      largest, subtree 128, 7,987,265 nodes). The reader replayed the whole tree in
      2,414 s: verdict closed, unresolved leaves none, 139,440,746 exact leaf
      certificates accepted (19,883,887 dual-bound, 21,834,304 Farkas, 97,722,555 closed
      by the fail-first leaf rule), three Trump-degenerate leaves closed by the BC-240
      local theorem, smallest certified margin 6.04e-10 above U's upper end, largest
      enclosure reach 2.93e-5 beyond the matched Trump image; statement
      target_is_at_least_U true and half-tangent box [91442076901/250000000000,
      73154061521/200000000000] (exp-232-h236-reader-final2.json.gz)
  - shape: determination
    role: cost
    question: What did the complete rung-0 tree cost?
    outcome: criterion_met
    checked_by: >-
      About 1.70e8 nodes and 8.6e8 LP solves over four producer runs (3,300 s, 9,118 s,
      11,409 s and 14,350 s of wall on 8 to 10 workers), and 139 million certificates.
      Against X-046's estimate of 10^3 to 10^5 LPs per box this is roughly four orders
      of magnitude larger, which prices rung 1 out of reach with this relaxation
  verdict:
    decision: accepted
    primary_criterion: >-
      A reader-closed complete tree with at least one Trump-degenerate leaf on the
      registered box at a target of at least U.
    reason: >-
      The independent reader closes all 256 subtrees with no unresolved leaf and three
      Trump-degenerate leaves, so every packing of six axis-aligned squares and five at a
      common tilt within 10^-6 of Trump's half-tangent has side at least U, with
      equality only on Trump's orbit; the local theorem it relies on is BC-240, accepted
      at retained-record-dependent scope pending BC-241, and the certificate tree
      itself (5.5 GB) is retained outside the record.
---
# Exp-232: Rung 0 Closes

[H-236](../../../hypotheses/H-236-n11-fixed-angle-global-optimality-at-trump.md) is
confirmed at its registered scope. Freeze the tilt of Trump’s five tilted squares to
within $10^{-6}$ in the half-tangent, keep the other six axis-aligned, and let every
centre and contact vary: no such packing fits in a square smaller than $U$, and the only
packings at $U$ are Trump’s own, up to symmetry and relabelling.
It is the first global optimality statement in any $n = 11$ family, and the first rung of
[X-046](../../../explorations/X-046-n11-settlement-program.md)’s settlement ladder.

[Exp-231](exp-231-h236-rung-zero-cell-tree.md) had closed 198 of 256 subtrees before its
caps. The remaining 58 ran overnight with the unchanged instrument, heaviest first, and
all completed; the independent reader then replayed every one of the 256 subtree files
and accepted all 139 million leaf certificates, with the three leaves containing Trump’s
packing closed by the quantified local theorem, as the
[contract review](../../../../../docs/project/reviews/review-2026-09-23-rung0-certificate-contract.md)
required.

The statement is narrow: it says nothing about any other tilt, and its terminal leaves
inherit BC-240’s scope, pending the BC-241 closure. Registering it as a frontier result
waits for a Fable max W2 review of the closed tree. The cost is the other finding: about
$1.7\times10^8$ nodes for one box, so the next rung needs a stronger bound per node
before it needs more boxes.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
