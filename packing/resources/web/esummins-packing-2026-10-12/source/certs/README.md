# certs/ — machine-checkable certificates and their verifiers

Everything here is meant to be re-checkable by anyone with Python 3 (stdlib only for the exact
paths; numpy is optional and only accelerates shortlists).  Nothing in this directory is a proof
until the corresponding verifier prints PASS; the verifiers are the trusted code, the JSON files are
just data.  Lean re-implementations live in `lean/PackingCert/` (see `attempts/A06-lean-setup/notes.md`).

## 1. Upper-bound certificates: `verify_certificate.py` (A03)

Claim: `s(n) <= side` — n closed unit squares placed inside `[0,side]^2` with pairwise disjoint
interiors (strict separating-axis test on the corners, exact rational arithmetic).

Two JSON formats, auto-detected:

```
(A) centre/tilt      {"format": "centre-tilt", "side": "p/q",
                      "squares": [{"cx": "p/q", "cy": "p/q", "t": "p/q"}, ...]}     t = tan(theta/2)
(B) integer corners  {"format": "integer-corners", "D": <int>, "side_D": <int>,
                      "squares": [{"corners": [[x0,y0],[x1,y1],[x2,y2],[x3,y3]]}, ...]}  coords = int/D
```

Run:  `python certs/verify_certificate.py certs/trump11_certificate_int.json`  (exit 0 = PASS).
Files: `trump11_certificate*.json` (Trump's 11-square packing, side 969271/250000 = 3.877084 and the
tight variant 3877083591023/10^12).

## 2. Lower-bound certificates

Both lower-bound verifiers decide the statement

> every CLOSED unit square Q contained in the closed square `[0,s]^2` (any orientation) meets the
> point set / has measure `mu(Q) >= 1`,

by exact branch-and-bound over `(t, cx, cy)`, `t = tan(theta/2) in [0,1]` (theta in [0,pi/2] suffices
by the 90-degree symmetry of the square), `cos = (1-t^2)/(1+t^2)`, `sin = 2t/(1+t^2)`.
Consequence (the only mathematics outside the program): if the point set has `n-1` points, or the
measure has total mass `< n`, then `n` pairwise-disjoint closed unit squares cannot fit in `[0,s]^2`,
hence `s(n) >= s` (scale a hypothetical packing of side `s' < s` up to side `s`, shrink each square
about its centre back to a unit square: the closed squares become disjoint and each carries mass >= 1).

### 2a. Point sets: `verify_unavoidable.py` (A05)

```
{"s0": "p/q", "points": [["p/q","p/q"], ...], "claim": "...", ...}
python certs/verify_unavoidable.py certs/unavoidable_10pt_3.7416.json [--minsize 1/10000000]
```
File: `unavoidable_10pt_3.7416.json` — 10 points unavoidable at s0 = 1870797/500000, i.e. s(11) >= 3.741594
(weaker than Stromquist's 3.7889, but machine-checked; also checked by `verify_measure.py` and in Lean).

### 2b. Measures ("fractional unavoidable sets"): `verify_measure.py` (A08)

Format `measure-certificate-v1` (frozen by A07, 2026-08-16); all numbers are exact rational strings
(`"19/5"`, `"3.8"`, `"0.40229885"` — decimals are read exactly; JSON floats are rejected):

```
{"format": "measure-certificate-v1",
 "n": 11,                          claim s(n) >= s          (optional, default 11)
 "s": "19/5",
 "atoms":   [["x","y"], ...],      all atoms (D4 images expanded)
 "weights": ["p/q", ...],          same length, >= 0
 "total":   "p/q",                 optional; must equal sum(weights) (< n)
 "symmetry": "D4",                 optional; if present the listed atoms are orbit representatives
                                   and are expanded to their distinct D4 images (same weight each)
 "provenance": {...}}              free-form
```

Run:
```
python certs/verify_measure.py cert.json                    # depth 48, one process
python certs/verify_measure.py cert.json --jobs 4 --report  # 4 processes, JSON report next to cert
python certs/verify_measure.py cert.json --strict-margin 1/1000   # require mass >= 1 + 1/1000 on every box
python certs/verify_measure.py cert.json --scale-weights 1.000001 # multiply weights (absorb LP rounding)
python certs/verify_measure.py --selftest                   # random cross-check int core vs Fraction core
```
Output: `PASS`/`FAIL`, total mass, box counts, depth histogram, runtime; on FAIL a JSON of witness
boxes (`<cert>.witnesses.json` or `--witness-file`), each with an admissible sample placement
`(t, cx, cy)` and its EXACT mass; kind = `hole` (exact mass < 1 at that placement: a rigorous
counterexample), `tight` (mass >= 1 only thanks to atoms exactly on the boundary of Q — a tangency no
box method can certify; the certificate must be perturbed), or `undecided` (not certified at this depth).
Exit codes: 0 PASS, 1 FAIL, 2 malformed / total >= n.

Notes: the accept decision is exact integer arithmetic (lengths scaled by `den(s) * 2^(depth+2)`,
`t` by `2^(depth+1)`); numpy is used only to shortlist atoms.  Boxes are clipped to the admissible
centre region `[w_min/2, s - w_min/2]` (rounded outward) before testing.  Certificates must be
*robust*: at every placement, atoms at positive distance from the boundary of Q must already reach
mass 1 (see `attempts/A08-measure-verify/notes.md` for why and for the cost model).

Files (A07, all PASS `verify_measure.py`): `measure_certificate_3.80.json` (s = 19/5, 1069 atoms, total
10.801639), `measure_certificate_3.81.json` (s = 381/100, 980 atoms, total 10.9852), `measure_certificate_3.82.json`
(s = 191/50, 1769 atoms, total 10.985474)  ==>  s(11) >= 3.82.  Producer: `attempts/A07-lp-dual/` (LP with
row+column generation; see its notes.md for the construction recipe and the verifier witness -> LP row loop).

## 3. Algebraic-identity certificates: `verify_sturm.py` (A63), `verify_cidl.py` (A69)

`verify_sturm.py certs/octic_root_isolation.json` — exact Sturm root isolation for the Trump
octic: exactly two real roots, exactly one in `[3.877083, 3.877084]` (the second), and the
all-positive Taylor shift at the left endpoint (the calculus-free monotonicity used by Lean's
`shat_spec`).  Stdlib fractions only.

`verify_cidl.py certs/cidl_identity.json` — the (c-idl) saturated ideal-membership certificate
closing `s-hat_A22 = s-hat_octic` (TopLevel axiom `shatA22_eq_shat`; construction and composition
in `docs/proofs/attainment_ub.md` §7).  The checker itself REBUILDS the 13 reduced A22 contact
generators from the A22 corner/edge conventions, then verifies exactly over Q: the canonical
octic, the polynomial identity `e(t)*Delta(t)^8*octic(S) = sum_j q_j(t,S)*G_j`, and the Sturm
sign gate (`e`, `Delta` root-free on `[3/10, 2/5]`, which contains `t-hat = tan(theta-hat/2)`).
PASS in 0.7 s.  Corruption gates (must FAIL): `--corrupt qcoeff|e|rowspec|octic`.
Exit codes: 0 PASS, 1 FAIL, 2 malformed.  Producer: `attempts/A69-cidl-identity/assemble.py`
(exact linear elimination; untrusted search — only the shipped identity matters).
