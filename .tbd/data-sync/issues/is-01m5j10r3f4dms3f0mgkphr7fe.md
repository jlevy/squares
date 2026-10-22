---
type: is
id: is-01m5j10r3f4dms3f0mgkphr7fe
title: Coordinate squaremath.org DNS, Pages, TLS, and live redirect checks
kind: task
status: in_progress
priority: 2
version: 7
spec_path: docs/project/specs/active/plan-2026-10-22-squaremath-domain.md
delegate: squaremath-coordinator
labels: []
dependencies: []
parent_id: is-01m5j0rns0p8gq9rrn3wnns7p1
hold: null
hold_until: null
created_at: 2026-10-22T14:42:37.294Z
updated_at: 2026-10-22T18:43:08.088Z
started_at: 2026-10-22T17:39:29.421Z
---

## Notes

2026-10-22 cutover: owner verified domain and saved four apex A records plus www CNAME; authoritative/public DNS verified, TXT/mail retained. PR727 merged at78dc902c19d814fa021432f66ed476b0fb1a4266 after31 applicable checks and senior reviews. Certificate approved for apex/www, expires2027-01-20; HTTPS enforcement true. Normal TLS checks using authoritative IP succeeded; HTTP upgrades to HTTPS, www redirects bare, deep profile200. Old host301 retains path/query, sometimes cached via HTTP then301HTTPS. Production packing39825552460 passed. Pages39825552463 attempt3 deploy and hosted audit succeeded:5459/5459checks at18:39UTC. Attempt1 audit rejected pre-certificate HTTP output; attempt2 duplicated generated artifact names. Original artifact12445779666 preserved externally, removed duplicate, reran failed deploy only. Do not rerun artifact assembly merely to refresh deployment URL. Remaining: local router DNS still returns earlier miss; verify ordinary browser access and legacy fragment retention, then finalize docs/close epic and disable monitor complete-square-math-domain-cutover. Presentation edits on codex/profile-naming-and-tally-order same external worktree; do not reset. Infra follow-up think-fqhc.
