---
type: is
id: is-01m26697w7prvp4mdkme3cspdc
title: Admit weighted five-site threshold atoms exactly
kind: task
status: open
priority: 1
version: 9
spec_path: docs/project/specs/active/plan-2026-09-10-n11-daytime-strategy-and-explainer.md
labels:
  - n11
  - research-tooling
dependencies:
  - type: blocks
    target: is-01m24r3sgyw8hj7k7cfd8spmxg
  - type: blocks
    target: is-01m2agbxkn3zzemwvx5pvwe2hp
  - type: blocks
    target: is-01m2agbxyzknj4s538jxexx8dz
parent_id: is-01m24r3sgyw8hj7k7cfd8spmxg
child_order_hints:
  - is-01m2bmgbj85wn7meq5afgrwmej
  - is-01m2bmgc6v2dx391qsg393hw2m
created_at: 2026-09-10T17:36:39.814Z
updated_at: 2026-09-12T20:44:03.944Z
---
Run the bounded W7 admission before any BC327 solve. Add explicit positive-integer multiplicities, weighted D4 keys, exact token budgets, strict versioned loading, independent source-charge replay, and agreeing direct/event/interval coverage controls. Materialize a fresh common row and point manifest and a maintained paired runner. Reject malformed integers, repeated-coordinate aliases, understated budgets, lossy old-verifier reads, incomplete coverage, and partial/deadline promotion. No scientific target runs until all admission stages pass.

## Notes

Stages 1 and 2 complete in session-127, PR 157 on branch claude/n11-w7-weighted-atom-admission.

STAGE 1 (representation and theorem) -- done. ThresholdAtom takes an explicit positive integer token count per distinct site, defaulting to all ones so a legacy atom is unchanged in every derived figure and gains no record key. size counts distinct SITES; token_count counts TOKENS. Geometry stays one membership rectangle per site, while the threshold, the budget w*floor(A/k), the D4 orbit key and the inclusion--exclusion expansion are per token. Audited every call site the distinction reaches: the sweep keeps its site-count cursor and expands those rectangles to one per token before signing subsets; the direct route paints each rectangle with its own count and shares nothing with that expansion; the int64 headroom bound reads token_count. The retained motif (2,2,1,1,1) at threshold 4 expands over 64 token subsets with absolute mass 209, where reading it as five sites reports 9 -- that 23x understatement is pinned as a control. Weighted records carry variant weighted-threshold/v1, which older readers refuse; dilation_corollary already uses that gate one level up, and the archived floor_atom_columns reader did read a bare multiplicities field through int under a float slack. decide_threshold_certificate, admit_fixed_support_dual and the interval route refuse a weighted atom rather than read it as lighter. dilation_corollary was already safe because it uses dataclasses.replace.

STAGE 2 (independent source replay) -- done. devtools/replay_weighted_atom_source.py rebuilds each retained receipt's atom through the production model and derives its token total, budget, charge and charged-placement list again from family geometry. All four retained receipts reproduce exactly: tokens 7, threshold 4, budget 1, charge 3/2, exact charged lists, on rational coordinates up to 965 characters wide. Both inputs are sha256-bound because nothing retained binds them -- the source fields name scratch paths that are gone. Eleven mutation controls; one structurally vacuous comparison was removed.

STAGES 3 and 4 -- not started, tracked as think-8c9e (coverage mechanics) and think-kj5u (paired instrument, blocked on 8c9e). No BC327 hypothesis, experiment or scientific target was registered or run.

Two findings filed separately: think-8frj (the orbit admitter's unreachable negative-weight branch) and think-ur2b ('size' means tokens in retained receipts and sites in the model). Kept out of defects.yaml because two other open branches already move that file's count.
