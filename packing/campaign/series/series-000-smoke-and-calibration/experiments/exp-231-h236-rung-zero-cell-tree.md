---
title: exp-231 — rung 0 of the n11 settlement ladder, Trump's own angle
softschema:
  contract: packing.squares:Experiment/v2
  schema: ../../../schemas/experiment.schema.yaml
  envelope: experiment
  status: enforced
experiment:
  id: exp-231
  series: series-000
  title: Rung 0 of the n11 settlement ladder, Trump's own angle
  date: '2026-09-23'
  hypotheses: [H-236]
  tier: confirmatory
  subject:
    label: >-
      A fixed-shape cell tree over the six-axis plus five-common-angle family on the
      half-tangent box of half-width 10^-6 around Trump's tilt, with midpoint-square
      rotational cores, fail-first branching over the six most violated pairs, Z/4 and
      relabelling symmetry rows, and exact leaf certificates; split at depth 5 into 256
      subtrees
    engine: >-
      packing/cases/trump11/fixed_angle_tree.py (frozen af1179a5, Amendment 1 9c92406
      adding only resume scheduling) with the independent reader
      fixed_angle_tree_check.py (c4ae4e48)
    assurance: verified
    method: exact-algebraic
    host_system: >-
      macOS, Claude Session 156; project Python 3.14.7; 8 workers under host load 80 to
      150, then 10 workers on a quieter host
  instance: {axis: n, point: 11, role: target}
  method:
    control: >-
      Axis sanity at n=2, 4 and 5 closes below and opens above the known value; the n=5
      family of four axis squares and one near 45 degrees closes at s(5) - 10^-3 in 229
      nodes and captures Goebel's pose within 0.0022 at s(5) + 10^-3; at n=11 the Trump
      cell stays open at 3.877081 at side U + 10^-3 with the local theorem off, and the
      full tree at U + 10^-3 does not close within 100,000 nodes; the Trump-degenerate
      path closes with margin 0.00401 against rho. Every control is reader-checked except
      the n=11 negative controls, which are producer-level (the reader refuses a non-root
      cell)
    candidate: >-
      The H-236 box. Confirm only when the reader closes the complete tree with at least
      one Trump-degenerate leaf; kill with a verified non-degenerate leaf below U; an
      unresolved list at the wall cap is a bounded negative on the instrument.
    runs_per_condition: 1
    interleaved: false
    operator: Claude Session 156, Opus extra-high lane and coordinator
    entry_point: packing/cases/trump11/fixed_angle_tree.py
    command: >-
      cd packing && .venv/bin/python3 -m cases.trump11.fixed_angle_tree h236 --strong 6
      --node-cap 20000000 --workers 8 (frozen run), then --resume-subtrees with
      --stop-launching-at and --stop-at twice (exp-231-h236-frozen.txt records each
      command, index list and deviation); reader: python3 -m
      cases.trump11.fixed_angle_tree_check h236.jsonl.gz --workers N
    budget: >-
      Declared caps of 3,300 s, then two resumes of 9,118 s and 11,409 s; about 6.4 hours
      of wall in all.
    record: packing/campaign/series/series-000-smoke-and-calibration/results/agenda-042/
  effort:
    timebox: 3,300 s frozen run plus two capped resumes
    wall_seconds: 23827
    stopped_by: timebox
  results:
  - shape: determination
    role: outcome
    question: >-
      Does the independent reader close the complete tree on the H-236 box, with at
      least one Trump-degenerate leaf?
    outcome: no_progress
    checked_by: >-
      198 of 256 subtrees closed across the frozen run and two resumes, on 1.19e8 nodes
      and about 5.9e8 LP solves; 58 subtrees remain at the wall cap. Every certificate
      the reader has checked is accepted, three Trump-degenerate leaves close by the
      BC-240 local theorem (subtrees 93, 109 and 117), and no open or non-degenerate
      leaf below U has appeared. The certificate tree is 5.5 GB and stays outside the
      record
  - shape: determination
    role: cost
    question: How large is the rung-0 tree, which prices every later rung?
    outcome: criterion_met
    checked_by: >-
      More than 1.19e8 nodes for 198 subtrees, against the 10^3 to 10^5 LPs per box
      X-046 estimated; the n=5 control needs 229 nodes, so each added square multiplies
      the tree by roughly six or seven. Rung 1's 10^2 to 10^3 boxes are out of reach
      with this relaxation
  verdict:
    decision: abandoned
    primary_criterion: >-
      A reader-closed complete tree with at least one Trump-degenerate leaf confirms; a
      verified non-degenerate leaf below U kills; an unresolved list at the cap is a
      bounded negative on the instrument.
    reason: >-
      The declared caps ran out with 58 of 256 subtrees open and no counterexample
      candidate, so H-236 is neither confirmed nor refuted; the remaining subtrees are a
      bounded computation for the unchanged frozen instrument.
    budget_spent: About 6.4 hours of wall on 8 to 10 workers; 1.19e8 nodes.
    best_reached: 198 of 256 subtrees closed; three Trump-degenerate leaves; no leaf below U.
    reopen_when: >-
      Run the 58 wall-cap subtrees with the unchanged Amendment 1 bytes (the index list
      is in the h236-resume2 summary), then the reader over the whole tree; on a quiet
      host this is a matter of hours, not a new instrument.
    resume_from: >-
      The top tree and 198 closed subtree files in attic/rung0 of the Session 156
      worktree (5.5 GB, outside the record), with exp-231-h236-resume2-summary.json.gz
      naming the 58 open subtrees.
---
# Exp-231: Rung 0 of the n11 Settlement Ladder

[H-236](../../../hypotheses/H-236-n11-fixed-angle-global-optimality-at-trump.md) asks
whether Trump’s packing is globally optimal once its angles are frozen: six squares at
$0°$, five at Trump’s tilt within $10^{-6}$ in the half-tangent.
It is the first rung of [X-046](../../../explorations/X-046-n11-settlement-program.md)’s
ladder, and the first global statement anyone has attempted in an n11 family.

The instrument works, and a
[W2 review](../../../../../docs/project/reviews/review-2026-09-23-rung0-certificate-contract.md)
found its contract sound.
The tree is the problem: it is about a thousand times larger than X-046 estimated.
After three runs, 198 of 256 subtrees are closed, every certificate the reader has
checked is accepted, and the three leaves that contain Trump’s own packing close through
the local theorem as they must.
No leaf below $U$ has appeared anywhere.

The remaining 58 subtrees need no new mathematics, only the same frozen command on a
quiet machine. The cost measurement matters more for what comes next: rung 1, the full
H-112 family, is out of reach with this relaxation, so the next piece of work is a
stronger bound per node rather than more boxes.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
