# Attribution

## Author

Kevin Fang.

## Builds on

- M. Z. Arslanov, S. A. Mustafin and Z. K. Shangitbayev, "Improved packings of n(n − 1) unit squares in a square", Electronic Journal of Combinatorics 28(4) (2021) P4.22, doi 10.37236/8586: the construction everything here comes from. Their decomposition of the square into two integer blocks and two squeezable pieces is the gluing lemma (Lemma 3 of the note, `tools/glue.py`), and their two-wedge packings of k² − k + 1 squares for k = 16, 17, 18 are the family the direct packings and rectangles grow from.
- David Ellsworth and Tej Stead: the n = 241, 273 and 307 packings on the Kingbird table (https://kingbird.myphotos.cc/packing/squares_in_squares.html), used as seeds for n = 308, 343, 344 and for the 17 × 16, 18 × 17 and 19 × 18 rectangles. Ellsworth's `check_packing.py` (https://github.com/Davidebyzero/packing_squares_in_squares__tools) produced the `check_packing_output.txt` files.
- Joost de Winter: the packing of 211 = 15² − 15 + 1 unit squares in side 14.99796… (https://github.com/JoostdeWinter/square-packing-211, 16 September 2026), the base case n = 15 of both theorems. It has no licence and is not copied here; `third_party/fetch_unlicensed.sh` downloads it.
- Daniil Ostashev: the later improvement of de Winter's n = 211 packing to side 14.99634…; not used in any certificate here.
- Evan Daniel (https://github.com/evand/square-packing): the certificate text format and the strict convention; the exact checker `verify_cert.py` (`tools/verify_cert_daniel.py`); the exact certificates of known packings used as B pieces and base cases (`third_party/daniel/n-*.cert`, and n-211.cert, fetched); and the improvements of our n = 308, 343, 344 packings by local search, posted in jlevy/squares#489 (`third_party/daniel/hunt3_n*.cert`). All MIT.
- Francisco Couzo: the packing of 342 unit squares (https://github.com/franciscouzo/square-packing), whose two eight-line wedges were the seed for n = 381 and 380 and, through 381, for n = 421 and the 21 × 20 rectangle; through 421, also for the 22 × 21 rectangle. Not redistributed here.
- The Squares Project (J. Levy et al., https://github.com/jlevy/squares): replayed and confirmed the n = 308, 343, 344 certificates with its own exact implementations (jlevy/squares#484), and verified and registered de Winter's 211.
- SQUISH (Nate Chaoweeraprasit): the json certificate layout.

## Review

An independent review of an early draft of the note by another language model, GPT-6 Astra, found the errors corrected in v0.2 of the note.

## AI assistance

Search, verifier and this bundle were written and run with Claude (Anthropic) as a coding and research agent, directed and reviewed by Kevin Fang.

## Licence

The code (`verify.py`, `tools/glue.py`, `tools/rectcheck.py`, the shell scripts) is MIT, see LICENSE. The certificates, text files, tables and drawings in `nNNNN/`, `rectangles/` and `composites/` are released under CC0 1.0. `third_party/daniel/` and `tools/verify_cert_daniel.py` are Evan Daniel's, under the MIT licence in `third_party/daniel/LICENSE`.
