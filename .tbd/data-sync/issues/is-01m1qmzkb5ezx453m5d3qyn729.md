---
type: is
id: is-01m1qmzkb5ezx453m5d3qyn729
title: Declaration guards in the n = 12, n = 17 and n = 20 replays, and the cross-links that never followed the verifier
kind: task
status: open
priority: 1
version: 1
labels: []
dependencies: []
parent_id: is-01m1qcc9devr6mz0m6erxswxjc
created_at: 2026-09-05T02:04:56.037Z
updated_at: 2026-09-05T02:04:56.037Z
---
Found by the residual audit of PR 80. (a) F4 landed on the n = 11 replay only (7907bd67): packing/cases/n{12,17,20}_fractional_certificate/__main__.py and replay.py still check total_mass alone and can print VERIFIED while the declared claim or least_cell_mass describes another theorem; PR 80 adds the claim and least_cell_mass refusal and a byte re-read to all three (git diff HEAD 04127189 -- 'packing/cases/n1*_fractional_certificate/__main__.py' 'packing/cases/n*_fractional_certificate/replay.py' packing/tests/test_fractional_certificate.py; its tests test_n{12,17,20}_replay_refuses_declared_value_drift and ..._refuse_a_file_changed_during_verification). Port them; keep the tests fast by stubbing the sweep as the n = 11 tests do. (b) t-018-proof.md and thirdparty/README.md still describe only the 19/5 package and never name minimal_verify.py (8cc52ae7) or PROOF-CARD.md; TUTORIAL.md does not embed t-018-proof-visual.svg. Three edits. (c) conventions.md never writes down the rule the branch follows everywhere: C0-C5 are the confirmation rungs of epistemics.md; numbered proof obligations are Condition N; add it (PR 80's wording is in git diff HEAD 04127189 -- conventions.md) with the t-018-proof.md filename convention. (d) tests/test_certificate_reach.py BAND = 0.005 while the renderer's prose claims 'within 0.001'; tighten the test to guard the sentence. (e) F5 (think-43pf) is the same package README: fold it in.
