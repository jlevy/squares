---
type: is
id: is-01m4wv27yed1e2wfnq55h1avr0
title: "Import wand125: s(37) >= 2599/400, s(39) >= 533/80, s(44) >= 2799/400 (check2 fine-net) and s(145) >= 306/25 (linear measure) at wand125/square-packing aba0e59 (no issue)"
kind: task
status: in_progress
priority: 1
version: 16
delegate: bold-ritchie-l10
labels:
  - result-import
dependencies: []
parent_id: is-01m4wsqt2sjrksybyz375sarb3
child_order_hints:
  - is-01m4xe5txp3t3t4xczs1swedc9
  - is-01m4xpvhty2mmgcx131estyhkg
  - is-01m4xpvk3p35kqfqcrszjw9zp6
  - is-01m4xpvm51z8nvp3j5xxjgdhr0
  - is-01m4xpvnd65tdxfgyjzvc1pzwh
hold: null
hold_until: null
created_at: 2026-10-14T09:14:31.758Z
updated_at: 2026-10-31T20:02:09.376Z
started_at: 2026-10-14T09:14:41.660Z
---
Found by the 2026-10-14 watch survey (think-fxs7): problems/square-lower-bounds/certificates/mixed_n37_L64975 (7a42c16, 2026-10-13T03:18Z), mixed_n39_L66625 (dfb2cf8, 03:01Z), mixed_n44_L69975 (9f24185, 03:01Z), mixed_n145_L1224 (22f06b3, 06:18Z). Against main: 37 above 161/25 = 6.44; 39 above 133/20 = 6.65; 44 above 2789/400 = 6.9725; 145 above the reported 12.2138669 (Green DS7, disputed in #308) and the verified 12.0434, and by monotonicity lifting 146-149. The 37/39/44 bundles take the T-142/T-143 route (think-i85v): stages 1-2 with the release assets, a priced stage 4 replay with sqverify-fast from reviewed source over all directions with whole-net controls, held for an owner budget.

## Notes

2026-10-14 stages 1-2 (intake lane wand125-lb, sub-agent of squares-43; worktree branch lane/wand125-lb from origin/main f73e9de13, not pushed): commits c4e9949b73c97aaa77f10f4d61ca91568dbcaf71 and b974b269c745f9c589aff15dec03cb1aeb0d610d (a README wording fix), packets packing/resources/web/wand125-fine-net-n37-n39-n44-2026-10-13/ and packing/resources/web/wand125-linear-n145-2026-10-13/, keys [wand125 fine-net n37 n39 n44 2026-10-13] and [wand125 linear n145 2026-10-13] in resources/README.md and bibliography.yaml.

Pins: mixed_n39_L66625 added at dfb2cf85fdf9ee5f95c5ec2c67fd49210854f146 (2026-10-13T03:01:37Z), mixed_n44_L69975 at 9f24185c602c8c0b83cf6a88b11a69ea8d668673 (03:01:53Z), mixed_n37_L64975 at 7a42c16eacaab112b537ab09e89d3485f6f4c75f (03:18:05Z, the fine-net packet's acquire_source pin), mixed_n145_L1224 at 22f06b31a9295c8185be5d30a1a7b19982b16847 (06:18:13Z, the linear packet's pin). Each directory is the same Git tree from its adding commit through the head 9a28a84 (2026-10-14T09:27Z; aba0e59, be1d5e9 and 9a28a84 change the site, papers and themes only); LICENSE blob bbfbff13 (MIT, wand125) throughout. Release square-lower-bounds-v1 assets, each equal to the API digest, SHA256SUMS and ASSET.json: certificates__mixed_n39_L66625.tar.gz 639,558 B 8e88ca06...851f (asset 635702665, SUMS line 442); __mixed_n44_L69975 631,497 B b4cf96d5...3eb4 (635703292, line 443); __mixed_n37_L64975 630,375 B 8aa78cc4...1965 (635741442, line 444); __mixed_n145_L1224 38,598,220 B 6a937dc7...2a49 (636102989, line 445). Retrieved 2026-10-14T09:22Z. Assets kept outside Git; the scratch copies are not hosted.

Claims (all four in the survey; none missed in problems/square-lower-bounds): s(39) >= 533/80 (687 rectangles, mass 3899999/100000; +1/80 over T-110's 133/20); s(44) >= 2799/400 (606, 4399999/100000; +1/40 over T-090's 2789/400, 1/400 below the upper bound 7); s(37) >= 2599/400 (612, 3699999/100000; +23/400 over T-069's 161/25); all core 4999/5000 on the 1/5002 net of 2,073 directions. s(145) >= 306/25 (594 point, 1,541 segment, 9 rectangle orbits, mass 14499999/100000, T-080's net and checker 0249726a), hence s(N) >= 12.24 for N >= 145: above Green's reported 12.21387 at 145-148 (disputed, #308), Nagamochi's 12.22497 at 149 (T-007) and the Karakus strip lane (T-083) at 145-149; 150 holds more. No count is settled (upper bounds 12.5355 to 12.7071), so 146-149 take the parent's scope. Who else holds values: no other report at 37/39/44 is above the record; at 149 the same source's closed form a(149) = 12.2804 (eb0fd19, think-tsox) is above 12.24 and later in report order, below it at 145-148. Seen past the last read and owned elsewhere: closed-form-v1 (think-tsox); right-isosceles s(15) = 6 (outside this record's container); release data/n17-m2048064-v1 (2026-10-13T00:29Z), one n = 17 sub-pattern certificate for row 4 of jlevy/squares#413, which no bead names (for the n = 17 lane).

Premises: fine_net_followup premises EXACT_PREMISES_HOLD for all three check2 candidates (Lemma N0 and last bin, mass n - 1/100000, one digest, full audit_check2; 11 documents equal their commit blobs; sealed bundles 16 files, 15 hashes; verifier archive e495f9bf). Each carries two reported complete author runs: check2 (n37 1,146.4 s at 16 threads, n39 1,682.7 s at 12, n44 2,785.4 s at 16; binary ec04d332, build ab6e33e1) and a separate pre-publication run (619, 697, 1,654 s). The bundled check2/src SOUNDNESS.md and INDEPENDENCE.md are this repository's notes at e020eb1e2 (pre-lemma-N0). linear-premises EXACT_PREMISES_HOLD for n145: 17,152 D4 images, digest 31788dc7, 201 records with 124,435,707 nodes (axis 3,330,973), 810 bundle files, all 201 inputs enclose the candidate (77 s); code/ 13 files byte-identical to retained copies. No source program ran.

Samples: sqverify-fast from reviewed source d97758bb (binary 567a0fd5), directions 0, 296, ..., 2072, one thread, one worker: 24/24 verified with the source's nodes and least bounds. 99/100 mutant (control-sample of fc3199fc0, unmerged branch claude/wand125-confirmations-2026-10-11, file blob 614d2be3, run with main's census): axis and least-bound oblique refusals count at n37 (axis gap 6.9e-11) and n44 (1.3e-10); at n39 the axis gap is 1.26e-9 > AXIS_ROUNDING 1e-9, CONTROL_SAMPLE_REFUSAL_NOT_COUNTED, so the n39 whole-net control would end CONTROL_FAILED (T-142’s defect; the owner’s answer on #543 for T-142 decides n39’s control too). n145 linear-sample: angles 35 and 111 REPLAYED to the certificate's records (163.7 and 382.4 CPU-s against the source's 138.1 and 312.2, ratio 1.213 at load 3-10).

Price (none ran; owner budget needed): n37 6.53 CPU-h (high 7.49), n39 7.09 (7.50), n44 16.95 (19.94), n145 36.97 (about 24 at T-144's idle ratio; high 64 from the author's 2 h 8 min at 30 workers). Total about 67.5 CPU-h at the measured ratios. Also needed: the candidates retained where the census reads them (#543), n145 registered in audit_wand125_linear with candidate.json and certificate.json retained, the AXIS_ROUNDING decision for n39, and a review of each certificate.

Register plan: four entries at V0/C0, pending adoption, in report order n39, n44, n37, n145, with evidence, coverage and COPY_SEPARATELY lists, in each packet's register-plan.yaml for the records lane. Case records unchanged. No issue asked, so no reply is owed.

Registered on 2026-10-14 in the 14 October records PR (branch claude/wizardly-meitner-wqn4x3-records-1014): T-175 (s(39)), T-176 (s(44)), T-177 (s(37)) and T-179 (s(145) to s(149)), V0 with C1 from the review; F-1 is think-4uun.

## Validation backlog (2026-10-14, owner's cap: hold anything > 40 CPU-h)

Each count's replay is its own bead: think-w76a s(37) 6.53 CPU-h, think-567s s(39) 7.09 CPU-h (its control waits on think-4uun), think-ec27 s(44) 16.95 CPU-h, think-v511 s(145) ~37 CPU-h (range 24-64, run with a stop at 40). Each is within the cap; the three fine-net counts wait on the owner's #543 answer on retaining the candidates where the census reads them. The total, 67.5 CPU-h, is over 40 only summed. The whole backlog is think-lh7d.

Renumbered on 14 October at review A3 of #602 (records PR, branch claude/wizardly-meitner-wqn4x3-records-1014): Kevin Fang's theorem, T-178 above, is now T-163, at Theorem 1's first commit (6028f31, 12 October); T-163 to T-177 above are now T-164 to T-178. T-179 to T-184 keep their ids.
