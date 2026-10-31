# Registration Request: 3 Verified Literature World Records (Category A)

**Credit name.** Mishapolk (Mikhail Polk) & Antigravity Autonomous Research Lab.  
GitHub: [Mishapolk](https://github.com/Mishapolk)  
Repository: [Mishapolk/square-packing-records](https://github.com/Mishapolk/square-packing-records)  
Target Repository: [`jlevy/squares`](https://github.com/jlevy/squares)  
Date: October 30, 2026  

---

## 1. Executive Summary & Verified Records

We report **3 new verified world record upper bounds** for unit square packing ($N \in \{130, 182, 268\}$), certified by exact rational arithmetic with strictly positive separation and wall margins. Every certificate has been strictly verified with arbitrary-precision rational arithmetic using Evan Daniel's separating-axis verifier (`verify_bound_certificate.py --strict`).

| $N$ | Certified Side $S$ (rounded up 12 dec) | Exact Rational Fraction | Literature / Official Register | Improvement vs Literature | Secondary Literature / Claims |
|:---:|:---:|:---|:---:|:---:|:---|
| **130** | `11.902430645983` | `5951215322991132879306459820277 / 500000000000000000000000000000` | `11.904483032516` (PR #574) | **$-2.052387\text{ mm}$** ($-2.052 \times 10^{-3}$) | Beats Francisco Couzo Issue #843 (`11.902430645985`) by **$-2.08\text{ pm}$** |
| **182** | `13.970916436215` | `6985458218107409544582181073397 / 500000000000000000000000000000` | `13.974090713122` (PingYou PR #574) | **$-3.174277\text{ mm}$** ($-3.174 \times 10^{-3}$) | Beats Kaggle leaderboard (`13.972761347065`) by **$-1.845\text{ mm}$** |
| **268** | `16.874361715871` | `527323803620963369940181046851 / 31250000000000000000000000000` | `16.874361715874` (Couzo verified) | **$-2.997641\text{ pm}$** ($-2.998 \times 10^{-12}$) | Beats Mishapolk Issue #593 by **$-4.453\text{ mm}$**, beats Kaggle by **$-1.20\text{ pm}$** |

---

## 2. Certificate Details and Machine Clearances

Every certificate strictly satisfies the open container / closed square disjointness criteria with strictly positive clearances:

### $N = 130$
- **Certificate Path:** `certificates/0000-0999/n130.cert`
- **Exact Fraction:** `5951215322991132879306459820277 / 500000000000000000000000000000`
- **Decimal:** `11.90243064598226574...`
- **Min Wall Clearance:** $+9.664 \times 10^{-15} > 0$
- **Min Pair Separation:** $+1.823 \times 10^{-14} > 0$
- **SHA-256:** `1e00cd74ccf3495b69d6d84f9c130432b63cebd447209d0dbeaf17077a669be7`

### $N = 182$
- **Certificate Path:** `certificates/0000-0999/n182.cert`
- **Exact Fraction:** `6985458218107409544582181073397 / 500000000000000000000000000000`
- **Decimal:** `13.97091643621481971...`
- **Min Wall Clearance:** $+5.000 \times 10^{-15} > 0$
- **Min Pair Separation:** $+9.244 \times 10^{-15} > 0$
- **SHA-256:** `8ece3310a7d6a632b5e6955651b85bd0eb3707cae64d02478b39f8dab9d3500f`

### $N = 268$
- **Certificate Path:** `certificates/0000-0999/n268.cert`
- **Exact Fraction:** `527323803620963369940181046851 / 31250000000000000000000000000`
- **Decimal:** `16.87436171587082611...`
- **Min Wall Clearance:** $+2.938 \times 10^{-14} > 0$
- **Min Pair Separation:** $+5.261 \times 10^{-14} > 0$
- **SHA-256:** `24d2892ae2d1c1b0f425df823244ef27607970d7faaaad1fe5b4615eac9e9ac5`

---

## 3. Independent Verification Instructions

To verify all 3 certificates with the official exact-arithmetic verifier:
```bash
git clone https://github.com/Mishapolk/square-packing-records.git
cd square-packing-records
python3 verify_bound_certificate.py --strict certificates/0000-0999/n130.cert
python3 verify_bound_certificate.py --strict certificates/0000-0999/n182.cert
python3 verify_bound_certificate.py --strict certificates/0000-0999/n268.cert
```
All commands output `{"valid": true, "strict_valid": true, "wall_margin_sign": 1, "pair_margin_sign": 1, "accepted": true}`.
