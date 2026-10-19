# squarepack-certs

Exact certificates for packings of n unit squares in a square of side S < ⌈√n⌉, i.e. upper bounds
s(n) ≤ S. Each folder holds one packing in three formats (Evan Daniel's text, SQUISH json, David
Ellsworth's centre-origin text), a drawing, the output of two independent checkers, and
checksums. `verify.py` is a standalone exact checker (Python 3.8+, standard library only).

| n | S (rounded up; exact value in the certificate) | best known before | status |
|---|---|---|---|
| 308 | 17.999309855162748 | 18, the grid (held by both registers) | not yet submitted |
| 343 | 18.994903529220497 | none, n > 324 (not on either register) | not yet submitted |
| 344 | 18.995489275430816 | none, n > 324 (not on either register) | not yet submitted |

## Verify

```bash
python3 verify.py n0308/n0308.cert --strict        # or n0308/n0308.cert.json; exit 0 iff valid
(cd n0308 && shasum -a 256 -c SHA256SUMS)
```

`verify.py` uses exact rational arithmetic: every square is a rational centre (x, y) and a
rational t = tan(θ/2), containment and pairwise separation are checked by separating axes, and
`--strict` requires every margin to be > 0. `check_packing_output.txt` is the output of
Ellsworth's `check_packing.py` (https://github.com/Davidebyzero/packing_squares_in_squares__tools)
on `nNNNN.txt` at 40 digits.

## Construction

All three belong to the k² − k + 1 family: two wedges of squares tilted by about 19° in opposite
corners (rows along the bottom wall, columns along the left wall), everything else axis-parallel.
They were grown from the Kingbird packings of Ellsworth and Stead (n = 273 for 308 = 18² − 18 + 2;
n = 307 for 343 = 19² − 19 + 1 and 344 = 19² − 19 + 2) by cutting once through each wedge's full
stack and adding a square to every line the cut crosses, then squeezed with a penalty method. The
result was rounded to rationals and repaired exactly: centres scaled by the smallest factor that
clears every overlap, then S raised by 2⁻⁶⁴ so every margin is strictly positive.

## Lineage and credit

The family is due to Arslanov, Mustafin and Shangitbayev (EJC 2021, doi 10.37236/8586), who gave
it for k = 16, 17, 18. The seed packings for n = 241, 273, 307 are David Ellsworth's and Tej
Stead's on the Kingbird table. The text certificate format and strict convention are Evan
Daniel's; the json layout is SQUISH's (Nate Chaoweeraprasit). Details in ATTRIBUTION.md.

Search, verifier and this bundle were written and run with Claude (Anthropic) as a coding and research agent, directed and reviewed by Kevin Fang.

## Conventions

Folders are never edited after submission. A new packing for an n already here goes in a new
dated folder, `nNNNN-YYYY-MM-DD/`. In the drawings, blue squares are tilted by 1° or more.
`verify.py` is MIT (LICENSE); the certificates and drawings are CC0.
