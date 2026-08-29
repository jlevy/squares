import math
from decimal import Decimal as D, getcontext as G

G().prec = 300 # precision
E = D("1E-100") # epsilon
PI = D("3.1415926535897932384626433832795028841971693993751058209749445923078164062862089986280348253421170679"
       "8214808651328230664709384460955058223172535940812848111745028410270193852110555964462294895493038196"
       "4428810975665933446128475648233786783165271201909145648566923460348610454326648213393607260249141273"
       "724587006606315588174881520920962829254091715364367892590360")

def cs(x):
    x = x % (2 * PI)
    t = D(1)
    r = D(1)
    n = 1
    x2 = x * x
    while True:
        t *= -x2 / ((2 * n) * (2 * n - 1))
        if abs(t) < D("1E-305"): break
        r += t
        n += 1
    return r

def sn(x):
    x = x % (2 * PI)
    t = x
    r = x
    n = 1
    x2 = x * x
    while True:
        t *= -x2 / ((2 * n + 1) * (2 * n))
        if abs(t) < D("1E-305"): break
        r += t
        n += 1
    return r

def make_sq(i, x, y, d):
    dx_val = D(x)
    dy_val = D(y)
    rad = D(d) * (PI / D(180))
    c = cs(rad)
    s = sn(rad)
    h = D("0.5")
    pts = [] 
    for dx in [-h, h]:
        for dy in [-h, h]:
            rx = dx * c - dy * s # transform
            ry = dx * s + dy * c
            pts.append((dx_val + rx, dy_val + ry))
    ax = [(c, s), (-s, c)] # SAT axes
    return {'i': i, 'pts': pts, 'ax': ax}


def pr(ax, pts):
    mn = D('Inf')
    mx = D('-Inf')
    for (x, y) in pts:
        p = (x * ax[0] + y * ax[1])
        if p < mn: mn = p
        if p > mx: mx = p
    return mn, mx

def ov(a, b):
    for x in a['ax']:
        mn1, mx1 = pr(x, a['pts'])
        mn2, mx2 = pr(x, b['pts'])
        if mx1 < mn2 + E or mx2 < mn1 + E: return False
    for x in b['ax']:
        mn1, mx1 = pr(x, a['pts'])
        mn2, mx2 = pr(x, b['pts'])
        if mx1 < mn2 + E or mx2 < mn1 + E: return False
    return True

def ld(fn):
    with open(fn, 'r') as f:
        raw = f.read().replace('\n', ' ') 
    
    val = D(raw.split("s:")[1].split()[0])

    lst = []

    chunks = raw.split("Square")[1:]
    
    for c in chunks:
        p = c.split() 
        i = int(p[0].replace(':', '')) 
        
        x = y = d = None
        for item in p:
            if "x=" in item: x = item.replace("x=", "").replace(",", "")
            if "y=" in item: y = item.replace("y=", "").replace(",", "")
            if "deg=" in item: d = item.replace("deg=", "").replace(",", "")
            
        lst.append(make_sq(i, x, y, d))
        
    return val, lst

def run():
    try:
        S, L = ld("squares.txt")
    except FileNotFoundError:
        print("Eror: squares.txt not found.")
        return

    if S is None: return
    print(f"--- CHECK (Prec: {G().prec}) ---")
    print(f"Epsilon: {E}")
    print(f"S: {S}")
    lim = S / D(2)
    fail = False
    
    for q in L:
        for cx, cy in q['pts']:
            if cx < -lim - E or cx > lim + E: # x bounds check
                print(f"FAIL: Square {q['i']} X-Out"); fail = True
            if cy < -lim - E or cy > lim + E: # y bounds check
                print(f"FAIL: Square {q['i']} Y-Out"); fail = True
    if not fail: print("Container: OK")
    
    col = 0
    
    for i in range(len(L)):
        for j in range(i + 1, len(L)):
            if ov(L[i], L[j]): # collision check
                print(f"FAIL: Squares {L[i]['i']}-{L[j]['i']}")
                col += 1
                
    if col == 0: print("Overlaps: NONE")
    print("-" * 30)
    print("VALID" if not fail and col == 0 else "INVALID")

if __name__ == "__main__":
    run()
