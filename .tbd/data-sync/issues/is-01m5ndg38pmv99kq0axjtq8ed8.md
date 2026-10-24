---
type: is
id: is-01m5ndg38pmv99kq0axjtq8ed8
title: "Address PR #758 review A (A1-A16)"
kind: task
status: in_progress
priority: 2
version: 3
delegate: c-fix-758-1023
labels: []
dependencies: []
parent_id: is-01m5myjasmbm71pa68wgypjv9s
hold: null
hold_until: null
created_at: 2026-10-23T22:18:26.454Z
updated_at: 2026-10-23T23:22:39.905Z
started_at: 2026-10-23T22:18:43.844Z
---

## Notes

2026-10-23 c-fix-758-1023: review A of #758 addressed.
- Head d7645385283ba99b48f7ad2e3f3236099d8ad407 (git ls-remote agrees). Commits: 52e05acd7 merge main 77aba4c02 (#747, #761); 5f70f06a6 the fixes (site-changelog.yaml + re-rendered CHANGELOG.md); d76453852 merge main 64b316b6c (#762).
- Dispositions reply (marker review=A, head d76453852): https://github.com/jlevy/squares/pull/758#issuecomment-6376713694. A1-A15 fixed against the records cited; A16 deferred to think-vph5 (Phase 1 of #759).
- Beyond the review: T-198/T-199 called "S2 refinements" in the #676/#692 rationale -> "arrangements" (their own rationales); #657 rationale "refinements and re-solves" -> adds "further arrangements" (T-187, T-188); 155/229 "reached the register on 19 October" -> registered 18 October; A10's suggested T-130 sentence narrowed to 175 per T-130's claim.
- Checks at d76453852: render_changelog --check (0 owed, 0 failing, record and view agree); pytest test_changelog + test_news_highlights 77 passed; packing-validate --records 53/53, 274.36 s; release_pin --check ok; check_release_impact ok. Hosted CI all 16 green: runs 40037548651, 40037548637, 40037545407.
- Not done: #657's story has no "since then" line though 154, 204, 271, 303 were re-housed later (stated in the PR's Limits). The first-mention link audit is a scratch script, not a test.
