# A215 -- CLOSED-NODE BENCHMARK of the current A211 runner (2026-09-14)

Each node re-run ROOT-TO-KILL with `attempts/A211-coarse-tree/code/run211.py page <nid> --pads <pad> --wall 3600 --no-inherit --cert-dir attempts/A215-closed-node-benchmark/certs --results attempts/A215-closed-node-benchmark/results/bench215.jsonl --no-fig`, every optimisation flag at its default (A213 integer core, A213b integer clip, A214 C kernel, A211e/f conditional coarse core, A211d/f memos), ONE process at a time, BelowNormal (A210's fix), BLAS pinned, `PYTHONDONTWRITEBYTECODE=1`.

`new (s)` is the WALL of the whole process (stage 0 + load + tree), which is what the old campaign seconds also measured.

| node | pad | old campaign | old (s) | new (s) | ratio | verdict | agrees? |
|---|---|---|---:|---:|---:|---|---|
| `k5_11_interior_Y0308` | g1 | A205 | 203.2 | 42 | 4.84x | DEAD | yes |
| `k5_16_interior_Y0054` | g1 | A205 | 312.2 | 28 | 11.15x | DEAD | yes |
| `k5_16_interior_Y0027` | g1 | A205 | 365.2 | 14 | 26.09x | DEAD | yes |
| `k5_16_interior_Y0565` | g1 | A205 | 397.1 | 33 | 12.03x | DEAD | yes |
| `k5_16_interior_Y0839` | g1 | A205 | 526.2 | 12 | 43.85x | DEAD | yes |
| `k5_16_interior_Y0881` | g1 | A211 pass 1 | 879.1 | 592 | 1.48x | DEAD | yes |
| `k5_16_interior_Y0719` | g1 | A211 | 236.6 | 178 | 1.33x | DEAD | yes |
| `k5_16_interior_Y1110` | g1 | A209 | 1765.5 | 57 | 30.97x | DEAD | yes |
| `k5_11_interior_Y0036_D07` | zero | A211f | 106.2 | 675 | 0.16x | DEAD | yes |
| `k5_11_interior_Y0985` | g1 | A206 | 2120.8 | 140 | 15.15x | DEAD | yes |
| `k5_11_interior_Y1104` | g1 | A206 | 2401.3 | 94 | 25.55x | DEAD | yes |

**Geometric-mean speedup over the 11 agreeing nodes: 7.22x**  (spread 0.16x -- 43.85x; median 12.03x)

**LIKE-FOR-LIKE sub-mean.** Only 6 of the 11 old numbers are themselves a ROOT-TO-KILL wall (the five A205 clip-tree pages and A209's Y1110); the other five old numbers had a head start this run did not (A211/A211f inherited dead branches, A206 started from A205's leaf certificates).  Over those 6 genuinely comparable nodes the geometric mean is **16.86x** (spread 4.84x -- 43.85x).

**Reading the one ratio below 1 (`k5_11_interior_Y0036_D07`, 0.16x).**  It is NOT a slowdown and NOT a regression: the page still dies, and it dies from the A203 ROOT with nothing inherited (52 nodes, 0 alive leaves, 671 s).  A211f's 106.2 s was a run that started from 6 inherited DEAD branches and 5 start nodes, i.e. most of the tree was already proved.  The comparable statement is that the whole page, root to kill, now costs 671 s where A211e could not close it at all inside 900 s even WITH the same inheritance.

No regression: every node still dies, with the old verdict.

## Per-run detail

| node | pad | nodes | alive leaves | rc | wall-limited | row seconds | leaf |
|---|---|---:|---:|---:|---|---:|---|
| `k5_11_interior_Y0308` | g1 | 25 | 0 | 0 | False | 40.4 | every branch DEAD (0 inherited from prior certificates + 13 proved here): R.1 TR(0,0)<-[23] by FC; R.2.1.1r1 root<-None  |
| `k5_16_interior_Y0054` | g1 | 8 | 0 | 0 | False | 27.2 | every branch DEAD (0 inherited from prior certificates + 3 proved here): R.1r1 root<-None by COUNT; R.2r1 root<-None by  |
| `k5_16_interior_Y0027` | g1 | 7 | 0 | 0 | False | 12.6 | every branch DEAD (0 inherited from prior certificates + 5 proved here): R.1 BR(0,1)<-[10] by FC; R.2r1 root<-None by Em |
| `k5_16_interior_Y0565` | g1 | 12 | 0 | 0 | False | 31.7 | every branch DEAD (0 inherited from prior certificates + 6 proved here): R.1 BR(0,1)<-[10] by FC; R.2r3 root<-None by Em |
| `k5_16_interior_Y0839` | g1 | 5 | 0 | 0 | False | 11.3 | every branch DEAD (0 inherited from prior certificates + 3 proved here): R.1 BR(0,1)<-[10] by FC; R.2r1 root<-None by Em |
| `k5_16_interior_Y0881` | g1 | 51 | 0 | 0 | False | 590.5 | every branch DEAD (0 inherited from prior certificates + 32 proved here): R.1r2 root<-None by FC; R.2.1 BR(0,1)<-[10] by |
| `k5_16_interior_Y0719` | g1 | 53 | 0 | 0 | False | 175.5 | every branch DEAD (0 inherited from prior certificates + 35 proved here): R.1 TR(0,1)<-[14] by REACH; R.2.1 BR(0,1)<-[10 |
| `k5_16_interior_Y1110` | g1 | 22 | 0 | 0 | False | 55.9 | every branch DEAD (0 inherited from prior certificates + 9 proved here): R.1.1r1 root<-None by EmptyBox; R.1.2r1 root<-N |
| `k5_11_interior_Y0036_D07` | zero | 52 | 0 | 0 | False | 670.7 | every branch DEAD (0 inherited from prior certificates + 32 proved here): R.1.1 TL(1,0)<-[13] by EmptyBox; R.1.2.1 BR(0, |
| `k5_11_interior_Y0985` | g1 | 45 | 0 | 0 | False | 138.2 | every branch DEAD (0 inherited from prior certificates + 31 proved here): R.1r1 root<-None by EmptyBox; R.2.1.1 TL(1,0)< |
| `k5_11_interior_Y1104` | g1 | 26 | 0 | 0 | False | 92.9 | every branch DEAD (0 inherited from prior certificates + 13 proved here): R.1 BR(0,1)<-[11] by EmptyBox; R.2.1 TL(1,0)<- |

## Caveats on the OLD seconds (quoted exactly from the campaign rows)

* `k5_11_interior_Y0308` pad g1 -- A205, 203.2 s, DEAD: clip tree, root-to-kill
* `k5_16_interior_Y0054` pad g1 -- A205, 312.2 s, DEAD: clip tree, root-to-kill
* `k5_16_interior_Y0027` pad g1 -- A205, 365.2 s, DEAD: clip tree, root-to-kill
* `k5_16_interior_Y0565` pad g1 -- A205, 397.1 s, DEAD: clip tree, root-to-kill
* `k5_16_interior_Y0839` pad g1 -- A205, 526.2 s, DEAD: clip tree, root-to-kill
* `k5_16_interior_Y0881` pad g1 -- A211 pass 1, 879.1 s, DEAD: WITH inherit (2 inherited dead branches)
* `k5_16_interior_Y0719` pad g1 -- A211, 236.6 s, DEAD: WITH inherit (4 inherited dead branches)
* `k5_16_interior_Y1110` pad g1 -- A209, 1765.5 s, DEAD: root-to-kill from the A203 root
* `k5_11_interior_Y0036_D07` pad zero -- A211f, 106.2 s, DEAD: pad 0; WITH inherit (6 inherited dead); A211e before = 528.9
* `k5_11_interior_Y0985` pad g1 -- A206, 2120.8 s, DEAD: Rule-NS tree on A205's leaves (not root-to-kill)
* `k5_11_interior_Y1104` pad g1 -- A206, 2401.3 s, DEAD: Rule-NS tree on A205's leaves (not root-to-kill)

## Stage table (A211f `code/profstage211.py`) for two runs

Two extra cProfile runs, same flags and same isolation.  The columns are, in order, `k5_16_interior_Y0027` pad g1 and `k5_16_interior_Y0839` pad g1 -- the two cheapest nodes, chosen so the profiler's overhead is paid on short runs.  cProfile roughly triples the wall (12.6 s -> 39.9 s, 11.3 s -> 35.0 s), so read the SHARES, not the seconds.  Note the shape against A211f's own table (Y0202, no-room-bound at 82%): on a page that dies FAST there is no no-room leaf at all -- the budget is the option table (52-63%, of which ROLE-REACH 10-15%), the coarse fixed point (26-29%) and K' (18-21%).  The lane cover, 40% of A211f's expensive page, does not appear.

```
stage                            prof_k5_16_i  prof_k5_16_i
TOTAL (s)                                39.9          35.0
coarse fixed point                   10.4 26.1%      10.1 28.8%
  ... normalise (page)               10.7 26.7%      10.3 29.6%
option table (build_options)         20.8 52.2%      22.1 63.1%
  ... ROLE-REACH                      3.8  9.6%       5.2 14.9%
MBox.rebuild (K') [outer]             7.0 17.6%       7.2 20.7%
  ... pieces_poly                     6.6 16.5%       6.7 19.3%
  ... polycore.build                  6.2 15.5%       6.3 18.0%
_clip_rect_obstacle [outer]           4.3 10.7%       3.6 10.4%
```
