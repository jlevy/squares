"""Turn a recover_k.py top-coefficient vector a (from a DEBUG log) into refined-root lines for the K missing roots.

    ../env.sh python3 addq.py BITS LOG OUT work/n29_ref133k_*.txt

Recomputes P from the known roots, D*Q from a (same recursion as recover_k.py), and writes the roots of Q (one of each
conjugate pair) in refine.jl's format with dummy t columns (imaginary parts set so reconstruct.py treats real/complex
correctly).
"""
import re, sys, math
sys.set_int_max_str_digits(0)
import flint
from flint import acb, arb, acb_poly
bits, log, out = int(sys.argv[1]), sys.argv[2], sys.argv[3]
flint.ctx.prec = bits + 64
txt = open(log).read()
a = [int(x) for x in re.search(r'a = \[([-0-9, ]+)\]', txt).group(1).split(',')]
K = len(a) - 1
roots = []
for fn in sys.argv[4:]:
    for l in open(fn):
        f = l.split()
        col = int(__import__('os').environ.get('COL', '0'))
        s = acb(arb(f[2 + 2 * col]), arb(f[3 + 2 * col]))
        roots += [acb(s.real)] if max(abs(float(x)) for x in f[5::2]) < 1e-30 else [s, s.conjugate()]
P = acb_poly.from_roots(roots); n0 = P.degree(); p = [P[i].real for i in range(n0 + 1)]
g = [None] * (K + 1)
for i in range(K + 1):
    v = arb(a[i])
    for j in range(i):
        v -= p[n0 - (i - j)] * g[K - j]
    g[K - i] = v
Q = acb_poly([acb(x) for x in g])
rs = Q.roots()
dQ = Q.derivative()
digits = int(bits * math.log10(2))
pol = []
for z in rs:
    z = acb(z.real.mid(), z.imag.mid())
    for it in range(40):                       # Newton at full precision (roots() stops early on clustered roots)
        dz = Q(z) / dQ(z)
        z = acb((z - dz).real.mid(), (z - dz).imag.mid())
        if abs(dz).mid() != 0 and float(abs(dz).mid().log()) / math.log(10) < -(digits - 200):
            break
    pol.append(z)
with open(out + '.all', 'w') as fa:
    for z in pol:
        fa.write(z.real.mid().str(digits, radius=False) + ' ' + z.imag.mid().str(digits, radius=False) + '\n')
with open(out, 'w') as fo:
    kept = []
    for z in pol:
        zi = complex(float(z.real.mid()), float(z.imag.mid()))
        if zi.imag < -1e-30 or any(abs(zi - w) < 1e-12 for w in kept):
            continue                           # one of each conjugate pair (the +imag one)
        kept.append(zi)
        real = abs(zi.imag) < 1e-30
        im = '0' if real else z.imag.mid().str(digits, radius=False)
        fo.write(f'q{len(kept)} -1 {z.real.mid().str(digits, radius=False)} {im} 0 {"0" if real else "1"}\n')
        r = abs(Q(z)).mid()
        print('root', zi, 'log10 |Q| / lc', float((r / abs(g[K]).mid()).log()) / math.log(10) if r != 0 else -1e9, flush=True)
