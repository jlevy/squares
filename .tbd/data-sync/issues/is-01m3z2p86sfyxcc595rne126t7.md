---
type: is
id: is-01m3z2p86sfyxcc595rne126t7
title: Register Bašić-Slivková's archived lower bound at n = 61 (7.8906, above Karakuš's 7.8655)
kind: task
status: closed
priority: 2
version: 3
labels: []
dependencies: []
parent_id: is-01m3xgkna3m3w1w50ky6gqyxyk
created_at: 2026-10-02T19:50:34.447Z
updated_at: 2026-10-03T15:46:52.872Z
closed_at: 2026-10-03T15:46:52.869Z
close_reason: "Registered as T-070 (Basic-Slivkova 2018, Theorem 7 with Proposition 8) by the new-result publication sequence: verified floors at n = 37 (5*sqrt(3)/2 + 2*sqrt(2) - 1) and n = 61 (7*sqrt(3)/2 + 2*sqrt(2) - 1), the only cases where it beats the held floor; devtools/check_piercing_lower_bounds.py replays the arithmetic. Hosted CI green at dd636b4cc and at the PR head c73d0cc25."
resolution: null
duplicate_of: null
---
Lane B of session-168 (think-xucp) found that Bašić-Slivková's archived but unregistered lower bound at n = 61, 7.8906, beats Karakuš 2026 Corollary 6.2's 7.8655, which became the operative verified floor at n = 61 once T-007 was withdrawn (review-2026-10-02-nagamochi-lemma1-karakus.md). Read the archived source under packing/resources/, verify the bound and its method at the register's evidence standard, add an evidence entry and result, and re-ground n = 61's verified lane on it if it holds. The case body already carries a dated note naming the stronger bound.

## Notes

2026-10-03 session-168 phase 9: registered as T-070 (V3/C1, S3, previously-published) with evidence E-basic-slivkova-piercing-lower, by the new result publication sequence (commit 293e6ee43). Theorem 7 with Proposition 8 read on the rendered pages and re-derived; it uses nothing of Nagamochi 2005. devtools.check_piercing_lower_bounds evaluates it exactly at every case: it beat the held verified floor at n = 61 (Theorem 10, 7*sqrt(3)/2 + 2*sqrt(2) - 1 ~ 7.890604) and at n = 37 (5*sqrt(3)/2 + 2*sqrt(2) - 1 ~ 6.158554, not stated in the paper), and nowhere else; it reproduces the paper's Table 1 and its Theorem 9 floors. Both case records carry dated updates; the frontier README counts and every rendered view are current; DATA_REVISION re-pinned. Close when hosted CI is green.
