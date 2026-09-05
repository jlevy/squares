---
type: is
id: is-01m1qhd3b0mx15h7nmmr6ykxb2
title: "Proof card: the tweet-length statement of s(11) >= 3.81 with its hash and the shortest verifier"
kind: task
status: closed
priority: 1
version: 3
labels: []
dependencies: []
parent_id: is-01m1qcc9devr6mz0m6erxswxjc
created_at: 2026-09-05T01:02:24.096Z
updated_at: 2026-09-05T01:35:23.114Z
closed_at: 2026-09-05T01:35:23.114Z
close_reason: Ported/delivered (cherry-picked from the sub-agent worktree commits 4d38a9ed, ae86a17b; the card's standing sentence brought to C5 on integration, which its own test caught).
resolution: null
duplicate_of: null
---
The operator wants the most minimal, self-contained, independently verifiable form of the s(11) >= 381/100 proof: the theorem and the counting argument stated in tweet length (the certificate's parameters -- 1121 nonnegative weighted points in the side-3.81 container, total weight below 11, every admissible shrunken square at any of the 181 net angles covering weight at least 1 -- so eleven unit squares cannot fit), the certificate's SHA-256 and where to fetch the bytes, and the shortest correct standard-library verifier that decides those bytes from the theorem statement alone. Deliverables: a one-screen proof card in the case package, a verifier well under 150 lines with no dependencies, and a check that the card's figures and hash are derived from the artifact (check_rung_figures or a test). Pairs with think-4iej (minimal_verify.py) and think-rph2 (the proof note).
