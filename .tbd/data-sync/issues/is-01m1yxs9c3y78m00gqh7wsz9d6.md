---
type: is
id: is-01m1yxs9c3y78m00gqh7wsz9d6
title: "[epic] Explainer fonts: every glyph from a shipped face on web and PDF"
kind: epic
status: open
priority: 1
version: 11
spec_path: docs/project/specs/active/plan-2026-09-07-math-text-face.md
labels:
  - explainer
  - pdf
dependencies: []
child_order_hints:
  - is-01m1ywfktvnzj22n1y9sc2mktj
  - is-01m1yxsge88fffnqznzjym9dtb
  - is-01m1yxsk25gtbjyhredzhqyp4f
  - is-01m1yxsn8850cw25h9mb6nbjea
  - is-01m1yyts2wc8p6403jkdqzhddf
  - is-01m1yzw4rzjjmtdpsc0fj438vq
  - is-01m1z03rmkes4xm9r9nbg2a45s
  - is-01m1z1str69ztdk6y35ayg3ccb
  - is-01m1zb00ss66pjnhm5rw9nawk1
  - is-01m20v1mq20k9d9p1wg9s5qdsq
created_at: 2026-09-07T21:53:27.418Z
updated_at: 2026-09-08T15:44:04.307Z
---
Rule (owner, 2026-09-07): the explainer resolves every text run to a face the page ships (PT Serif, Source Sans 3, the KaTeX faces and the KPress Math Text composite, and kpress's mono face once it ships), on screen and in the PDF; the one exception is the 100-best atlas figure, whose Helvetica is baked in by its own pipeline (build_known_best_atlas.py) and stays. Measured 2026-09-07 on the 946 KB PDF: sans as 345 KB of Type3 paths (think-988s), Menlo 56 KB for 134 characters of inline code on pages 6, 14, 15, Georgia 16 KB for 48 list bullets on the same pages, Helvetica 54 KB on page 3 (the atlas, accepted). Web page 1,418 KB with 636 KB of fonts, of which 216 KB is the composite's duplicate copies. Children: think-988s, the provenance guard, the KaTeX subsetting, and adopting kpress's mono, marker, and quote fixes.
