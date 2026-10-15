# Certificates instantiating the theorem, n = 15..64

For every n from 15 to 64, `n0NN_F<F>.cert` is an exact strict certificate of `n² − n + F(n)` unit
squares in a square of side `n − 1/20000`, where `F(n) = 1 + max{p + 2q : 16p + 21q ≤ n − 15}` is the
excess the note's Theorem 2 guarantees. Each was built by the uniform construction of the note:
start from the base piece for `r = n − 16p − 21q` (15 ≤ r ≤ 30), glue the 22 × 21 rectangle q times and
the 17 × 16 rectangle p times, every step being Lemma 3 at the common squeeze d0 = 1/10000
(`tools/glue.py --d 1/10000 --closed`), then scale centres and side once by 1 + d0/(2(n − d0)).
`inventory.tsv` has, per n: F, p, q, base, count, exact side, side rounded up to 15 places, the
checker verdicts, sha256 and the gluing chain. `PIECES.md` lists every input piece with its
squeeze and hash (d0 is below all of them). `best/` holds the 26 certificates where the same pieces
plus the excess-2 squares and the other rectangles give a larger excess than F(n) (`best.tsv`;
the inventory it ranges over is defined in PIECES.md). All of this regenerates from the pieces with
`tools/glue.py`; the private tool `instantiate_theorem.py` is the script that did it.
