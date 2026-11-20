# s(228) ≤ 15.596043116632

**This improves the published registry packing but does NOT beat the Kaggle per-puzzle leaderboard side-only entry, and it is not our own search result.** It is a public Kaggle packing by **jazivxt**, converted to exact rationals and checked. The leaderboard lists 15.596043116631669919627353… for team Nevska (submitted 2026-11-08 11:50:15 UTC; leaderboard notebook version 37, read 2026-11-18). Our exact side is 15.59604311663176650670114…, larger by 9.66e-14. That entry gives no packing; we cannot say whether it is the same arrangement, and nothing here links it to this one.

## Credit

- **The packing: jazivxt** (Kaggle user; notebook *Boxed In Sub*, https://www.kaggle.com/code/jazivxt/boxed-in-sub?scriptVersionId=370961355, run 370961355; dataset *Boxed In* v63, https://www.kaggle.com/datasets/jazivxt/boxed-in/versions/63; Apache 2.0 as declared on the dataset, text in `source/LICENSE-jazivxt-Apache-2.0`). The dataset describes crowdsourced coordinates and the notebook gives no per-count credit, so **the original finder of this arrangement is unresolved**. The notebook's overview credits ChatGPT and Codex as AI assistance.
- **Corroboration: Sergio Fernández Rubio (GeiserX)**, https://github.com/GeiserX/squares-in-squares, whose round-30 table credits jazivxt/boxed-in-sub for n = 228 (CC BY 4.0 for layouts; `source/NOTICE`, `source/LICENSE-CC-BY-4.0.txt`, `source/CITATION.cff` kept). His rounded 228 layout is the same packing to 2.3e-10 and was used only as a cross-check.
- **Exact rational conversion, checks and this registration: Doğa Özden** (AI-assisted: his OpenAI Codex Sol lab did the conversion and checks, and his AI agent posts this on his behalf). We claim no discovery.
- **Current registry record: Roberto Ono, with Claude** (jlevy/squares #984, T-301), after Francisco Couzo (improved by PingYou Ltd).

## Certificate

`n-228-candidate.yaml` is a packing.squares:Witness/v2 (centre + rational half-angle basis, rational scalars, 228 unit squares). Its `side` is the exact rational 389901077915794162667528670804703057/25000000000000000000000000000000000; rounded **up** at 12 decimals it is 15.596043116632. SHA-256 of the YAML: `1b816e2e9302ad58ca2d5bb5882f4f98b2c8fb4f9e5746a8ed3f823cfd4a3387`. `n228-witness.json` is the same witness as JSON. `source/hit-228.txt` is jazivxt's published decimal slice for n = 228 (first line `228 side`, then one row of three numbers per square; SHA-256 of the 228-row slice of the notebook output is in `PROVENANCE.json`).

Registry record at jlevy/squares main @1015fc17 (packing/frontier/n-228.md): 15.5960431209207917, Roberto Ono. Exact Fraction arithmetic: our side is smaller by 4.28902514e-09 (relative 2.75e-10). Public Kaggle numbers we compared (all fetched 2026-11-18): jazivxt's own decimal 15.59604311663169367 (ours is 7.28e-14 larger, the cost of the clearance below); GeiserX 15.5960431169528 and the Squares-Feeder aggregate 15.596043116996643 (ours smaller by 3.2e-10 and 3.6e-10).

## Exact conversion and checks

1. jazivxt's published decimal centres and orientations were converted to rational half-angle form (centre, t = tan(θ/2)), so every cos θ and sin θ is rational. One uniform radial clearance factor 2500000000000011391221/2500000000000000000000 (1 + 4.6e-18) about the origin was then applied so that all pairs have strictly positive clearance and the packing fits the exact side; nothing else was changed. Provenance and the factor are in `PROVENANCE.json` and `checks/source-exact-as-produced.json` (the unmodified conversion output; the squares are identical to the YAML's).
2. `packing-witness verify` of jlevy/squares @1015fc17, unmodified, on `n-228-candidate.yaml`: **VERIFIED**, exact-algebraic over Q, 25,878 pairs tested, minimum wall clearance 0, minimum pair gap 7419656657104237729564618131537107953/204583288553752924280716250000000000000000000000000000000000 (3.6e-23). Output in `verify-228.txt`, `checks/registry-verify.json`.
3. `verifier/sqcheck.py`, our checker written separately from the registry's code: **VALID exact-rational**, certified side ≤15.596043116631767 (`sqcheck-228.txt`, `checks/`).
4. A second, independently written exact Fraction separating-axis checker (checks/hit-228-independent.json, 151 near pairs) agrees: VALID, same exact side, on the same squares (SHA-256 of that file's input `c149799d…`).
The checkers share only the definitions of unit square, wall and non-overlap. No local-optimality, rigidity or proof-assistant check was done.

## Relation to the registry packing

Matched up to the square's eight symmetries, 86 of 228 centres move by more than 0.001 relative to Roberto Ono's packing (7 by more than 0.05; largest move 0.238); 2 squares retilt by more than 1 degree (largest 1.96); ours has 54 tilted squares, the registry packing 55. So this is a close relative of the registry arrangement. We have no information on which came first or whether one derived from the other. See `records/n-228-candidate-diff.png`.

Rerun in a clone of jlevy/squares @1015fc17:

```sh
cd squares/packing
uv run --frozen --no-dev --with sympy --with mpmath packing-witness verify /absolute/path/n-228-candidate.yaml
python3 /absolute/path/verifier/sqcheck.py /absolute/path/n-228-candidate.yaml
```

sqcheck needs mpmath, sympy and PyYAML. Our certificate files and text: CC BY 4.0 (`LICENSE.md`); code: MIT. The coordinates remain jazivxt's, under Apache 2.0, with the attribution above.
