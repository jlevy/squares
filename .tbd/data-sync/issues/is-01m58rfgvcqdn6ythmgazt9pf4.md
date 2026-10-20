---
type: is
id: is-01m58rfgvcqdn6ythmgazt9pf4
title: "Import Daniel: staircase deficiency and Ryu threshold improvements (no issue)"
kind: task
status: in_progress
priority: 2
version: 2
delegate: claude-code@spud10.local
labels:
  - result-import
dependencies: []
parent_id: is-01m572ssbx1x412zpvsw1sb6je
hold: null
hold_until: null
created_at: 2026-10-19T00:20:14.315Z
updated_at: 2026-10-19T00:20:25.440Z
started_at: 2026-10-19T00:20:25.439Z
---
W1 intake 2026-10-19. Source evand/square-packing 13da78235c611d6f9a422bd63226b231d879903b claims c*(k) < 18.9 k^(2/5)+35.7 k^(1/5)+122 for k>=300000 and Ryu bound c*(k) <= 20.668 k^(2/5)+0.623 for k>=8000000 (register currently starts at 16000000). The source adds four RyuStair* Lean modules, numerical companion, imports, and axiom declarations; later aa12b989aa7d4244c57ea6c3b06bb36318bd41ea packages verification script and write-up. Source link: https://github.com/evand/square-packing/commit/13da78235c611d6f9a422bd63226b231d879903b . Stage0 reported claims, not verified. Retain dependency-complete source/attribution, price kernel replay and axiom audit, independently review construction/Packs-to-deficiency bridge/strictness/thresholds, compare register and finite consequences, and import or document non-import. Coordinate with think-ahr2 Ryu and think-f8py improved filled-layer bound. No source run yet; author estimate of five minutes on 16 cores is not an observed result.
