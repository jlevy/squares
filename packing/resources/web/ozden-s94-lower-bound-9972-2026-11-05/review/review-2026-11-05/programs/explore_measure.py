"""Exploratory look at the certificate's measure (decides nothing)."""
import gzip, json, sys
from fractions import Fraction as Fr
from collections import Counter

path = sys.argv[1]
raw = gzip.open(path, 'rb').read() if path.endswith('.gz') else open(path, 'rb').read()
cert = json.loads(raw, parse_float=lambda s: (_ for _ in ()).throw(ValueError('float token ' + s)))
print('keys', sorted(cert))
for k in sorted(cert):
    if k != 'rectangles':
        print(' ', k, repr(cert[k])[:200])
rows = cert['rectangles']
print('rows', len(rows))
print('row keys', Counter(tuple(sorted(r)) for r in rows))
L = Fr(cert['L'])
ok_xyxy = ok_xxyy = 0
for r in rows:
    a = [Fr(v) for v in r['rectangle']]
    if a[0] < a[2] and a[1] < a[3]:
        ok_xyxy += 1
    if a[0] < a[1] and a[2] < a[3]:
        ok_xxyy += 1
print('valid as [x1,y1,x2,y2]:', ok_xyxy, ' as [x1,x2,y1,y2]:', ok_xxyy)
