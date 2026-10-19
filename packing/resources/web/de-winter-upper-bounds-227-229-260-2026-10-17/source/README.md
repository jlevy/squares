# Square packing

Packings of n unit squares in a square, each with a smaller side than the value listed by [the Squares Project](https://jlevy.github.io/squares/) on 17 October 2026.

| n | Side, rounded up | Squares Project, 17 October 2026 |
| ---: | ---: | ---: |
| [227](n227/) | 15.563796703670 | 15.57106781186547 |
| [229](n229/) | 15.650174756949 | 15.65685424949238 |
| [260](n260/) | 16.645778804182 | 16.65685424949238 |

Each folder holds the coordinates, an exact rational certificate, before/after figures, a proof report and three exact checkers. To check a packing, run `python3 -B verify_all.py` in its folder (Python 3.10 or later, standard library only).

The numerical search, rational certificate construction, checking and visualization were performed with OpenAI Codex agents under the direction of Joost de Winter.

All files are released under the MIT licence (see `LICENSE`).
