---
type: is
id: is-01m5frehkgm6ht7anfbzgf29a5
title: "PR #704 B1: the de Winter coverage note calls #678 unregistered; override reason should say smallest validated"
kind: bug
status: closed
priority: 2
version: 2
labels:
  - result-import
dependencies: []
parent_id: is-01m5fre23qy5rq285h9tsarhz0
created_at: 2026-10-21T17:34:23.344Z
updated_at: 2026-10-21T18:08:00.296Z
closed_at: 2026-10-21T18:08:00.296Z
close_reason: "fixed in 34cd6da71, carried through merge 9c4781199: coverage note and T-196's note name T-223; override_reason says 'smallest validated'; the merged 270 override rewritten by adopt_houses --refresh-openings --n 270; adopt_houses --check 70 OK (PR #704 head c3ed6c064)"
resolution: null
duplicate_of: null
---
Medium. packing/frontier/source-coverage.yaml:6232 at d2eca7108; adopt_houses.py:2580 override reason; T-196's results.yaml note. Review B: https://github.com/jlevy/squares/pull/704#issuecomment-6306759614
