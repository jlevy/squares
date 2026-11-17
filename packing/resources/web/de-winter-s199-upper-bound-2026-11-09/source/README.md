# Square packing

Packings of n unit squares in a square, each with a smaller side than the value listed by [the Squares Project](https://squaremath.org/) on the date shown.

| n | Side, rounded up | Squares Project value | Date |
| ---: | ---: | ---: | :--- |
| [199](n199/) | 14.614689853284 | 14.6175721735928069 | 9 November 2026 |
| [227](n227/) | 15.563796703670 | 15.57106781186547 | 17 October 2026 |
| [229](n229/) | 15.650174756949 | 15.65685424949238 | 17 October 2026 |
| [260](n260/) | 16.645778804182 | 16.65685424949238 | 17 October 2026 |

The folders for n = 227, 229 and 260 hold the coordinates, an exact rational certificate, before/after figures, a proof report and three exact checkers. To check one of these packings, run `python3 -B verify_all.py` in its folder (Python 3.10 or later, standard library only). The folder for n = 199 holds the exact rational coordinates, a figure and one exact checker (`python3 -B verify_exact.py`).

For n = 227, 229 and 260, the numerical search, rational certificate construction, checking and visualization were performed with OpenAI Codex agents under the direction of Joost de Winter. For n = 199, this work was performed with Claude (Anthropic) under the direction of Joost de Winter.

All files are released under the MIT licence (see `LICENSE`).
