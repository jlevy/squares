"""Exact side comparisons for review bold-ritchie-rv-daniel. Reads the case records' exact forms
(copied in by argument) and the certificates' header sides; decides each order exactly."""
import sys, yaml
from fractions import Fraction as F
from math import isqrt
root = sys.argv[1]
def lane(n, key):
    t = open(f'{root}/packing/frontier/n-{n}.md').read().split('\n---\n')[0].lstrip('-\n')
    return yaml.safe_load(t)['packing'][key]['exact_form']
def hdr(path):
    for line in open(path):
        if line.startswith('#'): continue
        n, s = line.split(); return int(n), F(s)
W = f'{root}/packing/resources/web'
C845 = f'{W}/evand-issue845-2026-10-29/source/search/packer/candidates'
new = {172: hdr(f'{C845}/s172_1028.cert')[1], 204: hdr(f'{C845}/s204_1028.cert')[1],
       260: hdr(f'{C845}/s260_1028.cert')[1], 293: hdr(f'{C845}/s293_1028.cert')[1],
       299: hdr(f'{W}/evand-n299-update-2026-10-29/source/search/packer/candidates/s299_1028.cert')[1]}
t248 = hdr(f'{W}/evand-n299-2026-10-26/source/search/packer/candidates/s299-1025.cert')[1]
def f(x): return f'{float(x):.6e}'
others = {
 172: [('house T-174 (reported/verified lane)', F(lane(172,'verified_upper_bound')))],
 204: [('house T-231', F(lane(204,'verified_upper_bound'))), ('#846 / e386aab 204', F('14808642830513087197802415708703/1000000000000000000000000000000'))],
 260: [('house T-225', F(lane(260,'verified_upper_bound'))), ('T-255 a5a5d76', F('67077942617632138527571542307/4031481829251000000000000000')),
       ('T-256 #844', F('104381051573626493618357957479/6274019722347000000000000000')), ('#846 260', F('4161438312629953048686324163329/250000000000000000000000000000'))],
 293: [('Kingbird 723/41 (reported lane)', F(723,41)), ('verified lane T-101', F(lane(293,'verified_upper_bound')))],
 299: [('verified lane T-101', F(lane(299,'verified_upper_bound'))), ('T-248 #824', t248), ('#846 299', F('2225461929414467349619294144451/125000000000000000000000000000'))],
}
for n, s in new.items():
    print(f'n={n} new side {s.numerator}/{s.denominator}')
    for name, o in others[n]:
        print(f'   {name}: other - new = {f(o - s)}  ({"new below" if s < o else "NEW NOT BELOW"})')
# 299 vs 33/2 + sqrt(7)/2 exactly: s < 33/2 + sqrt7/2  <=>  2s - 33 < sqrt 7
s = new[299]; d = 2*s - 33
print('299 vs 33/2+sqrt(7)/2: 2s-33 =', float(d), ' below:', d < 0 or d*d < 7)
s = t248; d = 2*s - 33
print('T-248 vs 33/2+sqrt(7)/2 below:', d < 0 or d*d < 7)
# T-244 Kim algebraic 172: printed 100 digits; compare with the decimal (enclosure +-1e-100)
kim = F('13.6189889568993984288635016293504898995040150521961793814779549035630128682876859236484103034563728798')
print('172 vs T-244 print (100 digits, +-1e-100):', f(kim - new[172]))
# 293 vs 260 sides
print('S293 - S260 - 1 =', f(new[293] - new[260] - 1))
print('T-248 - T-258 =', f(t248 - new[299]))
