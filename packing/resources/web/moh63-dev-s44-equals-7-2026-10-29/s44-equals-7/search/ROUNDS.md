# Search history (float LP value; zmx2 at factor 43.995/LP; "bad roots" = root boxes not certified)

Columns: point orbits + grid-line segment pieces (q = 50), D4 orbits.  Warm start: Daniel's s(45) = 7 cover scaled to
LP total.  Each run restarts from the previous round's cover and saved constraint rows.

| run/round | LP | factor | bad roots | uncertified boxes | note |
|---|---|---|---|---|---|
| C r0 | 43.7844 | 1.004808 | 509 | — | |
| D r0 | 43.7914 | 1.004647 | 302 | 123,616 | |
| E r0 | 43.7984 | 1.004487 | 215 | 88,040 | |
| E r1 | 43.8063 | 1.004305 | 141 | 57,415 | stall diagnosed: near-wall valleys at tilts 0.01°–3° |
| H r0 | 43.8030 | — | — | — | tilesep.py added; min 0.9706, zmx2 skipped |
| H r1 | 43.8083 | 1.004259 | 88 | 35,846 | |
| H r2 | 43.8096 | 1.004229 | 46 | 18,627 | |
| I r1 | 43.8113 | 1.004190 | 40 | 15,597 | |
| I r2 | 43.8160 | 1.004082 | 18 | 7,529 | |
| I r3 | 43.8192 | 1.004010 | 13 | 5,390 | |
| J r0 | 43.8213 | 1.003962 | 22 | 8,387 | restart |
| J r1 | 43.8233 | 1.003915 | 7 | 2,941 | |
| **K r0** | **43.8242** | **1.003896** | **0** | **0** | **VERIFIED-D4** → certificate |
