---
type: is
id: is-01m5fw6v3p9gb2jgen89a2ncs8
title: Separate account profiles from website and repository resources in directory
kind: task
status: closed
priority: 2
version: 3
delegate: about-profiles-implementation
labels: []
dependencies: []
parent_id: is-01m5fpv2yk09g6z1a17rts4wzc
hold: null
hold_until: null
created_at: 2026-10-21T18:40:05.225Z
updated_at: 2026-10-21T20:21:40.773Z
started_at: 2026-10-21T18:40:15.329Z
closed_at: 2026-10-21T20:21:40.773Z
close_reason: |
  Completed and pushed on PR #578 at commit 7b566ae73: https://github.com/jlevy/squares/pull/578 . The PR remains unmerged; hosted CI and final integration acceptance remain tracked by think-zpfo.

  The shared presentation now includes full-name, surname-sorted directory rows; a 16rem Name floor with natural resource wrapping and responsive wide-table scrolling; separate Results, Records, Credits, Resources and Accounts; visible account usernames and filtered additional Handles; normal theme foreground for primary content; full names in About narrative; nested-page breadcrumbs; shared resource cards ordered title, byline, source URL, description, tally; shared GitHub/X/navigation icons; muted parenthetical significance breakdowns; and a deduplicated directory summary. Formalization support remains explicitly labeled Contributors, preserving Lewis and Julian-JJ support roles and evidenced 2026 activity rather than inventing primary authorship.

  Final validation receipts: the retained 77-case rerun had 76 passing cases, and its remaining parser case passed separately in 8.05 seconds; all 53 UI cases and all eight profile design cases pass. Ruff, Biome and touched Python source/test types pass. Final assembled preview passes 7,294 of 7,294 publication checks. The resolved-destination audit scans 692 HTML pages with zero broken profile links and zero profile-label mismatches; it parses quoted and unquoted hrefs from each containing page. Live HTTP verifies corrected case-page profile destinations. Results-page projected size is 1,245,084 bytes under the unchanged 1,250,000-byte ceiling; T-174 is 277,778 bytes under 300,000 and case 17 is 501,484 bytes under 550,000.

  Preview: http://127.0.0.1:8790/profiles/index.html?layout=names-16rem . Output: /Volumes/spud-ext2/agent-scratch/about-profiles-20261020/site-integrated-reviewed . Evidence in the same scratch parent: integration-reviewed-site-check.log, integration-reviewed-profile-name-audit.json, integration-reviewed-final-live-links.json, profile-integration-test-fixes-types.log and profile-design-roles-overflow-focused.log. The four PDFs have valid profile annotations; the revised explainer retains all seven links. Atlas diagram person-link annotations remain deferred under think-wwav; historical population, uncertain identity and record-family follow-ups are not closed by these UI receipts.
resolution: null
duplicate_of: null
---
Keep directory Links for public account profiles (GitHub user, X and equivalent account profiles). Move personal/publication websites and project repositories into Resources, visibly rendered as domains or owner/repo with appropriate shared icons. Reuse individual-profile resource/account components and canonical resource inventory; avoid duplicates and preserve direct navigation. User request supersedes earlier all-link table column.
