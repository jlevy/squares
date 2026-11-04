---
type: is
id: is-01m6jt6e1ma73nnan4vg5y107t
title: "audit_fine_net_receipt's full run can never PASS mixed_n68_L853: it requires a mutant refusal at every direction, which the census control's FC-1 rule does not (n68's 99/100 mutant verified at r = 46-49)"
kind: task
status: open
priority: 3
version: 1
labels:
  - validation
dependencies: []
parent_id: is-01m684vnbc5mmkjn950c3edw3w
created_at: 2026-11-04T08:18:19.828Z
updated_at: 2026-11-04T08:18:19.828Z
---
Nit (c) of #892's confirming review, filed by intake lane L37 (bold-ritchie-l37, think-qpq0); no contract changed.

packing/devtools/audit_fine_net_receipt.py check_controls holds the 99/100 mutant's whole-net sweep to a refusal at every direction: require_complete_indices(refusals, measure.count), verified_directions == [] and summary_refused_directions == range(count). The census control (packing/devtools/sqverify_fast_census.py, module docstring and control(); FC-1 of the 6 October re-check, docs/project/reviews/review-2026-10-06-sqverify-fast-census-control-fc1.md) requires a refusal at one direction at least and every non-verified direction to be a coverage refusal: the mutant may verify where the original captures at least 100/99, because the least-bound direction is chosen by the branch and bound's termination margin.

mixed_n68_L853 (T-205, wand125 fine-net lower bounds of 16 October) has control receipt packing/benchmarks/measure-verifier/census-mixed/wand125-fine-net-lower-bounds-2026-10-16/mixed_n68_L853.control.json, status CONTROLS_REFUSED, whose mutant refused at 197 of 201 directions and verified at r = 46, 47, 48 and 49. The auditor's full run on it therefore always fails at require_complete_indices ('directions missing, duplicated or out of range'), although the census contract holds and T-205's evidence stands.

Decide, as a change a reviewer reads: (1) the auditor admits verified mutant directions as the census does (at least one refusal; every listed refusal checked as now; verified directions disjoint from refused and together the whole net; summary_refused_directions equal to the refused set), since a mutant verified at r is itself a certificate that the original captures at least 100/99 there; or (2) the auditor states that its scope is receipts whose mutant refuses everywhere and names n68 as outside it. Do not change the census contract. Done when the auditor's full run on mixed_n68_L853 either PASSes or refuses with a reason the instrument's docstring states, with a test either way. For reference, the full auditor PASSes on mixed_n94_L9965 in 37.5 s (600 refusals, 4 November 2026).
