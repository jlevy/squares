---
type: is
id: is-01m253zk0mvw2d49zmw4esm6r6
title: Resolve parent receipt pins from the repository root
kind: bug
status: closed
priority: 2
version: 8
spec_path: docs/project/specs/archive/plan-2026-09-10-n11-overnight-three-blocks.md
delegate: parent_receipt_binding_prep
labels: []
dependencies:
  - type: blocks
    target: is-01m24tw1hadnzxyw7rdvp3vmms
  - type: blocks
    target: is-01m25430wcdx8wn8f3qs7b4qjv
parent_id: null
created_at: 2026-09-10T07:37:11.955Z
updated_at: 2026-10-10T23:05:23.772Z
closed_at: 2026-10-06T08:50:00.258Z
close_reason: "Done: ParentInputPins in packing/devtools/wall_owner_parent_inputs.py on origin/main carries an explicit absolute repository_root and refuses a relative one (lines 81-84, 163-167); its parent think-fx2y is closed."
resolution: null
duplicate_of: null
---
Independent Astra xhigh source review reproduced a private constructor P2: wall_owner_parent_inputs.py passes repository-relative ReceiptPin paths directly to current-directory-relative loaders. From the documented packing/ build root, retained packing/... paths resolve as packing/packing/.... Synthetic interception reproduces without loading any retained target. Resolve one explicit repository root and join each validated pin before loaders while preserving repository-relative receipt identities. Add a control from a changed working directory, preserve source/check-out/class/manifests bindings, and obtain independent correction review before adoption. Candidate /private/tmp/n11-parent-adapter-prep/; review /private/tmp/n11-parent-input-independent-review.md. No scientific outcome or false geometric acceptance demonstrated.

## Notes

Sol repair now passes independent Astra xhigh correction review. ParentInputPins carries an explicit absolute repository root; all pins and identities are validated before absolute loader paths are resolved, while stored receipt identities remain repo-relative. Original/path/all-loader controls:7 passed; eight additional root, traversal, late-pin and escaping-symlink boundary controls passed. Candidate /private/tmp/n11-parent-adapter-prep/, correction note parent-input-path-correction.md, independent report /private/tmp/n11-parent-input-path-correction-review.md. No retained target was loaded and no parent restriction was computed. Production adoption remains pending; future think-acfb CLI must establish the authoritative Git cwd and clean checkout, freeze source, impose clocks, use both replay wrappers and retain result provenance.
