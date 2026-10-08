---
type: is
id: is-01m4edy0gkgv91t6evhbzeyk58
title: "PR #456: reduce frontier startup layout within the existing rendering budget"
kind: bug
status: in_progress
priority: 1
version: 2
delegate: codex-pr395-site-review
labels: []
dependencies: []
parent_id: is-01m4e2d5gyj7m218hm9f5g01xd
hold: null
hold_until: null
created_at: 2026-10-08T18:55:39.537Z
updated_at: 2026-10-08T18:57:07.172Z
started_at: 2026-10-08T18:57:07.172Z
---
Frontier startup violated unchanged300ms longest-task limit in mainf0ec run37808133069 at390/light341ms and PR456 head3d run37821312270 at390/dark395ms. Independent Astra MAX attribution found real early style/layout on324rows359formulas31315elements; later readability probes are not the offending task. Fixed table tracks rejected because CLS.177 exceeded.1 and largest layout did not improve. Next bounded candidate loads the two observed first-screen KaTeX math faces earlier only on frontier.html, using existing protocol-aware preload path; bootstrap must safely accept their ASCII uppercase/underscore hashed-local names. Preserve static content, all ordinarylinks, noJS/file-origin compatibility, print, same-origin/path restrictions and existing rendering limits. No accepted candidate or hosted cure yet. Require final review, exact-head CI and deployed verification under think-7wlz.
