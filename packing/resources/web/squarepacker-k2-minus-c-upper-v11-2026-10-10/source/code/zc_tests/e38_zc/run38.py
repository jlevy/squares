# run38.py -- build E38 for (b, y), certify exactly (cert.py, generic), internal proof checks, exact U.
# usage: python run38.py b y [cD cR aw] [nocert] [brute]
import sys, json, time, math
import z38
from z38 import F, fl, frac
import cert

def main_checks(C):
    out = dict(ok=True, notes=[], aligned_ok=True)
    def bad(m):
        if m.startswith('main residual') or m == 'tau':
            if out['aligned_ok'] or m == 'tau': out['notes'].append('hyp: ' + m)
            out['aligned_ok'] = False; return
        out['ok'] = False; out['notes'].append(m)
    Js = C['Js']; m = C['m']; ca, sa, ta, se, e = C['ca'], C['sa'], C['ta'], C['se'], C['e']
    if any(Js[i] > Js[i + 1] for i in range(len(Js) - 1)): bad('J monotone')
    if Js[0] < 0 or Js[-1] > m - 1: bad('J range')
    if not (m > C['G']): bad('m>G')
    for (ci, J, n) in C['cols']:
        gp = C['g'](ci - m * ta) - (J + n * ca + sa)
        if not (0 <= gp < e): bad('gap'); break
    W = C['Bd']['W']
    if not (W - C['DR'] - se < C['cN'] <= W - C['DR']): bad('cN window')
    mx = F(0)
    for (j, a, r, p) in C['mstretch']:
        ln = r - a
        if j >= C['J0']:
            if ln < 0 or frac(ln) > C['eps_m']: bad('main residual j=%d' % j); continue
            mx = max(mx, frac(ln))
        if not (j + 1 <= C['g'](a)): bad('row ceiling j=%d' % j); break
    if not (C['tau'] > 0 and C['tau'] <= ta): bad('tau')
    out['maxres'] = float(mx)
    return out

def run(b, y, cD=3, cR=3, aw=2.0, do_cert=True, brute=False):
    t0 = time.time()
    C = z38.build(b, F(y) if isinstance(y, int) else y, F(cD) if isinstance(cD, int) else cD,
                  F(cR) if isinstance(cR, int) else cR, aw)
    V = z38.V_total(C); A = z38.area_reg(C); U = A - V
    res = dict(b=b, y=str(C['y']), yf=float(C['y']), m=C['m'], D=C['D'], DR=C['DR'], N=C['N'], J0=C['J0'], JL=C['JL'],
               ta=float(C['ta']), tau=float(C['tau']), eps_m=float(C['eps_m']), V=int(V), U=float(U),
               U_b35=float(U) / b ** 0.6, U_b23=float(U) / b ** (2 / 3), aw=aw, cD=float(cD), cR=float(cR))
    res['main'] = main_checks(C)
    ws = {}
    for name, (Z, mp) in C['walls'].items():
        info = Z.get('info', {})
        zc = z38.zchecks(Z) if Z['blocks'] or Z['runs'] else dict(ok=True)
        Uz = z38.zarea(Z) - z38.zV(Z) if Z['L'] > 0 else F(0)
        bl = Z['blocks']
        ws[name] = dict(h0=float(Z['h0']), sig=float(Z['sig']), L=float(Z['L']), nblocks=len(bl),
                        ncols=len(Z['cols']), nruns=len(Z['runs']), U=float(Uz), fail=info.get('fail'),
                        ta_first=float(bl[0]['ta']) if bl else None, ta_last=float(bl[-1]['ta']) if bl else None,
                        checks=zc)
    res['walls'] = ws
    res['build_sec'] = round(time.time() - t0, 1)
    if do_cert:
        P = z38.polys(C)
        Bd = C['Bd']
        r = cert.certify(P, C['y'], Bd['W'], Bd['T'], Bd['s'], A)
        res['cert'] = {k: (v if not hasattr(v, 'numerator') or isinstance(v, int) else float(v)) for k, v in r.items()}
        res['cert_U_matches'] = (r.get('U') == U)
        if brute:
            res['brute'] = cert.brute(P)
    res['sec'] = round(time.time() - t0, 1)
    res['pass'] = bool(res['main']['ok'] and all(w['checks'].get('ok', True) for w in ws.values())
                   and (not do_cert or (res['cert'].get('all_pass') and res['cert_U_matches'])))
    res['aligned_regime'] = bool(res['main']['aligned_ok'] and all(not w['fail'] and w['nblocks'] > 0 for w in ws.values()))
    return res

if __name__ == '__main__':
    b = int(sys.argv[1]); ys = sys.argv[2].split('/'); y = F(int(ys[0]), int(ys[1]) if len(ys) > 1 else 1)
    cD = int(sys.argv[3]) if len(sys.argv) > 3 and sys.argv[3].isdigit() else 3
    cR = int(sys.argv[4]) if len(sys.argv) > 4 and sys.argv[4].isdigit() else 3
    aw = float(sys.argv[5]) if len(sys.argv) > 5 and sys.argv[5][0].isdigit() else 2.0
    print(json.dumps(run(b, y, cD, cR, aw, 'nocert' not in sys.argv, 'brute' in sys.argv)), flush=True)
