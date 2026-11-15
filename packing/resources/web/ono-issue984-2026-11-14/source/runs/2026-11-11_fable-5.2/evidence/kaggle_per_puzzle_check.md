# Kaggle per-puzzle leaderboard against the two catalogues (check made after the run)

- Source: `https://www.kaggle.com/code/inversion/squares-in-squares-per-puzzle-leaderboard`, a notebook kept by Kaggle staff and announced in the competition's pinned
  discussion "Per-Puzzle Leaderboard" (`https://www.kaggle.com/competitions/squares-in-squares/discussion/751633`). The post says it refreshes about once a day, with a lag.
- Copy used: notebook version 28; newest submission in the table 2026-11-08 04:29:46 UTC; retrieved 2026-11-11 22:06 UTC.
  The sides in it can only have gone down since.
- Columns: n, "Best Side Length L (50 decimals)", TeamName, DateSubmitted. Rows whose team is "-" are the
  organisers' baseline; the others are the smallest side the competition's grader has accepted from a team.
- It is **side only**: no packing is published.
- "Catalogues" below means the smaller of the Kingbird page and the Squares Project, which is what
  `records.json` held during the run.

## The two withdrawn claims

| n | certificate (this run) | certified side | Kaggle side, as published | team | submitted | certificate − Kaggle |
|---|---|---|---|---|---|---|
| 147 | `certificates/n147_S65104355.json` | 12.651043556587694… | 12.65104355317263277225840032221855070493196640140714 | Nevska | 2026-11-07 06:15:05 UTC | +3.4151e-09 |
| 228 | `certificates/n228_S59604312.json` | 15.596043120920791… | 15.59604311664627229390668802682613932021971821107903 | square1000 | 2026-10-29 14:18:39 UTC | +4.2745e-09 |
| 228 | `certificates/n228_S59708491.json` | 15.597084911486421… | 15.59604311664627229390668802682613932021971821107903 | square1000 | 2026-10-29 14:18:39 UTC | +1.0418e-03 |

The frozen verifier, run against the corrected `records.json`, prints `does not beat record` for all three.

## Every n ≤ 324 where a team's side is below both catalogues by more than 1e-12 (33 values of n)

| n | catalogues | Kaggle side (20 decimals; all 50 are in `records.json`) | team | submitted | Kaggle − catalogues |
|---|---|---|---|---|---|
| 109 | 10.94974746830583 | 10.94928958094335364214 | Nevska | 2026-11-07 22:37:45 UTC | -4.579e-04 |
| 132 | 11.9856801988458088115 | 11.98368406327818967266 | Jonathan Roy | 2026-11-07 16:07:25 UTC | -1.996e-03 |
| 147 | 12.65685424949238 | 12.65104355317263277225 | Nevska | 2026-11-07 06:15:05 UTC | -5.811e-03 |
| 172 | 13.6146898532862152 | 13.61468985328358057514 | Nevska | 2026-11-07 06:15:05 UTC | -2.635e-12 |
| 179 | 13.88379549051089845 | 13.88096037155557959469 | Nevska | 2026-11-07 06:15:05 UTC | -2.835e-03 |
| 199 | 14.6146898532862152 | 14.61320987563422946923 | OigaZhDn | 2026-10-31 15:51:55 UTC | -1.480e-03 |
| 202 | 14.72792206135785 | 14.72437270916633685494 | Cats and boxes 😼 | 2026-10-28 19:24:06 UTC | -3.549e-03 |
| 204 | 14.8043613836518588 | 14.80348918307308635060 | Monkey Supremacy | 2026-11-06 16:29:25 UTC | -8.722e-04 |
| 206 | 14.8601586633919032367 | 14.86013342702638543486 | Cats and boxes 😼 | 2026-10-26 10:17:41 UTC | -2.524e-05 |
| 210 | 14.9730011165876257419 | 14.97121063254497633486 | Cats and boxes 😼 | 2026-10-30 10:00:17 UTC | -1.790e-03 |
| 228 | 15.60460147572967429 | 15.59604311664627229390 | square1000 | 2026-10-29 14:18:39 UTC | -8.558e-03 |
| 232 | 15.7614096448817244 | 15.75885277528378877306 | Salut Monde | 2026-10-29 15:47:50 UTC | -2.557e-03 |
| 237 | 15.9026036382595969 | 15.89380558520937975554 | elegans | 2026-11-05 06:23:25 UTC | -8.798e-03 |
| 259 | 16.59137814549769816 | 16.59001643926448867898 | Cats and boxes 😼 | 2026-10-27 00:05:22 UTC | -1.362e-03 |
| 260 | 16.6335209508885336 | 16.63352095028338820883 | Vikram Tiwari | 2026-11-08 03:35:31 UTC | -6.051e-10 |
| 262 | 16.70710678118654 | 16.69811501869939442808 | Nevska | 2026-11-07 15:45:23 UTC | -8.992e-03 |
| 263 | 16.73316600789937898 | 16.72437270914329560243 | Cats and boxes 😼 | 2026-10-28 17:01:01 UTC | -8.793e-03 |
| 264 | 16.77473513238783285 | 16.77028852775006617662 | Cats and boxes 😼 | 2026-10-28 00:02:27 UTC | -4.447e-03 |
| 268 | 16.8720298490844502 | 16.87186813513754166923 | Cats and boxes 😼 | 2026-10-28 21:42:08 UTC | -1.617e-04 |
| 269 | 16.9009945799513249 | 16.88973007912474431175 | elegans | 2026-11-05 06:23:25 UTC | -1.126e-02 |
| 270 | 16.9281486033428544 | 16.92731421641869724033 | Cats and boxes 😼 | 2026-10-27 09:33:46 UTC | -8.344e-04 |
| 271 | 16.9489477337136576 | 16.94894002837464350396 | OigaZhDn | 2026-11-06 05:54:59 UTC | -7.705e-06 |
| 272 | 16.96558647483767064 | 16.96550117586544663178 | Cats and boxes 😼 | 2026-10-27 21:40:44 UTC | -8.530e-05 |
| 292 | 17.5913781454976982 | 17.58905394336789103313 | Cats and boxes 😼 | 2026-10-29 00:03:47 UTC | -2.324e-03 |
| 295 | 17.70423279073603036 | 17.69804292939389124879 | Cats and boxes 😼 | 2026-10-26 13:07:28 UTC | -6.190e-03 |
| 297 | 17.740417287543801851 | 17.73945551204330829779 | Cats and boxes 😼 | 2026-11-01 09:10:43 UTC | -9.618e-04 |
| 298 | 17.77817459305202 | 17.77688038937578319122 | Cats and boxes 😼 | 2026-10-28 02:29:33 UTC | -1.294e-03 |
| 299 | 17.8010044342552937 | 17.79363699181476005595 | Cats and boxes 😼 | 2026-10-27 21:40:44 UTC | -7.367e-03 |
| 303 | 17.9017892731564904 | 17.89592615827704284452 | Cats and boxes 😼 | 2026-11-01 09:10:43 UTC | -5.863e-03 |
| 304 | 17.9209440933402421 | 17.91800547284288772664 | square1000 | 2026-10-27 02:47:43 UTC | -2.939e-03 |
| 305 | 17.95046648213771228 | 17.94575583877918833198 | Cats and boxes 😼 | 2026-10-27 02:12:41 UTC | -4.711e-03 |
| 307 | 17.9792309603873628 | 17.97923096038388326682 | Nevska | 2026-11-07 15:45:23 UTC | -3.480e-12 |
| 308 | 17.9971491212709088 | 17.99714441820797244617 | Cats and boxes 😼 | 2026-10-30 21:54:30 UTC | -4.703e-06 |

## Same record, more digits (48 values of n)

A team's side is below the catalogue value by less than 1e-12 (largest difference 2.5e-13): the same packing, printed with more digits. `records.json` takes the
Kaggle digits here too, because the smaller published value is the safer bar.

n = 51, 70, 84, 86, 88, 102, 103, 105, 106, 108, 110, 123, 126, 127, 129, 130, 131, 146, 152, 153, 154, 155, 175, 176, 177, 181, 182, 183, 207, 208, 209, 211, 227, 229, 236, 238, 239, 240, 241, 258, 261, 266, 267, 273, 293, 301, 302, 306

## A team's side above the catalogues (3 values of n)

The catalogue value is newer than this copy of the Kaggle table, or more tightly rounded: n = 68 (+7.4e-52); n = 156 (+2.5e-11); n = 180 (+1.4e-03).

## How to fetch it again

Open the notebook; the table is in its rendered output, embedded as a JSON array (`DATA`) of
`{n, L, team, date}`. `search/add_kaggle_source.py` reads it as four tab-separated columns from
`work/web/kaggle_perpuzzle/per_puzzle_v28.tsv`.
