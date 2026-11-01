---
type: is
id: is-01m5vy0jp5b8fnq6j88zsdc871
title: "Stage 4 review of T-244 (Kim's exact sides at 172 and 263, #804) on its decided configurations, then adoption with regularization"
kind: task
status: open
priority: 2
version: 1
labels:
  - validation
  - result-import
dependencies: []
parent_id: is-01m5khvjtdjf8q14f59bmd8c1k
created_at: 2026-10-26T11:02:30.341Z
updated_at: 2026-10-26T11:02:30.341Z
---
Stage 4 review of T-244 (issue 804, Hyukdong Kim's exact sides at 172 and 263) now that both of the author's exact configurations are decided on two routes (think-4rzl, branch claude/friendly-einstein-gf9z0h-exact-804), then the house adoption the house rule takes once the review accepts.

## Validation
- Claim: s(172) <= S*_172 and s(263) <= S*_263, T-244's sides (degree 24 and 17). Certificate: the author's configurations, kept as derived facts in packing/resources/web/hyukdongkim-t244-configurations-2026-10-25/facts/ and rebuilt byte for byte. Checkers: sqpack.witness.exact_verify over K (route 1, independent) and the retained verify_exact.py (route 2, the author's reported checker), with receipts in the packet's receipts/.
- Run: the review lane as result-import.md stage 4 says (tbd-strong-max, maximum reasoning, own worktree, reading the source as data, running only code it writes): re-derive the argument from certificate to claim; read devtools.minpoly_configuration_facts and the empty-coefficient change to algebraic_witness_reports._coefficients; check the side receipt and the identity measurements (measure/identity-nNNN.json). Then map the review on T-244 (reviews, external_review on E-hyukdongkim-804-exact-forms-report), and run select_houses / adopt_houses at 172 and 263 (algebraic writer: upper_bound_houses.FIELD_COUNTS, think-ot5c), with each re-housed count's general and flip regularization in the adopting pull request, as the regularization gate requires.
- Cost: the review, an agent session; no compute beyond re-reading receipts (route 1 replay, if the reviewer reruns it, about 2.5 CPU-hours for both counts; route 2 about 0.2).
- Budget status: runnable (under the 5 CPU-hour item cap), gated on the PR that registers the replay merging.
- Depends on: the think-4rzl PR merged.
- Done when: an accepted review is mapped on T-244 and 172 and 263 are adopted as houses with their regularization, or a defect is recorded with its disposition.
- Machine note: none beyond a normal session.
