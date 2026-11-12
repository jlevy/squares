"""High-precision solution of the contact equations of a packing found in binary64.

Usage:
  python newton.py PACKING.npz OUTDIR TAG [MARGIN_EXPONENT]

Every corner of a square that lies within 1e-6 of the edge line of a neighbouring square (on an axis that separates the
two squares) gives one equation, and every corner within 1e-6 of a wall gives one equation. Newton's method solves an
independent subset of these equations with python-flint at 900 bits and reports the residual of all of them.
Output: OUTDIR/TAG_newton.pkl (the solution as decimal strings) and OUTDIR/TAG_exact.json (a rational packing that is
the solution scaled by 1 + 10^-MARGIN_EXPONENT and shifted by 10^-MARGIN_EXPONENT, verified exactly)."""
import sys,json,math,time,pickle
import numpy as np, scipy.linalg as sl
from fractions import Fraction as F
from flint import arb, arb_mat, ctx, fmpq
import slp, mkcert
ctx.prec=900
src,out,tag=sys.argv[1],sys.argv[2],sys.argv[3]
MARG=int(sys.argv[4]) if len(sys.argv)>4 else 60
d=np.load(src); S0=float(d['S']); P0=d['P'].copy(); n=len(P0)
P0[:,2]=(P0[:,2]+np.pi/4)%(np.pi/2)-np.pi/4
TOL=1e-6
X,Y,_,_=slp.verts(P0); pairs=slp.get_pairs(P0,1.4143+1e-5)
OX,OY=slp.OX,slp.OY
E=[]
# pair equations: every (vertex of A, axis of B, sign) with |f|<TOL on an axis that separates the pair
i_=pairs[:,0]; j_=pairs[:,1]
for A,B in list(zip(i_,j_))+list(zip(j_,i_)):
    cb,sb=math.cos(P0[B,2]),math.sin(P0[B,2])
    dx=X[A]-P0[B,0]; dy=Y[A]-P0[B,1]
    for m,(ax,ay) in enumerate(((cb,sb),(-sb,cb))):
        p=dx*ax+dy*ay
        for sg in (1,-1):
            vals=sg*p-0.5
            if vals.min()>-1e-7:
                for k in np.nonzero(vals<TOL)[0]: E.append(('p',int(A),int(k),int(B),m,sg))
for i in range(n):
    for k in range(4):
        for w,g in enumerate((X[i,k],Y[i,k],S0-X[i,k],S0-Y[i,k])):
            if g<TOL: E.append(('w',i,k,w))
print(tag,'n=%d equations %d (wall %d)'%(n,len(E),sum(e[0]=='w' for e in E)),flush=True)
N=3*n+1
def A_(x): return arb(float(x))
Xv=[A_(P0[i,0]) for i in range(n)]+[A_(P0[i,1]) for i in range(n)]+[A_(P0[i,2]) for i in range(n)]+[A_(S0)]
half=arb(1)/2
def build(Xv):
    R=[]; J=[]
    C=[(Xv[2*n+i].cos(),Xv[2*n+i].sin()) for i in range(n)]
    for e in E:
        if e[0]=='w':
            _,i,k,w=e; a,b=OX[k]*2,OY[k]*2; c,s=C[i]
            vx=Xv[i]+(a*c-b*s)*half; vy=Xv[n+i]+(a*s+b*c)*half
            dvx=(-a*s-b*c)*half; dvy=(a*c-b*s)*half
            row={}
            if w==0: r=vx; row[i]=arb(1); row[2*n+i]=dvx
            elif w==1: r=vy; row[n+i]=arb(1); row[2*n+i]=dvy
            elif w==2: r=Xv[3*n]-vx; row[i]=arb(-1); row[3*n]=arb(1); row[2*n+i]=-dvx
            else: r=Xv[3*n]-vy; row[n+i]=arb(-1); row[3*n]=arb(1); row[2*n+i]=-dvy
        else:
            _,A,k,B,m,sg=e; a,b=OX[k]*2,OY[k]*2; c,s=C[A]; cb,sb=C[B]
            vx=Xv[A]+(a*c-b*s)*half; vy=Xv[n+A]+(a*s+b*c)*half
            dvx=(-a*s-b*c)*half; dvy=(a*c-b*s)*half
            ux=vx-Xv[B]; uy=vy-Xv[n+B]
            if m==0: nx,ny,dnx,dny=cb,sb,-sb,cb
            else: nx,ny,dnx,dny=-sb,cb,-cb,-sb
            r=sg*(ux*nx+uy*ny)-half
            row={A:sg*nx,n+A:sg*ny,B:-sg*nx,n+B:-sg*ny}
            row[2*n+A]=row.get(2*n+A,arb(0))+sg*(dvx*nx+dvy*ny)
            row[2*n+B]=row.get(2*n+B,arb(0))+sg*(ux*dnx+uy*dny)
        R.append(r); J.append(row)
    return R,J
def amax(R): return max(R,key=lambda r:r.abs_upper()).abs_upper()
R,J=build(Xv); print('initial max residual',amax(R).str(5),flush=True)
Jf=np.zeros((len(E),N))
for a,row in enumerate(J):
    for c,v in row.items(): Jf[a,c]=float(v.mid())
sv=np.linalg.svd(Jf,compute_uv=False); rank=int((sv>1e-7*sv[0]).sum())
print('vars',N,'rank',rank,'sv at rank %.2e next %.2e'%(sv[rank-1],sv[rank] if rank<len(sv) else 0))
U,s_,Vt=np.linalg.svd(Jf); null=Vt[rank:]; print('max |S| component in null space %.2e'%(np.abs(null[:,3*n]).max() if len(null) else 0))
_,_,pc=sl.qr(Jf,pivoting=True,mode='economic'); cols=sorted(pc[:rank])
_,_,pr=sl.qr(Jf[:,cols].T,pivoting=True,mode='economic'); rows=sorted(pr[:rank])
print('cond %.2e'%np.linalg.cond(Jf[np.ix_(rows,cols)]),'S among solved variables:',3*n in cols,flush=True)
cidx={c:k for k,c in enumerate(cols)}
for it in range(12):
    R,J=build(Xv)
    M=arb_mat(rank,rank); b=arb_mat(rank,1)
    for a,ri in enumerate(rows):
        for c,v in J[ri].items():
            if c in cidx: M[a,cidx[c]]=v
        b[a,0]=-R[ri]
    dx=M.solve(b)
    for k,c in enumerate(cols): Xv[c]=arb((Xv[c]+dx[k,0]).mid())
    R2,_=build(Xv); rs=amax([R2[r] for r in rows]); ra=amax(R2)
    print('iter',it,'selected residual',rs.str(5),'all equations',ra.str(5),flush=True)
    if rs<arb('1e-200'): break
R2,_=build(Xv)
neg=[(float(r.mid()),E[k]) for k,r in enumerate(R2) if r< -arb('1e-150')]
pos=[float(r.mid()) for k,r in enumerate(R2) if r> arb('1e-150')]
print('equations left open (gap>0): %d, max %.2e ; violated (gap<0): %d, worst %.2e'%(len(pos),max(pos) if pos else 0,len(neg),min(v for v,_ in neg) if neg else 0))
Sx=Xv[3*n]; print('S =',Sx.str(60,radius=False),' float start',repr(S0))
pickle.dump(([x.mid().str(280,radius=False) for x in Xv],n,[e for e in E]),open(out+'/%s_newton.pkl'%tag,'wb'))
# rational certificate with margin
from decimal import Decimal, getcontext
getcontext().prec=320
D=10**250
def fr(a): return F(int((Decimal(a.mid().str(280,radius=False))*Decimal(D)).to_integral_value()),D)
viol=-min(v for v,_ in neg) if neg else 0.0
if viol>0: MARGX=F(int(viol*4e30),10**30)
else: MARGX=F(1,10**MARG)
sq=[]
for i in range(n):
    th=Xv[2*n+i]; t=fr((th/2).tan()); c=(1-t*t)/(1+t*t); s=2*t/(1+t*t)
    sq.append([fr(Xv[i])*(1+MARGX)+MARGX,fr(Xv[n+i])*(1+MARGX)+MARGX,c,s])
cs=[mkcert.corners(q) for q in sq]
x0=min(x for c in cs for x,_ in c); y0=min(y for c in cs for _,y in c)
x0=min(x0,F(0)); y0=min(y0,F(0))
for q in sq: q[0]-=x0; q[1]-=y0
cs=[mkcert.corners(q) for q in sq]
side=max(max(x for c in cs for x,_ in c),max(y for c in cs for _,y in c))
err=mkcert.verify(side,[tuple(q) for q in sq])
print('margin %.1e -> exact verification:'%float(MARGX),err or 'VALID',' side=%s'%arb(fmpq(side.numerator,side.denominator)).str(40,radius=False))
if err is None:
    json.dump({"n":n,"side":str(side),"square_size":"1","format":"each square: [center_x, center_y, cos, sin] as exact rationals; (cos, sin) is the unit direction of one edge","squares":[[str(v) for v in q] for q in sq]},open(out+'/%s_exact.json'%tag,'w'),indent=0)
    print('side above Newton solution by %.2e'%float(side-fr(Sx)))
