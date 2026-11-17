"""Write the certificate folder for one packing from its high-precision solution.

Usage:
  python package.py TAG INDIR OUTDIR

Reads INDIR/TAG_newton.pkl (written by newton.py). Squares whose angle is zero in the solution are written as exactly
axis-aligned. The packing is the solution scaled by 1 + 1e-60 and shifted by 1e-60, so that no two squares touch.
Writes nN_exact.json, nN_witness.yaml, nN_solution_250_digits.txt and nN_record.png to OUTDIR after an exact check."""
import sys,json,math,pickle,os,hashlib
from fractions import Fraction as F
from decimal import Decimal, getcontext
import mkcert
getcontext().prec=320
tag,indir,outdir=sys.argv[1],sys.argv[2],sys.argv[3]
Xs,n,E=pickle.load(open('%s/%s_newton.pkl'%(indir,tag),'rb'))
os.makedirs(outdir,exist_ok=True)
D=10**250; MARG=F(1,10**60)
CLAIM="Exact rational coordinates of a packing of %d unit squares. verify_exact.py checks in rational arithmetic that every edge direction is a unit vector, that every square lies in the container and that all pairs of squares have disjoint interiors. The file proves an upper bound for the side. It makes no statement on optimality."
def cut(v):
    v=v.strip(); return v if 'e' in v.lower() else v[:v.index('.')+251] if '.' in v else v
def fr(s): return F(int((Decimal(s)*Decimal(D)).to_integral_value()),D)
import mpmath as mp; mp.mp.dps=300
sq=[]; nal=0
for i in range(n):
    th=mp.mpf(Xs[2*n+i])
    if abs(th)<mp.mpf(10)**(-150): c,s=F(1),F(0); nal+=1
    else:
        t=fr(mp.nstr(mp.tan(th/2),290)); c=(1-t*t)/(1+t*t); s=2*t/(1+t*t)
    sq.append([fr(Xs[i])*(1+MARG)+MARG,fr(Xs[n+i])*(1+MARG)+MARG,c,s])
cs=[mkcert.corners(q) for q in sq]
x0=min(min(x for c in cs for x,_ in c),F(0)); y0=min(min(y for c in cs for _,y in c),F(0))
for q in sq: q[0]-=x0; q[1]-=y0
cs=[mkcert.corners(q) for q in sq]
side=max(max(x for c in cs for x,_ in c),max(y for c in cs for _,y in c))
err=mkcert.verify(side,[tuple(q) for q in sq]); assert err is None,err
Sopt=fr(Xs[3*n]); print(tag,'VALID; aligned squares',nal,'of',n,'; side above the high-precision solution by %.2e'%float(side-Sopt))
json.dump({"n":n,"side":str(side),"square_size":"1","format":"each square: [center_x, center_y, cos, sin] as exact rationals; (cos, sin) is the unit direction of one edge","squares":[[str(v) for v in q] for q in sq]},open('%s/n%d_exact.json'%(outdir,n),'w'),indent=0)
y=lambda v: (str(v) if '/' in str(v) else "'%s'"%str(v))
L=["softschema:","  contract: packing.squares:Witness/v2","  schema: https://github.com/jlevy/squares/blob/main/packing/witnesses/witness.schema.yaml","  envelope: witness","  status: enforced",
   "witness:","  id: W-n%d-de-winter"%n,"  n: %d"%n,"  side: "+str(side),"  square_size: '1'","  representation: center-basis","  scalar:","    kind: rational","  coordinates:","    origin: lower-left","    axes: x-right-y-up","    angle_unit: not-applicable",
   "  claim:","    coordinate_provenance: verified","    method: exact-algebraic","    limitations: "+CLAIM%n,"  squares:"]
for k,q in enumerate(sq,1):
    L+=["  - id: %d"%k,"    center:","    - "+y(q[0]),"    - "+y(q[1]),"    basis:","    - "+y(q[2]),"    - "+y(q[3])]
open('%s/n%d_witness.yaml'%(outdir,n),'w').write("\n".join(L)+"\n")
open('%s/n%d_solution_250_digits.txt'%(outdir,n),'w').write('# Solution of the contact equations, n = %d. First line: side. Then one line per square: x y theta (radians).\n'%n+cut(Xs[3*n])+'\n'+''.join('%s %s %s\n'%tuple(cut(Xs[o*n+i]) for o in range(3)) for i in range(n)))
ds=str(side.numerator*10**70//side.denominator); print('side',ds[:-70]+'.'+ds[-70:])
up12=-(-side.numerator*10**12//side.denominator); print('rounded up at 12 places: %s.%s'%(str(up12)[:-12],str(up12)[-12:]))
up10=-(-side.numerator*10**10//side.denominator); t10='%s.%s'%(str(up10)[:-10],str(up10)[-10:])
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
import matplotlib.font_manager as fm
names={f.name for f in fm.fontManager.ttflist}
plt.rcParams['font.family']='Arial' if 'Arial' in names else ('Liberation Sans' if 'Liberation Sans' in names else 'DejaVu Sans')
Sf=float(side); fig,ax=plt.subplots(figsize=(9,9.4))
for q in sq:
    cx,cy,c,s=map(float,q)
    Pp=[(cx+a*c/2-b*s/2,cy+a*s/2+b*c/2) for a,b in((1,1),(-1,1),(-1,-1),(1,-1))]
    ax.add_patch(Polygon(Pp,fc='#e6e6e6' if q[3]==0 else '#ffbf00',ec='black',lw=0.9))
ax.plot([0,Sf,Sf,0,0],[0,0,Sf,Sf,0],color='black',lw=2.5)
ax.set_xlim(-.2,Sf+.2);ax.set_ylim(-.2,Sf+.2);ax.set_aspect('equal');ax.axis('off')
ax.set_title('%d unit squares, side %s'%(n,t10),fontsize=14)
fig.savefig('%s/n%d_record.png'%(outdir,n),dpi=90,bbox_inches='tight')
print('tilted squares',n-nal)
