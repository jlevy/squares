# stated_v4.py -- from a merged_v4 json (cert_v4.py merge without --stated) propose the stated constants of a tier,
# all rounded UP: C_E (3 decimals), C_i (2 decimals), k_i (3 significant digits), a_i (2 significant digits).
# The proposal is then re-checked by "cert_v4.py merge --stated ..." (interval arithmetic). No box evaluation here.
import json, sys
from mpmath import iv, mp, mpf, ceil, log10, floor
iv.prec = 120; mp.prec = 120

def up(x, digits_after_point):
    q = mpf(10) ** digits_after_point
    return ceil(x * q) / q

def upsig(x, sig):
    e = int(floor(log10(x))) - sig + 1
    q = mpf(10) ** e
    return ceil(x / q) * q

m = json.load(open(sys.argv[1], encoding='utf-8-sig'))     # PowerShell '>' writes UTF-8 with BOM
ce = up(mpf(m['C_E_cert']), 3)
CE = iv.mpf([ce, ce])
b0 = iv.mpf(10) ** iv.mpf(m['lb0'])
ci = up(mp.make_mpf((iv.mpf('7.751277') * CE ** iv.mpf('0.625'))._mpi_[1]), 2)
ki = upsig(mp.make_mpf((iv.mpf('0.6') * CE * b0 ** iv.mpf('1.6'))._mpi_[1]), 3)
ai = upsig(mp.make_mpf((iv.mpf('2.4') * CE * b0 ** iv.mpf('-0.4'))._mpi_[1]), 2)
kx = mp.make_mpf(((iv.mpf([ci, ci]) / iv.mpf('20.668')) ** 40)._mpi_[1])
print(json.dumps(dict(stated='%s,%s,%s,%s' % (mp.nstr(ce, 10), mp.nstr(ci, 10), mp.nstr(ki, 6), mp.nstr(ai, 6)),
                      k_x_up=mp.nstr(upsig(kx, 3), 6))))
