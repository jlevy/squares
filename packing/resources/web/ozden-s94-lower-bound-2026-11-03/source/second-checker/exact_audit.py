import sys,csv
sys.path.insert(0,'work')
from independent import *
d=load('claim/rescaled/n94_L9965_net600.json');old=load('published/mixed_n94_L995/candidate.json.gz');L,B,D=F(d['L']),F(d['B']),F(d['proof_net']['step']);lam=L/F(old['L'])
checks={'sha256_matches_manifest':hashlib.sha256(Path('claim/rescaled/n94_L9965_net600.json').read_bytes()).hexdigest()=='b8b03ee83fd2738f723759e8a54442adb55e607a211dd57d28873a62db9c749c','rectangles_exact_similarity':len(d['rectangles'])==len(old['rectangles']) and all(F(a)*lam==F(b) for p,q in zip(old['rectangles'],d['rectangles']) for a,b in zip(p['rectangle'],q['rectangle'])),'masses_unchanged':all(F(p['mass'])==F(q['mass']) for p,q in zip(old['rectangles'],d['rectangles'])),'B_exact_similarity':B==F(old['B'])*lam,'new_step_one_third_old':D==F(83,40000)/3}
rows=list(csv.DictReader(open('claim/rescaled/n94_L9965_net600.csv')));checks['csv_complete_unique_600']=sorted(int(z['r']) for z in rows)==list(range(600));checks['csv_all_V']=all(z['verdict']=='V' for z in rows)
assert all(checks.values())
rs=list(range(600));info=prepare(d,'work/full.txt',rs);Path('work/full.premises.json').write_text(json.dumps(info,indent=2));assert all(info['checks'].values())
for r in rs:
    U=F(info['domains'][str(r)]['upper']);assert L/2<U
    a=max(F(0),(r-F(1,2))*D);assert a*a+2*a-1<0
# Compare inverse-scaled new domains with old domains at the 200 common directions.
def upper(L,B,D,r):
    a=max(F(0),(r-F(1,2))*D);t=r*D;c=(1-t*t)/(1+t*t);s=2*t/(1+t*t);return L-max((1+2*a-a*a)/(2*(1+a*a)),B*(c+s)/2)
growth=[(r,upper(L,B,D,r)/lam-upper(F(old['L']),F(old['B']),F(83,40000),r//3)) for r in range(0,600,3)]
common=[r for r in range(600) if r%3==0];new=[r for r in range(600) if r%3]
record={'checks':checks,'scale_factor':str(lam),'common_old_directions':common,'new_directions_count':len(new),'direction_zero_inverse_domain_growth':str(growth[0][1]),'inverse_domain_growth_positive_count':sum(v>0 for _,v in growth),'max_inverse_domain_growth':{'r':max(growth,key=lambda p:p[1])[0],'exact':str(max(v for _,v in growth))},'all_600_domains_nonempty':True,'all_bin_lower_endpoints_below_tan_pi8':True}
Path('work/exact_audit.json').write_text(json.dumps(record,indent=2));print(json.dumps({k:v for k,v in record.items() if k!='common_old_directions'},indent=2))
