---
type: is
id: is-01m3xj6w3z3jbrc3yrc1ddc1vj
title: "First paper: v0.4.3, a patch revision for its changes since the v0.4.2 deployment"
kind: task
status: closed
priority: 2
version: 4
spec_path: docs/project/specs/active/plan-2026-09-29-github-pages-overview.md
labels: []
dependencies: []
parent_id: is-01m3p52z585a2zb9jmy19b0r96
created_at: 2026-10-02T05:43:18.909Z
updated_at: 2026-10-02T05:56:49.645Z
closed_at: 2026-10-02T05:56:49.644Z
close_reason: "Merged as jlevy/squares#303 (commit 660e5a3a5): the first paper is v0.4.3, first published October 1, 2026 (the deployment f9a3409f0 at 2026-10-01T08:01:58Z, the first to hold the last substantive change, d205561f0). Its sentence: 'The settled-case revision: the frontier update records T-060's proof that s(11) is Trump's side, Figure 3 marks the endpoint, T-026 is rated V3/C3, and the raised n = 12 and 17 bounds are noted.' v0.4.2, v0.4.0 and v0.3.0 untouched; the PDF stays 22 pages; TUTORIAL names v0.4.3."
resolution: null
duplicate_of: null
---
Owner, 2026-10-01, answering the question from jlevy/squares#301 (the article changed in substance after the v0.4.2 deployment under the v0.4.2 label: the T-060 frontier update of 30 September, 249d42c37; the V4/C5 to V3/C3 regrade, d205561f0; Figure 3's verified mark; the n = 12 and n = 17 supersession footnote): 'it could be a patch revision to the paper itself'. So the first paper becomes v0.4.3: a new entry at the head of EXPLAINER_HISTORY in packing/src/sqpack/release.py saying what changed in the paper, dated by the UTC day that content was first live on the site (read from the Pages deployments), following the procedure #301 put in development.md. The paper's front reads v0.4.3 (version history); v0.4.2 and earlier stay as published. The PDF must stay within its page-count guard (22), so the sentence is at most three lines in the version history.

## Notes

State, 2026-10-02 (branch claude/explainer-v0.4.3, draft PR; not closed):

- `EXPLAINER_HISTORY` gains v0.4.3 at its head. Sentence: "The settled-case revision: the frontier update records T-060's proof that $s(11)$ is Trump's side, Figure 3 marks the endpoint, T-026 is rated V3/C3, and the raised $n = 12$ and $17$ bounds are noted." Three lines in the paper's version history; the PDF stays at 22 pages.
- What changed in the paper since the v0.4.2 deployment, from `git diff -M c19e6c0e2 main` on the article: the September 30 frontier update (249d42c37), the V4/C5 to V3/C3 regrade under the ladder of 2026-09-30 (d205561f0), Figure 3's verified endpoint mark and aria text (2c1afe6b0, 7862dc3e8), the footnote on Evan Daniel's n = 12 and the n = 17 line (a6f630dd7), and the consequent wording ("what was then the smallest open case", "two of which others have since raised"). Site chrome (the FRONT_MATTER slot, the slug's paths, the film's v0.4.2 release links) is not listed.
- Date: October 1, 2026, the UTC day of Pages deployment f9a3409f0 (2026-10-01T08:01:58Z), the first to hold d205561f0, the last substantive change. The T-060 update was live from d44ec0408 (2026-09-30T17:44:28Z); the cosmetic changes after it (9b459da65, 97e4069d5) first deployed on October 1 (f25a85cb5, 23:21:58Z) and October 2 (f1575dbb7); the substantive day is the one recorded, in the comment above the history.
- v0.4.2, v0.4.0, v0.3.0 unchanged. TUTORIAL says "the standalone v0.4.3 explainer"; README unchanged. `EXPLAINER_REVISED` unchanged (the article did not change). development.md's paragraph on the paper's history names v0.4.3 as the paper's first number of its own.
- test_release holds v0.4.3's date and that its sentence names T-060 and V3/C3.
