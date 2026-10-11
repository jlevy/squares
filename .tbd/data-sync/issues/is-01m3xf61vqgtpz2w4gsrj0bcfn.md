---
type: is
id: is-01m3xf61vqgtpz2w4gsrj0bcfn
title: "Papers are individually versioned: the repository's version no longer appears on a paper"
kind: feature
status: closed
priority: 2
version: 6
spec_path: docs/project/specs/active/plan-2026-09-29-github-pages-overview.md
labels: []
dependencies: []
parent_id: is-01m3p52z585a2zb9jmy19b0r96
created_at: 2026-10-02T04:50:26.294Z
updated_at: 2026-10-02T05:41:51.715Z
closed_at: 2026-10-02T05:41:51.707Z
close_reason: "Merged as jlevy/squares#301 (commits 9db42a9f9, ba222a506): each paper has its own version in sqpack.release (EXPLAINER_HISTORY, EXPLAINER_VERSION; the review keeps Draft v0.1.0), written by paper_front; no site version or data hash on a paper page, Markdown edition or colophon. The first paper reads v0.4.2 with a three-entry history (v0.3.0, v0.4.0, v0.4.2 as published; v0.4.1 and v0.5.0 dropped because the article did not change); its PDF stays 22 pages. Owner questions (a new paper version for the changes since v0.4.2; the poster's stamp inside Figure 2; where the site's edition history shows) are on think-cv22."
resolution: null
duplicate_of: null
---
Owner, 2026-10-01: 'And the repository version should not go on the papers anymore. Papers should be individually versioned in the future.' Today the first paper's credits print the publication's edition and data hash ('v0.5.0-971e5f (version history)'), its Version History lists every publication edition including site-only ones (v0.5.0, 'The website edition'), and the site's colophon with the repository version closes each paper and its PDF; the review already carries its own 'Draft v0.1.0'. Wanted: each paper has its own version and its own history in sqpack.release, written by devtools.paper_front; no repository version or data hash anywhere on a paper page, its Markdown edition or its PDF; the site's pages keep the repository version in their footer. This settles the first of #289's four questions on think-cv22 (the review keeps its own version). Done together with think-be7y in one PR, since both change devtools.cut_release and development.md's Cutting an edition.

## Notes

Edition table for the first paper (n11-lower-bounds-explainer), established from git on 2026-10-02 by diffing the article template between each edition's deployment commit (the commits in the comment above `PUBLICATION_HISTORY`): f060b1d78 (v0.3.0), f2e24e07b (v0.4.0), d5b1c2e1b (v0.4.1), c19e6c0e2 (v0.4.2), 8aaa411dc (v0.5.0). The article was `certificate_page.md` at v0.3.0, `explainer-article.md` from ca9013cff to 9b459da65, and `n11-lower-bounds-explainer-article.md` since.

| Edition | First published | What changed in the paper | Kept or dropped |
| --- | --- | --- | --- |
| v0.3.0 | September 5, 2026 | The first edition: T-018's point certificate proves s(11) >= 381/100. | Kept, as published |
| v0.4.0 | September 13, 2026 | The article rewritten around T-025 (191/50) and T-026 (3.8264474...), the 381/100 proof kept as the worked example (904 lines in, 484 out; no T-025 mention at v0.3.0, twelve at v0.4.0). | Kept, as published |
| v0.4.1 | September 22, 2026 | None. `git diff f2e24e07b d5b1c2e1b -- explainer-article.md` is empty. The window's renderer commits are the shared version stamp, the browser-floor refactor and the atlas's bound citations (a4bdfae4c, ad65a52fa, be84f7c8d); the atlas added T-030. | Dropped: a site and atlas edition |
| v0.4.2 | September 28, 2026 | A frontier update (September 22) records Kleddamag's verified s(11) >= 3.875 built on T-026 and presents T-026's bound as historical; the V4/C5 line names T-026; Figure 2's caption marks every recent result and gains the film; the credits gain First published / Last revised (1c27f8408, e070cf1ab, 42fc48fc0, 30222e632, e1ef6cf89, d48006f9c). | Kept, as published; the scope sentence trimmed to the paper's part. A judgement: the proofs did not change, the paper's statements of status did |
| v0.5.0 | October 2, 2026 | None in PR 291 (release.py, posters, claim documents, README, TUTORIAL). | Dropped: the website edition |

Question for the owner: between the v0.4.2 deployment (27 September) and the v0.5.0 cut, the article changed in substance under the v0.4.2 label: the frontier update of September 30 reports T-060's s(11) = 3.8770835... (249d42c37), the T-026 rating moved from V4/C5 to V3/C3 under the ladder of 2026-09-30 (d205561f0), "what was then the smallest open case", Figure 3's verified mark, and the n = 12 and n = 17 supersession footnote (a6f630dd7, 7862dc3e8, 2c1afe6b0). The PR keeps the paper at v0.4.2 (its last published number under which it changed) with "Last revised October 1, 2026", and does not invent a number for those changes; whether they are a version of the paper (v0.4.3, or the paper's own v0.5.0) is the owner's.

Colophon on a paper: the two lines without the version part ("The Squares Project · github.com/jlevy/squares" and "Formatted and typeset with Flowmark and KPress").

State, 2026-10-02 (PR #301, branch claude/paper-versions, draft; not closed):

- Done: `release.py` declares `EXPLAINER_HISTORY` (v0.4.2, v0.4.0, v0.3.0), `EXPLAINER_VERSION`, `EXPLAINER_FIRST_PUBLISHED`; the review keeps `OPTIMALITY_REVIEW_EDITION`. `paper_front` writes each paper's own version; the explainer's Version History is written from its own list; the colophon on a paper is the two lines without the version part (`render_overview.colophon_lines(edition="")`); `check_published_site` holds each paper to its own version and refuses the site's edition on it; `artifact_dates` reads the explainer's first day from its own history; README names the site's edition, TUTORIAL the explainer's v0.4.2; development.md and paper-design.md state the rule. Tests: test_release (the shared editions held to the site's numbers and dates, v0.4.1 and v0.5.0 held out; no paper version carries the stamp or hash), test_n11_lower_bounds_explainer (credits, history exactly the paper's list, no site version or hash in the page's words or the Markdown edition), test_paper_structure, test_render_n11_optimality_review, test_check_published_site, test_cut_release, test_artifact_dates.
- The first paper's PDF stays at 22 pages with the three-entry history.
- Known: the explainer PDF's text layer still contains `v0.5.0-971e5f` once, inside Figure 2, which embeds the atlas poster `known-best-1-100.svg` whose own footer carries the site's stamp (the posters are the site's assets and keep it). The paper's own words, credits, history, Markdown edition and colophon carry none. Whether the poster's stamp should be cropped out of the paper's figure is a question for the owner.
- Question: the article changed in substance after the v0.4.2 deployment (T-060's settlement on September 30, the V3/C3 rating) under the v0.4.2 label; the paper stays at v0.4.2 with "Last revised October 1, 2026". A new number is the owner's to give.
