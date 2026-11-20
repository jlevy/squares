---
type: is
id: is-01m7wx58nderf20ztnx9wkyqhq
title: "Stage 4 blind mathematical review of #1050's s(18) lower-bound argument (21-point covering, 187 cases, exact bounds, six tight cases)"
kind: task
status: closed
priority: 1
version: 5
delegate: r1050
labels: []
dependencies: []
parent_id: is-01m7khxdfnc5tynb8cjr4z7862
hold: null
hold_until: null
created_at: 2026-11-20T16:38:13.420Z
updated_at: 2026-11-20T21:17:15.562Z
started_at: 2026-11-20T16:39:26.015Z
---

## Notes

r1050, 2026-11-20 (blind stage 4 review of issue 1050, Mira Cult's s(18) = (7+sqrt7)/2). Branch claude/intake-2026-11-20-review-1050 (pushed; no PR).

Verdict: partially verified; no gap found. No blocking or major finding.

Freezes: plan 22f31fef7d (16:54:02Z); checkers 64a4a6ff88 (17:00:40Z) and 573188acd4 (17:28:46Z, after plan amendment 1); findings 08d98848d3 (18:52:03Z), before n-018.md was read.

Independent (own programs, written before any source program was opened): construction exact in Q(sqrt7), 72 walls and 153 pairs, 32 controls refused; covering lemma at eps 1e-5 by exact branch and bound (24,282 + 929 leaves), five controls fail with exact witnesses, true margin between eps 3/400 and 1/100; 187 orbits (Burnside), source keys one per orbit; six-tilt and eight-tilt packings (and 1,568 loose moves) only in case 53, inside chord-guard terminals; six-tilt is the exact equality case of the chord lemma (Q - P = 2u).

Source replay: verify_exact_18.py --workers 3 PASS, 428 terminals, 47m40s wall, ~30 CPU-min; five pre-stated mutations all refused (M4: case-53 slab holding the construction relabelled empty -> kernel OPEN). Kernel rules, cut/cover logic, chord, two-face and perpendicular-probe guards re-derived by hand.

Not independent: the 428 terminals rest on the source's single implementation; the lane's refuter decided 0 of 6 sampled cases (91, 93, 56, 86, 2, 80; all undecided at 20 min).

Findings F1-F9 (minor/notes); F9: source README prints H = 4.822875655286..., wrong from the 10th decimal (H = 4.8228756555322953...); issue 1050's body quotes the wrong digits.

Review docs/project/reviews/review-2026-11-20-mira-1050-n18.md; packet packing/resources/web/mira-cult-n18-1050-review-2026-11-20/. No registry record touched. Suggested significance S5 (no draft on main). About 3 CPU-hours used.
