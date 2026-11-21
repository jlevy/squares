"""Exact implementation of the cut, its local geometry and its two comparison tests."""
from fractions import Fraction as Q
from math import floor,ceil
from functools import lru_cache
import subprocess
G=2**28;DS=2**30;M=2**40
def must(value,reason):
    if not value:raise ValueError(reason)
def change(case,fam,period,fixed,moving,fs):
    if case.get('scope')=='wall-and-corner':
        from wall_pieces import altered_wall
        return altered_wall(case,fam,period,fixed,moving,fs)
    chosen={int(i):tuple(map(Q,[l,h,z]))for i,l,h,z in case['segments']}
    must(len(chosen)==len(case['segments'])>0 and set(chosen)<=set(range(len(fixed))),'invalid cut indices')
    pieces=[];cuts=[];amount=[];d0,d1=fam['d0'],fam['d1']
    def segment(k,trans,lo,hi,rho,other=None):
        hi=min(hi,Q(3))
        if lo<hi and 0<rho and trans<=3:pieces.append((k=='v',lo,hi,trans,trans if other is None else other,rho*(hi-lo)))
    for index,(kind,coord,lo,hi,rho)in enumerate(fixed):
        if index not in chosen:segment(kind,coord,lo,hi,rho);continue
        a,b,part=chosen[index];must(lo<=a<b<=hi and 0<part<=1 and rho>0,'invalid cut')
        ends=(coord,a,coord,b)if kind=='v'else(a,coord,b,coord);must(min(ends)>=0 and max(ends)<=Q(3,2),'cuts too large');cuts.append(ends);amount.append((b-a)*rho*part)
        for l,h,r in ((lo,a,rho),(a,b,rho*(1-part)),(b,hi,rho)):segment(kind,coord,l,h,r)
    for row in fs.repeated(fs.reflect_profile(period),2,True):segment(*row)
    for k,c,l,h,w in moving+fs.repeated(period,2):
        if k=='v':segment(k,c+d0,l,h,w,c+d1)
        else:segment(k,c,l+d1,h+d0,w)
    for xl,c,r in fam['V']:segment('h',c,xl,2+d0,r)
    for low in range(72,120):segment('h',Q(low,40),Q(9,5),Q(3),Q(1,40),Q(low+1,40))
    order=sorted(range(len(case['segments'])),key=lambda i:int(case['segments'][i][0]));points=[];relative=[]
    if 'point_unit'in case:
        unit=Q(case['point_unit']);must(unit>0,'bad point unit');relative=[case['relative_removed'][i]for i in order]
        must(len(relative)==len(amount) and all(type(w)is int and w>0 and w*unit==a for w,a in zip(relative,amount)),'relative masses')
        for x,y,w in case['points']:
            x,y=Q(x),Q(y);must(0<=x<=Q(3,2) and 0<=y<=Q(3,2)and type(w)is int and w>0,'point outside domain');points.append((x,y,w,w*unit))
    must(sum(amount)-sum(w for x,y,v,w in points)==Q(case['subtraction_per_corner'])>0,'unverified saving')
    return pieces,cuts,relative,points
def input_geometry(cuts,relative,points,flip):
    boxes=[]
    for x,y,X,Y in cuts:
        if flip:x,y,X,Y=y,x,Y,X
        boxes.append((floor(x*G),floor(y*G),ceil(X*G),ceil(Y*G)))
    atoms=[]
    for x,y,v,w in points:
        if flip:x,y=y,x
        atoms.append((floor(x*G),floor(y*G),ceil(x*G),ceil(y*G),v,floor(w*M)))
    return boxes,atoms
def append_wire(boxes,weights,points):
    s=str(len(boxes))+'\n'+''.join(' '.join(map(str,r))+'\n'for r in boxes)
    if weights:s+=' '.join(map(str,weights))+'\n'+str(len(points))+'\n'+''.join(' '.join(map(str,r))+'\n'for r in points)
    return s.encode()
def outer_units(offset,seg,planes):
    x,y,X,Y=offset;l,b,r,t=seg;vert=r-l<t-b
    lo,hi=(b,t)if vert else(l,r);length=max(1,hi-lo-2);bl,bh=(l,r)if vert else(b,t)
    ol,oh,pl,ph=(y,Y,x,X)if vert else(x,X,y,Y)
    for f in range(4):
        intervals=[]
        for aa,bb,c in planes[5*f:5*f+5]:
            a,d=(bb,aa)if vert else(aa,bb);right=c*G+a*(oh if a>0 else ol)+d*(ph if d>0 else pl)-d*(bl if d>0 else bh);low,high=lo,hi
            if a>0:high=min(high,-((-right)//a))
            elif a<0:low=max(low,right//a)
            elif right<0:continue
            if low<=high:intervals.append((low,high))
        if not intervals:return 0
        lo=min(z[0]for z in intervals);hi=max(z[1]for z in intervals)
        if hi<=lo:return 0
    return min(M,-((-(hi-lo)*M)//length))
def independent(lines,planes,xlim,ylim,boxes,weights,atoms,lower=(0,0),proportional=False):
    def hits(offset,seg):
        x,y,X,Y=offset;l,b,r,t=seg
        for face in range(4):
            if all(a*(l-X if a>=0 else r-x)+c*(b-Y if c>=0 else t-y)>d*G for a,c,d in planes[5*face:5*face+5]):return False
        return True
    def inside(offset,point):
        x,y,X,Y=offset;l,b,r,t=point[:4]
        return all(a*(r-x if a>=0 else l-X)+c*(t-y if c>=0 else b-Y)<=d*G for a,c,d in planes)
    @lru_cache(20000)
    def local(x,y):
        scores=[]
        for vert,lo,hi,fl,fh,rho in lines:
            L,U=lo,hi
            for a,b,c in planes:
                u,v=(b,a)if vert else(a,b);ox,oy=(y,x)if vert else(x,y);z=c*G+v*oy-v*(fh if v>0 else fl)
                if u>0:U=min(U,ox+z//u)
                elif u<0:L=max(L,ox-((-z)//u))
                elif z<0:U=L
                if U<=L:break
            scores.append(max(0,U-L)*rho*M//(G*DS))
        return scores
    stack=[(*lower,xlim,ylim)];nodes=0;skips=0
    while stack:
        q=stack.pop();x,y,X,Y=q;nodes+=1;inset=[a for a in atoms if inside(q,a)]
        cost=sum((weights[j]if weights else 1) for j,seg in enumerate(boxes) if hits(q,seg))
        supplied=sum(a[4]for a in inset)
        if proportional:
            cost=sum(w*outer_units(q,seg,planes)for w,seg in zip(weights,boxes,strict=True));supplied*=M
        if supplied>=cost:skips+=1;continue
        current=[sum(a[5]for a in inset)]*4
        for mass in zip(local(x,y),local(X,y),local(x,Y),local(X,Y)):
            if min(mass)>0:current=[u+v for u,v in zip(current,mass)]
        if min(current)>=M:continue
        must(max(X-x,Y-y)>4 and nodes<1600000,'independent change replay failed')
        if X-x>=Y-y:
            t=(x+X)//2;stack.extend([(x,y,t,Y),(t,y,X,Y)])
        else:
            t=(y+Y)//2;stack.extend([(x,y,X,t),(x,t,X,Y)])
    return nodes,skips
def replay(v,case,f,pr,cf,ct,exe,tmp,extra):
    pieces,cuts,weights,points=change(case,f,pr,cf,ct,v.fs);cnt=0;negcount=0
    for flip in (0,1):
        lower=v.geometry_rows(pieces,flip);boxes,atoms=input_geometry(cuts,weights,points,flip);xe=max(c[2]for c in boxes);ye=max(c[3]for c in boxes)
        low=(0,0)
        if case.get('scope')=='wall-and-corner':
            sx=max(Q(0),min(z[flip]for z in cuts)-Q(1415,1000));sy=max(Q(0),min(z[1-flip]for z in cuts)-Q(1415,1000));low=(floor(sx*G),floor(sy*G))
        path=tmp/'segments_and_changes.txt';path.write_bytes(v.wire(lower)+append_wire(boxes,weights,atoms));rr=[r for r in case['rows']if r['flip']==flip]
        hdrs=[[r['r'],20,*low,xe,ye]+[j for row in v.faces(r['k'],r['r'],True)for j in row]for r in rr]
        run=subprocess.run([exe,path],input=''.join(' '.join(map(str,h))+'\n'for h in hdrs),capture_output=True,text=True,check=True)
        lines=run.stdout.splitlines();must(len(lines)==len(rr),'missing changed case')
        for line,row in zip(lines,rr):
            tok=line.split();must(tok[1]=='PASS'and list(map(int,tok[2:]))==[row[k]for k in ('nodes','leaves','depth','minimum','skipped')],'local change receipt');cnt+=1
        zero=tmp/'negative_change.txt';zlines=[(*q[:-1],0)for q in lower];nilatoms=[(*q[:4],0,0)for q in atoms];zero.write_bytes(v.wire(zlines)+append_wire(boxes,weights,nilatoms))
        ctrl=subprocess.run([exe,zero],input=' '.join(map(str,hdrs[0]))+'\n',capture_output=True,text=True,check=True);must(ctrl.stdout.split()[1]=='OPEN','zero control unexpectedly passed');negcount+=1
        if extra:
            k=max(range(len(rr)),key=lambda k:rr[k]['nodes']);r=rr[k];pl=v.faces(r['k'],r['r'],True)
            must(independent(lower,pl,xe,ye,boxes,weights,atoms,low,case.get('proportional',False))==(r['nodes'],r['skipped']),'Python reproduction disagrees')
    return case['interval'],Q(case['subtraction_per_corner']),cnt,negcount
