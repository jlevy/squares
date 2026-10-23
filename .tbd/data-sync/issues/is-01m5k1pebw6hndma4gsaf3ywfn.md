---
type: is
id: is-01m5k1pebw6hndma4gsaf3ywfn
title: Audit and enforce shared 35em prose and card alignment across page families
kind: task
status: in_progress
priority: 2
version: 3
spec_path: docs/project/specs/active/plan-2026-10-22-site-navigation.md
delegate: sol-width-audit
labels: []
dependencies: []
parent_id: is-01m5jnsqdwj3t8m7hkbx6mr1m2
hold: null
hold_until: null
created_at: 2026-10-23T00:13:42.651Z
updated_at: 2026-10-23T00:29:48.546Z
started_at: 2026-10-23T00:13:56.643Z
---
User reports remaining inconsistent reading widths. Audit all standard prose, breadcrumb and card-group width rules for page-specific exceptions. Enforce one35em measure at shared18px base (630px), aligned outer edges for standard cards. Keep intentional wide data tables/visualizations distinct, not accidental prose exceptions. Verify computed browser geometry across main page families and rebuild affected preview pages; document any justified exception.

## Notes

Audit completed across21actual generated page families×5viewports=105page/viewport records, including Overview, News, Recent, Archive, About, Tutorials, Papers, profiles directory/individual, Resources, Posters predecessor Downloads, Documentation, Report, Project Epistemics, both tutorials and all4paperHTML.20families use rootbuilt artifact served8792; missing Verification rendered from current source; current navCSS injected for header update. Plain prose630px at1440/1256/768,358px at390 and288px at320. Collection outer frames match prose. Four paper shells742px intentionally contain630px prose; wide data/visuals retain separate tracks. News/callout body596px is padding inside630px outer surfaces; profile Sources details has628px inner panel and604px padded support text, not prose-width exception. No unintended measure conflict identified; no prose/card CSS override added. Retained current-producer regression covers17families×5widths (including newly registered Posters) and PASSES84.20s; fixture setup renders selectedHTML only, no PDF/fullbuild. Shared4shell×5width test also PASSES4.82s and preserves wide blocks. Biome/Ruff/focused basedpyright0errors0warnings/diff clean. Evidence reading-width-audit-initial.json, reading-width-audit-responsive.json, reading-width-source-family-tests-final.log in external scratch; retained probe tests/probes/site_navigation/reading-widths.js. Root owns final preview rebuild/acceptance; leave open until integrated artifact verified.
