---
type: is
id: is-01m5j10r3f4dms3f0mgkphr7fe
title: Coordinate squaremath.org DNS, Pages, TLS, and live redirect checks
kind: task
status: in_progress
priority: 2
version: 5
spec_path: docs/project/specs/active/plan-2026-10-22-squaremath-domain.md
delegate: squaremath-coordinator
labels: []
dependencies: []
parent_id: is-01m5j0rns0p8gq9rrn3wnns7p1
hold: null
hold_until: null
created_at: 2026-10-22T14:42:37.294Z
updated_at: 2026-10-22T17:49:23.115Z
started_at: 2026-10-22T17:39:29.421Z
---

## Notes

2026-10-22 attended cutover: owner verified domain and saved all five web-routing records. Authoritative Namecheap DNS confirmed four A records 185.199.108.153 through185.199.111.153 and www CNAME jlevy.github.io at10:45PDT. TXT and mail retained. Pages binding squaremath.org uses workflow source; protected_domain_state verified. PR727 merged after final31 passing applicable checks (28 conditional skips) and senior reviews A/B with A1 resolved. Merge78dc902c19d814fa021432f66ed476b0fb1a4266 at17:45:59UTC. Production Pages run39825552463 and packing39825552460 running. Old-host results.html?s=5 returns301 to http://squaremath.org/results.html?s=5, preserving path/query. Direct GitHub HTTP routing returns200; local DNS still negative-cached. HTTPS certificate null and enforcementfalse; direct TLS name validation fails as expected until issuance (no bypass used). Next: await certificate, enableHTTPS, finish production run/live audit and browser fragment tests, update lasting docs. CI install timeout follow-up think-fqhc. Source implementation think-v4ab closed; epic remains open until live verification.
