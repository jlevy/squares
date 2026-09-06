---
type: is
id: is-01m1tp64mzesec3ch9q0twmw37
title: Republish the explainer edition past the review fixes
kind: task
status: open
priority: 1
version: 1
labels:
  - review-gpt6
dependencies: []
created_at: 2026-09-06T06:23:42.238Z
updated_at: 2026-09-06T06:23:42.238Z
---
PR #92 pins every repository link on the explainer to PUBLICATION_REVISION (sqpack/release.py, currently 3bd273e6), which is the commit the edition was cut from. Until the edition is bumped, the deployed page links to verify_claim.py, the claim documents and the thirdparty package as they were before the 2026-09-05 review fixes (think-cd62). Bump PUBLICATION_VERSION/PUBLICATION_REVISION (and PUBLICATION_DATE) to a commit that carries the fixes, regenerate the atlas family that embeds the same stamp and is byte-compared against a fresh render, re-render the explainer and PDF, and confirm tests/test_explainer.py's permalink tests pass against the new commit. Same bead as the stale-stamp limit PR #92 records.
