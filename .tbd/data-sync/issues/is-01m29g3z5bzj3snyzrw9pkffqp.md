---
type: is
id: is-01m29g3z5bzj3snyzrw9pkffqp
title: "L2: the sources layer, in the explainer's own styling"
kind: feature
status: open
priority: 1
version: 2
spec_path: docs/project/specs/active/plan-2026-09-11-workbench-from-spike-to-product.md
labels: []
dependencies: []
parent_id: is-01m29g1hhddhwsqfr0fz4r175e
created_at: 2026-09-12T00:26:16.101Z
updated_at: 2026-09-12T00:26:44.912Z
---
A "Sources:" block on the panel carrying the citations behind this n's bounds, in abbreviated but complete form, styled the way the explainer paper styles its references -- the same serif, the same conventions, not a second citation style invented here.

Owner: "clean, consistent, formatted... optionally filled in in a way that's condensed and still fits on the page for all the pages where we have details... abbreviated and concise but complete form."

Three things to establish first, and the first decides the rest:

1. **Where the citations come from.** The composite figure record and the frontier register already carry provenance for the known-best sides; `devtools/render_explainer.py` already formats references for the published paper. Reuse both -- the rule this repository works under is that the generator reads the record rather than restating it, and the explainer's reference formatting is code that exists. Find out what the record actually holds per n before designing the block: it may be complete, partial, or absent for most n, and "all the pages where we have details" says the owner expects it to be partial.
2. **What abbreviated-but-complete means here.** Author, year, and enough to find it -- probably a short form, with the full reference on the atlas rather than on the page. Decide the form once and generate it; do not hand-write per n.
3. **Fitting.** The panel's rows are at fixed tops and the block is variable-length. A citation list that overflows is worse than none, so either the generator measures or the panel reflows -- the same problem think-ef9h has.

Depends on think-ef9h for where the block lives and when it is drawn.
