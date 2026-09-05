---
type: is
id: is-01m1qcc9devr6mz0m6erxswxjc
title: Port PR 80's improvements onto main, one at a time
kind: epic
status: open
priority: 0
version: 21
labels: []
dependencies: []
child_order_hints:
  - is-01m1qcc9xynr234fqa3h9qsy62
  - is-01m1qcca9tj74rwj6c7r62t674
  - is-01m1qccav372fjbyb9vw318anx
  - is-01m1qccbdv8sw50zhxwc4a3qfb
  - is-01m1qccc39dj2dg7btkg7dngp0
  - is-01m1qcccp547v6zx6f105tbd72
  - is-01m1qccd6ma739e4qkrbc967q9
  - is-01m1qccdpvx48fjqy7dy4whmwf
  - is-01m1qcceaaadd8cbb3p4qakf6k
  - is-01m1qccevbhwxxwxgdcbzgxktd
  - is-01m1qccfcyarmwryjycg3xywnf
  - is-01m1qccfya4yy6nd4jg64bas22
  - is-01m1qccggx7b0c9yjhanb42p94
  - is-01m1qcch1j2a7dpynp66qam2p7
  - is-01m1qcchmasjppsb50npxmkhbd
  - is-01m1qcnnz9mfwn7jcg8eemddq4
  - is-01m1qcnpbkcj1npasye0hzg9pd
  - is-01m1qcnppk7e67rxdhn9h3ddbe
  - is-01m1qey47ncj6qjqvrqekhr5kz
  - is-01m1qf18nme35gjp23rg0rp0ym
created_at: 2026-09-04T23:34:34.669Z
updated_at: 2026-09-05T00:20:59.187Z
---
PR 80 (codex/pr78-s11-adversarial-review) reviewed PR 78's s(11) >= 381/100 claim and found real things beside a great deal of weight. The operator's decision: merge PR 78, then port the valid improvements one by one onto a branch off main, each as its own commit, tracked here. The review that decides which is which is docs/project/reviews/review-2026-09-04-pr80-stacked-hardening.md; the mapping of the certificate conditions to Condition 1-5 is in it and both branches use it.

Already landed on PR 78 in 580efe58 and not repeated here: nonnegative weights as the theorem's precondition with the five-atom must-refuse fixture (their F1); a restricted direction sample cannot hold (F6); the ceiling over-claim (F14, D-447); the two comparison factors (F33, D-448); the n = 11 case body and the pinned-interval and gap forms in check_case_prose (D-445); the C5 wording (D-446).

Deliberately NOT ported, with the reason in the review: the Lean lake project (a research note links the spike; nothing builds it); the second standalone verifier unless the code lane finds it strictly better than thirdparty/verify.py; the 731-line hostile-input matrix for decide_certificate; the typographic edits inside quoted sources in five dated reviews and the rewritten observation in a sixth; the D-439 regression; their D-469 (duplicate of D-432); the renumbering of the parent's D-441; the suite budgets as measured on the Fraction sweep.

Their genuine defect entries are renumbered into this branch's sequence (D-449 onward) as each item lands; duplicates of D-441/D-442 are recorded once as concurrent discovery.
