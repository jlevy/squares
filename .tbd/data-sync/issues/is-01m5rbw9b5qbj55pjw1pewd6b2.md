---
type: is
id: is-01m5rbw9b5qbj55pjw1pewd6b2
title: "PR #801 (merge): senior review A of the deficiency rows (Daniel, Fang Theorem A)"
kind: task
status: closed
priority: 2
version: 4
delegate: c-rev-801-1024
labels:
  - result-import
dependencies: []
parent_id: is-01m5qsa0zpbykjt72q42fhz1fw
hold: null
hold_until: null
created_at: 2026-10-25T01:47:52.036Z
updated_at: 2026-10-25T02:12:53.726Z
started_at: 2026-10-25T01:47:57.044Z
closed_at: 2026-10-25T02:12:53.726Z
close_reason: "Review A of #801 posted (issuecomment-6392315606): approve once A1-A3 are fixed; S3; addressed by c-import-797-1024."
resolution: null
duplicate_of: null
---

## Notes

2026-10-25 c-rev-801-1024: Review A (senior, round 1) of #801 at a3e826606 (base 755ef426b) published as PR comment https://github.com/jlevy/squares/pull/801#issuecomment-6392315606. Verdict: approve once A1-A3 are addressed; 0 Blocker, 0 High, 3 Medium (A1 tail_100 in fang_theorem_a.comparisons computes 4*200-7 for 4*100-7, flag still true; A2 significance S2 -> S3 with News draft or omission; A3 comparisons.json not recomputed in CI, ~3 s), 4 Low (A4 truncated occurrence note 'reported on'; A5 a435c97 decline wording, k = 32 checked; A6 complementary_case wording; A7 tie limit() to H(1/b)), 1 suggestion (A8). All per-k counts, T-163 window, Lean bridge, credit order (activity API), custody and licences confirmed.
