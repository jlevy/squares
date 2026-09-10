---
type: is
id: is-01m253zk0mvw2d49zmw4esm6r6
title: Resolve parent receipt pins from the repository root
kind: bug
status: open
priority: 2
version: 1
spec_path: docs/project/specs/active/plan-2026-09-10-n11-overnight-three-blocks.md
labels: []
dependencies: []
parent_id: is-01m24tw1hadnzxyw7rdvp3vmms
created_at: 2026-09-10T07:37:11.955Z
updated_at: 2026-09-10T07:37:11.955Z
---
Independent Astra xhigh source review reproduced a private constructor P2: wall_owner_parent_inputs.py passes repository-relative ReceiptPin paths directly to current-directory-relative loaders. From the documented packing/ build root, retained packing/... paths resolve as packing/packing/.... Synthetic interception reproduces without loading any retained target. Resolve one explicit repository root and join each validated pin before loaders while preserving repository-relative receipt identities. Add a control from a changed working directory, preserve source/check-out/class/manifests bindings, and obtain independent correction review before adoption. Candidate /private/tmp/n11-parent-adapter-prep/; review /private/tmp/n11-parent-input-independent-review.md. No scientific outcome or false geometric acceptance demonstrated.
