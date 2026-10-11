---
type: is
id: is-01m3w2jdbfn97mxwfwzwmwfdw0
title: "n = 11 optimality paper: font weight and math match the original explainer"
kind: task
status: closed
priority: 2
version: 6
spec_path: docs/project/specs/active/plan-2026-09-29-github-pages-overview.md
labels: []
dependencies: []
parent_id: is-01m3p52z585a2zb9jmy19b0r96
created_at: 2026-10-01T15:50:45.346Z
updated_at: 2026-10-01T19:20:46.072Z
closed_at: 2026-10-01T19:05:22.800Z
close_reason: "Merged into jlevy/squares#276 (ec88c6a83): the optimality paper's shell lacked the head script that returns KaTeX's text-rendering to auto on macOS, so its formulas painted 16.6% (light) to 25.8% (dark) less ink; both renderers now take the stylesheet and script as one pair; site sans weights named; tests/test_site_glyphs.py holds every page. Owner list in the agent's report (Unicode math in figure captions, tutorial math as code, workbench formulas, Linux rendering difference)."
resolution: null
duplicate_of: null
---
Owner, 2026-10-01: 'investigate font weight and math consistency. The page here looks good, it is the original: https://jlevy.github.io/squares/explainer.html but the page here https://jlevy.github.io/squares/n11-optimality/t-060-explainer.html' (message cut off; the second page is the one that looks wrong). Compare the two live pages and the local builds in a browser: body, heading, caption, table and footnote font families, weights, sizes and line heights; whether the same font files load at the same weights (a missing weight is synthesized or falls back); inline and display math faces, sizes and weights (KaTeX fonts, math in sans contexts, math in headings and tables, bold math), and code-versus-math spans. Report every difference with computed values and screenshots, find the cause (the paper's own renderer and stylesheet against the shared paper-type.css), fix it at the shared layer so the two cannot drift, and pin with a browser test.

## Notes

2026-10-01, branch claude/n11-paper-type (worktree n11-paper-261), not pushed. CAUSE: the paper's shell inlined explainer-publication.css without explainer/native-math-metrics.js; the stylesheet's .katex rule is text-rendering: geometricPrecision, taken back to auto on macOS only under html[data-squares-native-math-metrics], which that script stamps. On macOS Chromium the paper's formulas stayed geometricPrecision and held 15-17% less ink (light) and 23-26% less (dark) than the same formula on the explainer; one-property toggles reproduce each page's ink on the other. FIX: render_explainer.publication_layer() gives both renderers the stylesheet and script as a pair; the paper also moved to the site math pipeline (katex_js + overview/math.js), \mathsf T -> \top, PDF asks for all formulas before printing. Also: 31 sans rules in site.css/site-result.css now name the regular weight 410 (were inheriting 400). TOOL: measure_site_pages glyphs (and figures, under think-y1z3). TESTS: tests/test_site_glyphs.py, test_render_n11_optimality_explainer.py. DOC: paper-design.md Math, Math Loading, Text (sans weights, role exceptions), Figures. Commits 435b4b31b, 527b77e14, af6e30eb6, 935556bbc, 73ec63f06 (+ merges of origin/main 766e5f573 and 3e5322f93 and paper-credits b7b7b7f1f), then d99d82fef for think-y1z3. OPEN for the owner: geometricPrecision off macOS on the two papers but not site pages; diagram labels with ≤ ≥ τ and subscripts as text (host glyphs, also in the PDF); math written as code in TUTORIAL/SYNOPSIS (Menlo); the star and check mark characters drawn from host faces; homepage hero caption at a literal 0.85; workbench formulas are stock KaTeX without MathML; result overview fragments unstyled when opened alone. Not verified: Firefox, WebKit, Linux CI.
