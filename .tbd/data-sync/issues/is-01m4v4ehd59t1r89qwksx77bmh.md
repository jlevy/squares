---
type: is
id: is-01m4v4ehd59t1r89qwksx77bmh
title: "Merge the n = 17 stack (#560, #571, #577) and later landings of main into PR #578"
kind: task
status: in_progress
priority: 2
version: 20
spec_path: docs/project/specs/active/plan-2026-10-10-contributor-profiles.md
delegate: profiles-final-merge
labels: []
dependencies: []
parent_id: is-01m4kvnfe7f9nak96hc7bgdwer
hold: null
hold_until: null
created_at: 2026-10-13T17:20:02.981Z
updated_at: 2026-10-18T09:14:59.084Z
started_at: 2026-10-13T17:20:09.838Z
---
Watch origin/main and merge it into the profiles branch, keeping both the Overbeck and Hosono renames, reconciling the census and regenerating views. Stack merged in 37b1c8bf7.

## Notes

Latest 15 October integration completed at fb3f3e351 on draft PR #578. Merge c474bef45 incorporates 94 additional upstream commits through 3685616df, resolving 12 conflicted files; combined recent integrations incorporate 405 commits. Numeric records, verification levels and archived sources are preserved. Release declarations retain upstream site v0.7.12 and proposed v0.8.0, with exact no-public-change scopes checked. All 31 active hosted checks pass on final head; gh pr checks --watch exited 0 with no failed or pending jobs, including overview, all behavioral suites, frontend, PDF and cross-browser checks.

Profiles and News preserve preferred-name links: 45 reviewed links across 27 News entries. Census: 27 profiles, 1376 structured spans, 1052 resolved, six non-person, 318 unresolved, 146 PDFs pending. URL registry 1061 rows, zero failures. T174 now299477 bytes under unchanged300000 ceiling with equivalent parsed HTML; 61 result tests and14 markup preservation tests pass. Two quote-sensitive assertions were converted to structural checks, both reproduced and passed locally and in final CI. Original edit run passed66 of67 steps; its sole merge-baseline prerequisite passed after committing. No claim that the original invocation was green.

Independent Astra review has no remaining findings. Rendered design QA passes16 desktop/mobile and light/dark contexts and10 navigation checks; shared sans-serif uppercase H1s, typography, overflow and clipping checked. Directory and News links navigate directly to profiles. The stale design-guide directory contract was corrected. Preview built and opened in the default browser at http://127.0.0.1:8791/profiles/index.html; server remains running and result pages refreshed without pruning profiles. Plan and PR capture handoff. This recurring upstream integration bead returns to open for future landings; remaining profile population stays in think-m7il. PR remains draft and unmerged.

2026-10-18 intake follow-up: fresh review A at e1f921bf09d6387fc27302b367cb4b1114b89082 recovered the originating independent senior review and browser evidence. Current-head standard CI:31 success,28 skipped; full checkpoint38857828303 passed14 jobs at77fe330dd. Main has284 commits after the integrated e2e018 base and now conflicts. High integration blocker and Low stale PR description remain; retain think-m7il for population. Review: https://github.com/jlevy/squares/pull/578#pullrequestreview-5562243378 . No merge authorized or performed.
