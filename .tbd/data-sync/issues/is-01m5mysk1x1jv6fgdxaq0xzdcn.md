---
type: is
id: is-01m5mysk1x1jv6fgdxaq0xzdcn
title: site_urls dates every new support-file URL at its 8 October registration day
kind: bug
status: open
priority: 2
version: 1
labels: []
dependencies: []
created_at: 2026-10-23T18:01:28.893Z
updated_at: 2026-10-23T18:01:28.893Z
---
devtools.site_urls._new_row defaults first_published to REGISTRATION_DATE (2026-10-08), and derive_registry keeps a row's date only from origin/main's registry, so a support file first published later (229 atlas/regularized/n-N.svg addresses added by flip regularization, think-l2i6, on 23 October 2026) is registered as first published on 8 October. A hand edit cannot stick: --write re-derives from origin/main. Fix: date a row new to the baseline at its first build day (a deterministic date, never the render clock), or let a builder declare it, as tutorial_packing_images does.
