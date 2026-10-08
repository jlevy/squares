---
type: is
id: is-01m4ev1m1g30gz1gtqe54tsp10
title: Correct degree-search and eliminant assurance labels before contact-driver reuse
kind: bug
status: open
priority: 2
version: 1
spec_path: docs/project/specs/active/plan-2026-10-06-exact-side-values.md
labels: []
dependencies: []
parent_id: is-01m4eszf0kjvjadgn77f0hy2pc
created_at: 2026-10-08T22:44:49.327Z
updated_at: 2026-10-08T22:44:49.327Z
---
Astra W6 readiness review: probe_system_degree.py infers not-degree20 from a Bezout upper bound; probe_minimal_polynomial.py and frontier/extra/X-004 make unsupported degree/coefficient exclusion claims from bounded PSLQ non-return; probe_elimination.verify_eliminant checks numerical residual and factorization without exact ideal membership or real-branch realization. Quarantine these helpers as numerical candidates/exports before think-s6np driver reuse; correct labels and retain scoped negatives. Acceptance: explicit algebraic identity, geometric realization and operational refusal contracts, with no promotion from a numerical relation alone. No change to existing case bounds or proof rungs.
