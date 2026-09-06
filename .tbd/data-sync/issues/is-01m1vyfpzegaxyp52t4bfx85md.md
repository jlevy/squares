---
type: is
id: is-01m1vyfpzegaxyp52t4bfx85md
title: Address shortcomings from the published square-packing adversarial review
kind: epic
status: in_progress
priority: 1
version: 12
labels: []
dependencies: []
child_order_hints:
  - is-01m1vy4nvz0f2m60aa95b15qvy
  - is-01m1vy4p6smq89byx6k4p1nxcw
  - is-01m1vy4ph1w9f4eb1faq643v8p
  - is-01m1vyj4w7bknpy3ggs34p3pdn
  - is-01m1vz0dft6sw4evjm7fq4c4zp
  - is-01m1vz4dvs8ng1e70vgzv9mfg7
  - is-01m1w02sjh48x0b0d16f1yz9ak
created_at: 2026-09-06T18:07:58.957Z
updated_at: 2026-09-06T19:03:08.239Z
---
W9 remediation entry, explicit user request. Six shortcomings are recorded as D-473 through D-478 in the durable published-core adversarial review. Five are repaired: unsafe ceiling screening, unguarded cutting bounds, float vertex deduplication, the unsupported n12 endpoint, and the missing fixed-net qualification. The independent geometric sweep oracle is contributed and documented. D-478 is contained by qualifying the historical BC206 floor; think-aenh remains open to recover or recompute its missing exact witness. PR https://github.com/jlevy/squares/pull/100 on codex/adversarial-review-fixes contains the completed wave at commit 237d9386. Pre-push checks, final-commit hosted CI, and the full local gate passed; the full gate included 2396 Python tests and finished in 1838.80 seconds on the review host. Six children are closed; only the witness-recovery child remains open. The headline s11>=3.81 was not refuted and no new packing result is claimed.
