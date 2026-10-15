# Independent exact checker for square and rectangle certificates (stdlib only, imports nothing from squarepack).
# Header "n S" or "n W H", rows "x y t". Checks all four wall margins against W and H and strict pairwise separation by SAT.
import sys
from fractions import Fraction as Fr
rows=[l.split() for l in open(sys.argv[1]) if l.strip() and not l.lstrip().startswith('#')]
n=int(rows[0][0]); W=Fr(rows[0][1]); H=Fr(rows[0][2]) if len(rows[0])>2 else W
sq=[]
for r in rows[1:n+1]:
    x,y,t=Fr(r[0]),Fr(r[1]),Fr(r[2]); d=1+t*t; c,s=(1-t*t)/d,2*t/d
    sq.append((x,y,c,s))
assert len(sq)==n
half=Fr(1,2)
def ext(c,s): return (abs(c)+abs(s))*half
minwall=None
for x,y,c,s in sq:
    e=ext(c,s)
    for m in (x-e, W-x-e, y-e, H-y-e):
        minwall=m if minwall is None or m<minwall else minwall
# pairwise SAT on 4 face normals of each square (8 axes incl. negatives, 4 suffice)
def proj_half(c,s,nx,ny):  # half-extent of unit square with axes (c,s),(-s,c) on normal (nx,ny)
    return (abs(nx*c+ny*s)+abs(-nx*s+ny*c))*half
minpair=None; bad=0
for i in range(n):
    xi,yi,ci,si=sq[i]
    for j in range(i+1,n):
        xj,yj,cj,sj=sq[j]
        dx,dy=xj-xi,yj-yi
        if dx*dx+dy*dy>2: continue
        best=None
        for (nx,ny) in ((ci,si),(-si,ci),(cj,sj),(-sj,cj)):
            gap=abs(nx*dx+ny*dy)-proj_half(ci,si,nx,ny)-proj_half(cj,sj,nx,ny)
            best=gap if best is None or gap>best else best
        if best<=0: bad+=1
        minpair=best if minpair is None or best<minpair else minpair
print(f"n={n} W={float(W):.12f} H={float(H):.12f} ceilW-W={float(W.__ceil__()-W):.3e} ceilH-H={float(H.__ceil__()-H):.3e}")
print(f"min wall margin {float(minwall):.3e}  min pair margin {float(minpair) if minpair is not None else float('inf'):.3e}  overlapping pairs {bad}")
ok = minwall>0 and (minpair is None or minpair>0) and bad==0
print("STRICT VALID" if ok else "INVALID")
sys.exit(0 if ok else 1)
