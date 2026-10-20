---
type: is
id: is-01m4s66qs6ep9c3jycyamqgmf2
title: "Documentation layout, deferred part: root documents, runbooks, generated views, sqverify_fast guides"
kind: task
status: open
priority: 3
version: 6
spec_path: docs/project/specs/active/plan-2026-10-11-documentation-organization.md
labels: []
dependencies: []
child_order_hints:
  - is-01m4t1y0xye322ehz1p8pts800
hold: blocked
hold_until: null
created_at: 2026-10-12T23:12:15.654Z
updated_at: 2026-10-13T08:06:51.573Z
---
The deferred part of the documentation-layout plan. The spec is docs/project/specs/active/plan-2026-10-11-documentation-organization.md on main; its "Status on 2026-10-12" section has the measured reasons. The conflict-free part landed in #576 (think-mv16, merged 2026-10-13 at ea227e62d).

Blocked on the owner's answers to plan decisions 2 (one docs/project prefix), 4 (synopsis and tutorial leave the root, breaking outside blob/main links) and 8 (runbooks to docs/project/runbooks/). It also needs a quiet PR queue: on 2026-10-12, 15 of 16 open PRs edited SYNOPSIS.md, 10 edited development.md and 9 edited packing/frontier/RESULTS.md.

Remaining work, in order:
1. Slice 0's mover exists: devtools.move_documents is built in PR #579 (open as of 2026-10-13); until it merges, take it from that branch. It validates the whole move list, applies it all or not at all, rewrites relative links by depth and exact repository-relative paths in every tracked text file (code, registers, the map, .flowmarkignore, .gitattributes), keeps math-markup.yaml sorted, and leaves fenced code and frozen records alone, reporting what it leaves. Slices 2-5 rewrite 10 to 30 times as many links as #576 did, which used a one-off script, and should start with it. What remains of it (case-only renames, and reports of bare basenames, blob/main links and AGENTS.md, CLAUDE.md and dot-directory references) is think-qgq1, under this bead.
2. Slice 2: conventions.md, epistemics.md and operating-rules.md to docs/project/policies/.
3. Slice 4: the four campaign runbooks to docs/project/runbooks/.
4. Slice 3: TUTORIAL.md, SYNOPSIS.md (lowercased) and development.md to docs/project/guides/. Renderers must write links relative to the output file. Optionally (decision 9) move the document-map table to docs/project/README.md.
5. Slice 5, in a window with no open result-registration PR:
   - defects.md to packing/defects.md, beside its register
   - site-urls.md to packing/site-urls.md, beside its register
   - lowercase the five generated frontier views
   - lowercase packing/sqverify_fast/SOUNDNESS.md and INDEPENDENCE.md, which evidence.yaml names 552 and 145 times
   - re-pin DATA_REVISION
6. Slice 7: empty check_documentation.LAYOUT_PENDING, which test_document_layout already keeps from growing. Add policy and guide roles to the map schema and re-role the entries.

## Notes

2026-10-13: #576 merged; #510 closed with a pointer to it. #435 was notified that its loose docs/project handoff must move to handoffs/ once it merges main; no other open PR adds a document the new check refuses. The one-line index conflicts (#497's stack on math-markup.yaml, #514 on document-map.yaml) are for those PRs to resolve. The four tests that fail only in cloud sessions are think-mn8m.
