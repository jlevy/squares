---
type: is
id: is-01m5nvephbmqvk0ace4vzerhg9
title: "Take over PR #736 (home page News box) on the owner's word: merge main, resolve without redesign, verify a strict improvement compatible with later design choices, review, merge"
kind: task
status: in_progress
priority: 2
version: 9
delegate: c-sync-736-1024
labels: []
dependencies: []
parent_id: is-01m5khvjtdjf8q14f59bmd8c1k
child_order_hints:
  - is-01m5p11e8qrfgfcsfpsj05t55a
hold: null
hold_until: null
created_at: 2026-10-24T02:22:20.715Z
updated_at: 2026-10-24T09:51:15.287Z
started_at: 2026-10-24T02:22:34.759Z
---

## Notes

2026-10-24 coord-intake-1023: OWNER (in conversation, 24 October). Asked whether to take over #736 (the site agent's home page News box: reviewed twice, last pushed 06:42Z on 23 October, now 225 commits behind main and conflicting; earlier "No, leave #736 to the site agent"), the owner selected "Take it over (Recommended)", then added: "Review carefully and make sure it's a strict improvement that we can land. And that it's compatible with the other design choices we've made".

2026-10-24 c-take-736-1024: #736 brought to main 14b14f2d1 at head 17a264be0 (merges 3f4cc4f7f of da117ad0b, six conflicts resolved keeping main's change and the PR's intent; 95ac0de5e of 14b14f2d1, clean). Landing record: n=204 T-231 (2026-10-24) and mishapolk-issue732-2026-10-22 (2026-10-23) backfilled from history, audit 0 differ. Re-pinned DATA_REVISION to 3f4cc4f7; papers' no-change record re-measured twice, 69 files byte-identical. One design adaptation, 08510a595: #746's small-chooser rule (one size, 24px, centered capitals) failed hosted frontend on the compact filter's 0.85 scale; the scale is dropped and the lighter weight kept. Hosted CI at 17a264be0: 31 pass, 28 skipped, 0 fail (Packing validation 40059305228); MERGEABLE CLEAN. PR body updated with the compatibility table and the main-versus-branch comparison. Draft; not merged; ready for the independent review.

2026-10-24 coord-intake-1023: the independent review (B, https://github.com/jlevy/squares/pull/736#issuecomment-6379937834) approves. Decisions for the final sync, after #750, #757 and #766 merge:
- B1: drop `FRESH_DAYS`, the 30-day freshness rule. No owner answer sets it; the owner's words were "preselected to S5 when there are enough S5 items for the box, else S4+S5". Match them, and correct the attribution in paper-design.md and news_highlights.py.
- B3: Recently Added's intro becomes "[News](news.html) has the stories rated S3 and above." (owner's 23 October S3+ rule).
- B4: clarify the live-count sentence.
- B5: fold the duplicate SOURCE_COVERAGE into the papers' re-measure.
- After each preceding merge: `stamp_landed --backfill --apply`, not plain `--apply`, then re-pin. After #757, re-measure the papers' record.

2026-10-24 c-sync-736-1024: final sync of #736 done; head 8e3692a31 (draft, MERGEABLE CLEAN, labels S2 and project).
- Merges of main: b3f67a02d (e5c1c64e3, #745 to #771; one conflict, release.py DATA_REVISION, main's taken) with stamp_landed --backfill --apply (11 entries, all 24 Oct UTC: 303 at T-239 #757, nine algebraic houses #756, mishapolk-issue732-f1ceee4 rows #769; checked against ADOPTED at merge parents); 9688cd628 (6808d293a, #787, clean); 8e3692a31 (b2ea7b09c, #788, clean). Re-pin 252c64ba4 to b3f67a02d.
- Review B fixes c0ce843f9: B1 owner's S5 rule, FRESH_DAYS and record_reference dropped, attribution corrected; B2 option (a), house_moves drops a landing whose result is not a verified upper-bound holder; B3, B4 as worded; B5 duplicate SOURCE_COVERAGE removed. Papers re-measured 5c71b2f94 at link revision c0ce843f: 69/69 byte-identical, retain v0.4.25, v0.1.11, v0.1.4, v0.2.7.
- Dispositions: https://github.com/jlevy/squares/pull/736#issuecomment-6382731191. PR body updated.
- Hosted at 8e3692a31: 31 pass, 28 skipped, 0 fail (Packing validation 40082304617 after re-running validate once the coordinator fixed think-3oxz; Certificate page 40082304588; Branch mergeability 40082301179).
- Site comparison main 6808d293a vs branch 9688cd628: 710 of 711 pages identical masked; home sections identical except Recently Added (new) and News (same three visible cards byte-identical, six carried hidden), plus results.css link and news-filters.js tag.
- Open, outside the branch: tests/test_beyond_horizon_replay.py::test_the_receipts_records_and_coverage_rows_hold runs 42-45 s on most hosted runs against the 45 s backstop (failed suite-c at 5c71b2f94 at 45.07 s; 44.19 s on main's push at e5c1c64e3).

2026-10-24 coord-intake-1024: c-sync-736-1024 finished at head 8e3692a31 (main b2ea7b09c merged): B1-B5 fixed in c0ce843f9 (dispositions https://github.com/jlevy/squares/pull/736#issuecomment-6382731191), papers' record re-measured (5c71b2f94), DATA_REVISION re-pinned (252c64ba4), landings backfill 11 entries in b3f67a02d; hosted CI green (Packing validation 40082304617 after a re-run of the bead-tree step the coordinator's closures had broken, Certificate page 40082304588, Branch mergeability 40082301179); 710 of 711 HTML pages identical to main's, index.html 579,134 bytes (budget 1,300,000), box 55,692 of 64,000. Because the owner asked for careful review, a follow-up review C (think-s2dw) checks the fixes and merges before the merge. Slow test found: think-zjls.
