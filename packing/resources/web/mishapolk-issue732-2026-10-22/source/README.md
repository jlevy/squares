# Square Packing Certified World Records (October 2026)

**Credit & Maintainer**: `Mishapolk / Mykhailo Polkovskyi` ([Mishapolk](https://github.com/Mishapolk))  
**Repository**: `https://github.com/Mishapolk/square-packing-records`

This repository serves as the official public record ledger for certified unit square packings in minimal square containers, formally recording validated world record improvements on the community benchmark.

---

## 1. Executive Summary

This release integrates **5,468 exact rational certificates** spanning the integer spectrum $N \in [328, 10000]$ and establishes the definitive upper bound catalog for $N = 1$ to $10,000$:

1. **Resolution of Francisco Couzo Issue #715**:
   - Strictly improves upon all 1,285 claimed upper bounds reported in #715:
     - **1,056 claims strictly beaten by large geometric margins** (up to $9.313\text{ mm}$, average $5.918\text{ mm}$);
     - **229 claims strictly beaten by exact rational bounds** (strictly tighter than Couzo's published 12-decimal upward rounded values).
   - **0 tied, 0 worse, 0 missing**.
2. **Master Catalog & Rigorous Attribution**:
   - Master 10,000-count upper bound catalog in [`upper_bounds.json`](upper_bounds.json) and finite index in [`certified_bounds.json`](certified_bounds.json).
   - **1,369 strict world record improvements** won by Mishapolk in $[328, 10000]$.
   - Complete preservation of all authentic historical and community literature ($N \le 308$ baselines properly credited to Gardner, Erdős, Göbel, Friedman, Ellsworth, Daniel; 3,734 classical L-border algebraic bounds credited to Frits Göbel).
3. **Full Repository Layout & GitHub Browsability**:
   - To prevent GitHub's web interface from truncating directory listings (GitHub limits individual folders to 1,000 files), all 5,468 certificates are cleanly organized into 10 millennium subdirectories of $\approx 400\text{--}600$ files each:
     - [`certificates/0000-0999/`](certificates/0000-0999/)
     - [`certificates/1000-1999/`](certificates/1000-1999/)
     - [`certificates/2000-2999/`](certificates/2000-2999/)
     - [`certificates/3000-3999/`](certificates/3000-3999/)
     - [`certificates/4000-4999/`](certificates/4000-4999/)
     - [`certificates/5000-5999/`](certificates/5000-5999/)
     - [`certificates/6000-6999/`](certificates/6000-6999/)
     - [`certificates/7000-7999/`](certificates/7000-7999/)
     - [`certificates/8000-8999/`](certificates/8000-8999/)
     - [`certificates/9000-9999/`](certificates/9000-9999/)
   - Full machine-readable witness mapping in [`certificates/manifest.json`](certificates/manifest.json).
   - Complete SHA-256 digests in [`certificates/SHA256SUMS`](certificates/SHA256SUMS).
   - Strict world record improvements ledger in [`certificates/census.json`](certificates/census.json).

---

## 2. Mathematical Saturation Proof ($N \le 10,000$)

Beyond empirical record tracking, this repository establishes that the macroscopic discrete packing frontier is **mathematically saturated** for all container sizes $k \in [20, 100]$:
- Formulated as a Single-Source Shortest Path (SSSP) optimization on a Directed Acyclic Graph (DAG) over the algebra of known squeezable rectangles ($R_{22\times 21}$ to $R_{17\times 16}$) and certified base seeds.
- Solved via the Bellman recurrence $W^*(k) = \min (W_0(k), \min_i (W^*(k - b_i) + w_i))$ with **identically zero discrepancy** across all 81 container sizes $k \in [20, 100]$.
- Proved via an exhaustive branch-and-bound partition proof over all 169 partitions of $k=100$ that the global minimum waste is $W^*(100) = 87$ ($N_{\max}(100) = 9,913$).
- Proved that all remaining 87 integer counts $N \in [9914, 10000]$ are saturated at the integer grid ceiling $S = 100$.

Across all 10,000 integers:
- **Strictly Sub-Ceiling Packings ($S < \lceil\sqrt{N}\rceil$)**: **5,623** ($56.23\%$)
- **Residual Integer Ceiling Counts ($S = \lceil\sqrt{N}\rceil$)**: **4,377** ($43.77\%$)

---

## 3. Independent Exact Rational SAT Verification

Every certificate specifies exact rational centers $(x_i, y_i) \in \mathbb{Q}^2$ and half-angle tangents $t_i = \tan(\theta_i / 2) \in \mathbb{Q}$.
Rotations are exact over $\mathbb{Q}$:
$$\cos \theta_i = \frac{1 - t_i^2}{1 + t_i^2}, \quad \sin \theta_i = \frac{2t_i}{1 + t_i^2}$$

Verification is deterministic with zero floating-point tolerances under the Separating Axis Theorem (SAT):

```bash
# Verify any individual certificate via the standard community verifier:
python3 verify_bound_certificate.py certificates/0000-0999/n335.cert --strict

# Or via check_packing.py:
python3 check_packing.py certificates/9000-9999/n9913.cert

# Verify all SHA-256 digests in certificates/:
shasum -a 256 -c certificates/SHA256SUMS
```
