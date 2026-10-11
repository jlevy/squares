# run_z.py m [check] -- wall filler alone on canonical Z: sig = 2.45/sqrt(m), L = m, h0 = 4 m^{3/4}, aw = 3/2
import sys, json, time, math
from r38 import QQ, zfill, zpieces, bw_bound, wall_t0, fl, Tilt, HAVE_GMP
import chk

def canon(m, sc=2.45, hc=4):
    # exact rationals close to the text's choice (sig = 2.45/sqrt(m), h0 = 4 m^{3/4}); any rational inputs are allowed by Lemma W
    sq = math.isqrt(m * 10 ** 12)          # ~ sqrt(m) * 1e6
    sig = QQ(int(round(sc * 10 ** 6)), sq)   # sc / sqrt(m)
    h0 = QQ(int(hc * m ** 0.75 * 1000), 1000)
    return h0, sig, QQ(m)

def main():
    m = int(sys.argv[1]); docheck = len(sys.argv) > 2 and sys.argv[2] == '1'
    Qs, Qf = 2 ** 40, 2 ** 48
    t_0 = time.time()
    sc = float(sys.argv[3]) if len(sys.argv) > 3 else 2.45; hc = float(sys.argv[4]) if len(sys.argv) > 4 else 4.0
    h0, sig, L = canon(m, sc, hc)
    t0 = wall_t0(sig, Qs)
    z = zfill(h0, sig, L, t0, Qs, Qf)
    t_1 = time.time()
    bw = bw_bound(h0, sig, L, t0, Qs, Qf)
    N0 = z['N0']
    eps = (Tilt(t0).se - 1) + N0 * QQ(21, 10) / Qs + QQ(1, Qf)
    rec = {'m': m, 'sc': sc, 'hc': hc, 'gmp': HAVE_GMP, 'h0': float(h0), 'sig': float(sig), 'L': float(L), 't0': str(t0),
           'ta0': float(Tilt(t0).ta), 'fail': z['fail'], 'blocks': len(z['blocks']),
           'reasons': [B.reason for B in z['blocks']], 'P': [B.P for B in z['blocks']],
           'ta_first_last': [float(z['blocks'][0].tl.ta), float(z['blocks'][-1].tl.ta)] if z['blocks'] else None,
           'F': [B.F for B in z['blocks']],
           'n_cols': sum(B.P for B in z['blocks']), 'n_rows': len(z['rows']),
           'naligned': z['naligned'], 'maxres': float(z['maxres']), 'eps': float(eps),
           'res_le_eps': bool(z['maxres'] <= eps), 'minl_aligned': (float(z['minl']) if z['minl'] is not None else None),
           'U': float(z['U']), 'U_exact': str(z['U']), 'U_over_m34': float(z['U']) / m ** 0.75,
           'BW': bw['BW_hi'], 'BW_over_m34': bw['BW_hi'] / m ** 0.75, 'U_le_BW': float(z['U']) <= bw['BW_hi'],
           'hyp': bw['margins'], 'hyp_ok': bw['hyp_ok'], 't_build': time.time() - t_0}
    if docheck:
        pcs = [('z', v, n) for v, n in zpieces(z)]
        hL = h0 + sig * L
        poly = [(QQ(0), QQ(0)), (L, QQ(0)), (L, hL), (QQ(0), h0)]
        r = chk.certify(pcs, poly, log=lambda s: print(s, flush=True))
        rec['cert'] = r
        rec['nsq_pieces'] = sum(n for _, _, n in pcs)
        rec['nsq_match'] = (rec['nsq_pieces'] == z['nsq'])
        rec['t_check'] = time.time() - t_1
    print(json.dumps(rec), flush=True)

if __name__ == '__main__':
    main()

