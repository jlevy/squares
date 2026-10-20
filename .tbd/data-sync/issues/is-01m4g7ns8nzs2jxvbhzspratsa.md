---
type: is
id: is-01m4g7ns8nzs2jxvbhzspratsa
title: "OR-1: turn the X-051 centre-survivor and triple replays into a devtools tool with tests"
kind: task
status: open
priority: 2
version: 3
spec_path: docs/project/reviews/review-2026-10-06-n17-w3-consolidation.md
labels:
  - n-17
dependencies: []
parent_id: is-01m4fwn82ckcw51qg67t4xtvsm
hold: paused
created_at: 2026-10-09T11:44:47.380Z
updated_at: 2026-10-13T00:55:29.315Z
---
H-328's instrument is two python -c replays in X-051 §3.1/§3.2 (build_model+check_primal over X051-centre-survivors/centre-survivors.json; exact Fraction triple minimum 562823713/423200000 over 2,024 triples). Per OR-1 and Review B (pullrequestreview-5469544287 B1), move both into packing/devtools/ with a test (triple minimum fast; 96-vector replay slow with a measured registry entry), set H-328 instrument_ready true, and register a W6 round that replays them.

## Notes

2026-10-13 owner decision: suspended pending Overbeck's proof that s(17) = L (#557; registered as T-153 by #560, credited by #571), which likely subsumes new s(17) research. Resumes only if the owner lifts the suspension, for example if T-153's replays and reviews find a gap or the candidate is withdrawn. OR-1 tool for X-051's centre-survivor and triple replays (H-328): an instrument built for the n = 17 proof.
