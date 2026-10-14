#!/usr/bin/env python3
"""Check the structure of all 34 families of the closed-form certificate.

Usage (from problems/closed-form):

    python3 structure/structure_all.py --assets DIR [--out receipts/structure.json]

DIR holds the release assets interval_<d0>_<d1>.tar.gz. For every interval in intervals.json the script

  1. extracts family.json and family_right.json from the asset and checks their SHA-256 against intervals.json;
  2. runs structure/validate_family.py on them (with --right, --line-alpha/--line-beta from intervals.json, and --open-left for
     intervals open on the left), which checks the family's format, nonnegativity and structure (SPEC.md §3, §2.3, §7.1 steps 1 and 2);
  3. checks that the certified line of intervals.json is exactly the line through the family's stored savings
     S_d0 and S_d1 (which validate_family recomputes and requires to be equal), i.e.
     α = (S_d1 − S_d0)/(d1 − d0) and β = S_d0 − α·d0. On each interval the family's saving is affine in δ
     (every corner piece of V has length 2 + δ − xl with xl ≤ 2 + d0), so the line equals S on the interval;
  4. checks that the four region bounds in intervals.json are the ones required by SPEC.md §2.3 (4):
     straddle [167/100, 251/100 + d1] × [0, 272/100], left [0, 167/100] × [0, 38/10],
     top [167/100, 251/100 + d1] × [272/100, 38/10], right [251/100, 38/10] × [0, 38/10] (shifted by δ).

It writes one result per interval to the output file and prints ALL STRUCTURE OK at the end if every check
passed. Python 3 standard library only.
"""
import argparse, hashlib, json, os, subprocess, sys, tarfile
from fractions import Fraction as Q

HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)


def sha(b): return hashlib.sha256(b).hexdigest()


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--assets', required=True); ap.add_argument('--work', default='structure-work')
    ap.add_argument('--out', default=os.path.join(ROOT, 'receipts', 'structure.json'))
    a = ap.parse_args()
    ivs = json.load(open(os.path.join(ROOT, 'intervals.json')))['intervals']
    os.makedirs(a.work, exist_ok=True); results = []; bad = 0
    for iv in ivs:
        tag = iv['asset'][:-len('.tar.gz')]; d = os.path.join(a.work, tag); os.makedirs(d, exist_ok=True)
        r = dict(index=iv['index'], interval=('(' if iv['open_left'] else '[') + f'{iv["d0"]}, {iv["d1"]}]', checks={})
        with tarfile.open(os.path.join(a.assets, iv['asset'])) as t:
            for name, want in (('family.json', iv['family_sha256']), ('family_right.json', iv['family_right_sha256'])):
                data = t.extractfile(f'{tag}/{name}').read()
                r['checks'][f'{name} sha256'] = sha(data) == want
                open(os.path.join(d, name), 'wb').write(data)
        cmd = [sys.executable, os.path.join(HERE, 'validate_family.py'), os.path.join(d, 'family.json'),
               '--right', os.path.join(d, 'family_right.json'), '--line-alpha=' + iv['certified_line']['alpha'], '--line-beta=' + iv['certified_line']['beta']]
        cmd += ['--open-left'] if iv['open_left'] else []
        p = subprocess.run(cmd, capture_output=True, text=True)
        lines = p.stdout.strip().splitlines()
        r['checks']['validate_family'] = bool(lines) and lines[-1] == 'VALIDATE OK' and p.returncode == 0
        r['validate_family_checks'] = sum(1 for l in lines if l.startswith('OK '))
        r['validate_family_failed'] = [l for l in lines if l.startswith('NG ')]
        f = json.load(open(os.path.join(d, 'family.json')), parse_float=str)
        d0, d1 = Q(iv['d0']), Q(iv['d1']); s0, s1 = Q(f['S_d0']), Q(f['S_d1'])
        al = (s1 - s0) / (d1 - d0); be = s0 - al * d0
        r['checks']['family interval'] = Q(f['d0']) == d0 and Q(f['d1']) == d1
        r['checks']['certified line = line through S_d0, S_d1'] = (Q(iv['certified_line']['alpha']) == al and Q(iv['certified_line']['beta']) == be)
        x1 = str(Q(251, 100) + d1)
        want = {'straddle': ['167/100', x1, '0', '272/100'], 'left': ['0', '167/100', '0', '38/10'],
                'top': ['167/100', x1, '272/100', '38/10'], 'right': ['251/100', '38/10', '0', '38/10']}
        r['checks']['region bounds'] = all([Q(v) for v in iv['regions'][g]['bounds']] == [Q(v) for v in want[g]] for g in want)
        r['checks']['regions use family/family_right'] = all(iv['regions'][g]['family'] == ('family_right.json' if g == 'right' else 'family.json') for g in want)
        r['ok'] = all(r['checks'].values()); bad += not r['ok']
        print(f'{tag}: {"OK" if r["ok"] else "FAILED " + str([k for k, v in r["checks"].items() if not v])} '
              f'({r["validate_family_checks"]} validate_family checks)', flush=True)
        results.append(r)
    json.dump(dict(schema='closed-form-structure/v1', tool='structure/validate_family.py via structure/structure_all.py',
                   validate_family_sha256=sha(open(os.path.join(HERE, 'validate_family.py'), 'rb').read()),
                   intervals=len(results), all_ok=not bad, results=results), open(a.out, 'w'), indent=1)
    print('ALL STRUCTURE OK' if not bad else f'{bad} interval(s) FAILED')
    sys.exit(1 if bad else 0)


if __name__ == '__main__':
    main()
