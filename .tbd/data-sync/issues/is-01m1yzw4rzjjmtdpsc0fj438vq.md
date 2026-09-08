---
type: is
id: is-01m1yzw4rzjjmtdpsc0fj438vq
title: "Sans math in the explainer's sans contexts: captions, footnotes and hero set their mathematics in Source Sans 3"
kind: feature
status: in_progress
priority: 2
version: 5
spec_path: docs/project/specs/active/plan-2026-09-07-math-text-face.md
labels:
  - explainer
  - typography
dependencies:
  - type: blocks
    target: is-01m1z03rmkes4xm9r9nbg2a45s
  - type: blocks
    target: is-01m1zzjddp742vysds0fzm3fe8
parent_id: is-01m1yxs9c3y78m00gqh7wsz9d6
created_at: 2026-09-07T22:29:58.149Z
updated_at: 2026-09-08T08:08:24.870Z
---
The explainer's captions, footnotes and hero are Source Sans 3 (410 light, 550 medium, 680 bold in the paper profile), and the mathematics inside them draws its letters and digits from PT Serif through KPress Math Text, so a caption mixes two text faces. kpress kpr-7f9z (branch squares/sans-math) adds KPress Math Text Sans and applies it inside sans contexts. Adopt it: bump the gitlink, confirm the caption and footnote mathematics resolves to Source Sans 3 at the context's weight on screen (CSS.getPlatformFontsForNode) and to the static instances in the PDF (render_explainer_pdf --fonts), extend the inliner's reachable-face rules to the sans composite's slots (render_explainer prunes composite slots by their KaTeX partner and refuses unknown families), regenerate the print instances if the requested weight set changes, check inspect_explainer_typography --check-supporting and check_print_layout, record the before and after in the plan spec's Font Consistency section, and open the page and PDF for the owner to judge the caption math beside the PT Serif prose math.

## Notes

From the kpress #57 senior review (K57-R2, comment 5577788026): the squares inliner breaks on the sans composite twice. render_explainer.py near line 786 counts @font-face blocks by the substring "KPress Math Text", which also matches "KPress Math Text Sans" (20 blocks instead of 8) and exits before the CSS check; count by exact family. And the page's selector-length heuristic (len(prelude.strip()) < 400) rejects the sans scope rules at 477 characters unless kpress splits them (the kpress address round is asked to keep every prelude under 400). Both must be fixed here before the gitlink can move to a kpress with sans math; the reviewer also notes that Markdown image captions are HTML-escaped, so caption math only exists through raw-HTML block captions, which the explainer uses.
