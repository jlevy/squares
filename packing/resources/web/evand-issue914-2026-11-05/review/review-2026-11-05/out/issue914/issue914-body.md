
**Credit name.** Evan Daniel (GitHub @evand).

**Claims.** Seven new upper bounds.  Each is the certificate's exact rational side, rounded up at 12 places.  Global optimality is not claimed.

| n | new upper bound | best public bound before it | improvement | that bound's source |
|---:|---:|---:|---:|---|
| 175 | 13.764050051544 | 13.764174317487 | 1.24·10⁻⁴ | register (Mishapolk) |
| 204 | 14.804361383652 | 14.807620995586 | 3.26·10⁻³ | register (Doğa Özden, #894) |
| 260 | 16.633520950889 | 16.633982501923 | 4.62·10⁻⁴ | register (#895, vitamoon) |
| 268 | 16.872499518136 | 16.874361715870 | 1.86·10⁻³ | register (Vladislav Lavrentev) |
| 293 | 17.623065212061 | 17.633982502123 | 1.09·10⁻² | register (ours, #845) |
| 303 | 17.901832750855 | 17.906978233799 | 5.15·10⁻³ | register (#763, Francisco Couzo) |
| 304 | 17.920944093341 | 17.926898900357 | 5.95·10⁻³ | register (Kirill Tymchishin) |

Comparison = the lowest of the register (main @249bb82e), open and closed issues through #910, David Ellsworth's catalogue, public Kaggle notebook outputs we have imported, and the monotone envelope; checked 2026-11-05.

**For information (side-only claims).**  Kaggle's per-puzzle leaderboard (staff notebook output, fetched 2026-11-05 15:18 UTC; no coordinates; sides below rounded up at 12 places) lists sides below ours at five of these counts, and at 175 and 293 sides 2.5·10⁻¹² above our exact sides.  We can't check them.  As far as we know, ours are the best publicly known *packings* at these counts.
* 175: 13.764050051546 (Yukai Liu, 2026-10-26 10:52 UTC); our exact side is 2.6·10⁻¹² below it.
* 204: 14.803489183116 (Cats and boxes, 2026-10-27 21:40 UTC).
* 260: 16.633520950297 (Toan Nguyen Mau, 2026-11-03 02:41 UTC); ours is 5.9·10⁻¹⁰ above it, probably the same packing less well polished (see Local optimality).
* 268: 16.871868135138 (Cats and boxes, 2026-10-28 21:42 UTC).
* 293: 17.623065212064 (Shadoks, 2026-11-04 06:30 UTC); our exact side is 2.5·10⁻¹² below it.
* 303: 17.895926158278 (Cats and boxes, 2026-11-01 09:10 UTC).
* 304: 17.918005472843 (square1000, 2026-10-27 02:47 UTC).

**Certificates.** In https://github.com/evand/square-packing at commit [bb4cc78e](https://github.com/evand/square-packing/tree/bb4cc78e/search/packer/candidates):

| file | what | SHA-256 |
|---|---|---|
| `s175_1105.cert` | exact KKT point, rational certificate (S' = 13.764050051543175143919941166751) | `32749cb2cc072a1fa70231b68908c1a255092c032748ff5c33c1ccfe018ea916` |
| `s175_1105_regularized.cert` | regularized view, same side | `786519adb0c0f103b7130eae165b65feaa4e59d3b02591cdd67c37e2f615c1d4` |
| `s204_trig1.cert` | exact KKT point (S' = 14.804361383651858725520289874026) | `17ed0e5b7c4e69ca8558195886be7d7a149e9c09a8f60caf57bef160f75cf687` |
| `s204_trig1_regularized.cert` | regularized view, same side | `55007aca9181eeb8ac53b9e48705c716974ede0bb0feee183ac6b8c493d9d107` |
| `s260_ks_1105.cert` | dilation certificate of `s260_ks_1105.input.txt` (S' = 16.633520950888535) | `24edcc0b45e4b3b57b6632bbe0430d2574425205c0b127e8f96f16fc3e38b663` |
| `s268_1105.cert` | exact KKT point (S' = 16.872499518135030646078935627448) | `50f9704860c186e47e30244226b983cccd36b3ff27ba3fd23bad31ce146a1844` |
| `s268_1105_regularized.cert` | regularized view, same side | `cfb1f7a793884bb938f29f10aa7dcd93b0c078700141af98a3bceb70ec69c0b2` |
| `s293_1105.cert` | exact KKT point (S' = 17.623065212060701770633564247069) | `0fc702287dc5a79360da89379822b42ef12de0d54f0d9b7b13f2f765ba659f28` |
| `s293_1105_regularized.cert` | regularized view, same side | `76d57b853e3e332b2e65084f07af863135dc74a1b0b179ba4a4e4d310cae9ab1` |
| `s303_1105.cert` | exact KKT point (S' = 17.901832750854048761575294038467) | `2f53c049a5f7feb793181e99282d0b36922b7c6f7fe9eece008f888c06a5c9a3` |
| `s303_1105_regularized.cert` | regularized view (its box is 1.9·10⁻³² larger than S*, inside the certificate's side S') | `42a8ecd958c7f381a5ca82131b3df1f8fe237605bb44d4cb2facca07443f1940` |
| `s304_1105.cert` | exact KKT point (S' = 17.920944093340242061198022152503) | `440402323670057e763ab6edac7cb4ba971222929d235a587b130f96d6d595cf` |
| `s304_1105_regularized.cert` | regularized view, same side | `ee95b657f24d0f93b2b02c073922147b36faed4996fcdd6df587f713fccad065` |

The f64 inputs (`<name>.input.txt`), the pre-descent inputs (`<name>.predescent.txt`), the 80-digit points (`<name>.exact.txt`) and the run summaries (`<name>.json`) are next to them.

**Credit and relationship.**  All seven are new packings, not refinements: each certified side is below the exact side of the packing it replaces, and where we compared exact points the contact graphs differ (numbers below).  All seven were built by our fault-line composer, which is our independent implementation of Chris Deotte's multi-gadget fault DP, described in his Kaggle notebooks.  Please credit Chris Deotte for the method.  The composer crops gadgets from packings in our store.  We did not log which packings donated gadgets before 2026-11-04, so for some of these the donor sources are unknown.
* **175:** built from gadgets of the register's s(175) packing (Mishapolk's, after Daniil Ostashev et al.; our store id 291599) and an earlier composer build of ours at 175.  Please credit that packing as the start.
* **204:** built from gadgets of our s(233) (a composer build of 2026-11-04) and an earlier s(370) of ours (side 19.808663234, 2026-10-13; not the one in #596).  No public start known to us.
* **260:** the same tilted island as our 260 of #845 (63 squares at 24.5° in both), recomposed in a 260 frame; same credit as #845's 260 (Kirill T (kirilltym)'s s(260) from his public Kaggle notebook as the start).
* **268, 293, 303, 304:** composer builds (first found 2026-11-01, 2026-11-02, 2026-11-02 and 2026-10-30), with gadget donors not recorded.  No public start known to us.

<details><summary>Checking</summary>

`search/exact/verify_cert.py` (separating axes) and `search/exact/verify_cert2.py` (polygon intersection) both report VALID on all thirteen certificate files; exact rational arithmetic, standard library only, e.g. `python3 search/exact/verify_cert.py search/packer/candidates/s303_1105.cert`.  The two checkers share an author (us) and the certificate format; the geometry tests differ.

</details>

<details><summary>Local optimality</summary>

Numerical evidence at 80 digits, not interval proofs.
* **175:** S* = 13.764050051543175143782…; a KKT point; positive semidefinite with 83 zero modes (strict only modulo these); no corner–corner MILP descent; 23 corner–corner contacts, 49 rattlers.
* **204:** S* = 14.804361383651858725372…; a KKT point; a local minimum of S, strict modulo 57 exact flat motions; 72 corner–corner contacts, 8 rattlers.
* **260:** not established.  Our exact solver did not converge, so the certificate dilates the f64 packing (by 8.8·10⁻¹²).  The corner–corner MILP linearization still suggests a small descent (dS* −1.2·10⁻⁶) that our descent step did not realise; Toan Nguyen Mau's side-only value suggests about 5.9·10⁻¹⁰ more is there.
* **268:** S* = 16.872499518135030645910…; a KKT point; inconclusive (negative curvature blocked at first order by weakly active contacts); no corner–corner MILP descent; 170 corner–corner contacts, 29 rattlers.
* **293:** S* = 17.623065212060701770457…; a KKT point; a local minimum of S, strict modulo 17 exact flat motions; 348 corner–corner contacts, 4 rattlers.
* **303:** S* = 17.901832750854048761396…; a KKT point, but not shown to be a local minimum: after releasing slack-separated pairs, the corner–corner branch MILP finds a first-order descent (dS −2.2·10⁻⁴) that our descent step did not realise.  The bound stands on the certificate either way.
* **304:** S* = 17.920944093340242061018…; a KKT point; a local minimum of S, strict modulo 103 exact flat motions; 123 corner–corner contacts, 9 rattlers.

</details>

<details><summary>Relationship to earlier packings: the numbers</summary>

*Refinement* here means the same local minimum only; otherwise a new packing.  Matched moves are over the best of the 8 box symmetries (regularized views, load-bearing squares; largest move; count moving more than 0.1 / more than 0.01).

| n | compared with | exact side gap | matched moves (max; > 0.1; > 0.01) | contact pairs (shared / only ours / only theirs) | verdict |
|---:|---|---:|---|---|---|
| 175 | register | 1.243·10⁻⁴ | 0.764; 26; 29 | 139 / 79 / 183 | different local minimum; no shared tilt angle |
| 204 | register (#894) | 3.260·10⁻³ | 1.03; 49; 103 | 262 / 175 / 132 | different local minimum; no shared tilt angle |
| 260 | register (#895) | 4.6·10⁻⁴ | | | new packing (our upper bound is below their exact side) |
| 268 | register | 1.862·10⁻³ | 1.07; 54; 70 | 405 / 241 / 142 | different local minimum; no shared tilt angle |
| 293 | register (#845) | 1.09·10⁻² | | | new packing (our upper bound is below their exact side) |
| 303 | register (#763) | 5.145·10⁻³ | 1.11; 110; 157 | 460 / 354 / 106 | different local minimum; no shared tilt angle |
| 304 | register | 5.95·10⁻³ | | | new packing (our upper bound is below their exact side) |

</details>

<details><summary>How it was found</summary>

All seven are hunts: composer builds run as event-triggered campaigns over our packing store (a build is redone when the gadget tables gain a cell that n can use, or when n's best changes), each build relaxed, and the store's improved packings fed back as gadget donors.
1. **Composition.**  A chain of gadgets (corner crops of store packings, at most K − 4 wide) is chosen by the fault DP at or a little above its minimum threshold, with gadgets drawn from several donors and orientations (175, 204: this variant; the others: the plain and loose chains), then relaxed.
2. **Polish and certify.**  Exact descent (corner–corner MILP kicks and re-solve) where the solver found the point not jammed, then `exactsolve.py` (KKT point, rational certificate) or, for 260, a dilation certificate.  260 also had relax passes (24 polish chains, an 8-arm relax sweep; only a kick-and-shrink relax gained, 5·10⁻⁸).
3. **Regularized views** by our regularizer.  303's needed a fix to it first (evand/square-packing 39fb4f02: rows violated after the angle step were dropped, and an inconsistent tight set was solved by least squares); with the fix the view's box is 1.9·10⁻³² larger than S*.

</details>

**AI assistance.**  The composer, the search, the checks and this request were done with Claude (Claude Code).  Evan Daniel directed the work and reviewed the results.
