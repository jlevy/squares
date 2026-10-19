---
type: is
id: is-01m5a76wv61fxeqx07z0m0wz5m
title: Preserve prior source-checker samples in historical mixed evidence prose
kind: bug
status: open
priority: 2
version: 1
delegate: codex@spud10
labels: []
dependencies: []
parent_id: is-01m5a1wv68nj53kemkw4t6ws0p
created_at: 2026-10-19T13:56:54.757Z
updated_at: 2026-10-19T13:56:54.757Z
---
Deferred C1 (Low), discovered in source-only reporter follow-up at e062abfacfef60aa160ccd7b177c5b29eb31c2f8. Trigger: regenerate evidence_entry for historical wand125-mixed-bounds-check2-2026-10-06/mixed_n29_L581. packing/devtools/sqverify_fast_census.py:1568-1572 unconditionally says the source checker was not run here on this certificate, while packing/frontier/evidence.yaml:27532-27536 records partial C++ reproduction at nodes 0, 1, 364 and 415. The identical terminal sentence is present at original reporter base 8f2d7981528fd31efd3af557cd367cc9741ba66e:1350-1352 and previous reviewed 5bced23963676b296b9aed9685184fd290c7df62; e062abfac changes neither it nor the scientific decision. B1 relationship correction and B2 unavailable-timing correction are accepted separately. Required fix: derive or qualify source-checker replay prose by retained case-specific history; do not deny known partial reproduction, claim a complete replay, or change its producer-code relationship. Required regression: render historical check2 mixed_n29_L581 evidence and assert its known partial reproduction is preserved or the unsupported no-run assertion is omitted; retain current fine-net shared-components and truthful own-checker wording. No source fix, historical regeneration, new native run, or publication was performed by this review. Root will generate only newly reviewed current fine-net certificates until this deferred issue is addressed. Review child think-povw; report .codex/intake-resume-20261019/fine-net-reporting-b1-b2-followup-review.md.
