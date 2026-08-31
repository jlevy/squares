---
type: is
id: is-01m0pdh5bj67ca8vk7ct53g5qt
title: "Defect remediation: classify, postmortem, and close the soundness gaps"
kind: epic
status: closed
priority: 0
version: 14
spec_path: docs/project/research/research-2026-08-22-packing-11-unit-squares.md
labels: []
dependencies: []
parent_id: is-01m0n6nyzx5pnark7xve1dy52x
child_order_hints:
  - is-01m0pd7gxn1a3cxzsrsgr1kt4t
  - is-01m0pd7heak20pe5sv132jmftx
  - is-01m0pcfqs45e16esmvw5wv57ax
  - is-01m0pd7hv533wjhpqxybnebvm0
  - is-01m0pdhvm1fc0fs4y8p48e06np
  - is-01m0pdhw0j8329gez9sw0efd86
  - is-01m0pdhwhbs1d2zsnk6z04w99m
  - is-01m0pdhx0dbsk8x90r58ge6pbx
  - is-01m0pdhxdvjmyttts8e3c42sd0
  - is-01m0pe76rbag3ztncnt22vvx9v
  - is-01m0pezhd7gzbz4hfwf1vfpwg1
  - is-01m0pf7a3ycs5y38kxesmhydw5
created_at: 2026-08-23T04:19:46.674Z
updated_at: 2026-08-23T05:44:20.928Z
closed_at: 2026-08-23T05:44:20.928Z
close_reason: "Ten of twelve children closed. The two that remain are not remediation: think-hg3u (the polished tier's ~1e-11 floor) is irreducible with a float LP and needs an exact rational LP, so it moves to the Phase 1 spine epic; think-v6l8 (bead the working process as it happens) is a standing practice, moved under the research epic. defects.md shows no open soundness item, which was this epic's exit condition."
---
Pause the experiment loops until the defect log's open items are closed and the pipeline that let a soundness bug through is fixed. Four strands: (1) postmortem on the soundness class, with prevention rules that generalise beyond the one bug; (2) close the four open defects D-018..D-021; (3) make the bookkeeping differentiate defect classes everywhere, not just in defects.yaml; (4) correct any research doc or plan whose claims the soundness and validity findings contradict. Resume the loops only when defects.md shows no open soundness item.
