"""The encoding of `LemmaEDec.lean`: a pair certificate as a list of chunk numbers (512 digits base
2^16 each; the digits are variable-length numbers, 15 bits per digit, the top bit continues)."""

CH = 512


def zz(z):
    return 2 * z if z >= 0 else -2 * z - 1


def unzz(a):
    return a // 2 if a % 2 == 0 else -((a + 1) // 2)


def nums_pc(c, out):
    if c == 'par':
        out.append(0)
        return
    out.append(1)
    out.append(len(c))
    for b1, sig, m, kind in c:
        out += [b1, 1 if sig else 0, m]
        if kind[0] == 'out':
            out += [0, kind[1], kind[2]]
        else:
            out.append(1)
            nums_vc(kind[1], out)


def nums_poly(p, out):
    out.append(len(p))
    out += [zz(a) for a in p]


def nums_sl(L, out):
    P, i, j, k, d = L
    for p in P:
        nums_poly(p, out)
    out += [i, j, k, d]


def nums_vc(vc, out):
    splits, fcs, hc, vcl, lc = vc
    out.append(len(splits))
    for q, nm, dm, np_, dp in splits:
        nums_sl(q, out)
        out += [nm, dm, np_, dp]
    out.append(len(fcs))
    for k, G, g1, m in fcs:
        out.append(k)
        nums_poly(G, out)
        nums_poly(g1, out)
        out.append(m)
    for ll in (hc, vcl):
        out.append(len(ll))
        for l in ll:
            out.append(len(l))
            for sc, tag in l:
                if sc[0] == 'drop':
                    out.append(0)
                elif sc[0] == 'box':
                    out.append(1)
                else:
                    out.append(2)
                    out.append(len(sc[1])); out += list(sc[1])
                    out.append(len(sc[2])); out += list(sc[2])
                if tag is None:
                    out.append(0)
                else:
                    out += [1, tag[0], 1 if tag[1] else 0]
    out.append(len(lc))
    for xs, ys in lc:
        for zs in (xs, ys):
            out.append(len(zs))
            for a in zs:
                if a[0] == 'zeroC': out.append(0)
                elif a[0] == 'zeroT': out += [1, a[1]]
                elif a[0] == 'par': out.append(2)
                elif a[0] == 'parT': out += [3, a[1], 1 if a[2] else 0]
                elif a[0] == 'linC': out.append(4)
                else: out += [5, a[1]]


def chunks(nums):
    digs = []
    for n in nums:
        assert n >= 0
        while n >= 32768:
            digs.append(32768 + n % 32768)
            n //= 32768
        digs.append(n)
    out = []
    for i in range(0, len(digs), CH):
        block = digs[i:i + CH]
        v = 0
        for d in reversed(block):
            v = v * 65536 + d
        out.append(v)
    return out


def enc_sb(sb):
    """one sub-bin (`LemmaESplit.decSB`)"""
    b1, sig, m, kind = sb
    out = [b1, 1 if sig else 0, m]
    if kind[0] == 'out':
        out += [0, kind[1], kind[2]]
    else:
        out.append(1)
        nums_vc(kind[1], out)
    return chunks(out)


def enc_pc(c):
    out = []
    nums_pc(c, out)
    return chunks(out)


# ------------------------------------------------------------------ the Lean decoder, mirrored (for tests)
def dec_nums(cs):
    digs = []
    for v in cs:
        for _ in range(CH):
            digs.append(v % 65536)
            v //= 65536
    out, acc, m = [], 0, 1
    for d in digs:
        if d < 32768:
            out.append(acc + d * m); acc, m = 0, 1
        else:
            acc += (d - 32768) * m; m *= 32768
    return out
