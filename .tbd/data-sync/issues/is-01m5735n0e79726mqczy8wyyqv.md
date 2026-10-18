---
type: is
id: is-01m5735n0e79726mqczy8wyyqv
title: "Import Hosono: s(42) >= 2749/400, fine-net mixed certificate (no issue)"
kind: task
status: in_progress
priority: 2
version: 3
delegate: claude-code@spud10.local
labels:
  - result-import
dependencies: []
parent_id: is-01m572ssbx1x412zpvsw1sb6je
hold: null
hold_until: null
created_at: 2026-10-18T08:48:36.364Z
updated_at: 2026-10-18T12:39:14.956Z
started_at: 2026-10-18T12:38:15.353Z
---
W1 intake 2026-10-18, parent think-xmxb. wand125/square-packing d7afe3e525299d70de298af72cf17c581a86c0b1, problems/square-lower-bounds/certificates/mixed_n42_L68725. New finite lower bound; source reports 2073/2073 directions and sensitive control on fresh Ubuntu. Stage1 must compare both n42 lanes, retain ASSET/candidate/checker metadata, price full census plus whole-net controls from source receipt, and commission mathematical review. No sample establishes C3; no CPU-hour replay launched.

Full source commit inventory retained in packing/campaign/issue-intake/intake-20261018/. Stage0 owned; triage before retention/replay. Budget status: no CPU-hour replay authorized in this pass. Draft acknowledgement/public issue only after significance and report identity are settled (S4+ requires tracking issue). Done when every claim is mapped and imported or reasoned non-import, replay/review individually priced and owned, and source/report is answered after publication where applicable.
blocked_on: none

## Notes

18 October 2026 — bounded independent n42 mathematical and receipt triage by Astra; source-read and exact admission arithmetic only. This is not a sealed stage 4 review or an independent capture replay. No claim, V/C status or frontier record changed.

Source: https://github.com/wand125/square-packing/tree/d7afe3e525299d70de298af72cf17c581a86c0b1/problems/square-lower-bounds/certificates/mixed_n42_L68725 . Read README.md, ASSET.json, bundle.json, files-sha256.json, check2/src/SPEC.md, SOUNDNESS.md, REPRODUCE.md, INDEPENDENCE.md and fine_net_check.sh. The corresponding declared-net implementation and patch were read at https://github.com/wand125/square-packing-tools/tree/5fba675ed61cbbb819c79467fa1ad7f71fdb969a/fine_net_verifier . No upstream code was executed.

The release asset certificates__mixed_n42_L68725.tar.gz (GitHub asset 652766210, 694394 bytes) was read in memory through gh api, without writing/extracting the source archive or another file. Its SHA-256 is 1b167b27c4c3b5f0680d7c0e3ff4073b3734a00d6d8a9b31e78daaebb3b47d74, matching the pinned ASSET.json. Selected data/receipt members were parsed in memory with the project Python 3.14 interpreter. candidate.json SHA-256 is fbcec85228ce5f0c36cbf923164dcb1f0bbe16415278a2e470c914bac6ba4898; its independently recomputed semantic digest is 48c87eb47bf709b6240a13c06198e9c7bdf601b6dc8c73ce491df5c5f104aaf8. Release URL: https://github.com/wand125/square-packing/releases/download/square-lower-bounds-v1/certificates__mixed_n42_L68725.tar.gz .

Exact Fraction arithmetic independently checked all 977 rectangles: positive masses, nondegenerate and contained in [0,L]^2, with zero points. Total mass is 4199999/100000, exactly 1/100000 below 42. L=2749/400, B=4999/5000, D=1/5002, last=2072. The strict core margin 1-B(1+D)=3/25010000 and stronger per-bin tangent margin=60023/500400075000 are positive. The endpoint is 1036/2501; t_last^2+2t_last-1=367/6255001>0; the last cell's lower endpoint has polynomial -22423/100080016<0, so it is below sqrt(2)-1. t_last<=1/2 and L^2>=2B^2 also hold.

The conditional theorem is sound for this rectangle-only candidate: D4-average each rectangle with one eighth of its listed mass on each image; a unit square at half-angle tangent t has a concentric B-core at its nearest declared node strictly inside it. Check every centre in [rho(a_j),L-rho(a_j)]^2, a_j=max(0,jD-D/2), rho(a)=(1+2a-a^2)/(2(1+a^2)). Quarter-turn symmetry justifies the first-quadrant centre reduction without reversing the angle. If every such core captures at least 1, the 42 disjoint interior cores force mass >=42, a contradiction. No concrete flaw was found in these exact premises or the geometric reduction. This does not check the continuous-centre capture assertion.

Source-receipt audit: check2/run.jsonl.gz contains 2073 direction records, each index 0..2072 exactly once, all marked verified at threshold 1, plus one summary. This proves log completeness/consistency only, not independent correctness. The source used its adaptation of the project's sqverify-fast; do not count it and a native sqverify-fast replay as two wholly separate implementations. The source's 197/200 mass control covers 32 indices, with 32 refusals but only 31 exact-below-threshold witnesses (the axis row is a refusal without that witness flag). It is not the project's required whole-net 99/100 control.

Replay price from check2/receipt.json: 1308716984 nodes; 54686.78132019803 direction CPU seconds (15.1908 CPU-hours); 4579.602468189 wall seconds on 12 threads. The separate fresh-host verification/prepublication-receipt.json reports 2333 wall seconds and the same candidate/build identities, but no CPU time or thread count. The generic reproduction prose of minutes per certificate underprices this case. The 32-direction source control took 3.3 seconds; a project whole-net 99/100 control remains unpriced and must not be inferred from that number.

Next owner action: retain the allowed candidate/receipts and digest-only source-archive metadata, compare both frontier lanes (the inspected n-042 record has reported=verified=2739/400; the new claim improves it by exactly 1/40), arrange the separate full mathematical review, and price/run a complete 2073-direction native census plus the existing reviewed whole-net 99/100 control, with separately checked in-domain exact refusal witnesses. No sampled roots or source-reported PASS establishes C3. No CPU-hour replay, GitHub comment, PR mutation, source-file edit, commit or code push was made in this triage.
