---
type: is
id: is-01m292rgtadddppyrzfkjz1sn4
title: "Phase 6D: no JavaScript or HTML inside Python"
kind: task
status: open
priority: 1
version: 1
spec_path: docs/project/specs/active/plan-2026-09-11-workbench-from-spike-to-product.md
labels: []
dependencies: []
parent_id: is-01m28p7h39vcykq99dgjmvwv98
created_at: 2026-09-11T20:32:49.481Z
updated_at: 2026-09-11T20:32:49.481Z
---
The hard chunk, and the one no auto-fix touches. JavaScript and HTML live inside Python in both directions:

- build_candidate.py emits the page's markup and TeX from Python string literals.
- The five checkers -- check_workbench.py, check_revision6.py, check_revision7.py, check_legend.py, test_candidate.py -- embed about 2,500 lines of JavaScript in Python string literals to drive the page.

That is why no checker can lint the page's script, and it is not theoretical: a TeX \\le written with a doubled backslash inside an f-string reached the rendered page and set the bound on a second line, because nothing between the author and the browser could read the string as code.

Two halves, each landing on its own:

C1. template.html keeps its 265 lines of markup and gains assets/workbench.js and assets/workbench.css; build_candidate.py inlines them at build time exactly as it inlines the faces. Done when the built page is byte-identical to the one before the split and the script is a file a checker could read.

C2. Every page.evaluate("() => { ... }") in the checkers becomes a .js file the checker loads. Done when each checker reports the same result and the same printed measurements as before, and no JavaScript is written inside a Python literal.

Open question, to decide at C1 when the file exists: what lints the script. A pinned biome or eslint in the build is cheaper; tsc --checkJs with JSDoc would have caught the \\le bug.
