# A226 survey -- corner status of the record packings below ceil(sqrt n)

Pattern = corners BL BR TR TL: F = flush (slot square present), k = number of squares meeting the open unit corner box.  Depth = 1 - min over the square of max(u, v) in the corner frame.

| n | side | ceil | slack | tilted | flush corners | singly met | doubly met | pattern | wall touchers F/R/C/L | source |
|---|---|---|---|---|---|---|---|---|---|---|
| 5 | 2.707107 | 3 | 0.2929 | 1 | 4 | 4 | 0 | F F F F | 2/2/2/2 | Goebel 1979 (proved: Goebel) (square-5) |
| 10 | 3.707107 | 4 | 0.2929 | 2 | 4 | 4 | 0 | F F F F | 3/3/3/3 | Goebel 1979 (proved: Stromquist 2003) (square-10) |
| 11 | 3.877084 | 4 | 0.1229 | 5 | 3 | 3 | 1 | F F 2 F | 3/3/2/3 | Trump 1979 (rigid) (square-11) |
| 17 | 4.675530 | 5 | 0.3245 | 7 | 4 | 4 | 0 | F F F F | 4/4/3/4 | Bidwell 1998 (square-17) |
| 18 | 4.822876 | 5 | 0.1771 | 8 | 4 | 4 | 0 | F F F F | 3/4/3/4 | Hamalainen 1980 / Gustafsson 1981 variant pictured (square-18) |
| 19 | 4.885618 | 5 | 0.1144 | 8 | 4 | 4 | 0 | F F F F | 4/4/3/3 | Wainwright 1979 (Cottingham) (square-19) |
| 26 | 5.621320 | 6 | 0.3787 | 9 | 4 | 4 | 0 | F F F F | 5/5/5/4 | Friedman 1997 (26b) (square-26b) |
| 27 | 5.707107 | 6 | 0.2929 | 5 | 4 | 4 | 0 | F F F F | 5/5/5/5 | Goebel 1979 (square-27) |
| 28 | 5.824445 | 6 | 0.1756 | 12 | 4 | 4 | 0 | F F F F | 5/5/5/5 | Ellsworth Dec 2025 (rigid) (square-28) |
| 29 | 5.933833 | 6 | 0.0662 | 14 | 4 | 4 | 0 | F F F F | 5/5/5/4 | Schadt / Ellsworth Dec 2025 (square-29) |
| 37 | 6.598620 | 7 | 0.4014 | 15 | 4 | 4 | 0 | F F F F | 6/6/5/5 | Cantrell 2002 (square-37) |
| 38 | 6.707107 | 7 | 0.2929 | 6 | 4 | 4 | 0 | F F F F | 6/6/6/6 | Goebel 1979 (square-38) |
| 39 | 6.810722 | 7 | 0.1893 | 15 | 4 | 4 | 0 | F F F F | 6/6/6/6 | Schadt / Ellsworth Jan 2026 (square-39) |
| 40 | 6.828427 | 7 | 0.1716 | 16 | 4 | 4 | 0 | F F F F | 6/6/6/6 | Goebel 1979 (rigid) (square-40) |
| 41 | 6.926693 | 7 | 0.0733 | 15 | 4 | 4 | 0 | F F F F | 6/6/6/6 | Schadt / Ellsworth Jan 2026 (square-41) |
| 50 | 7.571429 | 8 | 0.4286 | 16 | 4 | 4 | 0 | F F F F | 7/7/7/7 | Schadt / Ellsworth Dec 2025 (square-50) |
| 51 | 7.700799 | 8 | 0.2992 | 22 | 4 | 4 | 0 | F F F F | 7/7/7/7 | Schadt / Ellsworth 2026 (square-51) |
| 52 | 7.707107 | 8 | 0.2929 | 8 | 4 | 4 | 0 | F F F F | 7/7/7/7 | Goebel 1979 (square-52) |
| 53 | 7.822876 | 8 | 0.1771 | 14 | 4 | 4 | 0 | F F F F | 7/7/7/7 | Cantrell 2002 / Ellsworth 2026 (square-53) |
| 54 | 7.846667 | 8 | 0.1533 | 16 | 4 | 4 | 0 | F F F F | 7/7/7/7 | Cantrell 2005 / DeVincentis 2014 (square-54) |
| 55 | 7.945771 | 8 | 0.0542 | 18 | 4 | 4 | 0 | F F F F | 7/7/7/6 | Schadt / Ellsworth 2026 (square-55) |
| 11 | 3.877084 | 4 | 0.1229 | 5 | 3 | 3 | 1 | F F F 2 | 0/0/0/0 | certs/trump11_certificate.json (s0 = 969271/250000) (trump_cert) |

## Doubly-met corners (meeters: index, tilt deg mod 90 folded to [0, 45], depth, frame centre)

- n = 11 (square-11) TR: #2 tilt 0.000 depth 0.1555 centre (0.500, 1.345); #10 tilt 40.182 depth 0.1683 centre (1.536, 0.705)
- n = 11 (trump_cert) TL: #4 tilt 0.000 depth 0.1555 centre (0.500, 1.345); #6 tilt 40.182 depth 0.1683 centre (1.536, 0.705)
