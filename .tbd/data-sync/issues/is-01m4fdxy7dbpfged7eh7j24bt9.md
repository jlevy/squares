---
type: is
id: is-01m4fdxy7dbpfged7eh7j24bt9
title: "Fix Pages layout shift: frontier.html 1280px dark CLS 0.209 and 390px font-settle CLS 0.25"
kind: task
status: closed
priority: 1
version: 4
delegate: claude-code@vm
labels: []
dependencies: []
parent_id: is-01m4fdxw81pt2v4k29y9n58rn6
hold: null
hold_until: null
created_at: 2026-10-09T04:14:51.629Z
updated_at: 2026-10-09T05:43:58.571Z
started_at: 2026-10-09T04:20:34.268Z
closed_at: 2026-10-09T05:43:58.571Z
close_reason: "Production font-loading fix on #442 with hosted Pages and Packing green; CLS 0.1 unchanged"
resolution: null
duplicate_of: null
---
#448 Pages 37878589945 overview job: CLS 0.209 > 0.1. Original #449 4963448 Linux 390px light CLS 0.2512 while fonts settled. Find cause and fix in production; keep CLS 0.1.

## Notes

Fixed on #442: 29a79cd10 (PT Serif 400-italic and 700 preloads; screen-only metric-compatible 'Site Sans Arial' local alias behind Source Sans 3, size-adjust 93%/89.5%; glyph probe list), f020ace62 (prose_fonts_settled probe skips local()-only faces, fixing WebKit NetworkError). Cause: font-display:block faces requested late race first paint; frontier italic/bold PT Serif (0.209/0.134 reproduced to 4 digits with runner-like fontconfig), Source Sans->DejaVu fallback 22-35% wider at 390px (0.2506). After: frontier max 0.0005 in 40 runs; Source-Sans-held paper 0.0000. Hosted on f020ace62: Pages 37889299512 and Packing 37889299519 SUCCESS. Same flake seen on #443, #458 and other branches: pre-existing on main code. #468 merge 56bf4a659 fixed 5 pre-existing contract-test failures (FONT_DIAGNOSTIC modelled in tests, no limit change). Diagnostic dispatch impossible (403).
