"""Compare the genuine non-singular solution sets of two homotopy runs (filter.jl outputs) by S and t."""
import re, sys
def load(fn):
    out = []
    for l in open(fn):
        if not l.startswith('G N'):
            continue
        S = complex(re.search(r' S=(.*?) Sz=', l).group(1).replace('im', 'j').replace(' ', ''))
        ts = [complex(s.replace('im', 'j').replace(' ', '')) for s in re.split(r'(?<=im) ', l.split(' t=')[1].strip())]
        out.append((S, ts))
    return out
A, B = load(sys.argv[1]), load(sys.argv[2])
def key(z): return (round(z.real, 7), round(z.imag, 7))
def match(X, Y):
    idx = {}
    for S, t in Y:
        idx.setdefault(key(S), []).append(t)
    miss = []
    for S, t in X:
        cands = [u for dr in (-1e-7, 0, 1e-7) for di in (-1e-7, 0, 1e-7)
                 for u in idx.get(key(complex(S.real + dr, S.imag + di)), [])]
        if not any(max(abs(a - b) for a, b in zip(t, u)) < 1e-6 * max(1, max(abs(a) for a in t)) for u in cands):
            miss.append((S, t))
    return miss
mA, mB = match(A, B), match(B, A)
print(f'run 1: {len(A)} genuine; run 2: {len(B)} genuine; only in run 1: {len(mA)}; only in run 2: {len(mB)}')
for S, t in mB[:10]:
    print('  only in run 2: S =', S, ' |t| max', max(abs(x) for x in t))
for S, t in mA[:10]:
    print('  only in run 1: S =', S)
