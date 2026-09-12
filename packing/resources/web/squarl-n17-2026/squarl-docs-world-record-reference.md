# Published n=17 reference packing

`data/world-record.json` contains John Bidwell's best-known packing of 17
congruent squares. Its exact construction gives unit-square container width
`4.67553009360455095163411127048315...`; optimality has not been proved. The
JSON's `known_record_width` retains Squarl's existing float64 benchmark,
`4.67553009360455`.

The centres and angles are reconstructed from David Ellsworth's exact SVG
construction and normalised into Squarl's fixed unit container. The source
construction uses six squares at `39.8049589797678°`, one at
`-36.6237863834466°`, and ten axis-aligned squares.

Squarl stores geometry as `float32`. The JSON geometry therefore uses the
largest nearby side length that remains legal after all coordinates are
rounded to `float32`: `0.21387946605682373`, corresponding to container width
`4.675530654889137`. The exact published comparison value remains in
`known_record_width`.

The reference arrangement is repeated for the initial, polished-initial and
unpolished fields so the file remains compatible with the normal live
arrangement schema. It is reference data and does not replace
`data/best-ever.json`.

Sources:

- [David Ellsworth's current packing catalogue](https://kingbird.myphotos.cc/packing/squares_in_squares.html)
  and its [exact SVG construction](https://kingbird.myphotos.cc/packing/square-17.svg)
- [Gensane and Ryckelynck's numerical reconstruction](https://doi.org/10.1007/s00454-004-1129-z)
- [Erich Friedman's survey](https://erich-friedman.github.io/papers/squares.pdf)
