---
type: is
id: is-01m5j10r3f4dms3f0mgkphr7fe
title: Coordinate squaremath.org DNS, Pages, TLS, and live redirect checks
kind: task
status: in_progress
priority: 2
version: 6
spec_path: docs/project/specs/active/plan-2026-10-22-squaremath-domain.md
delegate: squaremath-coordinator
labels: []
dependencies: []
parent_id: is-01m5j0rns0p8gq9rrn3wnns7p1
hold: null
hold_until: null
created_at: 2026-10-22T14:42:37.294Z
updated_at: 2026-10-22T18:26:17.431Z
started_at: 2026-10-22T17:39:29.421Z
---

## Notes

2026-10-22 cutover: domain ownership verified; owner saved four GitHub Pages apex A records and www CNAME jlevy.github.io. Authoritative Namecheap and Google DoH DNS confirmed; TXT and mail retained. PR727 merged at 78dc902c19d814fa021432f66ed476b0fb1a4266 after 31 applicable checks and senior reviews A/B. Production packing run39825552460 succeeded. Pages run39825552463 publish succeeded, but verify-deployment correctly rejected the http://squaremath.org deployment output because HTTPS certificate is not issued yet. Do not weaken the HTTPS checker. API certificate null/enforcement false; Settings Pages confirms certificate unavailable. Legacy path/query redirect and www-to-bare HTTP redirect verified. Monitor complete-square-math-domain-cutover checks every five minutes. Next: await certificate, enable HTTPS, rerun publish plus dependent verification so deployment URL output becomes HTTPS, verify TLS/redirects/fragments/deep assets, update docs and close epic. Presentation work now on codex/profile-naming-and-tally-order in same external worktree; do not reset it. Infrastructure timeout follow-up think-fqhc.
