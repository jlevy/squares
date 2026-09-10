---
type: is
id: is-01m1ywfktvnzj22n1y9sc2mktj
title: "PDF export embeds the sans: page-weight Source Sans 3 instances at print time"
kind: feature
status: closed
priority: 1
version: 5
spec_path: docs/project/specs/active/plan-2026-09-07-math-text-face.md
labels:
  - explainer
  - pdf
dependencies:
  - type: blocks
    target: is-01m1yxsge88fffnqznzjym9dtb
parent_id: is-01m1yxs9c3y78m00gqh7wsz9d6
created_at: 2026-09-07T21:30:41.882Z
updated_at: 2026-09-08T05:30:22.654Z
closed_at: 2026-09-08T05:30:22.646Z
close_reason: "Shipped: squares#118 merged to main at 89bedd68 on 2026-09-08 after a senior review (approve) and its fixes; the PDF embeds the sans"
resolution: null
duplicate_of: null
---
The explainer PDF sets its sans (captions, footnotes, hero, footer) as Type3 outline paths because Chromium cannot embed Source Sans 3 Variable at 410/550/680; in Preview the smoothed PT Serif and KaTeX read heavier than the unsmoothed sans. kpress (stacked branch squares/print-sans-faces) ships static instances for its own weights and a generator, devtools/instance_sans.py, importable standalone. Squares: a devtool packing/devtools/sans_instances.py that imports the kpress generator by path, instances the weights the print pass actually requests (found by a Playwright probe of computed font-weight/font-style on every sans-family element in print media, so the set covers every request exactly), writes woff2 files under packing/devtools/templates/fonts/ with --check; render_explainer_pdf injects the faces as data-URI @font-face rules for the 'Source Sans 3' family before printing, so the served page's bytes do not change and the screen keeps the variable font; render_explainer's inliner drops kpress's print-fonts.css faces from the page (the PDF pass supplies the page's own set) and the reachability rule documents why; render_explainer_pdf --check verifies via pypdf (new dev dependency) that no font in the PDF is Type3; gitlink bumped to the kpress branch; the squares spec docs/project/specs/active/plan-2026-09-07-math-text-face.md gains the print section and the document map is updated.
