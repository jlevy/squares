# Exact forms of the best-known packings, n ≤ 324

For each register record: `S*`, the side of the packing, is the unique root of an irreducible integer polynomial `p` in a rational interval, and an exact configuration over a number field `K = ℚ[t]/f` realises it (`minpoly/data/n-N.minpoly.json.gz`).  Derived from the contact graph (`minpoly.py`), checked independently by `verify_exact.py` (stdlib only: contacts as identities mod `f`, every other pair and wall by rational intervals).  Machine-readable: `exact_forms.json`.

* exact forms: **269** of 324 (independent replay VALID: 269); open: 29, 55, 68, 71, 83, 88, 103, 105, 108, 110, 123, 126, 130, 131, 132, 154, 155, 156, 172, 179, 180, 181, 182, 199, 206, 207, 208, 209, 210, 211, 228, 235, 236, 237, 238, 239, 240, 241, 259, 263, 268, 269, 270, 271, 272, 273, 292, 297, 301, 302, 303, 304, 305, 306, 307
* Lean `Packs n S*` (kernel-checked, standard axioms; `lean_batch.py`): 258
* Lean local minimum (`IsLocalMinPacking`): 178 (band lemma: integer-side records; grade A: n = 11, 28)

| n | S* | deg p | p | field deg | verify_exact | Lean Packs | Lean local min | cross-check |
|---|---|---|---|---|---|---|---|---|
| 1 | 1.0 | 1 | `x - 1` | 1 | ✓ | yes | band lemma |  |
| 2 | 2.0 | 1 | `x - 2` | 1 | ✓ | yes | band lemma |  |
| 3 | 2.0 | 1 | `x - 2` | 1 | ✓ | yes | band lemma |  |
| 4 | 2.0 | 1 | `x - 2` | 1 | ✓ | yes | band lemma |  |
| 5 | 2.707106781186547524 | 2 | `2x^2 - 8x + 7` | 2 | ✓ | yes |  | findpoly ok |
| 6 | 3.0 | 1 | `x - 3` | 1 | ✓ | yes | band lemma |  |
| 7 | 3.0 | 1 | `x - 3` | 1 | ✓ | yes | band lemma |  |
| 8 | 3.0 | 1 | `x - 3` | 1 | ✓ | yes | band lemma |  |
| 9 | 3.0 | 1 | `x - 3` | 1 | ✓ | yes | band lemma |  |
| 10 | 3.707106781186547524 | 2 | `2x^2 - 12x + 17` | 2 | ✓ | yes |  | findpoly ok |
| 11 | 3.877083590022814177 | 8 | `x^8 - 20x^7 + 178x^6 - 842x^5 + 1923x^4 - 496x^3 - 6754x^2 + 12420x - 6865` | 8 | ✓ | yes | grade A (N11L) | findpoly ok, Ellsworth deg ok |
| 12 | 4.0 | 1 | `x - 4` | 1 | ✓ | yes | band lemma |  |
| 13 | 4.0 | 1 | `x - 4` | 1 | ✓ | yes | band lemma |  |
| 14 | 4.0 | 1 | `x - 4` | 1 | ✓ | yes | band lemma |  |
| 15 | 4.0 | 1 | `x - 4` | 1 | ✓ | yes | band lemma |  |
| 16 | 4.0 | 1 | `x - 4` | 1 | ✓ | yes | band lemma |  |
| 17 | 4.675530093604550951 | 18 | `degree 18, 12-digit coefficients (JSON)` | 18 | ✓ | yes |  | Ellsworth deg ok |
| 18 | 4.822875655532295295 | 2 | `2x^2 - 14x + 21` | 2 | ✓ | yes |  | findpoly ok |
| 19 | 4.885618083164126731 | 2 | `9x^2 - 54x + 49` | 2 | ✓ | yes |  | findpoly ok |
| 20 | 5.0 | 1 | `x - 5` | 1 | ✓ | yes | band lemma |  |
| 21 | 5.0 | 1 | `x - 5` | 1 | ✓ | yes | band lemma |  |
| 22 | 5.0 | 1 | `x - 5` | 1 | ✓ | yes | band lemma |  |
| 23 | 5.0 | 1 | `x - 5` | 1 | ✓ | yes | band lemma |  |
| 24 | 5.0 | 1 | `x - 5` | 1 | ✓ | yes | band lemma |  |
| 25 | 5.0 | 1 | `x - 5` | 1 | ✓ | yes | band lemma |  |
| 26 | 5.621320343559642573 | 2 | `4x^2 - 28x + 31` | 2 | ✓ | yes |  | findpoly ok |
| 27 | 5.707106781186547524 | 2 | `2x^2 - 20x + 49` | 2 | ✓ | yes |  | findpoly ok |
| 28 | 5.824444616674059296 | 6 | `x^6 - 24x^5 + 212x^4 - 812x^3 + 1025x^2 + 882x - 1615` | 6 | ✓ | yes | grade A (N28L) | findpoly ok, Ellsworth deg ok |
| 29 | open | | | | | | | open (timeout):   15 consistency rows -> 5 distinct irreduci |
| 30 | 6.0 | 1 | `x - 6` | 1 | ✓ | yes | band lemma |  |
| 31 | 6.0 | 1 | `x - 6` | 1 | ✓ | yes | band lemma |  |
| 32 | 6.0 | 1 | `x - 6` | 1 | ✓ | yes | band lemma |  |
| 33 | 6.0 | 1 | `x - 6` | 1 | ✓ | yes | band lemma |  |
| 34 | 6.0 | 1 | `x - 6` | 1 | ✓ | yes | band lemma |  |
| 35 | 6.0 | 1 | `x - 6` | 1 | ✓ | yes | band lemma |  |
| 36 | 6.0 | 1 | `x - 6` | 1 | ✓ | yes | band lemma |  |
| 37 | 6.598619609244360116 | 8 | `36x^8 - 2496x^7 + 59768x^6 - 733760x^5 + 5289248x^4 - 23462672x^3 + 63458276x^2 - 96673872x + 64068561` | 8 | ✓ | yes |  | Ellsworth deg ok |
| 38 | 6.707106781186547524 | 2 | `2x^2 - 24x + 71` | 2 | ✓ | yes |  | findpoly ok |
| 39 | 6.810722083068648851 | 5 | `9x^5 - 171x^4 + 999x^3 - 1959x^2 + 1636x + 166` | 5 | ✓ | yes |  | findpoly ok, Ellsworth deg ok |
| 40 | 6.828427124746190097 | 2 | `x^2 - 8x + 8` | 2 | ✓ | yes |  | findpoly ok |
| 41 | 6.926693094468802231 | 42 | `degree 42, 35-digit coefficients (JSON)` | 42 | ✓ |  |  | Ellsworth deg ok |
| 42 | 7.0 | 1 | `x - 7` | 1 | ✓ | yes | band lemma |  |
| 43 | 7.0 | 1 | `x - 7` | 1 | ✓ | yes | band lemma |  |
| 44 | 7.0 | 1 | `x - 7` | 1 | ✓ | yes | band lemma |  |
| 45 | 7.0 | 1 | `x - 7` | 1 | ✓ | yes | band lemma |  |
| 46 | 7.0 | 1 | `x - 7` | 1 | ✓ | yes | band lemma |  |
| 47 | 7.0 | 1 | `x - 7` | 1 | ✓ | yes | band lemma |  |
| 48 | 7.0 | 1 | `x - 7` | 1 | ✓ | yes | band lemma |  |
| 49 | 7.0 | 1 | `x - 7` | 1 | ✓ | yes | band lemma |  |
| 50 | 7.571428571428571428 | 1 | `7x - 53` | 1 | ✓ | yes |  | findpoly ok |
| 51 | 7.700799235417011723 | 12 | `degree 12, 8-digit coefficients (JSON)` | 48 | ✓ |  |  | Ellsworth deg ok |
| 52 | 7.707106781186547524 | 2 | `2x^2 - 28x + 97` | 2 | ✓ | yes |  | findpoly ok |
| 53 | 7.822875655532295295 | 2 | `2x^2 - 26x + 81` | 4 | ✓ | yes |  | findpoly ok |
| 54 | 7.846667192843489782 | 4 | `4x^4 - 112x^3 + 1164x^2 - 5304x + 8897` | 4 | ✓ | yes |  | findpoly ok |
| 55 | open | | | | | | | open: RuntimeError: msolve failed:  |
| 56 | 8.0 | 1 | `x - 8` | 1 | ✓ | yes | band lemma |  |
| 57 | 8.0 | 1 | `x - 8` | 1 | ✓ | yes | band lemma |  |
| 58 | 8.0 | 1 | `x - 8` | 1 | ✓ | yes | band lemma |  |
| 59 | 8.0 | 1 | `x - 8` | 1 | ✓ | yes | band lemma |  |
| 60 | 8.0 | 1 | `x - 8` | 1 | ✓ | yes | band lemma |  |
| 61 | 8.0 | 1 | `x - 8` | 1 | ✓ | yes | band lemma |  |
| 62 | 8.0 | 1 | `x - 8` | 1 | ✓ | yes | band lemma |  |
| 63 | 8.0 | 1 | `x - 8` | 1 | ✓ | yes | band lemma |  |
| 64 | 8.0 | 1 | `x - 8` | 1 | ✓ | yes | band lemma |  |
| 65 | 8.535533905932737622 | 2 | `2x^2 - 20x + 25` | 2 | ✓ | yes |  | findpoly ok |
| 66 | 8.656854249492380195 | 2 | `x^2 - 6x - 23` | 2 | ✓ | yes |  |  |
| 67 | 8.707106781186547524 | 2 | `2x^2 - 32x + 127` | 2 | ✓ | yes |  | findpoly ok |
| 68 | open | | | | | | | open (timeout):   16 consistency rows -> 8 distinct irreduci |
| 69 | 8.827194655729738914 | 38 | `degree 38, 44-digit coefficients (JSON)` | 38 | ✓ |  |  | Ellsworth deg ok |
| 70 | 8.881666757009004624 | 4 | `23x^4 - 742x^3 + 8848x^2 - 45876x + 86229` | 4 | ✓ | yes |  | findpoly ok, Ellsworth deg ok |
| 71 | open | | | | | | | open (timeout):   14 consistency rows -> 5 distinct irreduci |
| 72 | 9.0 | 1 | `x - 9` | 1 | ✓ | yes | band lemma |  |
| 73 | 9.0 | 1 | `x - 9` | 1 | ✓ | yes | band lemma |  |
| 74 | 9.0 | 1 | `x - 9` | 1 | ✓ | yes | band lemma |  |
| 75 | 9.0 | 1 | `x - 9` | 1 | ✓ | yes | band lemma |  |
| 76 | 9.0 | 1 | `x - 9` | 1 | ✓ | yes | band lemma |  |
| 77 | 9.0 | 1 | `x - 9` | 1 | ✓ | yes | band lemma |  |
| 78 | 9.0 | 1 | `x - 9` | 1 | ✓ | yes | band lemma |  |
| 79 | 9.0 | 1 | `x - 9` | 1 | ✓ | yes | band lemma |  |
| 80 | 9.0 | 1 | `x - 9` | 1 | ✓ | yes | band lemma |  |
| 81 | 9.0 | 1 | `x - 9` | 1 | ✓ | yes | band lemma |  |
| 82 | 9.535533905932737622 | 2 | `2x^2 - 24x + 47` | 2 | ✓ | yes |  | findpoly ok |
| 83 | open | | | | | | | open: msolve: system not zero-dimensional (code 1) |
| 84 | 9.707106781186547524 | 2 | `2x^2 - 36x + 161` | 2 | ✓ | yes |  | findpoly ok |
| 85 | 9.742640687119285146 | 2 | `4x^2 - 44x + 49` | 2 | ✓ | yes |  | findpoly ok |
| 86 | 9.822875655532295295 | 2 | `2x^2 - 34x + 141` | 2 | ✓ | yes |  | findpoly ok |
| 87 | 9.838815269948262260 | 41 | `degree 41, 54-digit coefficients (JSON)` | 41 | ✓ |  |  | Ellsworth deg ok |
| 88 | open | | | | | | | open: 1 consistency polynomials for 3 class angles: more tha |
| 89 | 9.949747468305832670 | 2 | `2x^2 - 20x + 1` | 2 | ✓ | yes |  | findpoly ok |
| 90 | 10.0 | 1 | `x - 10` | 1 | ✓ | yes | band lemma |  |
| 91 | 10.0 | 1 | `x - 10` | 1 | ✓ | yes | band lemma |  |
| 92 | 10.0 | 1 | `x - 10` | 1 | ✓ | yes | band lemma |  |
| 93 | 10.0 | 1 | `x - 10` | 1 | ✓ | yes | band lemma |  |
| 94 | 10.0 | 1 | `x - 10` | 1 | ✓ | yes | band lemma |  |
| 95 | 10.0 | 1 | `x - 10` | 1 | ✓ | yes | band lemma |  |
| 96 | 10.0 | 1 | `x - 10` | 1 | ✓ | yes | band lemma |  |
| 97 | 10.0 | 1 | `x - 10` | 1 | ✓ | yes | band lemma |  |
| 98 | 10.0 | 1 | `x - 10` | 1 | ✓ | yes | band lemma |  |
| 99 | 10.0 | 1 | `x - 10` | 1 | ✓ | yes | band lemma |  |
| 100 | 10.0 | 1 | `x - 10` | 1 | ✓ | yes | band lemma |  |
| 101 | 10.53553390593273762 | 2 | `2x^2 - 28x + 73` | 2 | ✓ | yes |  | findpoly ok |
| 102 | 10.60717468017605112 | 8 | `degree 8, 13-digit coefficients (JSON)` | 8 | ✓ | yes |  | **new** (no published form) |
| 103 | open | | | | | | | open (memory cap): n = 103: 97 squares in the system, 6 free |
| 104 | 10.70710678118654752 | 2 | `2x^2 - 40x + 199` | 2 | ✓ | yes |  | findpoly ok |
| 105 | open | | | | | | | open (memory cap): n = 105: 97 squares in the system, 8 free |
| 106 | 10.82290804413284755 | 32 | `degree 32, 35-digit coefficients (JSON)` | 32 | ✓ |  |  | **new** (no published form) |
| 107 | 10.84666719284348978 | 4 | `4x^4 - 160x^3 + 2388x^2 - 15744x + 38633` | 4 | ✓ | yes |  | findpoly ok |
| 108 | open | | | | | | | open (timeout):   field: degree 144 (factor of the eliminati |
| 109 | 10.94974746830583267 | 2 | `2x^2 - 24x + 23` | 2 | ✓ | yes |  | findpoly ok |
| 110 | open | | | | | | | open (memory cap): n = 110: 108 squares in the system, 2 fre |
| 111 | 11.0 | 1 | `x - 11` | 1 | ✓ | yes | band lemma |  |
| 112 | 11.0 | 1 | `x - 11` | 1 | ✓ | yes | band lemma |  |
| 113 | 11.0 | 1 | `x - 11` | 1 | ✓ | yes | band lemma |  |
| 114 | 11.0 | 1 | `x - 11` | 1 | ✓ | yes | band lemma |  |
| 115 | 11.0 | 1 | `x - 11` | 1 | ✓ | yes | band lemma |  |
| 116 | 11.0 | 1 | `x - 11` | 1 | ✓ | yes | band lemma |  |
| 117 | 11.0 | 1 | `x - 11` | 1 | ✓ | yes | band lemma |  |
| 118 | 11.0 | 1 | `x - 11` | 1 | ✓ | yes | band lemma |  |
| 119 | 11.0 | 1 | `x - 11` | 1 | ✓ | yes | band lemma |  |
| 120 | 11.0 | 1 | `x - 11` | 1 | ✓ | yes | band lemma |  |
| 121 | 11.0 | 1 | `x - 11` | 1 | ✓ | yes | band lemma |  |
| 122 | 11.53553390593273762 | 2 | `2x^2 - 32x + 103` | 2 | ✓ | yes |  | findpoly ok |
| 123 | open | | | | | | | open: 3 consistency polynomials for 5 class angles: more tha |
| 124 | 11.65685424949238019 | 2 | `x^2 - 12x + 4` | 2 | ✓ | yes |  | findpoly ok |
| 125 | 11.70710678118654752 | 2 | `2x^2 - 44x + 241` | 2 | ✓ | yes |  | findpoly ok |
| 126 | open | | | | | | | open (timeout):   18 consistency rows -> 6 distinct irreduci |
| 127 | 11.82287565553229529 | 2 | `2x^2 - 42x + 217` | 2 | ✓ | yes |  |  |
| 128 | 11.82509196821368702 | 40 | `degree 40, 48-digit coefficients (JSON)` | 40 | ✓ |  |  | Ellsworth deg ok |
| 129 | 11.88130621809000306 | 20 | `degree 20, 23-digit coefficients (JSON)` | 20 | ✓ | yes |  | Ellsworth deg ok |
| 130 | open | | | | | | | open: 2 consistency polynomials for 5 class angles: more tha |
| 131 | open | | | | | | | open (timeout): n = 131: 131 squares in the system, 0 free;  |
| 132 | open | | | | | | | open (memory cap): n = 132: 131 squares in the system, 1 fre |
| 133 | 12.0 | 1 | `x - 12` | 1 | ✓ | yes | band lemma |  |
| 134 | 12.0 | 1 | `x - 12` | 1 | ✓ | yes | band lemma |  |
| 135 | 12.0 | 1 | `x - 12` | 1 | ✓ | yes | band lemma |  |
| 136 | 12.0 | 1 | `x - 12` | 1 | ✓ | yes | band lemma |  |
| 137 | 12.0 | 1 | `x - 12` | 1 | ✓ | yes | band lemma |  |
| 138 | 12.0 | 1 | `x - 12` | 1 | ✓ | yes | band lemma |  |
| 139 | 12.0 | 1 | `x - 12` | 1 | ✓ | yes | band lemma |  |
| 140 | 12.0 | 1 | `x - 12` | 1 | ✓ | yes | band lemma |  |
| 141 | 12.0 | 1 | `x - 12` | 1 | ✓ | yes | band lemma |  |
| 142 | 12.0 | 1 | `x - 12` | 1 | ✓ | yes | band lemma |  |
| 143 | 12.0 | 1 | `x - 12` | 1 | ✓ | yes | band lemma |  |
| 144 | 12.0 | 1 | `x - 12` | 1 | ✓ | yes | band lemma |  |
| 145 | 12.53553390593273762 | 2 | `2x^2 - 36x + 137` | 2 | ✓ | yes |  | findpoly ok |
| 146 | 12.60090777851301824 | 16 | `degree 16, 18-digit coefficients (JSON)` | 16 | ✓ | yes |  | Ellsworth deg ok |
| 147 | 12.65685424949238019 | 2 | `x^2 - 14x + 17` | 2 | ✓ | yes |  | findpoly ok |
| 148 | 12.65685424949238019 | 2 | `x^2 - 14x + 17` | 2 | ✓ | yes |  | findpoly ok |
| 149 | 12.70710678118654752 | 2 | `2x^2 - 48x + 287` | 2 | ✓ | yes |  | findpoly ok |
| 150 | 12.77817459305202276 | 2 | `2x^2 - 20x - 71` | 2 | ✓ | yes |  | findpoly ok |
| 151 | 12.82287565553229529 | 2 | `2x^2 - 46x + 261` | 2 | ✓ | yes |  | findpoly ok |
| 152 | 12.83071880097660995 | 40 | `degree 40, 52-digit coefficients (JSON)` | 40 | ✓ |  |  | **new** (no published form) |
| 153 | 12.88166675700900462 | 4 | `23x^4 - 1110x^3 + 19960x^2 - 158164x + 464677` | 4 | ✓ | yes |  | findpoly ok, Ellsworth deg ok |
| 154 | open | | | | | | | open (timeout): n = 154: 154 squares in the system, 0 free;  |
| 155 | open | | | | | | | open (memory cap): n = 155: 152 squares in the system, 3 fre |
| 156 | open | | | | | | | open (timeout): n = 156: 155 squares in the system, 1 free;  |
| 157 | 13.0 | 1 | `x - 13` | 1 | ✓ | yes | band lemma |  |
| 158 | 13.0 | 1 | `x - 13` | 1 | ✓ | yes | band lemma |  |
| 159 | 13.0 | 1 | `x - 13` | 1 | ✓ | yes | band lemma |  |
| 160 | 13.0 | 1 | `x - 13` | 1 | ✓ | yes | band lemma |  |
| 161 | 13.0 | 1 | `x - 13` | 1 | ✓ | yes | band lemma |  |
| 162 | 13.0 | 1 | `x - 13` | 1 | ✓ | yes | band lemma |  |
| 163 | 13.0 | 1 | `x - 13` | 1 | ✓ | yes | band lemma |  |
| 164 | 13.0 | 1 | `x - 13` | 1 | ✓ | yes | band lemma |  |
| 165 | 13.0 | 1 | `x - 13` | 1 | ✓ | yes | band lemma |  |
| 166 | 13.0 | 1 | `x - 13` | 1 | ✓ | yes | band lemma |  |
| 167 | 13.0 | 1 | `x - 13` | 1 | ✓ | yes | band lemma |  |
| 168 | 13.0 | 1 | `x - 13` | 1 | ✓ | yes | band lemma |  |
| 169 | 13.0 | 1 | `x - 13` | 1 | ✓ | yes | band lemma |  |
| 170 | 13.53553390593273762 | 2 | `2x^2 - 40x + 175` | 2 | ✓ | yes |  | findpoly ok |
| 171 | 13.57142857142857142 | 1 | `7x - 95` | 1 | ✓ | yes |  | findpoly ok |
| 172 | open | | | | | | | open: 1 consistency polynomials for 3 class angles: more tha |
| 173 | 13.65685424949238019 | 2 | `x^2 - 16x + 32` | 2 | ✓ | yes |  | findpoly ok |
| 174 | 13.70710678118654752 | 2 | `2x^2 - 52x + 337` | 2 | ✓ | yes |  | findpoly ok |
| 175 | 13.77817459305202276 | 2 | `2x^2 - 24x - 49` | 2 | ✓ | yes |  | findpoly ok |
| 176 | 13.82287565553229529 | 2 | `2x^2 - 50x + 309` | 2 | ✓ | yes |  | findpoly ok |
| 177 | 13.82297973416944860 | 32 | `degree 32, 40-digit coefficients (JSON)` | 32 | ✓ |  |  | **new** (no published form) |
| 178 | 13.84666719284348978 | 4 | `4x^4 - 208x^3 + 4044x^2 - 34824x + 112001` | 4 | ✓ | yes |  | findpoly ok |
| 179 | open | | | | | | | open: 1 consistency polynomials for 5 class angles: more tha |
| 180 | open | | | | | | | open (timeout): n = 180: 180 squares in the system, 0 free;  |
| 181 | open | | | | | | | open (memory cap): n = 181: 180 squares in the system, 1 fre |
| 182 | open | | | | | | | open (memory cap):   elimination: 337 pivots, 23 consistency |
| 183 | 14.0 | 1 | `x - 14` | 1 | ✓ | yes | band lemma |  |
| 184 | 14.0 | 1 | `x - 14` | 1 | ✓ | yes | band lemma |  |
| 185 | 14.0 | 1 | `x - 14` | 1 | ✓ | yes | band lemma |  |
| 186 | 14.0 | 1 | `x - 14` | 1 | ✓ | yes | band lemma |  |
| 187 | 14.0 | 1 | `x - 14` | 1 | ✓ | yes | band lemma |  |
| 188 | 14.0 | 1 | `x - 14` | 1 | ✓ | yes | band lemma |  |
| 189 | 14.0 | 1 | `x - 14` | 1 | ✓ | yes | band lemma |  |
| 190 | 14.0 | 1 | `x - 14` | 1 | ✓ | yes | band lemma |  |
| 191 | 14.0 | 1 | `x - 14` | 1 | ✓ | yes | band lemma |  |
| 192 | 14.0 | 1 | `x - 14` | 1 | ✓ | yes | band lemma |  |
| 193 | 14.0 | 1 | `x - 14` | 1 | ✓ | yes | band lemma |  |
| 194 | 14.0 | 1 | `x - 14` | 1 | ✓ | yes | band lemma |  |
| 195 | 14.0 | 1 | `x - 14` | 1 | ✓ | yes | band lemma |  |
| 196 | 14.0 | 1 | `x - 14` | 1 | ✓ | yes | band lemma |  |
| 197 | 14.53553390593273762 | 2 | `2x^2 - 44x + 217` | 2 | ✓ | yes |  | findpoly ok |
| 198 | 14.57142857142857142 | 1 | `7x - 102` | 1 | ✓ | yes |  | findpoly ok |
| 199 | open | | | | | | | open: 1 consistency polynomials for 3 class angles: more tha |
| 200 | 14.65685424949238019 | 2 | `x^2 - 18x + 49` | 2 | ✓ | yes |  | findpoly ok |
| 201 | 14.70710678118654752 | 2 | `2x^2 - 56x + 391` | 2 | ✓ | yes |  | findpoly ok |
| 202 | 14.72792206135785543 | 2 | `x^2 - 4x - 158` | 2 | ✓ | yes |  | findpoly ok |
| 203 | 14.77817459305202276 | 2 | `2x^2 - 28x - 23` | 2 | ✓ | yes |  | findpoly ok |
| 204 | 14.82287565553229529 | 2 | `2x^2 - 54x + 361` | 2 | ✓ | yes |  | findpoly ok |
| 205 | 14.82445114612408822 | 40 | `degree 40, 52-digit coefficients (JSON)` | 40 | ✓ |  |  | Ellsworth deg ok |
| 206 | open | | | | | | | open (timeout):   field: degree 56 (factor of the eliminatin |
| 207 | open | | | | | | | open: Lagrange determinant vanishes identically |
| 208 | open | | | | | | | open (timeout): n = 208: 206 squares in the system, 2 free;  |
| 209 | open | | | | | | | open (memory cap): n = 209: 206 squares in the system, 3 fre |
| 210 | open | | | | | | | open (memory cap): n = 210: 208 squares in the system, 2 fre |
| 211 | open | | | | | | | open (memory cap): n = 211: 211 squares in the system, 0 fre |
| 212 | 15.0 | 1 | `x - 15` | 1 | ✓ | yes | band lemma |  |
| 213 | 15.0 | 1 | `x - 15` | 1 | ✓ | yes | band lemma |  |
| 214 | 15.0 | 1 | `x - 15` | 1 | ✓ | yes | band lemma |  |
| 215 | 15.0 | 1 | `x - 15` | 1 | ✓ | yes | band lemma |  |
| 216 | 15.0 | 1 | `x - 15` | 1 | ✓ | yes | band lemma |  |
| 217 | 15.0 | 1 | `x - 15` | 1 | ✓ | yes | band lemma |  |
| 218 | 15.0 | 1 | `x - 15` | 1 | ✓ | yes | band lemma |  |
| 219 | 15.0 | 1 | `x - 15` | 1 | ✓ | yes | band lemma |  |
| 220 | 15.0 | 1 | `x - 15` | 1 | ✓ | yes | band lemma |  |
| 221 | 15.0 | 1 | `x - 15` | 1 | ✓ | yes | band lemma |  |
| 222 | 15.0 | 1 | `x - 15` | 1 | ✓ | yes | band lemma |  |
| 223 | 15.0 | 1 | `x - 15` | 1 | ✓ | yes | band lemma |  |
| 224 | 15.0 | 1 | `x - 15` | 1 | ✓ | yes | band lemma |  |
| 225 | 15.0 | 1 | `x - 15` | 1 | ✓ | yes | band lemma |  |
| 226 | 15.53553390593273762 | 2 | `2x^2 - 48x + 263` | 2 | ✓ | yes |  | findpoly ok |
| 227 | 15.57106781186547524 | 2 | `4x^2 - 68x + 89` | 2 | ✓ | yes |  | findpoly ok |
| 228 | open | | | | | | | open (timeout):   27 consistency rows -> 12 distinct irreduc |
| 229 | 15.65685424949238019 | 2 | `x^2 - 20x + 68` | 2 | ✓ | yes |  | findpoly ok |
| 230 | 15.68292682926829268 | 1 | `41x - 643` | 1 | ✓ | yes |  | findpoly ok |
| 231 | 15.70710678118654752 | 2 | `2x^2 - 60x + 449` | 2 | ✓ | yes |  | findpoly ok |
| 232 | 15.77817459305202276 | 2 | `2x^2 - 32x + 7` | 2 | ✓ | yes |  | findpoly ok |
| 233 | 15.77817459305202276 | 2 | `2x^2 - 32x + 7` | 2 | ✓ | yes |  | findpoly ok |
| 234 | 15.82287565553229529 | 2 | `2x^2 - 58x + 417` | 2 | ✓ | yes |  | findpoly ok |
| 235 | open | | | | | | | open: msolve: system not zero-dimensional (code 1) |
| 236 | open | | | | | | | open: 1 consistency polynomials for 3 class angles: more tha |
| 237 | open | | | | | | | open: 1 consistency polynomials for 5 class angles: more tha |
| 238 | open | | | | | | | open (memory cap): n = 238: 237 squares in the system, 1 fre |
| 239 | open | | | | | | | open (memory cap): n = 239: 236 squares in the system, 3 fre |
| 240 | open | | | | | | | open (memory cap): n = 240: 237 squares in the system, 3 fre |
| 241 | open | | | | | | | open (memory cap): n = 241: 238 squares in the system, 3 fre |
| 242 | 16.0 | 1 | `x - 16` | 1 | ✓ | yes | band lemma |  |
| 243 | 16.0 | 1 | `x - 16` | 1 | ✓ | yes | band lemma |  |
| 244 | 16.0 | 1 | `x - 16` | 1 | ✓ | yes | band lemma |  |
| 245 | 16.0 | 1 | `x - 16` | 1 | ✓ | yes | band lemma |  |
| 246 | 16.0 | 1 | `x - 16` | 1 | ✓ | yes | band lemma |  |
| 247 | 16.0 | 1 | `x - 16` | 1 | ✓ | yes | band lemma |  |
| 248 | 16.0 | 1 | `x - 16` | 1 | ✓ | yes | band lemma |  |
| 249 | 16.0 | 1 | `x - 16` | 1 | ✓ | yes | band lemma |  |
| 250 | 16.0 | 1 | `x - 16` | 1 | ✓ | yes | band lemma |  |
| 251 | 16.0 | 1 | `x - 16` | 1 | ✓ | yes | band lemma |  |
| 252 | 16.0 | 1 | `x - 16` | 1 | ✓ | yes | band lemma |  |
| 253 | 16.0 | 1 | `x - 16` | 1 | ✓ | yes | band lemma |  |
| 254 | 16.0 | 1 | `x - 16` | 1 | ✓ | yes | band lemma |  |
| 255 | 16.0 | 1 | `x - 16` | 1 | ✓ | yes | band lemma |  |
| 256 | 16.0 | 1 | `x - 16` | 1 | ✓ | yes | band lemma |  |
| 257 | 16.53553390593273762 | 2 | `2x^2 - 52x + 313` | 2 | ✓ | yes |  | findpoly ok |
| 258 | 16.57106781186547524 | 2 | `4x^2 - 76x + 161` | 2 | ✓ | yes |  | findpoly ok |
| 259 | open | | | | | | | open: 1 consistency polynomials for 4 class angles: more tha |
| 260 | 16.65685424949238019 | 2 | `x^2 - 22x + 89` | 2 | ✓ | yes |  | findpoly ok |
| 261 | 16.68292682926829268 | 1 | `41x - 684` | 1 | ✓ | yes |  | findpoly ok |
| 262 | 16.70710678118654752 | 2 | `2x^2 - 64x + 511` | 2 | ✓ | yes |  | findpoly ok |
| 263 | open | | | | | | | open (timeout): n = 263: 263 squares in the system, 0 free;  |
| 264 | 16.77817459305202276 | 2 | `2x^2 - 36x + 41` | 2 | ✓ | yes |  | findpoly ok |
| 265 | 16.77817459305202276 | 2 | `2x^2 - 36x + 41` | 2 | ✓ | yes |  | findpoly ok |
| 266 | 16.82306208283780464 | 32 | `degree 32, 44-digit coefficients (JSON)` | 32 | ✓ |  |  | Ellsworth deg ok |
| 267 | 16.84666719284348978 | 4 | `4x^4 - 256x^3 + 6132x^2 - 65136x + 258809` | 4 | ✓ | yes |  | findpoly ok |
| 268 | open | | | | | | | open: Lagrange determinant vanishes identically |
| 269 | open | | | | | | | open: 1 consistency polynomials for 4 class angles: more tha |
| 270 | open | | | | | | | open (memory cap): n = 270: 270 squares in the system, 0 fre |
| 271 | open | | | | | | | open (timeout):   square 184: flat rotation, kept parallel t |
| 272 | open | | | | | | | open (memory cap): n = 272: 265 squares in the system, 7 fre |
| 273 | open | | | | | | | open (memory cap): n = 273: 264 squares in the system, 9 fre |
| 274 | 17.0 | 1 | `x - 17` | 1 | ✓ | yes | band lemma |  |
| 275 | 17.0 | 1 | `x - 17` | 1 | ✓ | yes | band lemma |  |
| 276 | 17.0 | 1 | `x - 17` | 1 | ✓ | yes | band lemma |  |
| 277 | 17.0 | 1 | `x - 17` | 1 | ✓ | yes | band lemma |  |
| 278 | 17.0 | 1 | `x - 17` | 1 | ✓ | yes | band lemma |  |
| 279 | 17.0 | 1 | `x - 17` | 1 | ✓ | yes | band lemma |  |
| 280 | 17.0 | 1 | `x - 17` | 1 | ✓ | yes | band lemma |  |
| 281 | 17.0 | 1 | `x - 17` | 1 | ✓ | yes | band lemma |  |
| 282 | 17.0 | 1 | `x - 17` | 1 | ✓ | yes | band lemma |  |
| 283 | 17.0 | 1 | `x - 17` | 1 | ✓ | yes | band lemma |  |
| 284 | 17.0 | 1 | `x - 17` | 1 | ✓ | yes | band lemma |  |
| 285 | 17.0 | 1 | `x - 17` | 1 | ✓ | yes | band lemma |  |
| 286 | 17.0 | 1 | `x - 17` | 1 | ✓ | yes | band lemma |  |
| 287 | 17.0 | 1 | `x - 17` | 1 | ✓ | yes | band lemma |  |
| 288 | 17.0 | 1 | `x - 17` | 1 | ✓ | yes | band lemma |  |
| 289 | 17.0 | 1 | `x - 17` | 1 | ✓ | yes | band lemma |  |
| 290 | 17.53553390593273762 | 2 | `2x^2 - 56x + 367` | 2 | ✓ | yes |  | findpoly ok |
| 291 | 17.53553390593273762 | 2 | `2x^2 - 56x + 367` | 2 | ✓ | yes |  | findpoly ok |
| 292 | open | | | | | | | not run |
| 293 | 17.63414634146341463 | 1 | `41x - 723` | 1 | ✓ | yes |  | findpoly ok |
| 294 | 17.65685424949238019 | 2 | `x^2 - 24x + 112` | 2 | ✓ | yes |  | findpoly ok |
| 295 | 17.70710678118654752 | 2 | `2x^2 - 68x + 577` | 2 | ✓ | yes |  | findpoly ok |
| 296 | 17.70710678118654752 | 2 | `2x^2 - 68x + 577` | 2 | ✓ | yes |  | findpoly ok |
| 297 | open | | | | | | | open: 1 consistency polynomials for 3 class angles: more tha |
| 298 | 17.77817459305202276 | 2 | `2x^2 - 40x + 79` | 2 | ✓ | yes |  | findpoly ok |
| 299 | 17.82287565553229529 | 2 | `2x^2 - 66x + 541` | 2 | ✓ | yes |  |  |
| 300 | 17.82412338847854347 | 40 | `degree 40, 56-digit coefficients (JSON)` | 40 | ✓ |  |  | Ellsworth deg ok |
| 301 | open | | | | | | | open (memory cap):   settled 1 flat directions on near-conta |
| 302 | open | | | | | | | open (timeout): n = 302: 281 squares in the system, 21 free; |
| 303 | open | | | | | | | open (memory cap):   square 265: flat rotation, kept paralle |
| 304 | open | | | | | | | open (memory cap): n = 304: 301 squares in the system, 3 fre |
| 305 | open | | | | | | | open (timeout):   square 205: flat rotation, kept parallel t |
| 306 | open | | | | | | | open (memory cap): n = 306: 304 squares in the system, 2 fre |
| 307 | open | | | | | | | open (timeout): n = 307: 302 squares in the system, 5 free;  |
| 308 | 18.0 | 1 | `x - 18` | 1 | ✓ | yes | band lemma |  |
| 309 | 18.0 | 1 | `x - 18` | 1 | ✓ | yes | band lemma |  |
| 310 | 18.0 | 1 | `x - 18` | 1 | ✓ | yes | band lemma |  |
| 311 | 18.0 | 1 | `x - 18` | 1 | ✓ | yes | band lemma |  |
| 312 | 18.0 | 1 | `x - 18` | 1 | ✓ | yes | band lemma |  |
| 313 | 18.0 | 1 | `x - 18` | 1 | ✓ | yes | band lemma |  |
| 314 | 18.0 | 1 | `x - 18` | 1 | ✓ | yes | band lemma |  |
| 315 | 18.0 | 1 | `x - 18` | 1 | ✓ | yes | band lemma |  |
| 316 | 18.0 | 1 | `x - 18` | 1 | ✓ | yes | band lemma |  |
| 317 | 18.0 | 1 | `x - 18` | 1 | ✓ | yes | band lemma |  |
| 318 | 18.0 | 1 | `x - 18` | 1 | ✓ | yes | band lemma |  |
| 319 | 18.0 | 1 | `x - 18` | 1 | ✓ | yes | band lemma |  |
| 320 | 18.0 | 1 | `x - 18` | 1 | ✓ | yes | band lemma |  |
| 321 | 18.0 | 1 | `x - 18` | 1 | ✓ | yes | band lemma |  |
| 322 | 18.0 | 1 | `x - 18` | 1 | ✓ | yes | band lemma |  |
| 323 | 18.0 | 1 | `x - 18` | 1 | ✓ | yes | band lemma |  |
| 324 | 18.0 | 1 | `x - 18` | 1 | ✓ | yes | band lemma |  |
