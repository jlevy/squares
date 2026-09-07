import numpy as np, math, csv, json
from fractions import Fraction
S=Fraction(9141,2000);G=4000;DEN=10**12;SAFETY=Fraction(10003,10000)
z=np.load('/mnt/data/recovered2/cont83_4p5705000_fixed.npz',allow_pickle=True)
reps=z['reps'];w=z['weights'];active=np.where(w>1e-11)[0]
rows=[];orbits=[];mass=0
for i in active:
 x=Fraction(round(float(reps[i,0])*80),80); y=Fraction(round(float(reps[i,1])*80),80)
 if abs(float(x)-reps[i,0])>1e-10 or abs(float(y)-reps[i,1])>1e-10: raise ValueError((i,reps[i],x,y))
 o={(x,y),(S-x,y),(x,S-y),(S-x,S-y),(y,x),(S-y,x),(y,S-x),(S-y,S-x)}
 wn=math.ceil(float(w[i]*SAFETY)*DEN-1e-8)
 orbits.append((i,x,y,len(o),wn))
 for px,py in sorted(o):
  X=int(px*G);Y=int(py*G)
  assert Fraction(X,G)==px and Fraction(Y,G)==py
  rows.append((X,Y,i,wn));mass+=wn
with open('/mnt/data/square17_4p5705_candidate/certificate_orbits.csv','w',newline='') as f:
 c=csv.writer(f);c.writerow(['column','X','Y','orbit_size','weight_numerator','weight_denominator','orbit_mass_numerator'])
 for i,x,y,s,wn in orbits:c.writerow([i,int(x*G),int(y*G),s,wn,DEN,s*wn])
with open('/mnt/data/square17_4p5705_candidate/atoms.csv','w',newline='') as f:
 c=csv.writer(f);c.writerow(['X','Y','orbit_index','weight_num']);c.writerows(rows)
summary={'side_fraction':'9141/2000','side':float(S),'grid':G,'active_orbits':len(orbits),'expanded_atoms':len(rows),'weight_denominator':DEN,'safety_factor':'10003/10000','mass_numerator':mass,'mass':mass/DEN,'slack':17-mass/DEN,'unsafed_mass':float(z['obj'])}
open('/mnt/data/square17_4p5705_candidate/candidate_summary.json','w').write(json.dumps(summary,indent=2));print(json.dumps(summary,indent=2))
