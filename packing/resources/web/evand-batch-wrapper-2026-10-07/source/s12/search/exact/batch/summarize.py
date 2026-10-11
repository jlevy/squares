#!/usr/bin/env python3
"""Batch summary: for every n in candidates.json, the final certified exactsolve report (if any), both independent
certificate checks, KKT classification, and the gap to the current register value.

  summarize.py            -> results.md (table) + results_final.json; certificates copied to certs/
KKT local min = multipliers lambda >= 0 exist at the exact point (equilibrium residual 0), second order PSD/PD, jammed in every
corner-corner branch.  'bound only' = the certificate is valid (an upper bound) but the point is not certified KKT.
"""
import json, os, shutil, subprocess, sys
from fractions import Fraction

HERE = os.path.dirname(os.path.abspath(__file__))
EX = os.path.dirname(HERE)


def final_report(n):
    d = os.path.join(HERE, 'work', f'n-{n}')
    best = None
    for name in ('witness', 'polished'):
        p = os.path.join(d, name + '.json')
        if os.path.exists(p):
            r = json.load(open(p))
            if r.get('cert_valid'):
                if best is None or Fraction(r['S_cert']) < Fraction(best[1]['S_cert']):
                    best = (name, r)
    return best


def check(cert):
    a = subprocess.run([sys.executable, os.path.join(EX, 'verify_cert.py'), cert], capture_output=True, text=True)
    b = subprocess.run([sys.executable, os.path.join(EX, 'verify_cert2.py'), cert], capture_output=True, text=True)
    return (a.stdout.splitlines()[-1].strip().startswith('VALID:') if a.stdout else False, b.returncode == 0)


if __name__ == '__main__':
    cf = sys.argv[1] if len(sys.argv) > 1 else 'candidates_all.json'
    tag = ''
    os.makedirs(os.path.join(HERE, 'inputs'), exist_ok=True)
    C = json.load(open(os.path.join(HERE, cf)))
    os.makedirs(os.path.join(HERE, 'certs'), exist_ok=True)
    rows = []
    for c in C:
        n, reg = c['n'], c['register']
        fr = final_report(n)
        if fr is None:
            rows.append(dict(n=n, register=reg, by=c['by'], status='not certified'))
            continue
        name, r = fr
        cert = os.path.join(HERE, 'work', f'n-{n}', name + '.cert')
        v1, v2 = check(cert)
        dst = os.path.join(HERE, 'certs', f'n-{n}.cert')
        shutil.copy(cert, dst)
        shutil.copy(os.path.join(HERE, 'work', f'n-{n}', name + '.txt'), os.path.join(HERE, 'inputs', f'n-{n}.txt'))
        so = (r.get('second_order') or {}).get('status', '')
        lam = r.get('lambda_A_maxmin')
        kkt = (lam is not None and lam > 0 and (r.get('equilibrium_residual_exact') or 0) < 1e-30
               and so.startswith(('local minimum', 'PD', 'rigid')) and (r.get('vv_milp_dS') or 0) > -1e-9)
        rows.append(dict(n=n, register=reg, by=c['by'], status='KKT local min' if kkt else 'bound only',
                         S_exact=r['S_exact'][:40], S_cert=r['S_cert_decimal'], S_cert_fraction=r['S_cert'],
                         delta=float(Fraction(r['S_cert']) - Fraction(reg)), lam=lam, second=so, from_=name,
                         forced=r.get('forced_pairs'), verify1=v1, verify2=v2, free=r.get('free_squares'),
                         input='register witness' if name == 'witness' else 'witness polished by SLP (local optimizer)'))
    json.dump(rows, open(os.path.join(HERE, 'results.json'), 'w'), indent=1)
    L = ['| n | register (found by) | certified S\' (20 digits) | S\' − register | status | min λ | verifiers | input |', '|---|---|---|---|---|---|---|---|']
    for r in rows:
        by = ', '.join(r['by'] or [])
        if r['status'] == 'not certified':
            L.append(f"| {r['n']} | {r['register']} ({by}) | — | — | not certified | | |")
            continue
        lam = f"{r['lam']:.1e}" if r['lam'] is not None else '—'
        L.append(f"| {r['n']} | {r['register']} ({by}) | {r['S_cert'][:22]} | {r['delta']:+.2e} | {r['status']} | {lam} | "
                 f"{'✓' if r['verify1'] else '✗'}{'✓' if r['verify2'] else '✗'} | {'W' if r['input'].startswith('register') else 'P'} |")
    open(os.path.join(HERE, 'results.md'), 'w').write('\n'.join(L) + '\n')
    k = sum(r['status'] == 'KKT local min' for r in rows)
    b = sum(r['status'] == 'bound only' for r in rows)
    below = sum(1 for r in rows if r.get('delta', 0) < 0 and r['verify1'] and r['verify2'])
    cov = 0
    for r in rows:
        if r['n'] == cov + 1 and r['status'] != 'not certified' and r['verify1'] and r['verify2']:
            cov = r['n']
        elif r['n'] > cov:
            break
    kcov = 0
    for r in rows:
        if r['n'] == kcov + 1 and r['status'] == 'KKT local min' and r['verify1'] and r['verify2']:
            kcov = r['n']
        elif r['n'] > kcov:
            break
    print(f'coverage: every n <= {cov} certified (both verifiers); every n <= {kcov} a certified KKT local minimum')
    print(f'{len(rows)} records: {k} KKT local min, {b} bound only, {len(rows) - k - b} not certified; '
          f'{below} certified below the register (both verifiers)')
