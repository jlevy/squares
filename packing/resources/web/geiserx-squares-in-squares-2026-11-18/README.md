# Sergio Fernández Rubio’s Squares in Squares Repository at f822b34

This packet retains part of
[GeiserX/squares-in-squares](https://github.com/GeiserX/squares-in-squares/tree/f822b34456b29addec9b59478aac4eb2306f7566)
at `f822b34456b29addec9b59478aac4eb2306f7566` (committed 2026-11-18T18:37:44Z), the
commit
[issue #1040](https://github.com/jlevy/squares/issues/1040) names and the head when the
lane read it on 20 November 2026.
The repository is Sergio Fernández Rubio’s (GeiserX) code, layouts and notes for the
Kaggle competition “Squares in Squares”. Its first commit, `c409de5` (15:41:34Z on 18
November), publishes the whole tree. The four after it change documents, images and
repository settings, and nothing under `results/`. The submission and the results table
retained here have the same blobs at `c409de5` and at the pin.

Intake lane c7-pointers (think-squj) retained it on 20 November 2026 as the cited public
source of issue #1040, which Joost de Winter filed as a pointer.

## What the Issue and the Source Claim

- **The issue** says GeiserX published a packing of 259 unit squares with side
  16.590016439573 in `data/submission-best.csv.gz` at `f822b34`, under CC BY 4.0, joining
  tilted bands from his 292- and 445-square packings, 0.00136 below T-193’s
  16.591378145498. It says Nevska reached the same side on Kaggle on 8 November 2026
  without published coordinates. It attaches `packing-259.zip`, which it says holds an
  exact rational Witness/v2 of the packing and a verifier, and asks that the packing be
  credited to GeiserX.
- **`data/README.md`** says the file is the gzip of the author’s best submission, round
  38 a, with one packing for every n from 1 to 1000 in the competition’s format
  `id,n,square_id,x,y,angle`, the angle in radians. It gives a public score of
  22.1124018632, rank 29 of 2,226 at 15:00 UTC on 18 November, and the SHA-256 of the
  CSV and of the `.gz`, and says the author’s gate found a smallest gap of 2.2 × 10⁻¹¹.
  The latest results table that lists an n gives the source of its layout.
- **`results/round33-best-2026-11-17.tsv`**, the last table to list 259, gives L =
  16.590016439573077 from `k123_join.py`: the first band of the author’s 292 up to chain
  6 joined with the second band of his 445 from chain 13, shifted 5 rows, then
  `k123_turn.py` and an fq quench loop. Its licence cell reads “our own construction on
  held packings (upstream notices in the named ancestry)”.
- **Credit.** `README.md`, `NOTICE`, `AUTHORS` and `AI_NOTICE.md` ask that any reuse
  credit “Sergio Fernández Rubio (GeiserX), https://github.com/GeiserX/squares-in-squares”
  and keep `NOTICE`. `NOTICE` lists the third-party sources the layouts build on.

## Retained Here

`devtools.acquire_source` wrote the packet from
[acquisition/declaration.json](acquisition/declaration.json). Every file is bound to its
Git blob at the pin. Nine files are retained under [source/](source/): the root
attribution files, `data/README.md` and the round 33 table.
`data/submission-best.csv.gz` (7,437,306 bytes) is pinned by digest only. It is above
OR-18’s per-blob ceiling and holds binary64 rows, not a certificate. The digests
`data/README.md` gives for it and for its CSV match the pinned file. The rest of the
tree, about 5,250 scripts, notes and tables, is out of scope.

## What This Packet Does Not Do

The source states no exact coordinates and no certificate: its rows are binary64
decimals with angles in radians. So nothing here is imported, and no register entry
rests on this packet.
The issue’s attachment, which it says holds an exact Witness/v2, is refused by this
session’s proxy (HTTP 403 for GitHub’s `user-attachments`) and was not read.
The 259 result stays queued on think-squj until a session that can read the attachment
retains it, or the author commits it to a watched repository. Then it is replayed on both
maintained routes, measured against T-193’s packing, walked at 259, and registered with
the credit the issue asks for.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
