---
type: is
id: is-01m4wv27yed1e2wfnq55h1avr0
title: "Import wand125: s(37) >= 2599/400, s(39) >= 533/80, s(44) >= 2799/400 (check2 fine-net) and s(145) >= 306/25 (linear measure) at wand125/square-packing aba0e59 (no issue)"
kind: task
status: in_progress
priority: 1
version: 2
delegate: serene-hopper
labels:
  - result-import
dependencies: []
parent_id: is-01m4wsqt2sjrksybyz375sarb3
hold: null
hold_until: null
created_at: 2026-10-14T09:14:31.758Z
updated_at: 2026-10-14T09:14:41.660Z
started_at: 2026-10-14T09:14:41.660Z
---
Found by the 2026-10-14 watch survey (think-fxs7): problems/square-lower-bounds/certificates/mixed_n37_L64975 (7a42c16, 2026-10-13T03:18Z), mixed_n39_L66625 (dfb2cf8, 03:01Z), mixed_n44_L69975 (9f24185, 03:01Z), mixed_n145_L1224 (22f06b3, 06:18Z). Against main: 37 above 161/25 = 6.44; 39 above 133/20 = 6.65; 44 above 2789/400 = 6.9725; 145 above the reported 12.2138669 (Green DS7, disputed in #308) and the verified 12.0434, and by monotonicity lifting 146-149. The 37/39/44 bundles take the T-142/T-143 route (think-i85v): stages 1-2 with the release assets, a priced stage 4 replay with sqverify-fast from reviewed source over all directions with whole-net controls, held for an owner budget.
