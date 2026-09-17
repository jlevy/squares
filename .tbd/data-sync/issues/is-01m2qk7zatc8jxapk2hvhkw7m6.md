---
type: is
id: is-01m2qk7zatc8jxapk2hvhkw7m6
title: "M3 kill test: exact-ownership 11-point set at n=11 in Stromquist's Memo II idiom"
kind: task
status: open
priority: 2
version: 1
spec_path: docs/project/specs/active/plan-2026-09-10-n11-daytime-strategy-and-explainer.md
labels:
  - n11
  - research
dependencies: []
parent_id: is-01m2exznj4k1zyz1rczby8ch2k
created_at: 2026-09-17T11:50:15.129Z
updated_at: 2026-09-17T11:50:15.129Z
---
Adversarial review 2026-09-17 (think-4woh, X-037): an 11-point exact-ownership set at n=11 is not a sum of D4 orbit sizes {1,4,8}, so no producer in the record can search for it; an existing verifier (green17 interval_audit) can check a candidate. Expected outcome is integral piercing >= 12 at 3.80 (a kill). Run as a bounded kill test before any hand-proof route (M4 was killed at 3.82).
