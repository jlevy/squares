# Registration Request: 11 Verified Exact Refinement Packings (Category B)

**Credit name.** Mishapolk (Mikhail Polk) & Antigravity Autonomous Research Lab.  
GitHub: [Mishapolk](https://github.com/Mishapolk)  
Repository: [Mishapolk/square-packing-records](https://github.com/Mishapolk/square-packing-records)  
Target Repository: [`jlevy/squares`](https://github.com/jlevy/squares)  
Date: October 30, 2026  

---

## 1. Executive Summary & Claims

We report **11 exact, verified rational certificates** refining upper bounds on `jlevy/squares`. Every certificate has been strictly verified with arbitrary-precision rational arithmetic via `verify_bound_certificate.py --strict` to possess strictly positive machine clearances ($\text{min\_wall} > 0, \text{min\_gap} > 0$) with zero micro-overlaps.

| $N$ | New Upper Bound $S_{\text{cert}}$ | Exact Rational Fraction | Literature / Standing Verified Bound | Improvement ($\Delta S$) | Machine Clearances (Wall / Gap) |
|:---:|:---:|:---|:---:|:---:|:---:|
| **105** | `10.789303783743` | `674331486483935962030222957609 / 62500000000000000000000000000` | `10.789303783743` | $-1.0000 \times 10^{-21}$ | `4.00e-21` / `1.00e-20` |
| **146** | `12.583782190152` | `12583782190151860342291508597077 / 1000000000000000000000000000000` | `12.583782190152` | $-1.0000 \times 10^{-21}$ | `4.00e-21` / `1.00e-20` |
| **156** | `12.979165853835` | `648958292691713822691804519015415761935308555406679 / 50000000000000000000000000000000000000000000000000` | `12.979165853847` | $-1.2980 \times 10^{-11}$ | `4.00e-41` / `1.00e-40` |
| **204** | `14.808642830514` | `14808642830513184650000000000001 / 1000000000000000000000000000000` | `14.808642830517` | $-3.7188 \times 10^{-12}$ | `5.00e-15` / `8.65e-15` |
| **211** | `14.993549626300` | `14993549626299421038935530460881 / 1000000000000000000000000000000` | `14.993549626300` | $-1.0000 \times 10^{-21}$ | `4.00e-21` / `1.00e-20` |
| **229** | `15.650161513877` | `15650161513876431064008548865321 / 1000000000000000000000000000000` | `15.650161513877` | $-4.5970 \times 10^{-13}$ | `4.00e-21` / `1.00e-20` |
| **241** | `15.987117095151` | `1598711709514999999999999999999 / 100000000000000000000000000000` | `15.987117095151` | $-1.0000 \times 10^{-21}$ | `4.00e-21` / `1.00e-20` |
| **260** | `16.645753250520` | `4161438312629953048686324163329 / 250000000000000000000000000000` | `16.645753250537` | $-1.6690 \times 10^{-11}$ | `4.00e-21` / `1.00e-20` |
| **299** | `17.803695435316` | `2225461929414467349619294144451 / 125000000000000000000000000000` | `17.822875655532` | **$-19.180\text{ mm}$** vs PingYou<br>**$-17.26\text{ pm}$** vs Daniel #824 | `1.06e-13` / `2.12e-13` |
| **304** | `17.926898900367` | `8963449450183382079945018248601 / 500000000000000000000000000000` | `17.929427758093` | **$-2.5289\text{ mm}$** vs literature | `1.52e-13` / `3.11e-13` |
| **308** | `17.997149121271` | `3599429824254181747030432150463 / 200000000000000000000000000000` | `17.997149121289` | $-1.7998 \times 10^{-11}$ | `4.00e-21` / `1.00e-20` |

---

## 2. Independent Verification Instructions

Each packing is verified using the official separating-axis verifier:
```bash
git clone https://github.com/Mishapolk/square-packing-records.git
cd square-packing-records
python3 verify_bound_certificate.py --strict certificates/0000-0999/n105.cert
python3 verify_bound_certificate.py --strict certificates/0000-0999/n146.cert
python3 verify_bound_certificate.py --strict certificates/0000-0999/n156.cert
python3 verify_bound_certificate.py --strict certificates/0000-0999/n204.cert
python3 verify_bound_certificate.py --strict certificates/0000-0999/n211.cert
python3 verify_bound_certificate.py --strict certificates/0000-0999/n229.cert
python3 verify_bound_certificate.py --strict certificates/0000-0999/n241.cert
python3 verify_bound_certificate.py --strict certificates/0000-0999/n260.cert
python3 verify_bound_certificate.py --strict certificates/0000-0999/n299.cert
python3 verify_bound_certificate.py --strict certificates/0000-0999/n304.cert
python3 verify_bound_certificate.py --strict certificates/0000-0999/n308.cert
```
All certificates yield `{"valid": true, "strict_valid": true, "wall_margin_sign": 1, "pair_margin_sign": 1, "accepted": true}`.
