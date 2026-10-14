"""Candidates not in the refined base set: genuine (G N or G S) solutions from the given filter outputs, deduplicated
by t, closed under complex conjugation, minus the base set.  Output in filter.jl's line format (only S= and t= used).
    python3 union.py BASE_GENUINE OUT OTHER_GENUINE...   (BASE's G N lines are the refined set)"""
import re, sys
def parse(l):
    S = complex(re.search(r' S=(.*?) Sz=', l).group(1).replace('im', 'j').replace(' ', ''))
    ts = [complex(s.replace('im', 'j').replace(' ', '')) for s in re.split(r'(?<=im) ', l.split(' t=')[1].strip())]
    return S, ts
def same(a, b): return max(abs(x - y) for x, y in zip(a, b)) < 1e-6 * max(1, max(abs(x) for x in a))
base = [parse(l)[1] for l in open(sys.argv[1]) if l.startswith('G N')]
bidx = {}
def key(t): return tuple(round(z.real, 4) for z in t[:2])
for t in base:
    bidx.setdefault(key(t), []).append(t)
def in_base(t):
    return any(same(t, u) for u in bidx.get(key(t), []))
cands = []
for fn in [sys.argv[1]] + sys.argv[3:]:
    for l in open(fn):
        if not l.startswith('G '):
            continue
        try:
            S, t = parse(l)
        except ValueError:          # S = NaN (Sd = 0): degenerate
            continue
        for tt, SS in ((t, S), ([z.conjugate() for z in t], S.conjugate())):
            if any(abs(x) != abs(x) for x in tt):   # NaN
                continue
            if in_base(tt) or any(same(tt, c[1]) for c in cands):
                continue
            cands.append((SS, tt))
with open(sys.argv[2], 'w') as out:
    for S, t in cands:
        out.write(f'G N C S={S.real}+{S.imag}im Sz=0 t=' + ' '.join(f'{z.real} + {z.imag}im' for z in t) + '\n')
print(f'base {len(base)}; new candidates {len(cands)}')
