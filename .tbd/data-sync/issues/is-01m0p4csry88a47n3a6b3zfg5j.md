---
type: is
id: is-01m0p4csry88a47n3a6b3zfg5j
title: Add the atlas to test.sh drift checks
kind: task
status: closed
priority: 3
version: 7
spec_path: docs/project/specs/paused/plan-2026-08-22-minimal-packing-toolkit.md
labels: []
dependencies: []
parent_id: is-01m0p4cr8nk338kqtbksaf63f9
created_at: 2026-08-23T01:40:06.557Z
updated_at: 2026-10-12T23:52:44.602Z
closed_at: 2026-10-06T08:45:52.425Z
close_reason: "Obsolete: explorations/packing/test.sh no longer exists anywhere on origin/main; the atlas is validated by packing-validate's atlas steps (packing/src/sqpack/cli/validate.py)."
resolution: canceled
duplicate_of: null
---
Once the atlas artifact exists, validate it in explorations/packing/test.sh alongside the frontier corpus and the campaign record, and check the descriptor definitions have not drifted from the archive keys.
