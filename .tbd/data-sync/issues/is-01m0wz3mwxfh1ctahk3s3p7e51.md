---
type: is
id: is-01m0wz3mwxfh1ctahk3s3p7e51
title: Tutorial labeled the pure-Python-to-compiled speedup an exact-to-float ratio
kind: bug
status: closed
priority: 2
version: 2
labels: []
dependencies: []
parent_id: is-01m0wy9s97fwegw5kqrge2p8sy
created_at: 2026-08-25T17:22:24.797Z
updated_at: 2026-08-25T17:49:30.605Z
closed_at: 2026-08-25T17:49:30.605Z
close_reason: Fixed on the PR 33 branch; see review-2026-08-25-tutorial-soundness-iteration-2.md and defects D-320..D-328. Full gate green.
resolution: null
duplicate_of: null
---
TUTORIAL.md section 5 said 'the exact-to-float ratio grows with algebraic degree - 177x at degree 8, 578x at degree 62'. The source (infrastructure research doc) measures 177x/578x as FLINT-over-pure-Python for the same exact multiplication, not exact-over-float. Reworded; also marked the compiled bignum backend row 'benchmarked; not integrated' to agree with section 11.
