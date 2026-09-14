---
type: is
id: is-01m2exznj4k1zyz1rczby8ch2k
title: "N11 strategy reset: significant bound improvements or a much simpler proof"
kind: epic
status: open
priority: 1
version: 5
spec_path: docs/project/specs/active/plan-2026-09-10-n11-daytime-strategy-and-explainer.md
labels:
  - n11
  - strategy
dependencies: []
parent_id: is-01m24sm7wm3s5eh8ke6vze7mw1
child_order_hints:
  - is-01m2ey0af1m0nfd9942ffkby3a
  - is-01m2ey0c330crgmbpxncejahnx
  - is-01m2ey0d8smw4f4w72hyay9070
  - is-01m2ey0dsfhs4cfjqhy7098m7h
created_at: 2026-09-14T03:04:47.426Z
updated_at: 2026-09-14T03:05:12.238Z
---
Owner direction, 2026-09-14: stop heavy computer-assisted proof work aimed at very small bound improvements. Pursue routes likely to significantly improve n=11 results, or to significantly simplify the proof of s(11) >= 3.82.

Where things stand (evidence gathered 2026-09-14, lane reports in the landing worktree attic/n11-stack-landing/):
- Proved lower bound T-026 s(11) >= 3.8264474 (computer-assisted, exact, unpublished); previous published bound Stromquist 2+4/sqrt(5) = 3.7889 (printed Figure 14 false, repaired by exp-017); best upper bound Trump 1979, 3.8770836, conjectured optimal, never beaten. About 43% of the 3.7889–3.8771 gap closed; no bound change since 2026-09-09 despite 17 n=11 PRs.
- Proved ceiling: every pure point/density certificate is blocked at L* = 38200/9977 ≈ 3.8288 (X-027); T-026 is 0.0024 below it. Threshold atoms have no proved ceiling, but recent gains were 1e-5 to 3e-4 (BC329 +0.000274). Weighted atoms (#157) have no quantified gain.
- Literature pattern: every hard exact s(n) value (6, 7, 10, 13, 46, ...) needed a forcing or helper step beyond point sets; Stromquist (email 2026-09-07) says helper arguments "may be essential".
- BC303 targets s(11) > 3.84 but its local-availability lemma has no candidate proof; T1 and H-161 were negative.
- No human-readable proof above 3.79 exists on record; the smallest certificate at 3.80 has 425 atoms on 181 directions.

Candidate routes (children): systematic case split at 3.85; pairwise SDP bound with an n=6 control; orientation-class structure theorem; a serious upper-bound search. Select the main lane from the first cheap tests. Paused: BC329 lane (think-zwlf), weighted-atom stages 3–4, BC303 T2 charge tests pending a routing idea.
