# finalize_v3.py -- merge the slices of every tier (cert_v3.py merge), choose the stated constants of Theorem 4E'
# (C_E rounded up to 3 decimals, C_i up to 2 decimals, k_i and a_i up to 2 significant digits), write them into
# tiers_v3_final.json, re-run the merge with the theorem checks, and print the tier tables of the paper.
# usage: python finalize_v3.py <dir with c_<tier>_<iz0>_<iz1>.json> [tiers...]
import json, sys, glob, os, subprocess, math, shutil
from mpmath import iv, mp
iv.prec = 120

d = sys.argv[1]
base = json.load(open('tiers_v3.json'))
tiers = sys.argv[2:] or list(base.keys())

def up(x, nd):            # round up to nd decimals (as a decimal string)
    q = 10 ** nd
    return ('%.' + str(nd) + 'f') % (math.ceil(x * q * (1 + 1e-15)) / q)

def up_sig(x, ns):        # round up to ns significant digits, as a string in e-notation
    e = math.floor(math.log10(x))
    m = math.ceil(x / 10 ** (e - ns + 1) * (1 + 1e-15))
    if m >= 10 ** ns:
        m //= 10; e += 1
    s = str(m)
    return '%s.%se%d' % (s[0], s[1:], e)

final = {}
rows = []
for t in tiers:
    files = sorted(glob.glob(os.path.join(d, 'c_%s_*.json' % t)))
    m = json.loads(subprocess.run(['python', 'cert_v3.py', 'merge', '--tier', t] + files, capture_output=True,
                                  text=True).stdout)
    P = base[t]
    # the slices must have been run with exactly the parameters of the tier table
    assert all(str(P[k]) == str(m[k]) for k in ('lb0', 'cy', 'cd', 'cr', 'aw', 'mu', 'parts')), t
    assert m['valid'], t
    ce = m['C_E_cert']
    CE = up(ce, 3)
    CEi = iv.mpf(CE)
    B0 = iv.mpf(10) ** iv.mpf(P['lb0'])
    Cp = iv.mpf(32) / 5 * (iv.mpf(5) / 3) ** iv.mpf('0.375') * CEi ** iv.mpf('0.625')
    C = up(float(mp.make_mpf(Cp._mpi_[1])), 2)
    k = up_sig(float(mp.make_mpf((iv.mpf(3) / 5 * CEi * B0 ** iv.mpf('1.6'))._mpi_[1])), 2)
    a = up_sig(float(mp.make_mpf((iv.mpf(12) / 5 * CEi * B0 ** iv.mpf('-0.4'))._mpi_[1])), 2)
    final[t] = dict(P, CE=CE, C=C, k=k, a=a)
    rows.append((t, m))
json.dump(final, open('tiers_v3_final.json', 'w'), indent=1)
# re-merge with the stated constants (cert_v3.py reads tiers_v3.json from the current directory)
if not os.path.exists('tiers_v3_params_only.json'):
    shutil.copy('tiers_v3.json', 'tiers_v3_params_only.json')
shutil.copy('tiers_v3_final.json', 'tiers_v3.json')
res = {}
for t in tiers:
    files = sorted(glob.glob(os.path.join(d, 'c_%s_*.json' % t)))
    m = json.loads(subprocess.run(['python', 'cert_v3.py', 'merge', '--tier', t] + files, capture_output=True,
                                  text=True).stdout)
    res[t] = m
json.dump(res, open('merged_v3.json', 'w'), indent=1)
print('TABLE 3.1')
print('   tier parts b0      cy         cD=cR    aw       mu        boxes     Psi_sup   C_E^cert  C_E    (E-iii) (W2)/z  t0     (E-iv)')
for t in tiers:
    m = res[t]; F = final[t]; mm = m['margins_min']
    w2 = min(v for kk, v in mm.items() if kk.startswith('W2_'))
    t0 = min(v for kk, v in mm.items() if kk.startswith('t0_'))
    print('   %-4s %-5s 10^%-4s %-10s %-8s %-8s %-9s %dx%-5d %-9.4f %-9.5f %-6s %-7.3f %-7.4f %-6.4f %-7.4f' % (
        t, F['parts'], F['lb0'], F['cy'], F['cd'], F['aw'], F['mu'], m['nz'], m['nt'], m['Psi_sup'], m['C_E_cert'], F['CE'],
        mm['Eiii'], w2, t0, mm['Eiv']))
print('TABLE 4.1')
print('   tier parts b0      C_E     C_i     k_i      a_i      k_x(2/5)   lam_bound  theorem_ok')
for t in tiers:
    m = res[t]; F = final[t]; ch = m['theorem_check']
    print('   %-4s %-5s 10^%-4s %-7s %-7s %-8s %-8s %-10.3g %-10.2e %s' % (t, F['parts'], F['lb0'], F['CE'], F['C'], F['k'],
          F['a'], ch['cross_2_5'], ch['lambda_bound'], m.get('theorem_ok')))
    print('        checks:', {kk: v for kk, v in ch.items() if isinstance(v, bool)})
print('WORST')
for t in tiers:
    w = res[t]['worst']
    print('   %s z=[%.6g,%.6g] t/z^2=[%.5f,%.5f] tri %.3f other %.3f left %.3f right %.3f' % (
        t, w['z'][0], w['z'][1], w['tn'][0], w['tn'][1], w['tri'], w['other'], w['left'], w['right']))
