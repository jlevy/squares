---
type: is
id: is-01m1yzw4rzjjmtdpsc0fj438vq
title: "Sans math in the explainer's sans contexts: captions, footnotes and hero set their mathematics in Source Sans 3"
kind: feature
status: open
priority: 2
version: 2
spec_path: docs/project/specs/active/plan-2026-09-07-math-text-face.md
labels:
  - explainer
  - typography
dependencies:
  - type: blocks
    target: is-01m1z03rmkes4xm9r9nbg2a45s
parent_id: is-01m1yxs9c3y78m00gqh7wsz9d6
created_at: 2026-09-07T22:29:58.149Z
updated_at: 2026-09-07T22:34:07.886Z
---
The explainer's captions, footnotes and hero are Source Sans 3 (410 light, 550 medium, 680 bold in the paper profile), and the mathematics inside them draws its letters and digits from PT Serif through KPress Math Text, so a caption mixes two text faces. kpress kpr-7f9z (branch squares/sans-math) adds KPress Math Text Sans and applies it inside sans contexts. Adopt it: bump the gitlink, confirm the caption and footnote mathematics resolves to Source Sans 3 at the context's weight on screen (CSS.getPlatformFontsForNode) and to the static instances in the PDF (render_explainer_pdf --fonts), extend the inliner's reachable-face rules to the sans composite's slots (render_explainer prunes composite slots by their KaTeX partner and refuses unknown families), regenerate the print instances if the requested weight set changes, check inspect_explainer_typography --check-supporting and check_print_layout, record the before and after in the plan spec's Font Consistency section, and open the page and PDF for the owner to judge the caption math beside the PT Serif prose math.
