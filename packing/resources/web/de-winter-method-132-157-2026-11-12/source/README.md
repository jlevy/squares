# Square packing

Packings of n unit squares in a square, each with a smaller side than the value listed by [the Squares Project](https://squaremath.org/) on the date shown.

| n | Side, rounded up | Squares Project value | Date |
| ---: | ---: | ---: | :--- |
| [132](n132/) | 11.976048383604 | 11.9856801988458088 | 11 November 2026 |
| [157](n157/) | 12.993302611344 | 13 | 11 November 2026 |
| [172](n172/) | 13.614689853284 | 13.6146898532862152 | 10 November 2026 |
| [199](n199/) | 14.614689853284 | 14.6175721735928069 | 9 November 2026 |
| [227](n227/) | 15.563796703670 | 15.57106781186547 | 17 October 2026 |
| [229](n229/) | 15.650174756949 | 15.65685424949238 | 17 October 2026 |
| [260](n260/) | 16.645778804182 | 16.65685424949238 | 17 October 2026 |

The folders for n = 227, 229 and 260 hold the coordinates, an exact rational certificate, before/after figures, a proof report and three exact checkers. To check one of these packings, run `python3 -B verify_all.py` in its folder (Python 3.10 or later, standard library only). The folders for n = 132, 157, 172 and 199 hold the exact rational coordinates, a figure and one exact checker (`python3 -B verify_exact.py`).

For n = 227, 229 and 260, the numerical search, rational certificate construction, checking and visualization were performed with OpenAI Codex agents under the direction of Joost de Winter. For n = 172 and 199, this work was performed with Claude (Anthropic) under the direction of Joost de Winter. For n = 132 and 157, this work was performed with Claude Fable 5.2 (Anthropic) under the direction of Joost de Winter.

The folder [above324](above324/) holds fifteen further packings for n between 413 and 910, each with a smaller side than the best value recorded by the Squares Project on 9 November 2026. This work was performed with Claude (Anthropic) under the direction of Joost de Winter.

The folder [above324_refined](above324_refined/) holds twenty-two packings for n between 597 and 991 that refine public packings of the Kaggle competition "Squares in Squares". This work was performed with Claude (Anthropic) under the direction of Joost de Winter.

The folder [method_n132_n157](method_n132_n157/) holds the code that produced the packings for n = 132 and 157: the growth step, the optimization model, the high-precision solutions and two further checks.

All files are released under the MIT licence (see `LICENSE`).
