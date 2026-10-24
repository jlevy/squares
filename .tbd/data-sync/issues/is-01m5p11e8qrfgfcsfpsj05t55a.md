---
type: is
id: is-01m5p11e8qrfgfcsfpsj05t55a
title: "PR #736 independent review after the takeover (strict improvement, compatibility, the merges)"
kind: task
status: in_progress
priority: 2
version: 3
delegate: c-rev-736-1024
labels: []
dependencies: []
parent_id: is-01m5nvephbmqvk0ace4vzerhg9
hold: null
hold_until: null
created_at: 2026-10-24T03:59:57.719Z
updated_at: 2026-10-24T04:37:43.862Z
started_at: 2026-10-24T04:00:07.200Z
---

## Notes

2026-10-24 c-rev-736-1024: Review B (follow-up, round 3) posted on #736 at head 17a264be0, base 14b14f2d1: https://github.com/jlevy/squares/pull/736#issuecomment-6379937834

Verdict: approve. On landing day it is a strict improvement and compatible with every listed design choice; nothing in the code blocks the merge.

- Strict improvement: every home-page section but News is byte-identical to main 1aa953fad's (assets and version masked). The box's 3 visible cards are byte-identical to main's 3. 700 of the 702 built pages are identical; the 702nd differs only by #759's SYNOPSIS row. index.html is 548,093 against 483,082 bytes (budget 1,300,000). No-script: 3 S5 cards, no strip.
- Landings: all 105 entries re-derived by two methods with 0 differences. T-231 is dated 2026-10-24 (#753) and mishapolk-issue732 2026-10-23 (#742). --audit is vacuous until the merge.
- Findings:
  - B1 (Medium): the 30-day S5 freshness rule is credited to the owner, but no owner answer is recorded; think-aqv8 calls it a coordinator decision. From 13 November the box would show T-194 plus two S4 project stories, where main's shows T-194, T-154 and T-153. The owner's question: confirm the rule, or drop FRESH_DAYS.
  - B2 (Low): a stale house landing renders as a current claim, and Pages would deploy it (the #757 race after this merges).
  - B3 (Low): the intro wording; replace with "[News](news.html) has the stories rated S3 and above."
  - B4 (Low): paper-design.md:1247 describes the live count backwards.
  - B5 (Low): SOURCE_COVERAGE is defined twice; fold the fix into the re-measure #757 forces.
- Landing order:
  - after each of #745, #750, #757 and #766, use `stamp_landed --backfill --apply`, not plain --apply (expected: 303 at T-239 on #757's day);
  - re-pin;
  - re-measure the papers' record after #757 (overview_sections.py) and update "Retain main's v0.4.22..." to the explainer's v0.4.23 or later;
  - re-run the home and News tests, test_site_homepage, check_site_rendering, render_changelog --check and site_urls --check, with hosted CI green.
- Tests: 677 passed (home, News, landing, overview, release and URL suites); test_site_homepage 32 passed in Chromium; browser floor 3/3; all record and release checks pass.
