# p3test.py -- exact test of construction ZC' (paper, version 1.1, rule (Z4')) and of Lemma W'' (B_W'').
# Uses r38.py (independent reimplementation of ZC, copied unchanged) with its row-placement rule replaced by (Z4'),
# and cert.py (generic exact certificate, copied unchanged from the author's programs). Inputs: canonical Z of run_z.canon.
# usage: python p3test.py m sc hc aw mu docert
import sys, json, time, math
import r38, cert
from r38 import QQ, fl, Tilt
import mpmath

def canon(m, sc=2.45, hc=4):   # identical to run_z.canon / run_exact.canon
    sq = math.isqrt(m * 10 ** 12)
    sig = QQ(int(round(sc * 10 ** 6)), sq)
    h0 = QQ(int(hc * m ** 0.75 * 1000), 1000)
    return h0, sig, QQ(m)

STATS = dict(moved=0, moved_sq=0)
_orig_place = r38._place

def place_zc_prime(rows, a, r, j, h):
    h0 = h(QQ(0)); sig = h(QQ(1)) - h0
    ast = max(QQ(a), QQ(0), (j + 1 - h0) / sig)
    if r - ast >= 1:
        k = fl(r - ast)
        rows.append((ast, j, k))
        if ast != a or not (a >= 0 and j + 1 <= h(a)):
            STATS['moved'] += 1; STATS['moved_sq'] += k

def bounds(h0, sig, L, t0, Qs, Qf, mu):
    iv = mpmath.iv; iv.prec = 150
    def I(x):
        x = QQ(x); return iv.mpf(int(x.numerator)) / iv.mpf(int(x.denominator))
    tl = Tilt(t0)
    h0i, sigi, Li = I(h0), I(sig), I(L)
    N0 = fl(QQ(h0)) - 1
    ta0, se0, e0, ca0 = I(tl.ta), I(tl.se), I(tl.e), I(tl.ca)
    mu = iv.mpf(mu)
    g = iv.mpf(21) / 10 / Qs
    hL = h0i + sigi * Li
    Mmax = hL + N0 * e0
    sm = iv.sqrt(1 + mu ** 2 * ta0 ** 2)
    emin = (mu * ta0) ** 2 / (sm * (sm + 1))
    Lam = (emin * N0 - 1 - sigi * ta0) / sigi
    Kbar = Li / Lam
    eps = (se0 - 1) + N0 * g + iv.mpf(1) / Qf
    W = dict(W1=Lam - N0 * ta0,
             W2=(1 - mu) * ta0 - ((e0 / N0) * (Li + Kbar * (1 + sigi * ta0) / sigi) + Kbar * g),
             W3=N0 * ca0 - (sigi * se0 / emin + ta0 + sigi * (2 + se0 + Mmax * ta0) + (1 + sigi * ta0) / emin),
             W4=1 - eps, W5a=mu * ta0 - g, W5b=iv.mpf('0.21') - ta0)
    ccol = ta0 + se0 * e0 + se0 * sigi * (se0 + N0 * e0 * ta0)
    hT = 1 + sigi * se0 / emin + ta0 + sigi * (1 + se0 + Mmax * ta0)
    wT = 1 + (hL + 1) * (e0 ** 2 / sigi + g)
    AT = hT * wT
    ATp = (hT + 1) * (1 + ta0) + (2 + sigi * (wT + ta0 + sigi * ta0)) * (wT + ta0)
    w0 = (1 + N0 * e0) * ta0
    we = 1 + se0 + (hL + N0 * e0) * ta0
    fh0 = fl(QQ(h0))
    common = Li * ccol + fh0 * (1 + ta0 / 2) + w0 * (1 + sigi * w0) + hL * (1 + ta0 / 2)
    blk = (N0 - 1) * (eps + ta0) + ((1 + sigi * ta0) / emin) * (1 + ta0)
    BW = common + Kbar * (blk + AT) + we * (4 + 2 * sigi * we)
    BW2 = common + Kbar * (blk + ATp) + we + 2 * (1 + ta0)
    hyp = all(float(v.a) > 0 for v in W.values()) and QQ(t0) <= QQ(1, 10) and QQ(h0) >= 4
    return dict(BW=float(BW.b), BW2=float(BW2.b), hyp=hyp, margins={k: float(v.a) for k, v in W.items()})

def main():
    m = int(sys.argv[1]); sc = float(sys.argv[2]); hc = float(sys.argv[3]); aw = QQ(sys.argv[4]); mu = sys.argv[5]
    docert = int(sys.argv[6])
    Qs, Qf = 2 ** 40, 2 ** 48
    h0, sig, L = canon(m, sc, hc)
    t0 = r38.wall_t0(sig, Qs, aw)
    T0 = time.time()
    r38._place = _orig_place
    z1 = r38.zfill(h0, sig, L, t0, Qs, Qf)
    r38._place = place_zc_prime
    z2 = r38.zfill(h0, sig, L, t0, Qs, Qf)
    h = lambda x: h0 + sig * x
    # internal checks of the placed rows of ZC' (containment conditions of Lemma P3a)
    rows_ok = all(a >= 0 and j + 1 <= h(a) and a + k <= L and k >= 1 for (a, j, k) in z2['rows'])
    b = bounds(h0, sig, L, t0, Qs, Qf, mu)
    res = dict(m=m, sc=sc, hc=hc, aw=str(aw), mu=mu, blocks=len(z2['blocks']), fail=z2['fail'],
               U_ZC=float(z1['U']), U_ZCp=float(z2['U']), U_ZCp_exact=str(z2['U']), gain=float(z1['U'] - z2['U']),
               moved_rows=STATS['moved'], moved_squares=STATS['moved_sq'], rows_ok=rows_ok,
               BW=b['BW'], BW2=b['BW2'], hyp=b['hyp'], margins=b['margins'],
               U_ZC_le_BW=float(z1['U']) <= b['BW'], U_ZCp_le_BW2=float(z2['U']) <= b['BW2'])
    if docert:
        P = [v for (v, n) in r38.zpieces(z2)]
        c = cert.certify(P, h0, L, sig, QQ(0), z2['area'])
        res['cert'] = dict(all_pass=c['all_pass'], inter_overlaps=c.get('inter_overlaps'),
                           intra_overlaps=c.get('intra_overlaps'), contain_bad=c['contain_bad'],
                           U_match=(c.get('U') == z2['U']), npieces=len(P))
    res['sec'] = round(time.time() - T0, 1)
    print(json.dumps(res), flush=True)

if __name__ == '__main__':
    main()
