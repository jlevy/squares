---
type: is
id: is-01m5j10r3f4dms3f0mgkphr7fe
title: Coordinate squaremath.org DNS, Pages, TLS, and live redirect checks
kind: task
status: in_progress
priority: 2
version: 4
spec_path: docs/project/specs/active/plan-2026-10-22-squaremath-domain.md
delegate: squaremath-coordinator
labels: []
dependencies: []
parent_id: is-01m5j0rns0p8gq9rrn3wnns7p1
hold: null
hold_until: null
created_at: 2026-10-22T14:42:37.294Z
updated_at: 2026-10-22T17:39:53.554Z
started_at: 2026-10-22T17:39:29.421Z
---

## Notes

2026-10-22: user verified ownership and explicitly authorized attended cutover once checks passed. PR727 head73a28c47fb0499999fb1a9b9e8baad78a6589215 now all31 applicable checks passed,28 conditional skips; reviewA/B resolved. PUT repos/jlevy/squares/pages cname=squaremath.org succeeded. Readback: build_type workflow, cname squaremath.org, protected_domain_state verified, html_url http://squaremath.org/, https_enforced false, https_certificate null. User given four185.199.108–111.153 apexA records and www CNAME jlevy.github.io; awaiting saved-record confirmation. Preserve TXT and mail. Next: confirm DNS; merge reviewed PR with merge commit; watch production deployment; confirm certificate and enforceHTTPS; audit apex/www/oldhost deep query and fragment redirects plus live publication; update plan/guide. Prior preview build+7333local audit passed. CI installer stalled apt~57min, cancel+failed-onlyretry succeeded; missing timeout separate follow-up.
