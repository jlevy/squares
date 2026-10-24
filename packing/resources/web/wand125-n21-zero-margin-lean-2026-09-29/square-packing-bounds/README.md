# Lower bounds for packing 18–21, 26–32, 39, 45, 53, 55, 56, 69, 70 and 72 unit squares

Let `s(n)` be the least side of a square that holds `n` unit squares with
arbitrary orientations, no two overlapping. This repository contains exact
weighted fractional certificates proving

```
s(26) >= 109/20  = 5.45
s(29) >= 557/100 = 5.57
s(39) >= 13/2    = 6.5
s(53) >= 369/50  = 7.38
s(55) >= 377/50  = 7.54
s(56) >= 381/50  = 7.62
s(69) >= 841/100 = 8.41
s(70) >= 171/20  = 8.55
s(72) >= 861/100 = 8.61
```

and, as a cross-check on the generator, a tenth certificate for `s(40) >= 13/2`
that also follows from the `n = 39` bound by monotonicity.

It also contains certificates of a different kind, rectangle-density
certificates in tokoharu's format built here with his solver, proving

<!-- auto:claims:begin -->
```
s(18) >= 939/200    = 4.695
s(19) >= 963/200    = 4.815
s(20) >= 979/200    = 4.895
s(26) >= 553/100    = 5.53
s(27) >= 28/5       = 5.6
s(28) >= 143/25     = 5.72
s(29) >= 579/100    = 5.79
s(30) >= 1173/200   = 5.865
s(31) >= 1187/200   = 5.935
s(37) >= 257/40     = 6.425
s(38) >= 327/50     = 6.54
s(39) >= 663/100    = 6.63
s(40) >= 1339/200   = 6.695
s(41) >= 1351/200   = 6.755
s(42) >= 679/100    = 6.79
s(43) >= 172/25     = 6.88
s(44) >= 1387/200   = 6.935
s(51) >= 2977/400   = 7.4425
s(52) >= 1507/200   = 7.535
s(53) >= 1521/200   = 7.605
s(54) >= 3067/400   = 7.6675
s(55) >= 771/100    = 7.71
s(56) >= 777/100    = 7.77
s(57) >= 1567/200   = 7.835
s(58) >= 789/100    = 7.89
s(59) >= 198/25     = 7.92
s(60) >= 397/50     = 7.94
s(61) >= 199/25     = 7.96
s(66) >= 67/8       = 8.375
s(67) >= 1691/200   = 8.455
s(68) >= 1701/200   = 8.505
s(69) >= 343/40     = 8.575
s(70) >= 431/50     = 8.62
s(71) >= 1737/200   = 8.685
s(72) >= 437/50     = 8.74
s(73) >= 439/50     = 8.78
s(74) >= 221/25     = 8.84
s(75) >= 89/10      = 8.9
s(76) >= 223/25     = 8.92   (also n = 77)
s(77) >= 891/100    = 8.91
s(78) >= 1791/200   = 8.955
s(86) >= 1871/200   = 9.355
s(88) >= 189/20     = 9.45
s(89) >= 191/20     = 9.55   (also n = 90)
s(91) >= 1929/200   = 9.645
s(94) >= 1959/200   = 9.795
s(95) >= 49209/5000 = 9.8418
```
<!-- auto:claims:end -->

The `n = 29` certificate supersedes the point certificate above and, by
monotonicity, also gives `s(30), s(31) >= 5.7775`. See
[s(29): a ladder of rectangle-density certificates](#s29-a-ladder-of-rectangle-density-certificates-built-here),
[n = 32 and n = 45](#n--32-and-n--45-rectangle-density-certificates-from-our-own-parents)
and [n = 18 to 28](#n--18-to-28-rectangle-density-certificates-past-the-register).
A further rectangle certificate for `n = 26` reaches a value that
others already hold. They are included as independent certificates of those
values; see [Matching certificates](#matching-certificates).

### Standing rectangle certificates

The highest published rectangle certificate for each `n`. The table is
regenerated on every publication, so it is always current. The sections
further down explain how the certificates were built and list earlier rungs.
"previous record" is the best bound held without our rectangle certificates.
It includes our own point certificates. A certificate also covers every
larger `n` above its total mass.

<!-- auto:standing:begin -->
| `n` | bound | exact | total mass | directory | previous record | kind | verifier nodes |
|---|---|---|---|---|---|---|---|
| 18 | **4.695** | 939/200 | 17.990000 | `rect_n18_L4695` | 4.679000 (jlevy/squares) | record | 25,076,758 |
| 19 | **4.815** | 963/200 | 18.990000 | `rect_n19_L4815` | 4.800000 (jlevy/squares) | record | 20,589,220 |
| 20 | **4.895** | 979/200 | 19.990000 | `rect_n20_L4895` | 4.850000 (jlevy/squares) | record | 12,652,620 |
| 21 | **4.9875** | 399/80 | 20.999000 | `rect_n21_L49875` | 5.000000 (evand) | match | 45,191,252 |
| 26 | **5.53** | 553/100 | 25.990000 | `rect_n26_L553` | 5.508000 (tokoharu) | record | 17,165,686 |
| 27 | **5.6** | 28/5 | 26.999000 | `rect_n27_L56` | 5.508000 (tokoharu) | record | 11,492,606 |
| 28 | **5.72** | 143/25 | 27.990000 | `rect_n28_L572` | 5.511709 (Green) | record | 19,056,355 |
| 29 | **5.79** | 579/100 | 28.990000 | `rect_n29_L579` | 5.710000 (tokoharu) | record | 12,223,906 |
| 30 | **5.865** | 1173/200 | 29.990000 | `rect_n30_L5865` | 5.710000 (tokoharu) | record | 12,985,999 |
| 31 | **5.935** | 1187/200 | 30.990000 | `rect_n31_L5935` | 5.710000 (tokoharu) | record | 15,093,494 |
| 32 | **5.95** | 119/20 | 31.990000 | `rect_n32_L595` | 6.000000 (evand) | match | 5,808,912 |
| 37 | **6.425** | 257/40 | 36.990000 | `rect_n37_L6425` | 6.350603 (Green) | record | 28,286,611 |
| 38 | **6.54** | 327/50 | 37.990000 | `rect_n38_L654` | 6.350603 (Green) | record | 20,270,571 |
| 39 | **6.63** | 663/100 | 38.990000 | `rect_n39_L663` | 6.500000 (this work) | record | 18,162,666 |
| 40 | **6.695** | 1339/200 | 39.990000 | `rect_n40_L6695` | 6.500000 (this work) | record | 17,444,552 |
| 41 | **6.755** | 1351/200 | 40.990000 | `rect_n41_L6755` | 6.500000 (this work) | record | 19,190,037 |
| 42 | **6.79** | 679/100 | 41.990000 | `rect_n42_L679` | 6.567764 (Nagamochi) | record | 25,783,865 |
| 43 | **6.88** | 172/25 | 42.990000 | `rect_n43_L688` | 6.656854 (Nagamochi) | record | 29,358,408 |
| 44 | **6.935** | 1387/200 | 43.990000 | `rect_n44_L6935` | 6.744563 (Nagamochi) | record | 30,236,962 |
| 45 | **6.955** | 1391/200 | 44.990000 | `rect_n45_L6955` | 7.000000 (evand) | match | 15,360,958 |
| 51 | **7.4425** | 2977/400 | 50.990000 | `rect_n51_L74425` | 7.317426 (Green) | record | 22,911,774 |
| 52 | **7.535** | 1507/200 | 51.990000 | `rect_n52_L7535` | 7.380000 (this work) | record | 24,539,623 |
| 53 | **7.605** | 1521/200 | 52.990000 | `rect_n53_L7605` | 7.380000 (this work) | record | 25,741,548 |
| 54 | **7.6675** | 3067/400 | 53.990000 | `rect_n54_L76675` | 7.403124 (Nagamochi) | record | 23,226,446 |
| 55 | **7.71** | 771/100 | 54.990000 | `rect_n55_L771` | 7.540000 (this work) | record | 26,199,121 |
| 56 | **7.77** | 777/100 | 55.990000 | `rect_n56_L777` | 7.620000 (this work) | record | 23,792,428 |
| 57 | **7.835** | 1567/200 | 56.990000 | `rect_n57_L7835` | 7.633250 (Nagamochi) | record | 28,668,321 |
| 58 | **7.89** | 789/100 | 57.990000 | `rect_n58_L789` | 7.708204 (Nagamochi) | record | 31,706,414 |
| 59 | **7.92** | 198/25 | 58.990000 | `rect_n59_L792` | 7.782330 (Nagamochi) | record | 28,400,348 |
| 60 | **7.94** | 397/50 | 59.990000 | `rect_n60_L794` | 7.855655 (Nagamochi) | record | 32,869,712 |
| 61 | **7.96** | 199/25 | 60.990000 | `rect_n61_L796` | 7.928203 (Nagamochi) | record | 20,526,671 |
| 66 | **8.375** | 67/8 | 65.990000 | `rect_n66_L8375` | 8.289966 (Green) | record | 24,419,529 |
| 67 | **8.455** | 1691/200 | 66.990000 | `rect_n67_L8455` | 8.289966 (Green) | record | 25,217,361 |
| 68 | **8.505** | 1701/200 | 67.990000 | `rect_n68_L8505` | 8.410000 (this work) | record | 25,686,679 |
| 69 | **8.575** | 343/40 | 68.990000 | `rect_n69_L8575` | 8.410000 (this work) | record | 26,472,386 |
| 70 | **8.62** | 431/50 | 69.990000 | `rect_n70_L862` | 8.550000 (this work) | record | 28,154,881 |
| 71 | **8.685** | 1737/200 | 70.990000 | `rect_n71_L8685` | 8.550000 (this work) | record | 26,773,005 |
| 72 | **8.74** | 437/50 | 71.990000 | `rect_n72_L874` | 8.610000 (this work) | record | 28,630,683 |
| 73 | **8.78** | 439/50 | 72.990000 | `rect_n73_L878` | 8.615773 (Nagamochi) | record | 27,329,821 |
| 74 | **8.84** | 221/25 | 73.990000 | `rect_n74_L884` | 8.681146 (Nagamochi) | record | 28,314,633 |
| 75 | **8.9** | 89/10 | 74.990000 | `rect_n75_L89` | 8.745967 (Nagamochi) | record | 29,959,986 |
| 76 | **8.92** | 223/25 | 75.990000 | `rect_n76_L892` | 8.810250 (Nagamochi) | record | 32,409,668 |
| 77 | **8.91** | 891/100 | 76.990000 | `rect_n77_L891` | 8.874008 (Nagamochi) | record | 21,404,934 |
| 78 | **8.955** | 1791/200 | 77.990000 | `rect_n78_L8955` | 8.937254 (Nagamochi) | record | 30,376,068 |
| 86 | **9.355** | 1871/200 | 85.990000 | `rect_n86_L9355` | 9.306624 (Nagamochi) | record | 28,780,525 |
| 88 | **9.45** | 189/20 | 87.990000 | `rect_n88_L945` | 9.426150 (Nagamochi) | record | 25,894,800 |
| 89 | **9.55** | 191/20 | 88.990000 | `rect_n89_L955` | 9.485281 (Nagamochi) | record | 30,206,476 |
| 91 | **9.645** | 1929/200 | 90.990000 | `rect_n91_L9645` | 9.602325 (Nagamochi) | record | 29,755,717 |
| 94 | **9.795** | 1959/200 | 93.990000 | `rect_n94_L9795` | 9.774964 (Nagamochi) | record | 30,426,378 |
| 95 | **9.8418** | 49209/5000 | 94.990000 | `rect_n95_L98418` | 9.831761 (Nagamochi) | record | 34,659,569 |
<!-- auto:standing:end -->

The previous figures for these cases come from a private communication from
Trevor Green to Erich Friedman, reported in Friedman's survey *Packing Unit
Squares in Squares* (Electronic Journal of Combinatorics, DS7), whose last
revision is dated 14 August 2009. The underlying argument has not been
published. The bounds here are the first to improve them, and they arrive with
certificates anyone can re-check.

| `n` | previously reported | this repository | improvement |
|---|---|---|---|
| 26 | 5.3923 | 5.45 (since improved elsewhere, see below) | +0.0577 |
| 29 | 5.5119 | 5.57 (superseded here by 5.7775, see below) | +0.0581 |
| 32 | 5.7958 | **5.82** (rectangle density, see below) | +0.0242 |
| 39 | 6.3512 | **6.5** | +0.1488 |
| 45 | 6.8310 | **6.8725** (rectangle density, see below) | +0.0415 |
| 53 | 7.3246 | **7.38** | +0.0554 |
| 55 | 7.4807 | **7.54** | +0.0593 |
| 56 | 7.5574 | **7.62** | +0.0626 |
| 69 | 8.3485 | **8.41** | +0.0615 |
| 70 | 8.4162 | **8.55** | +0.1338 |
| 72 | 8.5498 | **8.61** | +0.0602 |
| 40 | 6.4061 | 6.5 (follows from `n = 39`) | +0.0939 |

For `n = 32, 45, 53, 55, 56, 69, 70, 72` the standing figure is Nagamochi's closed form, which
is the strongest independently verified bound the survey records for those
cases; for `n = 26, 29, 39` it is Green's. By monotonicity `s(39) >= 6.5` also
covers `n = 40..44` against the DS7 table and `s(70) >= 8.55` covers `n = 71`.

The `n = 53`, `n = 56`, `n = 69` and `n = 72` certificates carry no further
entries with them. Nagamochi's closed form already exceeds 7.38 from `n = 54`
on, 7.62 from `n = 57` on and 8.61 from `n = 73` on, and this repository's own
`s(70) >= 8.55` covers everything above `n = 69`, so monotonicity gives nothing
there; these four improve their own cases only.

`s(56)` and `s(72)` improve on what our own earlier certificates already gave.
Monotonicity from `s(55) >= 7.54` put `s(56)` at 7.54 and from `s(70) >= 8.55`
put `s(72)` at 8.55; the direct certificates raise those by 0.08 and 0.06.

## n = 26 and n = 29 have since been improved

[tokoharu/square-packing-density-bounds](https://github.com/tokoharu/square-packing-density-bounds)
proves `s(26) >= 1377/250 = 5.508` and `s(29) >= 571/100 = 5.71`, past the two
point certificates here, and by monotonicity those also carry `n = 27, 30, 31`.
We have since carried his method further ourselves: `n = 29` to
`2311/400 = 5.7775`, and `n = 27, 28` to `277/50 = 5.54`. For `n = 26` we
have an independent certificate at his 5.508 but nothing beyond it.

That work generalizes the basis from point masses to uniform densities on
axis-aligned rectangles, D4-symmetrized about the centre, so the quantity a
placement captures is an area integral rather than a sum of point weights. A
point is caught or missed outright; a rectangle is captured in proportion to
the overlap, which gives the optimizer a degree of freedom the point basis does
not have. For `n = 29` it reaches the better bound with *fewer* basis elements
(552 rectangles against 748 atoms here), so the gain is in what each element
can express, not in how many there are.

The certificates here are unaffected as proofs -- they still establish what
they claim -- but for these two cases they are no longer the strongest known.
Both of tokoharu's certificates were re-checked against their verifier,
compiled and run independently, as part of confirming this.

## s(29): a ladder of rectangle-density certificates built here

`certificates/rect_n29_L*/` holds twenty-one certificates in tokoharu's format, each
proving a better lower bound on `s(29)` than his own `571/100 = 5.71`:

| directory | `L` | exact | total mass | budget | verifier nodes |
|---|---|---|---|---|---|
| `rect_n29_L574` | 5.74 | 287/50 | 28.307500 | 29 | 6,220,710 |
| `rect_n29_L57403125` | 5.7403125 | 18369/3200 | 28.312239 | 29 | 6,259,495 |
| `rect_n29_L5740625` | 5.740625 | 1837/320 | 28.292811 | 29 | 6,801,596 |
| `rect_n29_L574125` | 5.74125 | 4593/800 | 28.900000 | 29 | 4,861,306 |
| `rect_n29_L574375` | 5.74375 | 919/160 | 28.317278 | 29 | 6,821,444 |
| `rect_n29_L574625` | 5.74625 | 4597/800 | 28.358148 | 29 | 6,734,510 |
| `rect_n29_L574875` | 5.74875 | 4599/800 | 28.376913 | 29 | 7,091,278 |
| `rect_n29_L575125` | 5.75125 | 4601/800 | 28.414424 | 29 | 7,132,455 |
| `rect_n29_L5751875` | 5.751875 | 9203/1600 | 28.413163 | 29 | 7,326,490 |
| `rect_n29_L57525` | 5.7525 | 2301/400 | 28.418591 | 29 | 7,357,544 |
| `rect_n29_L575375` | 5.75375 | 4603/800 | 28.990000 | 29 | 5,222,853 |
| `rect_n29_L5755` | 5.755 | 1151/200 | 28.990000 | 29 | 5,246,956 |
| `rect_n29_L57575` | 5.7575 | 2303/400 | 28.990000 | 29 | 5,530,431 |
| `rect_n29_L576` | 5.76 | 144/25 | 28.990000 | 29 | 5,470,623 |
| `rect_n29_L57625` | 5.7625 | 461/80 | 28.990000 | 29 | 5,435,964 |
| `rect_n29_L5765` | 5.765 | 1153/200 | 28.990000 | 29 | 5,726,956 |
| `rect_n29_L57675` | 5.7675 | 2307/400 | 28.990000 | 29 | 6,020,892 |
| `rect_n29_L577` | 5.77 | 577/100 | 28.990000 | 29 | 6,180,299 |
| `rect_n29_L57725` | 5.7725 | 2309/400 | 28.990000 | 29 | 6,391,897 |
| `rect_n29_L5775` | 5.775 | 231/40 | 28.990000 | 29 | 6,682,472 |
| **`rect_n29_L57775`** | **5.7775** | **2311/400** | **28.990000** | 29 | 6,974,142 |

The last row is the standing bound: **`s(29) >= 2311/400 = 5.7775`**. Its total
mass is `2899/100 < 30 < 31`, so the same certificate also proves
`s(30) >= 5.7775` and `s(31) >= 5.7775`.

They were produced with tokoharu's solver, driven by `push.py`, the ladder
driver we contributed to his repository
([PR #1](https://github.com/tokoharu/square-packing-density-bounds/pull/1),
[PR #2](https://github.com/tokoharu/square-packing-density-bounds/pull/2), both
merged). Starting from his certified `n = 29` certificate at 5.71, the driver
raises the side one rung at a time, running his `engine.py` search, then his
`certify.py`, and keeping a rung only when the certificate is accepted. The
rungs were 5.73, 5.7325, 5.73375, 5.735, 5.7375, 5.738125, 5.73875, 5.74,
5.7403125, 5.740625, 5.74125, 5.74375, 5.74625, 5.74875, 5.75125 and
5.751875; every one of them was certified before the next was attempted.

The last rung is smaller than the others because the two attempts above it,
at 5.75375 and 5.7525, were both rejected by the solver's own LP residual
check, so the driver halved its step twice, from 1/400 to 1/1600, and the
rung that then certified advances the bound by 1/1600 rather than 1/400.
No tolerance was relaxed to obtain it. The ladder then certified 5.7525 as an
ordinary rung.

### The rungs from 5.75375 on: fixed support, then scaling

Every rung from `5.75375` to `5.7775` came from a second route, which keeps
the parent's rectangles instead of searching for new ones. For each rung the
previous certified rung is the parent. Its rectangles are carried to the new
side with their positions scaled, and his LP is solved again over that fixed
support. Placements that fall short in his screen are added as rows. For
`5.75375` the rows also included 13 counterexamples saved from an earlier
attempt at that side. Once the screen found no violation, every weight was
multiplied by one exact rational factor that brings the total mass to exactly
`2899/100 = 28.99`. This is the scaling step described in the next subsection,
used here with a reserve of 0.01 instead of 0.1. The factor is recorded in
each `certified_candidate.json` under `scaling_experiment` (for `5.7775` it takes
28.890942 to 28.99). The scaled certificate then went through the unmodified
verifier.

This route did not use `push.py`. The reserve is thinner than on the ladder
rungs, 0.01 under the budget rather than about 0.6, but that affects only how
easily the next rung can be found, not the validity of the certificate.

### How the 5.74125 rung was obtained

`5.74125` did not come from the ladder. The search had spent six hours on that
side without converging: its incumbent sat at mass 28.2747354324, and each
further repair round shaved off less than the round before. Rather than keep
minimising, we used the room left under the budget. Every weight of that stalled
incumbent was multiplied by the exact rational

```
289000000000000000000/282747354324056990663
```

which takes the total mass to exactly `289/10 = 28.9`, still strictly below 29.
Scaling every weight by a common factor preserves the covering structure and
raises every captured amount by the same factor, so a placement that fell short
of 1 by less than that factor now clears it. The scaled certificate was then put
through the unmodified verifier, which accepted all 201 angle cases in 538
seconds.

The trade is margin for time: that certificate leaves only 0.1 under the budget
where the 5.740625 rung leaves 0.707. It is a certificate either way — the
budget condition is met — but it is a thinner foundation for the next rung.

**The next rung repaired it.** Restarting the ladder from the scaled certificate,
`5.74375` came back with mass 28.317278, a margin of 0.683 — within a whisker of
the 0.707 the ordinary rungs carry, and 6.8 times the margin it started from. The
thin foundation lasts exactly one rung. That is what makes the scaling step worth
repeating rather than a one-off rescue: it costs one rung of margin to convert a
stalled search into a certificate.

### Checking them

Each directory holds the data the verifier reads and the verifier itself:

| file | meaning |
|---|---|
| `certified_candidate.json` | the certificate: `L`, `B = 9977/10000`, and the rectangles with exact rational densities |
| `certificate_input.txt` | the same data in the text form `verify.cpp` parses, as outward-rounded interval endpoints; its header counts the D4 images of the positive-weight rectangles |
| `certificate_metadata.json` | exact total mass and the SHA-256 of the input |
| `verify.cpp`, `run_verify.py` | tokoharu's interval verifier and its runner, unchanged (MIT; `verify.cpp` SHA-256 `a75140df…`) |
| `verification_summary.json`, `verified_angles.jsonl` | the record of the accepting run: 201 angle cases and every leaf lower bound at least `10001/10000` |

To re-check one (needs `g++`; a few minutes on four cores):

```bash
cd certificates/rect_n29_L576 && python3 run_verify.py --workers 4
```

It ends by writing `verification_summary.json` with `"status": "VERIFIED"`.
That happens only when all 201 angle cases (`r = 0..200`) finish and every
case reports `status: verified` with a leaf lower bound of at least
`10001/10000`. A missing or failed case makes the runner exit nonzero, and it
writes no summary. The runner does not check the budget condition. Check it
from `certificate_metadata.json`: `mass_exact` must be strictly below `n`. The
`n` of a certificate is the one in its directory name, and any larger `n` also
satisfies the condition. For every rectangle certificate here, the
`input_sha256` recorded by the accepting run matches the one in its metadata,
so the bytes verified are the bytes published.

Before publication, every standing certificate (the highest one for each
`n`, including the matching ones) was replayed on a second machine from the
published files alone. Each
`certificate_input.txt` was regenerated from `certified_candidate.json` and
matched byte for byte. The exact mass was recomputed from the rational weights.
The unmodified verifier was run again, and every replay was accepted with the
same node count as the original run. The other rungs were checked for hash
agreement and exact mass.

The argument
behind `verify.cpp` — outward-rounded interval arithmetic, a certified
inscribed-polygon area for each rectangle overlap, derivative bounds over centre
boxes, and the same rational angular net as above — is tokoharu's and is
documented in his repository; nothing in the mathematics is ours. What is ours
is the driver, the machine time, the fixed-support route, the scaling step
described above, and the choice of parents described below.

`src/verify.py` does not read this format: it checks point certificates only.

## n = 32 and n = 45: rectangle-density certificates from our own parents

Two more certificates in the same format and checked by the same unmodified
verifier improve cases nobody had a certificate for. The standing figure for
both was Nagamochi's closed form:

| directory | `L` | exact | total mass | budget | previous | verifier nodes |
|---|---|---|---|---|---|---|
| **`rect_n32_L582`** | **5.82** | **291/50** | 31.990000 | 32 | `1 + sqrt(23)` = 5.795832 | 2,766,145 |
| `rect_n45_L68525` | 6.8525 | 2741/400 | 44.990000 | 45 | `1 + sqrt(34)` = 6.830952 | 7,443,908 |
| `rect_n45_L687` | 6.87 | 687/100 | 44.990000 | 45 | `1 + sqrt(34)` = 6.830952 | 7,995,368 |
| **`rect_n45_L68725`** | **6.8725** | **2749/400** | 44.990000 | 45 | `1 + sqrt(34)` = 6.830952 | 8,174,359 |

Both beat the previous figure exactly: `(5.82 - 1)^2 = 23.2324 > 23` and
`(6.8725 - 1)^2 = 34.48625625 > 34`.

**n = 32.** The first rung, 5.80, took its rectangles from the `n = 29`
certificate at 5.751875 above, scaled to the new side. His LP was solved again
with row generation against the budget of 32. Fixed-support rungs then gave
5.81 and 5.82. For 5.82 the LP solution, at mass 30.325272, was scaled up to
exactly `3199/100` as described above, and the factor is in the file. The
certificate has 54 rectangles of positive weight, each of which stands for its
D4 images.

**n = 45.** No rectangle certificate existed near this size, so the parent is
our point certificate for `n = 39` at 6.5. The positions of its positive-weight
atoms were scaled to the new side and each one was replaced by a small square
support. Wall-anchored supports and a coarse full-container fallback were
added. His LP then optimized from scratch, so no point weight is carried over
as a rectangle weight. The first rung to certify was 6.84. From there,
fixed-support rungs as for `n = 29` raised it through 6.8425, 6.845, 6.8475
and 6.85 to 6.8525, and later in steps of 1/400 to 6.8725. Every rung was
scaled to mass `4499/100` and verified before the next was attempted. Only
6.8525, 6.87 and 6.8725 are published here.

## n = 18 to 28: rectangle-density certificates past the register

Six more certificates, in the same format and checked by the same unmodified
verifier, go past the verified lane of the
[jlevy/squares](https://github.com/jlevy/squares) register (as of its commit
`db3f5f3`, 2026-09-25):

| directory | `L` | exact | total mass | budget | register, verified lane | verifier nodes |
|---|---|---|---|---|---|---|
| **`rect_n18_L469`** | **4.69** | **469/100** | 17.990000 | 18 | 4.679 (jlevy/squares) | 12,577,765 |
| **`rect_n19_L481`** | **4.81** | **481/100** | 18.990000 | 19 | 4.80 (jlevy/squares) | 10,759,911 |
| **`rect_n20_L488`** | **4.88** | **122/25** | 19.990000 | 20 | 4.85 (jlevy/squares) | 7,981,881 |
| `rect_n21_L493` | 4.93 | 493/100 | 20.990000 | 21 | 4.88 (jlevy/squares) | 11,243,723 |
| **`rect_n21_L494`** | **4.94** | **247/50** | 20.990000 | 21 | 4.88 (jlevy/squares) | 8,690,560 |
| **`rect_n27_L554`** | **5.54** | **277/50** | 26.990000 | 27 | 5.508 (tokoharu, by monotonicity) | 11,903,829 |
| **`rect_n28_L554`** | **5.54** | **277/50** | 27.990000 | 28 | 5.508 (tokoharu, by monotonicity) | 20,615,178 |

For `n = 28` the register's reported lane also carries Green's
`2*sqrt(2) + 6/sqrt(5)` = 5.511709, and 5.54 is above that as well. The
`n = 27` certificate has mass 26.99, so it also proves `s(28) >= 5.54`. The
`n = 28` certificate was found separately and is a direct one.

The chains for `n = 18`, `19`, `21` and `28` go back to our own point
certificates for those sizes. `n = 20` started from the `n = 19` rectangle
certificate at 4.62. As for `n = 45`, the positive-weight atoms were
replaced by small rectangle supports, and his LP optimized the weights from
scratch. Each chain then climbed rung by rung. Most rungs used the fixed-support
route described for `n = 29`. Some rungs also added columns: new free-standing
rectangles priced against the LP duals. For `n = 19` and `n = 21` the LP was
first solved by an interior-point method rather than simplex. That changes how
the optimum is found, not the certificate the verifier checks. `n = 27` takes
its rectangles from the `n = 26` certificate below, with fixed support at
side 5.54. Every certificate was scaled to mass exactly `n - 1/100` before
verification, and the factor is in the file.

## Matching certificates

These reach values that other people had already proved. They are included
because they were reached independently and pass the same unmodified verifier.
They do not improve any record.

| directory | `L` | exact | total mass | budget | value already held by | verifier nodes |
|---|---|---|---|---|---|---|
| `rect_n18_L4679` | 4.679 | 4679/1000 | 17.990000 | 18 | jlevy/squares, point certificate (now superseded here by 4.69) | 9,971,192 |
| `rect_n26_L5508` | 5.508 | 1377/250 | 25.990000 | 26 | tokoharu | 19,606,206 |
| `rect_n21_L488` | 4.88 | 122/25 | 20.990000 | 21 | jlevy/squares (now superseded here by 4.94) | 9,136,007 |
| `rect_n28_L5508` | 5.508 | 1377/250 | 27.990000 | 28 | tokoharu, by monotonicity (now superseded here by 5.54) | 18,949,885 |

The `n = 26` certificate is a direct one for `n = 26`, found independently of
tokoharu's. Its last stage fixed a support that had been grown by
free-rectangle pricing and repaired it at 5.508.

## n = 50: certificates past Green's bound, checked with their own verifiers

[`certificates/mixed_n50_L740`](certificates/mixed_n50_L740/README.md) proves

```
s(50) >= 37/5 = 7.4
```

This is above Green's `7.3174260…` by more than `0.0825`. The measure is 553 uniform-density rectangles
with total mass `4999999/100000`, built directly at L = 7.4. Every net angle has coverage `>= 1`, and
the lowest is `1.0000000004…`. It uses the same verifier as `mixed_n50_L7318`. The full 201-angle replay
was run again from the published tarball before publication. It supersedes the two certificates below.

[`certificates/mixed_n50_L735`](certificates/mixed_n50_L735/README.md) proves

```
s(50) >= 147/20 = 7.35
```

This is above Green's `7.3174260…` by more than `0.0325`. The measure is 499 uniform-density
rectangles with total mass `4999999/100000`. Every net angle has coverage `>= 1`; the lowest is
`1.0000000005…`. It was checked with the verifier shipped in its bundle, and the audit and the
full 201-angle replay were run again from the published tarball before publication. It
supersedes the earlier certificate below.

[`certificates/mixed_n50_L7318`](certificates/mixed_n50_L7318/README.md) proves

```
s(50) >= 3659/500 = 7.318
```

This is above Green's `2√2 + 101/25 + 3√14/25 = 7.3174260…` by more than `0.000573`.
The measure is 355 rectangles of uniform density with total mass
`4999999/100000 < 50`. The setting is the same as the rectangle certificates here:
core side `B = 9977/10000`, and 201 net angles with step `83/40000`.

Every net angle was proved with coverage `>= 1`; the lowest is `1.0000019…`.
That is below the `1.0001` which tokoharu's `verify.cpp` asks for, so this certificate
is not in his format and is not listed in the tables above. It was checked instead with
a research copy of that verifier, which proves coverage `>= 1` over every centre domain.
The argument rests on `B(1 + 83/40000) < 1`, which puts a net-angle core strictly inside
every unit square.

The directory has the rational candidate, the checker and the complete 621-file bundle.
The full replay, the integer axis tables and all 200 oblique angles, was run where the
certificate was made and again from the published tarball, and both passed. The oblique
replay uses the same outward-rounded algorithm as the proof, not a second implementation.

## Closed-square endpoint certificate for n = 21

The separate [point-only endpoint bundle](point_n21_L5/README.md) proves
`s(21)=5` by a rational all-position, all-angle computational check and an
explicit boundary-contact argument. Its complete split replay and a fresh
one-command M1 run have passed. Monotonicity also gives `s(n)=5` for `22..25`.
Evan Daniel's earlier mixed-measure proof is acknowledged; priority for the
exact value is not claimed. The same certificate also gives a hypothesis-free Lean 4
proof of `minSide 21 = 5`, kernel-checked through Evan Daniel's zero-margin box tree with only
the standard axioms ([lean/zero-margin/](point_n21_L5/lean/zero-margin/README.md)).

The [point-only s(45) bundle](point_n45_L7/README.md) proves `s(45)=7` with a D4-invariant
point measure of total `44.99999100001… < 45`, checked over every position and angle by
Evan Daniel's unmodified `zmx2` (`VERIFIED-D4`, 4,900 roots, no uncertified box), built from
the pinned upstream commit by `verify.sh`. His mixed-measure proof of the same value came
first; this is a separate points-only route.
The earlier tables and instructions below describe the other certificate
families; use the endpoint bundle's own reproduction instructions for this proof.

## How the proof works

Scatter finitely many points in the container and give each a nonnegative
rational weight. If every unit square that fits, at every orientation and
position, covers total weight at least 1, then `n` non-overlapping squares
cover at least `n`. Choose the weights so the total is strictly below `n` and
no such packing exists.

The certificate is the list of points and weights. Checking it means checking
five conditions, of which the fifth — that *every* placement covers mass 1 —
is the one that needs a computer. Two devices make it finite: a shrunken square
of side `B < 1` tested against a rational net of 201 directions, with
`B(1 + D) < 1` so the shrink absorbs the net's angular gap; and a sweep over
regions of centre positions rather than individual points.

This is the weighted fractional unavoidable-set method. It is not ours; see
[Attribution](#attribution).

## Verifying the certificates

### With this repository's checker

Requires Python 3.10+, NumPy.

```bash
pip install -r requirements.txt
python3 src/verify.py certificates/cert_n29_L557.json
```

It prints each condition as it decides it and ends with `VERIFIED`. It accepts
only JSON; a certificate is data, and loading one from a pickle would run
whatever the file contained.

Conditions 1 to 4 are decided exactly in `Fraction`. Condition 5 runs a
branch-and-bound recursion over centre boxes in float64 under a stated error
budget: `EPS = 1e-9` on geometric comparisons, mass threshold `1 + 1e-9`, boxes
not subdivided below `1e-7`. Coordinates stay under 100 in magnitude and each
compared quantity takes at most six floating-point operations, so rounding error
stays near `1e-13`; the mass is a sum of at most `10^4` nonnegative terms below
1, so its error stays near `1e-11`. Weights are rounded *up* to multiples of
`1e-8`, so rounding can only add mass.

Box counts, zero failures in each: 4,811,681 (`n=26`), 2,524,711 (`n=29`),
8,409,303 (`n=39`), 7,531,281 (`n=40`). Counts vary slightly between runs
because the split order is not deterministic; the outcome does not.

### With jlevy/squares' checker

[`jlevy/squares`](https://github.com/jlevy/squares) carries an independent
implementation that decides Condition 5 in exact integers on the weights'
common scale and returns the true minimum over event cells, rather than testing
a threshold in floating point. **It is the stronger check**, and all four
certificates pass it unmodified.

```bash
git clone https://github.com/jlevy/squares.git
cp src/check_with_sqpack.py certificates/*.json squares/
cd squares && python3 check_with_sqpack.py cert_n29_L557.json
```

```
n = 29   L = 557/100 = 5.57
atoms = 748   total mass = 453011/15625 = 28.992704   budget = 29
accepted = True   (13.8s)
  [ok  ] Condition 1 atoms carry the declared symmetry: 748 atoms closed under D4 about the centre
  [ok  ] Condition 2 total mass below n: total 453011/15625 against n = 29
  [ok  ] Condition 3 net reaches pi/4: final half-tangent 83/200, t^2 + 2t - 1 = 89/40000
  [ok  ] Condition 4 containment B(1 + D) < 1: B = 9977/10000, D = 83/40000, B(1 + D) = 399908091/400000000
  [ok  ] Condition 5 every reachable cell carries mass 1: least cell mass 1000003/1000000 at direction 0
=> s(29) >= 557/100 = 5.57
```

Results on one core, single worker:

| `n` | atoms | distinct under `D4` | total mass | margin under `n` | `verify` |
|---|---|---|---|---|---|
| 26 | 1376 | 179 | 646393601/25000000 = 25.855744 | 0.144256 | accepted, 28.2s |
| 29 | 748 | 100 | 453011/15625 = 28.992704 | **0.007296** | accepted, 13.8s |
| 39 | 2724 | 362 | 481487971/12500000 = 38.519038 | 0.480962 | accepted, 73.4s |
| 55 | 3196 | 410 | 1362984297/25000000 = 54.519372 | 0.480628 | accepted, 131.4s |
| 70 | 8060 | 1058 | 108946291/1562500 = 69.725626 | 0.274374 | accepted, 548.5s |
| 40 | 1892 | 250 | 975019903/25000000 = 39.000796 | 0.999204 | accepted, 45.1s |

The `n = 29` margin is the interesting one: the weights land `0.0073` under
budget, close to the ceiling the method allows. That is why `n = 29` was the
hardest of the three to find, while `n = 39` had room to spare.

## Certificate format

Each JSON file carries

| field | meaning |
|---|---|
| `n` | number of unit squares |
| `L` | container side, exact rational string |
| `B` | shrink factor `9977/10000` |
| `net` | the direction net as a rule: `theta_r = 2*atan(r*83/40000)`, `r = 0..200` |
| `atoms` | `[x, y, weight]` triples, exact rational strings |
| `total_mass` | sum of weights |
| `claim`, `verification` | the statement proved and the command that checks it |

The net is stored as a rule rather than a list; the half-angle tangents are
exactly `r * 83/40000`. `src/check_with_sqpack.py` shows the one-line
conversion to the form `jlevy/squares` expects.

## Finding the certificates

`src/lp.py` and `src/certify.py` search for them. The program is a covering
linear program over `D4` orbit representatives, solved with HiGHS through SciPy,
with rows generated by using the Condition 5 sweep as a separation oracle and
columns generated from dual reduced costs. A run is abandoned once the LP
optimum reaches `n`, since further rows only raise it.

```bash
python3 src/certify.py --n 29 --L 557/100
```

Runs are long and memory-hungry; the searches behind these four certificates
took hours each on a 128 GB machine, and `certify.py` checkpoints its own
progress so a run can resume. Those checkpoints are pickles it wrote itself
and are not part of the verification path.

## Attribution

The method is not ours.

- **Walter Stromquist** introduced unavoidable point sets with unit weights
  (unpublished memos 1984–85; *Packing 10 or 11 Unit Squares in a Square*,
  Electron. J. Combin. 10 (2003) #R8).
- **Hiroshi Nagamochi** introduced weighted score systems tuned by hand
  (Electron. J. Combin. 12 (2005) #R37).
- **Sam Burns** and **Gustavo Massaccesi** fractionalized the weights and
  introduced the exact rational direction net with the `B(1 + D) < 1` shrink,
  in August 2026. Our `B = 9977/10000` on 201 directions is a parameter choice
  within their framework.
- **[jlevy/squares](https://github.com/jlevy/squares)** added row generation
  via a separation oracle, dual-priced column generation, and branch-and-bound
  as a second Condition 5 decider, and documents the whole pipeline.

What is ours is the observation that nobody had run this machinery above
`n = 21`, the search runs, and the certificates. [`docs/prior-art-method.md`](docs/prior-art-method.md)
breaks the method into six components and attributes each;
[`docs/prior-art-results.md`](docs/prior-art-results.md) records the search for
prior publication of the bounds themselves. Japanese originals are alongside as
`*.ja.md`.

If any attribution here is wrong, please open an issue and we will correct it.

## Layout

```
certificates/   the ten point certificates as JSON, and rect_n*_L*/ in tokoharu's format
src/verify.py            our checker
src/check_with_sqpack.py adapter for the jlevy/squares checker
src/lp.py, src/certify.py the search
docs/lower-bounds.md      write-up of the argument and the numbers
docs/prior-art-method.md  which parts of the method are prior art, and whose
docs/prior-art-results.md search for prior publication of these bounds
docs/prior-art-*.ja.md    Japanese originals of the two notes above
```

## Status

Computer-assisted certificates. The point certificates are checked by two
independent implementations. The rectangle certificates are checked by
tokoharu's verifier, which was run again on a second machine for the standing
ones (see above). None of them has been peer reviewed. [jlevy/squares](https://github.com/jlevy/squares)
records the point bounds for `n = 39, 40, 53, 55, 56, 69, 70, 72` in its
frontier register, in both the reported and the verified lane, after an exact
replay of these files with its own checker (evidence
`E-wand125-point-source-replay`, 2026-09-22). As of its commit `db3f5f3`
(2026-09-25), the register does not yet include the rectangle certificates
here.

Parts of this work were produced with AI assistance under human direction.

## License

MIT. See `LICENSE`.
