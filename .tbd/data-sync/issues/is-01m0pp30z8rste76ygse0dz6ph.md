---
type: is
id: is-01m0pp30z8rste76ygse0dz6ph
title: Cut history notation and meta-commentary from the living docs
kind: task
status: closed
priority: 3
version: 2
spec_path: docs/project/research/research-2026-08-22-packing-11-unit-squares.md
labels: []
dependencies: []
parent_id: is-01m0pp24qsn326dyxy9na7wc50
created_at: 2026-08-23T06:49:20.615Z
updated_at: 2026-08-23T07:01:15.467Z
closed_at: 2026-08-23T07:01:15.467Z
close_reason: "Cut from SYNOPSIS: the blockquote narrating how to read the document (replaced by the rule that actually binds -- the artifact wins, and check_synopsis enforces it), and the paragraph narrating that a sentence used to read differently until D-024 falsified it, which is D-028's story to tell. Also replaced two filler uses of 'load-bearing', which common-doc-guidelines names as jargon to avoid outside genuinely descriptive use."
resolution: null
duplicate_of: null
---
common-doc-guidelines: describe the present state, not what it replaced, and avoid talking about talking. Living docs should not carry the author's path. Two specifics. (1) SYNOPSIS's defect section narrates that a sentence 'read the gate caught none of them until D-024 made it false' -- that history belongs to D-028 in the defect log, which is an allowed exception; the synopsis should state the present claim and reference it. (2) The blockquote under the synopsis title narrates how to read the document. Trim the narration, keep the navigation, since organising rule 1 does want a reader to be able to move between documents.
