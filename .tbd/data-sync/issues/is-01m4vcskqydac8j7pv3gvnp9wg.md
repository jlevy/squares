---
type: is
id: is-01m4vcskqydac8j7pv3gvnp9wg
title: Mark reconstructed run costs explicitly instead of matching RUN_MEASURED_BY's sentence
kind: task
status: open
priority: 3
version: 1
labels:
  - regularization
dependencies: []
created_at: 2026-10-13T19:45:54.429Z
updated_at: 2026-10-13T19:45:54.429Z
---
#559 review B, B3. regularize_evand.run_block tells a reconstructed cost by exact inequality with RUN_MEASURED_BY, so rewording run's sentence would give every older measured receipt a note when its block is rebuilt. An explicit marker (cost.reconstructed) would not depend on the wording, but the receipts are outside the repository, the one reconstructed receipt (refreshed-adopt518-v2) was written by hand and carries only the sentence, and no tool writes reconstructed receipts; so a marker needs a tool that writes reconstructed receipts, with the sentence comparison kept for receipts already written. Do it when a reconstruction tool exists, or freeze RUN_MEASURED_BY with a test.
