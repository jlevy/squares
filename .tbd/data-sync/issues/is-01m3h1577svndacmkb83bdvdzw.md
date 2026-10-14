---
type: is
id: is-01m3h1577svndacmkb83bdvdzw
title: "BC-393: decide Kleddamag's s(17) > 466001/100000 natively for C4 (4.66001 loader, winning-subset atom, cap lift to >= 20,856 sites; 2,168 rows, ~2-12 CPU-h)"
kind: task
status: open
priority: 1
version: 5
spec_path: packing/campaign/agendas/agenda-042-overnight-n11-settlement-and-low-n-angles.md
labels:
  - agenda-042
  - n17
dependencies: []
hold: paused
created_at: 2026-09-27T08:54:25.785Z
updated_at: 2026-10-13T00:54:47.568Z
---
Retarget of BC-386 after Kleddamag v1.1.0: load the 4.640020 certificate (280 point orbits; 2-of-3, 3-of-4 with coefficients [2,1,1,1], 3-of-5 and 4-of-7 thresholds; 30 winning-mask intersecting-rule orbits on 7 sites; 2,048 rows) into the parent-core interval route; add the winning-subset atom with its capacity-one lemma reviewed; lift the 8,192-site ceiling behind a byte budget; run all rows on 2 workers, about 1-6 CPU-h. A refusal is a refusal, never a negative.

## Notes

2026-10-13 owner decision: suspended pending Overbeck's proof that s(17) = L (#557; registered as T-153 by #560, credited by #571), which likely subsumes new s(17) research. Resumes only if the owner lifts the suspension, for example if T-153's replays and reviews find a gap or the candidate is withdrawn. BC-393 decides an earlier Overbeck lower bound (466001/100000) natively for C4: new s(17) bound work that T-153 would subsume.
