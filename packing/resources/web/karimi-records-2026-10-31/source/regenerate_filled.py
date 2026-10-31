#!/usr/bin/env python3
"""Rebuild the exact certificates of filled_records.csv.

    python3 regenerate_filled.py            # all rows -> certificates_filled/n<N>.cert
    python3 regenerate_filled.py 9946 9945  # only these n
Then check, e.g. with the register's verifier:
    python3 verify_bound_certificate.py certificates_filled/*.cert
"""
import csv, os, sys
from fractions import Fraction as F
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from filled_ends import build, write_cert

only = {int(a) for a in sys.argv[1:]}
here = os.path.dirname(os.path.abspath(__file__))
os.makedirs(os.path.join(here, 'certificates_filled'), exist_ok=True)
for r in csv.DictReader(open(os.path.join(here, 'filled_records.csv'))):
    n, K = int(r['n']), int(r['K'])
    if only and n not in only:
        continue
    S, sq = build(K, int(r['bV']), F(r['tV']), F(r['yV']),
                  int(r['bH']), F(r['tH']), F(r['yH']), n)
    assert S == F(r['side_exact'])
    write_cert(os.path.join(here, 'certificates_filled', f'n{n}.cert'), K, n, S, sq,
               f"filled-end L packing (Ryu L-frame; Daniel axis-layer end fill; "
               f"independent bands and search: Mohsen Karimi) K={K} "
               f"bV={r['bV']} tV={r['tV']} bH={r['bH']} tH={r['tH']}")
    print('wrote', n)
