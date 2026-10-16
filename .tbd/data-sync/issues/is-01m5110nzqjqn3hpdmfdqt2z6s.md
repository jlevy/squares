---
type: is
id: is-01m5110nzqjqn3hpdmfdqt2z6s
title: "After stack #632 deploys: run check_published_site and, if the deploy lands after 15 October, correct v0.7.11 first_published in release.py and regenerate the URL registry (#627 review B3)"
kind: task
status: in_progress
priority: 1
version: 4
delegate: user-eb-intake-residue
labels:
  - result-import
dependencies: []
parent_id: is-01m50gnwbxd5kxbynyx9nd162p
hold: null
hold_until: null
created_at: 2026-10-16T00:15:29.783Z
updated_at: 2026-10-16T06:04:28.694Z
started_at: 2026-10-16T05:13:40.781Z
---

## Notes

2026-10-16 ~06:00Z user-eb-intake-residue (lane A, think-mu5v): done on branch claude/intake-2026-10-16-residue, commit 1f3f54c44 (PR to follow).
Deployment: stack #632 reached main as bbc12b6173983af4e20c889db28fb9e0ca43a28b (the merge of #631, 2026-10-16T01:17:34Z). Its first Pages deployment is 7108522265 (sha bbc12b61, created 01:25:16Z, success 01:25:34Z, run 38834331641); it is the first deployment whose release.py carries v0.7.11 (the previous one, 22a67ce4a at 2026-10-15T21:20:56Z, has v0.7.10 at the head). The current deployment of main is 7110828510 (e2e018f32b2627a7d4b38ed95790bee145b1524a, success 2026-10-16T04:23:12Z, Pages run 38849809939), which contains #632.
check_published_site --commit e2e018f32b2627a7d4b38ed95790bee145b1524a, from packing/ with project Python: run 1 (05:42:54Z to 05:49:01Z, PLAYWRIGHT_BROWSERS_PATH=/opt/pw-browsers) 4509 of 4511 passed, exit 1. Both failures were environment: /opt/pw-browsers has chromium_headless_shell-1194 and the project's Playwright 1.62.0 needs build 1234 (forwarders' arrival and workbench startup could not launch a browser). After python -m playwright install chromium-headless-shell into scratch (PLAYWRIGHT_BROWSERS_PATH=<scratch>/laneA/pw-browsers), run 2 (05:50:17Z to 05:56:34Z): 4519 of 4519 checks passed, exit 0, no skips reported. Receipts: scratchpad laneA/check_published_site.log and check_published_site-2.log.
Correction: the deploy landed after 15 October (UTC, the history's rule), so v0.7.11's first_published is now 'October 16, 2026' in packing/src/sqpack/release.py, and the comment above PUBLICATION_HISTORY records the deployment. URL registry: python -m devtools.site_urls --check reports 1012 rows, 0 failures, before and after, so regenerating it changes nothing (result pages take their first_published from each result's registered date, not the edition). Release impact: a site no-public-change record (no page prints a non-head edition's date). Close this bead when that PR merges; no record names it.

2026-10-16 06:08Z user-eb-intake-residue: the correction is in draft PR https://github.com/jlevy/squares/pull/647 (head 1f3f54c44). This bead waits on that PR's merge, then closes; the title's #632 is a stack number, not an issue, and #627 merged.
blocked_on: jlevy/squares#647
