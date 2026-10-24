---
type: is
id: is-01m5nvt5g3enrh90fphg6y7rwt
title: "PR #750 (merge): senior review"
kind: task
status: in_progress
priority: 2
version: 3
delegate: c-rev-750-1024
labels: []
dependencies: []
parent_id: is-01m5khvjtdjf8q14f59bmd8c1k
hold: null
hold_until: null
created_at: 2026-10-24T02:28:36.483Z
updated_at: 2026-10-24T03:08:06.048Z
started_at: 2026-10-24T02:28:43.524Z
---

## Notes

2026-10-24, c-rev-750-1024 (coordinator coord-intake-1023): senior review A, round 1, of PR #750 at head d8d5c6774bf1a8f519457aa2e3d682b2487b062f, base 5664ac1e8e752ec4f4c00e7ffac22ff53e25a929 (merge base with main). Posted as a PR comment: https://github.com/jlevy/squares/pull/750#issuecomment-6379115396 (marker `<!-- tbd:review v=1 id=A kind=senior pr=750 round=1 head=d8d5c6774bf1a8f519457aa2e3d682b2487b062f base=5664ac1e8e752ec4f4c00e7ffac22ff53e25a929 -->`). No earlier tbd:review marker existed on the PR.

Verdict: approve with fixes; nothing blocks merge. No Blocker or High findings.
- Medium: A1 (declared AI assistance missing or not in the source's terms in T-234, T-235, T-236, T-238; attribution.md:37-38) and A2 (T-238's headline and claim say "proved in Lean 4 twice" in the record's voice at V0/C0; Daniel's Lean states no s(n)). Both should land before merge.
- Low: A3 (credit chains of the two wand125 Lean keys drop the cover keys' antecedents; Ryu credited on T-236), A4 (T-237's C1 and C3 named in next_rung, no unfinished_confirmations or bead), A5 (T-237's wording on what n-002 to n-005 rest on), A6 (News "each checked by Lean's kernel"; the announcement's "2 new results ... (verified)" for a 1979 value is the owner's call), A7 (lean_closure: no `decide +native` escape pattern; origin URL written verbatim; srcDir).
- Suggestions: A8 (check_rung_figures lookbehind misses √), A9 (cite the S3 precedent as T-006/T-008's own rationales).
- T-237 kind, V3/C0 and S3 judged right; [Friedman DS7] entry and index edit judged faithful and minimal; T-238 kind and one-entry form right; T-234 to T-236 claims match their Lean statements; T-163 unchanged; release records hold; scope rule holds. No dedicated review warranted.

Tests at d8d5c6774 (nice -n 2, 2 workers): test_bound_citations 122 passed; test_lean_closure passed; test_results_register 6 failed, all on contiguity (T-232, T-233); check_results contiguity only; check_standing, check_source_coverage, build_bound_citations --check, check_rung_figures, state_ai_assistance --check, check_release_impact --baseline-ref 5664ac1e8, release_pin --check pass; acquire_source --check PACKET_MATCHES_ITS_CONTRACT for all five packets; merge-tree with main 14b14f2d1 clean.
