# Theorem A: k² − ⌈√(32k)⌉ − 1 unit squares in a square of side less than k

Code and certificates for the note *Packing k² − ⌈√(32k)⌉ − 1 unit squares in a square of side less than k* (Kevin Fang, draft v0.2, 2026-10-24, https://doi.org/10.5281/zenodo.23624565; `note/main.pdf`, source `note/main.tex`).

The same idea and constant were found first by Evan Daniel, who proves c*(k) ≤ 4⌈√(2k − 7)⌉ − 1 for every k ≥ 7 in Lean (https://github.com/evand/square-packing, `certificates/k2-minus-c/`, commit aa12b98, 18 October 2026). For k ≥ 89 the two integer bounds differ by at most 2. Theorem A is an independent second proof.

**Theorem A.** For every integer k ≥ 6, k² − ⌈√(32k)⌉ − 1 unit squares fit in a square of side less than k. Equivalently c*(k) < 4√(2k) + 1, where c*(k) is the largest c with s(k² − c) = k.

The packing is Sungjoon Ryu's L-shaped packing (doi:10.5281/zenodo.23278927, Theorem 1.3 and Section 6): an aligned (k − b)² grid and two bands of b rows tilted by θ, with tan(θ/2) just above 1/b. Here both ends of each band are filled with axis-parallel rows, and b is the odd integer nearest √(2k).

## Files

```
lband.py            the construction in exact rationals (stdlib only); writes a strict certificate for one k,
                    or checks the bound for a range of k without building (--bound)
windowed_check.py   runs ../verify.py --strict and ../tools/verify_cert_daniel.py, unchanged, on overlapping
                    4 x 4 windows (needed from n ~ 10^4; the argument is in the docstring)
regenerate.sh       rebuilds k = 300 and 600 (12 MB and 49 MB, not shipped) and checks LARGE.sha256
LARGE.sha256        SHA-256 of the k = 300 and 600 certificates
certs/kKKK.cert     the construction for k = 6..40 and 101 (Daniel's text format; the header comment gives
                    b, the count, the waste, the squeeze and both band plans); certs/SHA256SUMS
note/               the note, PDF and LaTeX source
```

## Checking

```bash
python3 theorem-a/lband.py --bound 6 20000          # exact: k^2 - n < 4 sqrt(2k) + 2 for the construction (about 2 s)
for f in theorem-a/certs/k0*.cert; do               # k <= 40: all three checkers, all pairs
  python3 verify.py $f --strict | tail -1; python3 tools/verify_cert_daniel.py $f | tail -1; python3 tools/rectcheck.py $f | tail -1
done
python3 theorem-a/windowed_check.py theorem-a/certs/*.cert   # all 36, both checkers, windowed
sh theorem-a/regenerate.sh                          # k = 300, 600: rebuild, hash, check (a few minutes)
(cd theorem-a/certs && shasum -a 256 -c SHA256SUMS)
```

Every certificate is the closed packing at side S = k − b + W < k, scaled once about the origin by 1 + (k − S)/(2S). So every wall and pair margin is positive, and the side is (S + k)/2 < k. `lband.py` picks the squeeze k − S as 1/(10⁶k³), divided by 10 until the note's conditions (a)–(d) and H(t) < 4√(2k) + 2 hold, decided exactly. By Lemma 2 of the note, every layout it returns satisfies the bound.

`lband.py` is a standalone copy of `proof_layout` in the research repository's `squarepack/lband.py`. The certificates it writes are byte-identical to that program's (checked at k = 6, 7, 31, 101, 300, 600).
