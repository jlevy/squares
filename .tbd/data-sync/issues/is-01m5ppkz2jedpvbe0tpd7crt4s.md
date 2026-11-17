---
type: is
id: is-01m5ppkz2jedpvbe0tpd7crt4s
title: "PR #781 (merge): follow-up review B of review A's fixes (A1 evidence entry, the test_house_adoption guard edit)"
kind: task
status: closed
priority: 1
version: 5
delegate: c-rev-781b-1024
labels: []
dependencies: []
parent_id: is-01m5khvjtdjf8q14f59bmd8c1k
hold: null
hold_until: null
created_at: 2026-10-24T10:17:04.850Z
updated_at: 2026-10-24T11:18:00.135Z
started_at: 2026-10-24T10:17:12.801Z
closed_at: 2026-10-24T10:34:45.293Z
close_reason: "Review B posted https://github.com/jlevy/squares/pull/781#issuecomment-6383157716 at 8241aa881: approve (B1, B2 Low; B3, B4 suggestions); A1's fix and the guard-test edit verified; addressed with the #736 main merge by c-fix-781-1024."
resolution: null
duplicate_of: null
---

## Notes

Review B (follow-up, round 2) of #781 published by c-rev-781b-1024 at head 8241aa881, base b2ea7b09c: https://github.com/jlevy/squares/pull/781#issuecomment-6383157716. Verdict: approve. Dispositions A1-A7 all hold; A1's discharger is well formed, its four-count scope honest, the note chain 3 with the replay and 0 without; receipt re-run identical to the committed receipt and to the 14 Oct outputs. Guard edit eba2bc491 narrows one named citation at 241/T-182 and 273/T-174 without weakening the guard. #787 merge kept both sides. Findings: B1 (Low) replayed bytes bind to PIECES.md by name only (binding holds by data-line identity with the Lean packet copies; record and test it); B2 (Low) #603 draft's 'a read raises confirmation, not verification' and its '2 to 3 CPU-hours' vs the record's 1.5 to 3. Suggestions B3 (pin real atom rank in the discharge test), B4 (rewrap three folded lines). Records tier 53/53 incl. bead tree, 218.8 s; tests 21+9+111+92 passed. Not synced (brief).

## Review B addressed, 2026-10-24 (c-fix-781-1024, worktree /home/user/wt-781)

Head 1f2b930e927e7afc34131d19b75c5c87107692fd (ls-remote agrees); hosted CI green there (Packing validation 40088493642, Certificate page 40088493641, Branch mergeability 40088490617; 31 pass, 28 skipped, 0 fail; MERGEABLE). Dispositions reply: https://github.com/jlevy/squares/pull/781#issuecomment-6383557187. PR body refreshed.

Commits: d86d9ff7c (B1 limitations and test piece_bindings: Daniel's 7 by PIECES.md SHA-256, 11 by data lines = Lean copies with those digests; B3 check_results.verification_level used by _supported_rung and the discharge test; B4 rewraps), 2cded21a2 (merge main f354a34f5, #736; conflict only DATA_REVISION), 480c44021 (re-pin to 2cded21a), 3d96fba0a and 1f2b930e9 (papers' record: check_results.py added to its paths, re-measured at 3d96fba0 with main's five inputs swapped in, 69 files byte-identical x3). B2: think-494l's #603 draft reworded to the conditional-proof reason and "about 1.5 to 3 CPU-hours" (local, not synced); PR body cost matched.

Validation: packing-validate --records all steps pass incl. bead tree (147 s); 16 focused modules 715 passed; stamp_landed nothing to stamp; release_pin and check_release_impact pass.
