---
type: is
id: is-01m7w5v7yx2kbywepf76h0sdwe
title: "Stage 4 review: #1012's 109, de Winter's transcription of Kodaj's Kaggle pinwheel (T-335, provisional)"
kind: task
status: in_progress
priority: 1
version: 4
delegate: r1012
labels:
  - intake
  - validation
dependencies: []
parent_id: is-01m7khxdfnc5tynb8cjr4z7862
hold: null
hold_until: null
created_at: 2026-11-20T09:50:47.773Z
updated_at: 2026-11-20T12:01:56.586Z
started_at: 2026-11-20T11:10:12.516Z
---
Stage 4 blind review of T-335 (provisional id): jlevy/squares#1012's 109, Joost de Winter's exact corner Witness/v2 transcription of Tomáš Kodaj's CC0 Kaggle rows, s(109) <= 547464479047171949843/50000000000000000000 = 10.94928958094343899686, retained as packet de-winter-kodaj-n109-2026-11-18 (JoostdeWinter/square-packing aae089c), imported by lane c7-pointers on branch claude/intake-2026-11-20-pointers-109-259 (think-wvr8).

Scope: the mathematics of the certificate; a clean-room exact checker with sharp controls; the identity against the house (T-101) and against Samanyu-dev's public 109 (Samanyu-dev/squares_in_squares 53551d7, best_fit_101_500.csv, SHA-256 377b9177febf1b89f08d655531880fb683666e494a3b303f10645e7440996c04); the option D comparison (think-b0w5) that the import measured, Samanyu-dev's packing contracted to first contact 5.57e-14 below this side; and the draft significance S3. Mapped as an adversarial review. Written blind to the import lane's README and register text until its own findings are written. tbd-strong-max, maximum reasoning, own worktree.

## Notes

## Lane r1012 (stage 4 review), 2026-11-20

- Branch claude/intake-2026-11-20-review-1012 (no PR). Review docs/project/reviews/review-2026-11-20-de-winter-1012-n109.md; packet packing/resources/web/de-winter-kodaj-n109-1012-review-2026-11-20/.
- Verdict: accepted, no blocking or major finding (F1-F15: notes, F10 minor). Certificate n109_kaggle/n109_tomkodaj.yaml at JoostdeWinter/square-packing aae089c (blob 9f270d76, SHA-256 56b4655f...), side 547464479047171949843/5e19; both clean-room exact methods decide all 109 squares, 436 square-walls, 5,886 pairs: all apart, least margin 2.0e-15 (square-59, square-69), 2 exact wall contacts (corners of square-38 left, square-63 bottom), top slack 5.83e-21, right 3.68e-15. Claim 10.949289580944 is the 12-place ceiling and is accepted directly (S1e); the issue body's 10.949289580943 is refused (S1f). 37 of 37 controls as stated; all four priors held.
- Freezes: checker+plan 11:31:47Z (f7fba53, list SHA-256 43fe9989...), findings 11:41:02Z (b65873d, list SHA-256 b41abd08...).
- After the freeze: custody holds against SHA256SUMS (the comment states no YAML digest; zip 403 here). Identity: new arrangement vs T-101 (no symmetry; 56 beyond 0.1); one to one with Samanyu-dev's 109 (37 beyond 1e-3, 5 beyond 1e-2, max 0.0256). Contraction: certificate 1.99e-14; T-101 1.1e-19; Samanyu-dev 1.995e-12 (this lane's exact reading), gain 0.9725 of it, Samanyu-dev shrunk to first contact 5.497e-14 below the certificate (import's reading 5.570e-14). Option D: restatement if Samanyu-dev's unregistered public 109 counts as the predecessor; for the import lane/owner. Significance: S3 confirmed. main's witness-corners adapter refuses ids square-0..square-108 (F13).
- Not done here (registry records): verifiers.yaml registration of r1012 programs, evidence entry, external_review mapping; for the import lane.
