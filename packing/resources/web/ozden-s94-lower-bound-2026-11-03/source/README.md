# s(94) ≥ 1993/200 = 9.965

A measure-capture (density) certificate showing that 94 unit squares do not fit in a
square of side `L = 1993/200 = 9.965`. The best verified lower bound before this was
`199/20 = 9.95`, Hiroaki Hosono's `mixed_n94_L995` certificate
([wand125/square-packing-bounds@797bdf6e](https://github.com/wand125/square-packing-bounds/tree/797bdf6e10eba5f9dccca9da06f8352e81ba9dde/certificates/mixed_n94_L995);
jlevy/squares T-091). The upper bound is the 10 × 10 grid.

This is a modest sharpening of Hosono's bound, not a new measure. The certificate is
Hosono's measure dilated about the origin by `λ = 1993/1990`, with a finer half-angle net
declared so that the dilated core still fits inside every unit square.

Claimed by Doğa Özden ([@dogaozden](https://github.com/dogaozden), https://dogaozden.com/math/live/square-packing/).
Found by his AI research lab; this repository and the registration were prepared by his
AI agent (GitHub account `kenaznia-doga`) on his behalf.

## The certificate

`certificate/n94_L9965.json.gz`, format M of jlevy/squares' `sqverify-fast` (Hosono's
format, with a declared `proof_net`):

| | value |
|---|---|
| side | `L = 1993/200` |
| core side | `B = 19884161/19900000` (Hosono's `9977/10000` × λ) |
| net | `proof_net` step `D = 83/120000`, `last = 599`: 600 half-angle directions, last tangent `49717/120000` > tan(π/8) |
| shrink premise | `B(1 + D) = 2387749705363/2388000000000 < 1` |
| measure | Hosono's 853 rectangle orbits, every coordinate × λ, masses unchanged |
| total mass | `9399999/100000 = 93.99999 < 94` |
| SHA-256 of the JSON text | `b8b03ee83fd2738f723759e8a54442adb55e607a211dd57d28873a62db9c749c` |
| SHA-256 of the `.json.gz` file (the `input_sha256` in the receipts) | `116c83425959a943196287a910ad799b2fe1bb9dec433085ea222bd62d5a16f8` |

It is regenerated exactly from Hosono's published `candidate.json` (SHA-256
`64d819536a9994172b1f7a7b2095e7b40e420a09efa7441d459e73191a20667a`) by

```sh
python3 tools/rescale.py candidate.json.gz 1993/200 out.json.gz 83/120000 599
```

`verify.sh` does this and compares the hash.

## Why a dilation needs a full re-check

Scaling the container, the measure and the core by λ maps a core of side `λB` at a centre
`p` to a core of side `B` at `p/λ` with the same mass, so on the old directions the old
coverage carries over for centres that map into the old centre domain. Two things do not
carry over, and both are re-checked here from scratch:

1. Unit squares do not scale. The admissible centre domain `[ρ, L − ρ]²` therefore grows,
   in old coordinates, toward the walls (at direction 0 by exactly `3/3986`). Coverage of
   those centres is new.
2. `λB(1 + 83/40000) > 1`, so Hosono's net no longer admits the larger core. The finer
   net (step `83/120000`) makes `B(1 + D) < 1` hold again, and 400 of its 600 directions
   are not in Hosono's net.

So the dilation is only how the candidate was found; the bound rests on the full
verification below. The route's ceiling, as the step goes to zero, is
`L/B = 99500/9977 ≈ 9.9729`. Larger dilations were not attempted here; a mutant at
`L = 9.975` with the core held admissible is refused at direction 144.

The same move fails at n = 31: Hosono's `2391/400` measure dilated to `2989/500 = 5.978`
on a step-`1/8600` net is refused by sqverify-fast at direction 529 with an exact
counterexample (capture `0.99999999719`, centre near a wall, in the region the dilation
adds), and still below 1 after spending all of the certificate's mass slack
(`notes/n31-negative/`). So the gain is case by case, not automatic.

## Checking

`sqverify-fast` from jlevy/squares, `packing/sqverify_fast`, source unchanged at
`e6e8d57726db80cd0e6a1523166a96c5d36a3119`:

| run | build | directions | result | cost |
|---|---|---|---|---|
| full | rustc 1.93.1, with only the `rust-version = "1.98"` line removed from `Cargo.toml` (source digest `85f02254…`) | 600/600 | `VERIFIED`, min certified lower bound `1.0000000000314`, 296.8 M nodes | 7,985 CPU-s (55 min wall, 4 threads) |
| full | unmodified, rustc 1.98.0 (source digest `d97758bb…`) | 600/600 | `VERIFIED`, min certified lower bound `1.0000000000314`, 296.8 M nodes; every direction identical to the 1.93 run | 7,887 CPU-s (113 min wall on a busy 4-core machine) |

Receipts are in `receipts/`. Rerun with

```sh
sh verify.sh            # regenerate and hash-check the certificate, build sqverify-fast, run all 600 directions
sh verify.sh 0,144,599  # the same, on a subset of directions
```

A second, independent check is in `second-checker/`: an exact-integer branch and bound
written by an OpenAI Codex agent for the review of this claim. It verified all 600
directions over their full centre domains (166.4 M nodes, minimum certified lower bound
`1.0000000000020`, 4,801 CPU-s on Apple arm64; directions 0, 144 and 599 reproduce
exactly on x86-64). Its reviewer's report, `second-checker/GRADE.md`, gives the verdict
SOUND and includes mutant controls that are each rejected with an exact counterexample.

What the two checkers share: the theorem (net, shrink, centre domain, D4 reduction,
counting). The second checker's author had `sqverify-fast`'s SOUNDNESS.md prose but not
its source; its arithmetic (fixed-point integers with directed rounding, exact rational
directions) and its code are separate. Both were written by AI agents.

## Not done

- No formalization in a proof assistant.
- No human review outside this project.
- An exploratory checker written in the lab is not offered as evidence: an independent
  review found that it can accept a false certificate (its allowance for summation error
  over many inside rectangles is too small).

## Lineage and credit

- The measure, its format and the certificate method are Hiroaki Hosono's (wand125),
  after Tokoharu's rectangle-density certificates and verifier.
- Declared finer nets: jlevy/squares#366. The dilation idea is the one the registry used
  at n = 11 (T-022, T-024); for a density certificate it needs the re-check above.
- `sqverify-fast` is jlevy/squares' clean-room verifier.
- New here: the dilation of Hosono's n = 94 measure to 1993/200 on a finer net, and its
  verification.

## AI assistance

The search, the certificate, the verification runs and this write-up were produced by AI
agents (Claude, Anthropic; and an OpenAI Codex agent for the second check) in Doğa Özden's
research lab, under his direction.
