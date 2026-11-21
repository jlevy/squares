# Best submitted file

`submission-best.csv.gz` is the best file that Sergio Fernández Rubio (GeiserX) submitted to the Kaggle competition "Squares in Squares". The competition page is https://www.kaggle.com/competitions/squares-in-squares. It is the gzip of round 38 a (`round38-2026-11-18a.csv`, Kaggle ref 58514241), the last round. It has one packing for every n from 1 to 1000, in the competition's submission format (`id,n,square_id,x,y,angle`).

`x` and `y` are the centre of each unit square. `angle` is in radians, so the tilted square of n = 5 has 0.7853981633974483, which is π/4.

| | |
|---|---|
| Public score | 22.1124018632 (rank 29 of 2,226 at 15:00 UTC on 2026-11-18) |
| Local score with `score.py` | 22.1124018632 |
| Gate (`tools/gate.py`) | GREEN, smallest gap between two squares 2.2e-11 |
| SHA-256 of the CSV | `1378c9fd83966c98e4273fa9b9685ea6270802d81a9d0d890255068369714332` |
| SHA-256 of the `.gz` | `c490841279b793a963129680483a21b075fb55e8e26c24d37901c0655c704989` |

## Score it

From the repository root, with Python 3.12 or newer, mpmath, numpy and pandas:

```sh
gunzip -k data/submission-best.csv.gz
python3 score.py data/submission-best.csv --jobs 4 --out per_n.tsv
python3 pdscore.py data/submission-best.csv 4
python3 tools/gate.py data/submission-best.csv --out gate-out --jobs 4
```

`score.py` runs the official metric (`kaggle_metric.py`, unchanged) on each n and writes one row per n. `pdscore.py` reads the file with pandas first, as Kaggle does. A score check takes about 5 minutes on 4 cores.

## Where each layout comes from

Each submitted round has a table in `../results/`. `../results/harvest-best-*.tsv` and `../results/round*-best-*.tsv` give, for each n that the round changed, the score, the side `L`, the source and the licence. For any n, the latest table that lists it gives the source of its layout in this file. Some rows build on public packings. [NOTICE](../NOTICE) lists their authors and terms.

A licence cell "see README" in a results table refers to the project log, now [docs/LANE-LOG.md](../docs/LANE-LOG.md) (sections "Outside data (2026-11-07)" and "Files"). Rows whose source is "seed merged0" start from the seed that `build_seed.sh` assembles from franciscouzo/square-packing (MIT) and Samanyu-dev/squares_in_squares.

## Licence

This file is under CC BY 4.0 (see [LICENSE-CC-BY-4.0.txt](../LICENSE-CC-BY-4.0.txt)). The third-party layouts in it keep their own terms, as [NOTICE](../NOTICE) says. If you use this file or a layout from it, credit Sergio Fernández Rubio (GeiserX, https://github.com/GeiserX/squares-in-squares).
