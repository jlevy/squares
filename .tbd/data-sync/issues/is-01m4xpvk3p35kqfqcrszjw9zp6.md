---
type: is
id: is-01m4xpvk3p35kqfqcrszjw9zp6
title: "Validate: wand125 s(39) >= 533/80 (mixed_n39_L66625), census of all 2,073 directions with whole-net controls (~7.1 CPU-h; control needs think-4uun)"
kind: task
status: open
priority: 2
version: 1
labels:
  - validation
  - result-import
dependencies: []
parent_id: is-01m4wv27yed1e2wfnq55h1avr0
created_at: 2026-10-14T17:20:13.941Z
updated_at: 2026-10-14T17:20:13.941Z
---
Validation part of think-u0av for n = 39 (T-175 in the 14 October records PR #602, V0/C1). Record-changing, but the whole-net control cannot pass until think-4uun lands.

## Validation
- Claim: s(39) >= 533/80 = 6.6625 by the check2 measure certificate mixed_n39_L66625 (687 positive rectangles, mass 3899999/100000, candidate digest 3b464f3f...9cfc, core 4999/5000, net {step 1/5002, last 2072}) at wand125/square-packing dfb2cf85fdf9ee5f95c5ec2c67fd49210854f146; release square-lower-bounds-v1 asset certificates__mixed_n39_L66625.tar.gz, 639,558 B, SHA-256 8e88ca06...851f (asset 635702665).
- Run: from packing/, `uv run --frozen --all-extras --group dev python -m devtools.sqverify_fast_census --family mixed --only mixed_n39_L66625 --threads 2 --resume`, then `--control` (99/100 mutant at every direction; original and near-threshold mutant at the least-bound direction, 1804), then `--evidence`; sqverify-fast from the reviewed crate source d97758bb (binary 567a0fd5). Packet packing/resources/web/wand125-fine-net-n37-n39-n44-2026-10-13/ (receipts/premises-n39.json, sample-diagnostic-n39.json, control-sample-n39.json).
- Cost: 7.09 CPU-h (full capture 12,758 CPU s + whole-net controls 12,781 CPU s), from this host's ratio 0.945 to the source on an 8-direction sample (48.06 vs 50.86 CPU s, 2026-10-14; packet README); 7.50 CPU-h at the source's own CPU (author's check2 run: 13,502 direction CPU s).
- Budget status (owner, 2026-10-14): runnable (<= 40 CPU-h).
- Possible <= 40 CPU-h subset: n/a (runnable as a whole).
- Depends on: think-4uun (the axis refusal judged against the sweep's enclosure; n = 39's axis gap is 1.26e-9 > AXIS_ROUNDING 1e-9, so under today's rule the control ends CONTROL_FAILED although the refusal is sound; owner's choice of option on jlevy/squares#543 for T-142); and the owner's #543 answer on retaining the check2 candidates where the census reads them.
- Done when: all 2,073 directions verified with the source's nodes and least bounds; the whole-net controls end CONTROLS_REFUSED under the fixed rule; the `--evidence` entry is registered on T-175 with the 14 October review as the mapped review; noted on think-u0av.
- Machine note: 4 CPUs shared with gates; a run > 2 wall-h should be scheduled outside a validation gate. About 3.5 wall-h at two workers on an idle host.
