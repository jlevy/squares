---
type: is
id: is-01m4yst7ny3g52xgq8yr82r2az
title: "Validate: Couzo 487b058's 296 beyond-horizon certificates, exact replay on both routes (38-48 CPU-h; HELD)"
kind: task
status: open
priority: 3
version: 3
labels:
  - result-import
dependencies: []
parent_id: is-01m4yd28hxb6m3ns2fbzws27ns
created_at: 2026-10-15T03:31:09.628Z
updated_at: 2026-10-16T00:13:48.073Z
---
Validation part of think-nj7h (franciscouzo/square-packing 487b05809099d8f7d006aaeb6bfc1ebe95cb8d0d, first committed 2026-10-14T17:45:39Z, no issue). HELD by the owner's cap (2026-10-14: hold anything above 40 CPU-h).

## Validation
- Claim: the 296 certificates 487b058 adds or changes beyond n = 324 (339, 370, 378 to 382, 403 to 991), each a finite upper bound at its exact header side. 294 are recorded under the per-count rule against the record's beyond-horizon rows, the grid and every earlier report (2 are above Fang's earlier composites at 812 and 930); all 296 are later superseded by #607 (16 counts) and the 4e4c8ce index (all). Packet packing/resources/web/couzo-verified-bounds-2026-10-14/ on claude/wizardly-meitner-wqn4x3-reads-1015; comparison in its review/beyond-horizon-comparison.json, claims record review/beyond-horizon-claims.json.
- Custody: the 296 files (33,074,931 bytes) are bulk data under OR-18 and pinned by SHA-256 in acquisition/upstream-subtree.sha256, not retained; a replay reads them from a checkout at the pin (git clone --filter=blob:none, sparse checkout of the scope in acquisition/declaration.json) or from a hosted release the owner publishes (devtools.hosted_data; publishing is outside the session's grant). Either way the bytes are held to the manifest digests first.
- Run: the two maintained exact routes of devtools.evand_arrangement_reports, a positive, a duplicate-square and an outside-container job per count, one worker. devtools.upper_bound_reports certifies only retained rows, so this needs either a scratch packet that retains the 296 (never committed) with `python -m devtools.upper_bound_reports PACKET certify --jobs-dir SCRATCH/jobs --workers 1`, keeping only a summary receipt in Git, or a W7 slice that lets a packet certify pinned-only rows from a checkout. The full receipt would itself be tens of MB (it keeps every deciding input) and belongs in a hosted release.
- Cost: 456,922,338 pair decisions (3 n(n-1) summed); at the 0.30 to 0.38 ms a decision the 211 and 237 replays measured here (50 route CPU-s each), 38 to 48 CPU-h. The largest job (n = 991, 981,090 decisions over both routes) is about 300 to 370 CPU-s, under the kernel's 600 s job deadline on a quiet host.
- Budget status: HELD (the upper estimate is above 40 CPU-h).
- Proposed subsets (each well under the cap; proposals only): the 31 recorded counts whose earlier best is a report rather than the grid (339, 370, 378 to 382, 420 to 422, 462 to 464, 506 to 508, 552, 553, 600, 601, 650, 651, 702, 756 to 758, 813, 814, 870, 871, 964): 33,181,470 decisions, 2.8 to 3.5 CPU-h; or every count up to 500: 2.7 to 3.5 CPU-h.
- Depends on: the owner's word on hosting (OR-18) or a W7 slice for pinned-only replay; the owner's budget for the whole.
- Done when: every replayed count passes both routes with both controls refused, the receipt or its summary is retained, and the evidence is registered with the beyond-horizon rows.
- Machine note: four shared CPUs; a whole run is about 10 to 12 wall-hours at one worker.

## Notes

## 2026-10-15: the hosted-release step (coordinator: keep the OR-18 pinning; host the bytes for the replay)

The 296 certificates stay out of Git, pinned by SHA-256 in the packet's acquisition/upstream-subtree.sha256. For a replay they go out as a data release by development.md, "Publishing Hosted Data", from packing/:

1. Fetch: blobless clone of franciscouzo/square-packing, sparse checkout of the packet's declared scope at 487b05809099d8f7d006aaeb6bfc1ebe95cb8d0d; hold every certificates/nNNN.cert (NNN > 324) to its manifest digest (or let `devtools.upper_bound_reports couzo-verified-bounds-2026-10-14 derive --checkout CHECKOUT --check`'s checkout_problems do it).
2. Pack: one deterministic tarball of the 296 files rather than 296 assets (`tar --sort=name --mtime=@0 --owner=0 --group=0 --numeric-owner`, then `gzip -n`), about 33 MB raw, with its member list equal to the packet's manifest lines for those paths.
3. Ignore the local directory that holds it (for example packing/hosted-data/couzo-487b058/) in .gitignore.
4. Stage: `python -m devtools.hosted_data stage --manifest hosted/couzo-487b058-beyond-horizon-certificates.yaml --from hosted-data/couzo-487b058 --repository jlevy/squares --tag data/couzo-487b058-beyond-horizon-certificates-v1`, add a description naming the packet and the pin, and commit the manifest (never the bytes) in a pull request.
5. Publish (the owner: publishing a release is outside the session's grant): `python -m devtools.hosted_data publish --manifest hosted/couzo-487b058-beyond-horizon-certificates.yaml`, which uploads and then downloads and checks every asset.
6. Replay lane: `python -m devtools.hosted_data fetch --manifest hosted/couzo-487b058-beyond-horizon-certificates.yaml`, unpack, hold each member to the packet manifest, then certify (the scratch-packet route or the W7 pinned-only route above). The full receipt keeps every deciding input, tens of MB, so it goes out the same way under data/couzo-487b058-beyond-horizon-receipts-v1, and Git keeps only its summary and the manifest.

Göbel update (same day): 42 of the rows the packet compares are now `undecided-goebel` (above Göbel's classical construction at their count), pending the owner; 252 are recorded. The proposed subset of 31 report-beaten counts is now 30 (964 is undecided-goebel): 339, 370, 378-382, 420-422, 462-464, 506-508, 552, 553, 600, 601, 650, 651, 702, 756-758, 813, 814, 870, 871. The price of the whole is unchanged (456,922,338 pair decisions, 38-48 CPU-h, HELD).

2026-10-16 coordinator: fold in hosting of the 296 487b058 certificates (bytes held only in Couzo's repository at the pin; #627 616/A7, owner decision 2): the replay needs them until a hosted release keeps them.
