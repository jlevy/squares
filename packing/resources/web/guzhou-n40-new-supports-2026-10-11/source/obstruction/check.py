"""独立 Python 有理数核查固定矩形族对偶界。
Independent Python-rational check of the fixed-rectangle-family dual bound.
"""
from pathlib import Path
import sys,math,time,argparse,json,hashlib
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parent/'verifier'))
sys.path.insert(0,str(HERE.parent/'tests'))
from exact import source,load,save,sha,require as need,Q,L,ORIGINAL as SOURCE_HASH
from oracle import cs,area

def generate_input(cert):
 d=source();ids=list(range(len(d['rectangles'])))
 need(cert['source_indices']==ids and cert['L']=='67/10' and cert['B']=='335/336' and cert['n']==40 and cert['X']=='168/25' and cert['source_sha256']==SOURCE_HASH,'DUAL_SCOPE')
 rows=[]
 for j in ids:
  a,b,c,e=map(Q,d['rectangles'][j]);images=[]
  # 与 C++ 的反射后连续转动不同，此处使用交换及坐标符号变换。
  # Unlike C++ reflection followed by rotation, use coordinate swapping and sign changes.
  for sw in (False,True):
   x1,y1,x2,y2=(b,a,e,c) if sw else (a,b,c,e)
   for fx in (False,True):
    for fy in (False,True):
     left,right=(L-x2,L-x1) if fx else (x1,x2);bot,top=(L-y2,L-y1) if fy else (y1,y2);images.append((left,bot,right,top))
  rows.append((images,8*(c-a)*(e-b)))
 units=[]
 for p in cert['poses']:
  need(type(p['units']) is int and p['units']>0,'DUAL_POSITIVE');u,v,t=[Q(p[k]) for k in ('u','v','t')];need(0<=u<=1 and 0<=v<=1 and 0<=t<=Q(1,2),'DUAL_LEGAL_POSE');units.append(p['units'])
 need(sum(units)==cert['sum_units']>0 and cert['coefficient_rounding_scale']==10**12,'DUAL_NORMALIZATION')
 text='67/10 335/336 2526 '+str(len(units))+'\n'+''.join(' '.join(str(Q(v)) for v in d['rectangles'][i])+'\n' for i in ids)+''.join(' '.join(p[k] for k in ('u','v','t'))+' '+str(p['units'])+'\n' for p in cert['poses'])
 return rows,text

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--certificate',type=Path,default=HERE/'certificate.json');ap.add_argument('--output',type=Path,required=True);args=ap.parse_args();cert=load(args.certificate);rows,text=generate_input(cert)
 need(hashlib.sha256(text.encode()).hexdigest()=='87bc1fe1bd72973719cd230267d024ff8952b05f8674c75e32c8f20a5f07d29b','CPP_INPUT_REGENERATION');B=Q(cert['B']);scores=[0]*2526;G=cert['coefficient_rounding_scale'];start=time.monotonic()
 for i,p in enumerate(cert['poses']):
  u,v,t=[Q(p[k]) for k in ('u','v','t')];c,s=cs(t);E=L/2-B*(c+s)/2;cx=L/2+u*E;cy=L/2+v*E;ex=B*(c+s)/2;h=B/2
  xlo,xhi,ylo,yhi=cx-ex,cx+ex,cy-ex,cy+ex
  need(E>0 and 0<=xlo<=xhi<=L and 0<=ylo<=yhi<=L,'POSE_CONTAINMENT')
  for j,(images,den) in enumerate(rows):
   total=Q(0)
   for a,b,d,e in images:
    if d<=xlo or a>=xhi or e<=ylo or b>=yhi:continue
    if all(abs(c*(x-cx)+s*(y-cy))<=h and abs(-s*(x-cx)+c*(y-cy))<=h for x in (a,d) for y in (b,e)):
     total+=(d-a)*(e-b)
    else:total+=area((a,b,d,e),cx,cy,t,B)
   coeff=total/den;need(0<=coeff<=1,'COEFFICIENT_RANGE');scores[j]+=p['units']*math.ceil(coeff*G)
  if (i+1)%25==0:print('poses',i+1,'/',len(cert['poses']),flush=True)
 maximum=max(scores);den=cert['sum_units']*G;slack=den-40*maximum;need(slack>0,'DUAL_NOT_STRICT')
 result={'schema':'n40-all-source-family-check/v1','status':'EXACT_FAMILY_OBSTRUCTION','source_sha256':SOURCE_HASH,'certificate_sha256':sha(args.certificate),'checker_sha256':sha(Path(__file__)),'sites':2526,'poses':len(cert['poses']),'max_column':scores.index(maximum),'max_score_numerator':str(maximum),'max_score_denominator':str(den),'strict_scaled_slack':str(slack),'seconds':time.monotonic()-start,'method':'Python Fraction clipping; independent D4 expansion and clip implementation'}
 save(args.output,result);print(json.dumps(result,indent=2),flush=True)
if __name__=='__main__':main()
