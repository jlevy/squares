import glob,re,sys,os,json
D=sys.argv[1];files=sorted(glob.glob(D+'/*.out'),key=lambda p:int(os.path.basename(p).split('_')[0]));pos=0;rows=[]
for f in files:
 a,b=map(int,os.path.basename(f).replace('.out','').split('_'));s=open(f).read();m=re.search(r'cells=(\d+) runs=(\d+) min_arrangement_coverage=(-?\d+) ok=(\d+) seconds=([0-9.eE+-]+)',s)
 assert m and 'EXACT SEGMENT COVERAGE PASS' in s and a==pos
 pos=b;c,r,mn,ok,sec=m.groups();rows.append((int(c),int(r),int(mn),int(ok),float(sec)))
assert pos==148937 and all(x[3] for x in rows)
print('cells=',sum(x[0] for x in rows))
print('runs=',sum(x[1] for x in rows))
print('minimum_arrangement_coverage=',min(x[2] for x in rows))
print('EXACT COVERAGE AGGREGATION PASS')
