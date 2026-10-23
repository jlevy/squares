---
type: is
id: is-01m5ner2jepdx1mbwdmcp9je3d
title: "Post-merge: test_site_drawing_hover still expected atlas/house/n-11.svg after flip regularization"
kind: bug
status: closed
priority: 2
version: 3
delegate: claude-orientation-coordinator-u2p5tx
labels: []
dependencies: []
hold: null
hold_until: null
created_at: 2026-10-23T22:40:16.462Z
updated_at: 2026-10-23T23:13:38.785Z
started_at: 2026-10-23T22:40:20.021Z
closed_at: 2026-10-23T23:13:38.782Z
close_reason: "Fixed by PR #762 (merge 64b316b6c). Main's post-merge Packing validation run 40034964765 passes test_site_drawing_hover; its remaining failures (test_site_ladders 57 errors, test_site_text_tokens 3, test_site_wide_blocks 6) match the run at 7cd0a94bf before #761 exactly."
resolution: null
duplicate_of: null
---
Main's post-merge Packing validation at 77aba4c02 (merge of #761) failed test_cached_svg_loads_the_complete_declared_artwork in packing/tests/test_site_drawing_hover.py: every atlas tile now starts on atlas/regularized/n-N.svg (regularization policy section 13), but the test asserted atlas/house/n-11.svg. PR CI skips this browser suite, so it surfaced only post-merge. Fixed in PR #762 (merged 64b316b6c); close once main's post-merge run shows the test passing.
