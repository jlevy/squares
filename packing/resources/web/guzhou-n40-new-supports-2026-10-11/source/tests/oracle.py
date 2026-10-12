"""独立精确半平面裁剪；仅用于逐姿态审计和反例。\nIndependent exact half-plane clipping for pose audits and counterexamples."""
from fractions import Fraction as Q

def cs(t):
 t=Q(t);return (1-t*t)/(1+t*t),2*t/(1+t*t)

def area(rect,cx,cy,t,B):
 a,b,d,e=rect;poly=[(a,b),(d,b),(d,e),(a,e)];c,s=cs(t);h=B/2
 for nx,ny in ((c,s),(-c,-s),(-s,c),(s,-c)):
  rhs=h+nx*cx+ny*cy;result=[]
  for j,v in enumerate(poly):
   u=poly[j-1];fu=rhs-nx*u[0]-ny*u[1];fv=rhs-nx*v[0]-ny*v[1]
   if (fu>=0)!=(fv>=0):
    r=fu/(fu-fv);result.append((u[0]+r*(v[0]-u[0]),u[1]+r*(v[1]-u[1])))
   if fv>=0:result.append(v)
  poly=result
  if len(poly)<3:return Q(0)
 return abs(sum(poly[i-1][0]*p[1]-p[0]*poly[i-1][1] for i,p in enumerate(poly)))/2

def capture(rows,cx,cy,t,B):
 c,s=cs(t);ex=B*(c+s)/2;tot=Q(0)
 for a,b,d,e,rho in rows:
  if d<=cx-ex or a>=cx+ex or e<=cy-ex or b>=cy+ex:continue
  if all(abs(c*(x-cx)+s*(y-cy))<=B/2 and abs(-s*(x-cx)+c*(y-cy))<=B/2 for x in (a,d) for y in (b,e)):
   tot+=rho*(d-a)*(e-b)
  else:tot+=rho*area((a,b,d,e),cx,cy,t,B)
 return tot
