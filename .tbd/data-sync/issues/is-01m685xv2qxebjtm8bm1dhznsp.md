---
type: is
id: is-01m685xv2qxebjtm8bm1dhznsp
title: "Import maximusrufus: a second-machine replay of ValidTilt9, T-081's box-9 premise, with Daniel's qx2_zm.py (openai-math-replays 80cb822) (#316)"
kind: task
status: open
priority: 3
version: 2
labels:
  - result-import
  - decision
dependencies: []
created_at: 2026-10-31T05:11:42.423Z
updated_at: 2026-10-31T05:22:41.555Z
---
maximusrufus's comment of 2026-10-26T14:39:55Z on closed #316 (https://github.com/jlevy/squares/issues/316#issuecomment-6418796038) reports a full replay of the producer's qx2_zm.py run on K4_k008_box9.txt (ValidTilt9, the box-9 premise of s(k^2 - 4) = k, T-081) on a second machine: evand/square-packing 2eb15455, s12/certificates/k2m4/, input sha256 4151d7c4...7801, qx2_zm.py sha256 6294052a...e737; Ubuntu, 32 logical cores, Python 3.14.4, --depth 18 --nproc 20 --exact-umax 1/2 --exact-from 3 --dump-leaves, exit 0; VERIFIED-D4, 16200/16200 roots, uncert 0, 115,268 leaves (the published run's), 214,336 boxes, max depth 17; wall 66,832 s, CPU 1,328,518 s (about 369 CPU-hours); per-root records equal to the published run_k4x_k008_leaves.jsonl.gz at all 16,200 roots (cpu seconds excluded). Receipts: maximusrufus/openai-math-replays at 80cb822, t081-rebuild/ (BUILD.txt, run.out, time.txt, record_compare.txt, run.jsonl.gz, SHA256SUMS). Same code and input as the producer's run: reproducibility, not an independent implementation; no Lean build and no separate check of the region statement. Read into #316's entry on 2026-10-31 (think-6m6e); nothing retained yet. Work: retain the receipts at a pinned revision (packet), check SHA256SUMS and record_compare against the producer's published leaves, and record it as a third party's report beside T-081. Whether a retained third-party full replay of the producer's code moves T-081 (V0/C1 since the owner declined the full replay on 6 October and #316's final reply said a complete replay here or elsewhere would move it) is the owner's decision, as think-n6ga holds the same question for #565's T-154 rebuild. Done when the receipts are retained and the owner's decision is recorded, and #316 gets the follow-up its state owes.

## Notes

2026-10-31 bold-ritchie-l1 (think-6m6e): read into #316's entry on PR #833's branch (claude/friendly-einstein-gf9z0h-records-1026), read_through 2026-10-26T14:39:55Z; this bead is #316's answer bead from that change. The follow-up it owes is posted only after #833 merges: render `check_requests --draft 316` from main, check main and the deployed site, then post and record it under #316's replies. Draft, to edit against the rendered draft:

> @maximusrufus, thank you for replaying the ValidTilt9 run on a second machine. It is now in the record on `main`: the producer's full `qx2_zm.py` run on `K4_k008_box9.txt` at evand/square-packing 2eb15455, `VERIFIED-D4` at all 16,200 roots with none uncertified and the published 115,268 leaves, and every root's record equal to the published run's but for its CPU time. It runs the producer's code on the producer's input, so it shows that the run reproduces; it is not a separate implementation, and it builds no Lean and checks no region statement, as you say. Its receipts (`maximusrufus/openai-math-replays@80cb822`, `t081-rebuild/`) are not yet retained here, so T-081 stays at V0/C1. Retaining them, and the owner's decision on whether a third party's complete replay of the producer's code moves T-081, are `think-s4ul`'s. The issue stays closed; this brings what the record says up to date.

Record it with reported: k2m4 T-081 V0/C1 (and status reviewed only if the text says it), and beads [think-s4ul].
