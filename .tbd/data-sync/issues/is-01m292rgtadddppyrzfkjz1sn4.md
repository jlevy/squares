---
type: is
id: is-01m292rgtadddppyrzfkjz1sn4
title: "Phase 6D: no JavaScript or HTML inside Python"
kind: task
status: open
priority: 1
version: 6
spec_path: docs/project/specs/active/plan-2026-09-11-workbench-from-spike-to-product.md
labels: []
dependencies: []
parent_id: is-01m28p7h39vcykq99dgjmvwv98
child_order_hints:
  - is-01m298ns08hd103tjq6et26685
created_at: 2026-09-11T20:32:49.481Z
updated_at: 2026-09-11T22:16:49.235Z
---
The hard chunk, and the one no auto-fix touches. JavaScript and HTML live inside Python in both directions:

- build_candidate.py emits the page's markup and TeX from Python string literals.
- The five checkers -- check_workbench.py, check_revision6.py, check_revision7.py, check_legend.py, test_candidate.py -- embed about 2,500 lines of JavaScript in Python string literals to drive the page.

That is why no checker can lint the page's script, and it is not theoretical: a TeX \\le written with a doubled backslash inside an f-string reached the rendered page and set the bound on a second line, because nothing between the author and the browser could read the string as code.

Two halves, each landing on its own:

C1. template.html keeps its 265 lines of markup and gains assets/workbench.js and assets/workbench.css; build_candidate.py inlines them at build time exactly as it inlines the faces. Done when the built page is byte-identical to the one before the split and the script is a file a checker could read.

C2. Every page.evaluate("() => { ... }") in the checkers becomes a .js file the checker loads. Done when each checker reports the same result and the same printed measurements as before, and no JavaScript is written inside a Python literal.

Open question, to decide at C1 when the file exists: what lints the script. A pinned biome or eslint in the build is cheaper; tsc --checkJs with JSDoc would have caught the \\le bug.

## Notes

Both halves landed and are re-verified by the coordinator.

D1 (74dc3d95): template.html 5,704 -> 275 lines; assets/workbench.css 395, assets/workbench.js 5,079; rebuilt with the banner it is sha256 abb090b1, byte-identical to the published page; node --check parses the script; RENDER_INPUTS and both Pages filter blocks now name the assets.

D2 (e52b50a6, 612943aa): 605 page.evaluate sites across five checkers now load JavaScript from 180 files. 108 of them had Python values formatted in, and 17 more passed a positional array the two sides had to agree the order of. check_probes.py reports all 180 parsing, functions, named and answered. Evidence: check_workbench byte-identical output and exit 0; check_legend the same; check_revision7 identical but its measured-duration line; test_candidate byte-identical and exit 1, as before (think-tn0j); check_revision6 has no end-to-end comparison because it cannot finish (think-i15w), so 17 of its 19 sites were compared old-JS against new-probe on the page instead.

Left as its own chore: five byte-identical probe bodies across directories and two naming conventions (think-x406).

Open decision for the owner: what lints assets/workbench.js. Recommendation is a pinned Biome, check-only.
