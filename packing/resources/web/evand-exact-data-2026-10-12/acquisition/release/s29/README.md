# s(29): minimal polynomial (degree 7213): data

From the release `exact-data-2026-10-12` of https://github.com/evand/square-packing.  Method, verification table and
caveats: `search/exact/homotopy/N29.md` in the repo.  Scripts are in `search/exact/homotopy/` and run under
`search/exact/env.sh` (python-flint 0.9.0, mpmath 1.3.0).

s(29) = 5.9338334626769291896894606163520191384338341810778869746388259150802... is a root of the irreducible integer
polynomial p below, so p is its minimal polynomial.

| file | contents |
|---|---|
| `n29_poly_q4.json` | p: `coeffs_ascending` (7213 + 1 integers; leading coefficient 325 digits, height 5074 digits), plus metadata |
| `n29_param_t{1..5}.json` | shape-lemma parametrization of the class angles: t_i = g_i(S) / (den_i p'(S)) |
| `n29_system.jl` | the exported system: 5 consistency polynomials F(t1..t5), S = Sn/Sd, the 152-row contact system (from `export_system.py 29`) |
| `n29_krawczyk.json` | Krawczyk box: F has exactly one zero t* in tstar +- 1e-50 |
| `n29_S0.txt` | the record's S to ~40,000 digits (centre of the `link.py` interval) |
| `n29_q4_ref133k.txt` | the 4 roots missed by the homotopy and recovered algebraically (`recover_k.py`), 40k digits |
| `n29_*.log` | the original verification logs (irred, link, vmod = verify_mod, cmod = contacts_mod) |

## Replay (from `search/exact/homotopy/`, with D = this directory)

    P="$D/n29_param_t1.json $D/n29_param_t2.json $D/n29_param_t3.json $D/n29_param_t4.json $D/n29_param_t5.json"
    ../env.sh python3 irred.py        $D/n29_poly_q4.json 12                                  # rigorous: irreducible (degree patterns mod 12 primes)
    ../env.sh python3 krawczyk.py     $D/n29_system.jl 1e-50 OUT.json                         # rigorous: unique zero t* of F in the box
    PREC=220000 ../env.sh python3 link.py $D/n29_system.jl $D/n29_poly_q4.json $D/n29_krawczyk.json $D/n29_S0.txt $P   # rigorous: a root of p maps into the box
    ../env.sh python3 verify_mod.py   $D/n29_system.jl $D/n29_poly_q4.json $P NPRIMES SEED    # Monte Carlo: F(tau) = 0, Sn = x Sd in Q[x]/(p)
    ../env.sh python3 contacts_mod.py $D/n29_system.jl $D/n29_poly_q4.json $P NPRIMES SEED    # Monte Carlo: full contact system consistent, S = x

`link.py` needs `PREC=220000` (bits); at its default 140000 the sign test reports `?` and the check prints NOT LINKED.
The original run used 50 primes for `verify_mod.py` (about 2 min per prime) and 21 for `contacts_mod.py` (about 18 s
per prime).

## Caveats

* Two steps are Monte Carlo: identities in Q[x]/(p) are checked modulo random 62-bit primes (see N29.md for the
  error bound).  A deterministic check was not attempted.
* The packing's non-overlap inequalities are not checked at the exact point.  The record's rational certificate
  covers validity at S slightly above s(29).
* The 7209 homotopy roots at 40k digits (1.8 GB) that `param.py` used to build the parametrization are not included.
  The identities above are what certify it.  Ask if you want them.
