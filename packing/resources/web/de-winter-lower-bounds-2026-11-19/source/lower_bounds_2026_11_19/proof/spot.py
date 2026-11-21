"""Independently integrate exact rectangle–polygon intersections at a hard center from the subdivision tree."""
from pathlib import Path
from fractions import Fraction as F
import argparse,subprocess,tempfile,json,collections,math
import check
def clip(poly,xn,yn,limit):
    if not poly:return []
    result=[];p=poly[-1];v=xn*p[0]+yn*p[1]-limit
    for q in poly:
        w=xn*q[0]+yn*q[1]-limit
        if (v<=0)!=(w<=0):
            t=v/(v-w);result.append((p[0]+t*(q[0]-p[0]),p[1]+t*(q[1]-p[1])))
        if w<=0:result.append(q)
        p=q;v=w
    return result
def geometry(a):
    L=F(a['L']);parts=collections.defaultdict(F)
    for q in a['rectangles']:
        x,y,X,Y=map(F,q['rectangle']);w=F(q['mass'])/8
        for i,I in ((x,X),(L-X,L-x)):
            for j,J in ((y,Y),(L-Y,L-y)):
                parts[(i,j,I,J)]+=w;parts[(j,i,J,I)]+=w
    check.require(sum(parts.values())==F(a['total_mass']),'incorrect mass expansion');return parts
def integrate(parts,center,header,kernel):
    c,s,e=header[:3];C=F(c,e);H=F(s,e);xx,yy=center
    if kernel=='square':
        normals=[(C,H),(-H,C)];limit=F(header[3]*e+header[4],e*check.bm.G)
    else:
        sigma=F(header[-1],10**7);normals=[(C-sigma*H,H+sigma*C),(C+sigma*H,H-sigma*C),(-H+sigma*C,C+sigma*H),(-H-sigma*C,C-sigma*H)];limit=F(1,2)
    normals=normals+[(-x,-y)for x,y in normals];unit=2**68;lower=0;upper=0;cuts=0;inside=0
    for (x,y,X,Y),w in parts.items():
        if X<xx-1 or x>xx+1 or Y<yy-1 or y>yy+1:continue
        box=[(x-xx,y-yy),(X-xx,y-yy),(X-xx,Y-yy),(x-xx,Y-yy)];poly=box
        for u,v in normals:
            poly=clip(poly,u,v,limit)
            if len(poly)<3:break
        if len(poly)<3:continue
        area=abs(sum(p[0]*q[1]-p[1]*q[0]for p,q in zip(poly,poly[1:]+poly[:1])))/2
        if not area:continue
        if area==(X-x)*(Y-y):inside+=1;val=w
        else:cuts+=1;val=w*area/((X-x)*(Y-y))
        lower+=math.floor(val*unit);upper+=math.ceil(val*unit)
    return F(lower,unit),F(upper,unit),inside,cuts
def run(folder,save=False):
    man=check.verify(folder);kernel=man.get('kernel','square');cpp=check.here/({'square':'bmcheck.cpp','octagon':'octagon.cpp','octagon-gram':'gram.cpp'}[kernel])
    source=cpp.read_text();old='least=std::min(least,bound);';check.require(old in source,'unrecognized diagnostic insertion')
    source=source.replace('I C,H,E;', 'I track_box[4]; I C,H,E;').replace(old,'if(bound<least){least=bound;track_box[0]=b.x0;track_box[1]=b.y0;track_box[2]=b.x1;track_box[3]=b.y1;}')
    source=source.replace('return ok?0:1;', 'if(ok)std::cerr<<"LEAST "<<track_box[0]<<" "<<track_box[1]<<" "<<track_box[2]<<" "<<track_box[3]<<"\\n"; return ok?0:1;')
    study=[]
    with tempfile.TemporaryDirectory()as td:
        tmp=Path(td);f=tmp/'trace.cpp';f.write_text(source);bin=tmp/'check';subprocess.run(['c++','-O3','-std=c++17',f,'-o',bin],check=True)
        for v in man['levels']:
            a,rows=check.read_level(folder,v);parts=geometry(a);target=[min(rows,key=lambda k:k['lower_units'])]
            if rows[0]['r']==0 and target[0]['r']!=0:target.append(rows[0])
            rf=tmp/'rects';rf.write_bytes(check.input_bytes(list(check.bm.rows(a))))
            for r in target:
                h=tmp/'header';h.write_text(' '.join(map(str,r['header']))+'\n');z=subprocess.run([bin,rf,h,'2100000'],capture_output=True,text=True);tok=z.stdout.split();check.require(z.returncode==0 and tok[0]=='PASS','uncertified replay')
                coords=next(line.split()[1:]for line in z.stderr.splitlines()if line.startswith('LEAST '));i,j,I,J=map(int,coords);center=(F(i+I,2*check.bm.G),F(j+J,2*check.bm.G))
                lo,hi,full,cuts=integrate(parts,center,r['header'],kernel);check.require(lo>=F(int(tok[5]),check.bm.M)>=1 and hi/4<1,'direct intersection comparison failed')
                study.append(dict(K=v['K'],r=r['r'],center=list(map(str,center)),integer_leaf_bound=str(F(int(tok[5]),check.bm.M)),direct_mass_lower=str(lo),direct_mass_upper=str(hi),whole_rectangles=full,partial_rectangles=cuts))
    result=dict(n=man['n'],side=man['side'],kernel=kernel,tests=study)
    if save:
        q=folder/'spot_checks.pending';q.write_text(json.dumps(result,indent=2)+'\n');q.replace(folder/'spot_checks.json')
    else:
        previous=folder/'spot_checks.json'
        if previous.exists():check.require(json.load(open(previous))==result,'direct cross-check changed')
    print(folder.name,len(study),'independent polygon integrations',flush=True);return result
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('folder');p.add_argument('--save',action='store_true');a=p.parse_args();run(Path(a.folder).resolve(),a.save)
