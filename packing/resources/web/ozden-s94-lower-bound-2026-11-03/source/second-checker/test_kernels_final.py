import subprocess,random,time,json
from fractions import Fraction as F
from independent import S,clip
rng=random.Random(5022026)
cases=[]
for i in range(2500):
    r=rng.choice([0,1,2,48,96,144,300,599,rng.randrange(600)]);D0=F(83,120000);t=r*D0
    den=120000**2+r*r*83**2;c=120000**2-r*r*83**2;s=2*r*83*120000
    x=rng.randrange(-S,S);X=x+rng.randrange(1,2*S);y=rng.randrange(-S,S);Y=y+rng.randrange(1,2*S)
    if i%4==0:X=x+rng.randrange(1,100)
    if i%4==1:Y=y+rng.randrange(1,100)
    a=rng.randrange(1,S);b=rng.randrange(1,S)
    cases.append((c,s,den,x,X,y,Y,a,b))
p=subprocess.run(['work/kernel_probe_final'],input=''.join(' '.join(map(str,v))+'\n' for v in cases),text=True,capture_output=True,check=True)
maxgap=F(0)
for case,line in zip(cases,p.stdout.splitlines()):
    c,s,den,x,X,y,Y,a,b=case;A,vl,vh,hl,hh=map(int,line.split());cc,ss=F(c,den),F(s,den)
    poly=[(F(x),F(y)),(F(X),F(y)),(F(X),F(Y)),(F(x),F(Y))]
    for u,v,w in ((cc,ss,a),(-cc,-ss,a),(-ss,cc,b),(ss,-cc,b)):
        poly=clip(poly,u,v,w)
    exact=abs(sum((poly[i][0]*poly[(i+1)%len(poly)][1]-poly[i][1]*poly[(i+1)%len(poly)][0] for i in range(len(poly))),F(0)))/2 if poly else F(0)
    assert F(A)*S<=exact,(case,'area',A,exact)
    # Error is diagnostic only; the proof uses the lower bound alone.
    maxgap=max(maxgap,(exact-F(A)*S)/(S*S))
    def edge(vertical):
        low,high=map(F,(y,Y) if vertical else (x,X));constant=F(x if vertical else y)
        for A1,B1,H in ((cc,ss,a),(-cc,-ss,a),(-ss,cc,b),(ss,-cc,b)):
            coef=B1 if vertical else A1; intercept=(A1 if vertical else B1)*constant
            if coef>0:high=min(high,(H-intercept)/coef)
            elif coef<0:low=max(low,(H-intercept)/coef)
            elif intercept>H:return F(0)
        return max(F(0),high-low)
    ev,eh=edge(True),edge(False)
    assert vl<=ev<=vh,(case,'v',vl,ev,vh)
    assert hl<=eh<=hh,(case,'h',hl,eh,hh)
print(json.dumps({'cases':len(cases),'all_lower_areas_sound':True,'all_edge_enclosures_sound':True,'max_area_gap':float(maxgap)}))
