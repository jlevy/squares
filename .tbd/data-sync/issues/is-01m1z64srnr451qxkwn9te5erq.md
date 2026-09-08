---
type: is
id: is-01m1z64srnr451qxkwn9te5erq
title: Integrate the newly merged 324-case atlas into the v0.2.4 explainer PR
kind: task
status: in_progress
priority: 2
version: 4
labels: []
dependencies: []
created_at: 2026-09-08T00:19:33.268Z
updated_at: 2026-09-08T00:46:41.995Z
---
Continue PR #117 via merge-upstream after main advanced from373beb36 to28696526 during final closeout. Review upstream and local overlaps, merge without losing the revised opening, Figure1/2 numbering, framework box, representative lower bounds, and Figure5/touch fixes; regenerate publication artifacts for the enlarged atlas with v0.2.4 fixed. Use three independent integration reviews, run the required local and hosted checks, rebuild/open the web and PDF, update the PR and close/sync all completed beads. Do not merge PR #117.

## Notes

Merged main 28696526 in cef19bfe, then regenerated both atlas families and three claim documents in 87ac7ea9. Publication version remains v0.2.4; pinned atlas/claim content revision is cef19bfe. Exactly 12 publication files changed in regeneration; no mathematical records, witnesses, individual renderings, certificates or verifiers changed. Recovery: the first geometry build completed in 263.76s but a protected macOS timing wrapper stripped the Cairo library environment before export. The redundant retry was stopped during compute; the generator export functions completed against saved SVGs in 12.73s and claims regenerated in 0.84s with the environment applied directly to project Python. All three known-best checks, including the whole 324-case rebuild, passed in 558.37s. The new Figure2 star-count regression and five related tests passed. Visual review caught the longer atlas caption crossing a page; a concise caption preserves both PDF links and all mathematical/source meaning and now fits with the figure on page4. Independent prose review accepted it; strict desktop/phone/touch/print checks passed. Upstream live deployment verified 29/29 at 28696526. Remaining: finish publication/pre-push tests, commit caption, push, finish hosted checks, reopen final previews, and sync beads.
