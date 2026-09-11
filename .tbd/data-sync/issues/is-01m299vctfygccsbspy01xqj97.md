---
type: is
id: is-01m299vctfygccsbspy01xqj97
title: "J5: the page's markup, or a stated reason not to"
kind: task
status: closed
priority: 2
version: 2
spec_path: docs/project/specs/active/plan-2026-09-11-workbench-from-spike-to-product.md
labels: []
dependencies: []
parent_id: is-01m299tcsrh44b8n8m1c6jpgcb
created_at: 2026-09-11T22:36:43.726Z
updated_at: 2026-09-11T23:08:50.760Z
closed_at: 2026-09-11T23:08:50.759Z
close_reason: "Declined at this pin, with the measurement. Biome 2.5.11's experimental HTML support formats a simple fragment but will not process template.html: it reports 'these paths were provided but ignored' rather than a parse error, and does the same for a 4 KB head of the file with and without its doctype, while a three-line fragment in the same directory under the same config formats fine. So there is nothing to adopt yet. Re-test when the Biome pin moves; the template is 275 lines of markup and the thing to watch for then is whether the formatter reflows the substitution-token lines, since asset() strips exactly one trailing newline because the token's own line supplies it."
resolution: null
duplicate_of: null
---
`template.html` is 275 lines of markup since the script and styles moved out. Biome 2.x has experimental HTML support -- the sibling trading repository enables it with `html.experimentalFullSupportEnabled`.

Either bring the template under it, or decline with a reason written down. The reason not to, if there is one, is that the template carries substitution tokens (`__WORKBENCH_JS__` and friends) on lines of their own, and an HTML formatter that reflows them changes what `build_candidate.py` matches -- `asset()` strips exactly one trailing newline because the token's own line supplies it.

Measure before deciding: run the formatter in check mode and see whether it would touch those lines at all.
