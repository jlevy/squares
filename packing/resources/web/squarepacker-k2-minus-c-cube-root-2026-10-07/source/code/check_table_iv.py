"""Checks the eight cases of Table 1 of the paper (conditions (i)-(iv) of Proposition 6.1) in interval arithmetic.

Theorem 5.1 of the paper, with the rounded-up constants of Section 2.1 (as allowed at the start of Section 6):
   (1 - 2 tau0)(k - 6) <= W/nu0 + A W/(2 beta) + beta (k/2 - 1) L(W)/(1 - nu0 - E(beta, W)),
   L(W) = A' W max(1/betabar, B1 W/(2 tau1)) + L1 W + 4 delta,
   L1 = (1 + S_K delta^2)/delta + (C_M + C_E + C_G) delta + 4 B1,   B1 = (A/2 + 2 betabar)/cos(betabar),
   E(beta, W) = 0.50001 beta (A + beta/delta) W,   delta = 1e-5,   betabar = 1.5e-6.
Proposition 6.1: with beta(k) = b k^(p-1) and W(k) = gamma k^p, and R+(k) the right side at W(k), beta(k) with k/2 - 1
replaced by k/2, it suffices to check at k = k_a:
  (i)  beta(k_a) <= betabar and tau0 - 1.0001 beta(k_a) > tau1;  (ii) E(beta(k_a), W(k_a)) < 1 - nu0;
  (iii) (1 - 2 tau0)(k_a - 6) > R+(k_a);  (iv) if p = 1/2: gamma k_b^(1/2) <= W1 = 2 tau1/(B1 betabar).
All quantities are mpmath intervals (40 digits); a condition counts as satisfied only if it holds for the whole interval.
Usage: python check_table_iv.py   (needs mpmath; runs in about a second). Writes check_table_iv.out.txt."""
import sys
from mpmath import iv, mp

iv.dps = 40
mp.dps = 40
DL = iv.mpf('1e-5')
BB = iv.mpf('1.5e-6')
CASES = {'K=9': dict(A='10.6067', Ap='10.6068', S='56.2501', CM='318.20', CG='56.2501', CE='754.8'),
         'K=13': dict(A='12.7476', Ap='12.7476', S='81.2502', CM='459.7', CG='81.26', CE='1090.3')}
OUT = []


def dn(x):
    return mp.make_mpf(x._mpi_[0])


def up(x):
    return mp.make_mpf(x._mpi_[1])


def imax(x, y):
    return iv.mpf([max(dn(x), dn(y)), max(up(x), up(y))])


def pw(k, p):  # k^p for p in {'1/2', '1/3', '-1/2', '-2/3'}
    return iv.exp(iv.log(k) * iv.mpf(p.split('/')[0]) / iv.mpf(p.split('/')[1]))


def consts(case):
    c = {key: iv.mpf(v) for key, v in CASES[case].items()}
    c['B1'] = (c['A'] / 2 + 2 * BB) / iv.cos(BB)
    c['L1'] = (1 + c['S'] * DL ** 2) / DL + (c['CM'] + c['CE'] + c['CG']) * DL + 4 * c['B1']
    return c


def say(s):
    print(s)
    OUT.append(s)


def nst(x):
    return mp.nstr(dn(x), 6)


def check(no, case, p, gamma, b, ka, kb, tau0, tau1, nu0):
    c = consts(case)
    k = iv.mpf(ka)
    tau0, tau1, nu0, gamma, b = (iv.mpf(x) for x in (tau0, tau1, nu0, gamma, b))
    W = gamma * pw(k, p)
    beta = b * pw(k, '-1/2' if p == '1/2' else '-2/3')
    ok_par = up(DL) < dn(tau1) and up(tau1) < dn(tau0) and up(tau0) < 0.5 and up(nu0) < 0.5 and dn(nu0) > 0
    ok_beta = up(beta) <= dn(BB) and dn(tau0 - iv.mpf('1.0001') * beta) > up(tau1)
    Es = iv.mpf('0.50001') * beta * (c['A'] + beta / DL) * W
    ok_E = up(Es) < dn(1 - nu0)
    m = imax(1 / BB, c['B1'] * W / (2 * tau1))
    L = c['Ap'] * W * m + c['L1'] * W + 4 * DL
    rhs = W / nu0 + c['A'] * W / (2 * beta) + beta * (k / 2) * L / (1 - nu0 - Es)
    lhs = (1 - 2 * tau0) * (k - 6)
    ok_main = dn(lhs) > up(rhs)
    ok_branch = True
    if p == '1/2':
        W1 = 2 * tau1 / (c['B1'] * BB)
        ok_branch = up(gamma * pw(iv.mpf(kb), '1/2')) <= dn(W1)
    ok = ok_par and ok_beta and ok_E and ok_main and ok_branch and dn(k) >= 14
    kb_s = 'infinity' if kb is None else mp.nstr(mp.mpf(kb), 3)
    say(f"case {no} [{case}] W > {nst(gamma)} k^{p} for all integers k in [{mp.nstr(mp.mpf(ka), 3)}, {kb_s}]"
        f"  (tau0={nst(tau0)}, tau1={nst(tau1)}, nu0={nst(nu0)}, b={nst(b)}): {'OK' if ok else 'FAIL'}")
    say(f"      (i) beta(k_a) <= {mp.nstr(up(beta), 4)}: {ok_beta};  (ii) E <= {mp.nstr(up(Es), 3)}: {ok_E};"
        f"  (iv): {ok_branch};  parameters: {ok_par}")
    say(f"      (iii) left/k_a >= {mp.nstr(dn(lhs / k), 15)} > R+/k_a <= {mp.nstr(up(rhs / k), 15)}: {ok_main}")
    return ok


if __name__ == '__main__':
    say("== check_table_iv.py: Table 1 of the paper, conditions (i)-(iv) of Proposition 6.1 ==")
    for case in CASES:
        c = consts(case)
        cinf = ((iv.mpf(4) / 27) / (c['A'] * c['Ap'] * c['B1'])) ** (iv.mpf(1) / 3)
        say(f"[{case}] B1 in [{mp.nstr(dn(c['B1']), 12)}, {mp.nstr(up(c['B1']), 12)}], L1 <= {mp.nstr(up(c['L1']), 10)}, "
            f"c_inf with the rounded constants >= {mp.nstr(dn(cinf), 10)}")
    res = [check(1, 'K=9', '1/2', '1.0e-4', '1.2e-3', '1e8', '2.5e15', '0.0205', '0.02', '0.001'),
           check(2, 'K=9', '1/2', '7.0e-5', '1.2e-3', '2.5e15', '3.5e17', '0.1675', '0.167', '0.001'),
           check(3, 'K=9', '1/3', '0.06', '1.0', '3.5e17', None, '0.1675', '0.167', '0.01'),
           check(4, 'K=9', '1/3', '0.0625', '1.0', '1e21', None, '0.1668', '0.1667', '0.005'),
           check(5, 'K=13', '1/2', '8.5e-5', '1.2e-3', '1e8', '2.4e15', '0.0205', '0.02', '0.001'),
           check(6, 'K=13', '1/2', '6.0e-5', '1.2e-3', '2.4e15', '3.39e17', '0.1675', '0.167', '0.001'),
           check(7, 'K=13', '1/3', '0.05', '1.0', '3.39e17', None, '0.1675', '0.167', '0.01'),
           check(8, 'K=13', '1/3', '0.052', '1.0', '1e21', None, '0.1668', '0.1667', '0.005')]
    say('ALL OK' if all(res) else 'SOME CASE FAILED')
    with open('check_table_iv.out.txt', 'w', encoding='utf-8') as f:
        f.write('\n'.join(OUT) + '\n')
    sys.exit(0 if all(res) else 1)
