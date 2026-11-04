#!/usr/bin/env python3
"""Run only after the full independent verifier has exited successfully."""
import sys,json,hashlib,time,datetime
from pathlib import Path
from fractions import Fraction as F
from zoneinfo import ZoneInfo
from independent import load,capture,S,floor
sys.set_int_max_str_digits(0)
start=time.process_time()
rows=[json.loads(z,parse_float=str) for z in Path('work/full.jsonl').read_text().splitlines()]
assert len(rows)==600
assert [z['r'] for z in rows]==list(range(600))
assert all(z['verdict']=='VERIFIED' and z['scale']==S and z['min_bound_units']>=S for z in rows)
assert all(z['leaves']>0 and z['nodes']==2*z['leaves']-1 for z in rows)
premises=load('work/full.premises.json');assert all(premises['checks'].values())
assert all(premises['integer_limits'][k] for k in ('L_lt_10','max_expanded_density_lt_65536','sum_density_times_vertical_edge_length_lt_16384'))
audit=load('work/exact_audit.json');assert all(audit['checks'].values())
d=load('claim/rescaled/n94_L9965_net600.json')
expected='b8b03ee83fd2738f723759e8a54442adb55e607a211dd57d28873a62db9c749c'
assert hashlib.sha256(Path('claim/rescaled/n94_L9965_net600.json').read_bytes()).hexdigest()==expected
assert d['L']=='1993/200' and d['n']==94
old_tangents={k*F(83,40000) for k in range(201)}
old_D4_tangents=old_tangents|{(1-t)/(1+t) for t in old_tangents}
new_not_old_images=[r for r in range(600) if r*F(83,120000) not in old_D4_tangents]
assert new_not_old_images==[r for r in range(600) if r%3]
assert len(new_not_old_images)==400

def decimal(q,digits=15,upper=False):
    n=-floor(-q*10**digits) if upper else floor(q*10**digits)
    return f'{n//10**digits}.{n%10**digits:0{digits}d}'

exact=[]
for row in rows:
    r=row['r'];x,y=(F(v,S) for v in row['arg_units'])
    rawx,rawy=x,y;L=F(d['L']);U=F(premises['domains'][str(r)]['upper'])
    x=max(L/2,min(U,x));y=max(L/2,min(U,y))
    q=capture(d,r,x,y)
    assert q>=1
    if (x,y)==(rawx,rawy):assert q>=F(row['min_centre_lower_units'],S)
    exact.append({'r':r,'centre':[str(x),str(y)],'capture_exact':str(q),'capture_decimal_floor':decimal(q),'projected_to_exact_domain':(x,y)!=(rawx,rawy)})
    if r%50==0:print('Exact centre audit',r,flush=True)
Path('work/full_exact_centres.json').write_text(json.dumps(exact,indent=2))
best=min(exact,key=lambda v:F(v['capture_exact']));q=F(best['capture_exact'])
lower=min(z['min_bound_units'] for z in rows);lowerq=F(lower,S)
cpu=sum((F(z['cpu_seconds']) for z in rows),F(0))
sample=load('work/premises.json')
samplerows=[json.loads(z,parse_float=str) for z in Path('work/sample.jsonl').read_text().splitlines()]
samplecpu=sum((F(z['cpu_seconds']) for z in samplerows),F(0))
cpudisplay=decimal(cpu,3);samplecpudisplay=decimal(samplecpu,3)
now=datetime.datetime.now(ZoneInfo('America/Los_Angeles')).strftime('%Y-%m-%d %H:%M:%S %Z')
mutants=load('work/mutant_results.json');assert len(mutants)==4 and all(z['verdict']=='REJECT' for z in mutants.values())
for z in mutants.values():
    if 'capture_exact' in z:assert F(z['capture_exact'])<1
summary={
    'claim':'s(94)>=1993/200','verdict':'SOUND','independent_full_direction_count':600,
    'indices':list(range(600)),'all_directions_verified':True,'no_missing_or_duplicate_indices':True,
    'net_directions_absent_from_original':400,'new_angles_checked_against_all_old_D4_images':True,'nodes':sum(z['nodes'] for z in rows),
    'leaves':sum(z['leaves'] for z in rows),'scale':S,'minimum_certified_bound_units':lower,
    'minimum_certified_bound_exact':str(lowerq),'minimum_certified_bound_decimal_floor':decimal(lowerq),
    'minimum_observed_capture':best,'minimum_observed_capture_decimal_upper':decimal(q,upper=True),
    'full_replay_cpu_seconds':cpudisplay,'initial_sample_cpu_seconds':samplecpudisplay,
    'exact_full_centre_audit_cpu_seconds':str(F(str(time.process_time()-start))),
    'full_replay_started_local':'2026-11-02 14:44:53 PST','finalized_local':now,
    'source_and_evidence_sha256':{p:hashlib.sha256(Path(p).read_bytes()).hexdigest() for p in ('work/independent.py','work/intcheck_final.cpp','work/intcheck_final','work/INTEGER-SOUNDNESS.md','work/full.txt','work/full.jsonl','work/full.premises.json','work/exact_audit.json','work/full_exact_centres.json','work/mutant_results.json')}
}
Path('work/final_summary.json').write_text(json.dumps(summary,indent=2))
grade=load('GRADE.json');grade['verdict']='SOUND';grade['status']='Complete independent integer proof of all 600 directions; supplied floating-point checker is not relied upon'
grade['confidence']='High, conditional on the audited integer implementation and compiler; no proof-assistant formalization'
grade['independent_directions_checked']=list(range(600))
grade['min_capture_found']=float(q) # Reporting only; all decisions above use exact fractions.
grade['min_capture_found_interval']=[decimal(q),decimal(q,upper=True)]
grade['min_capture_direction']=best['r'];grade['min_capture_centre']=best['centre']
grade['min_capture_population']='600 retained admissible centres, one per direction; an exact global minimum was not computed'
grade['min_certified_bound']=str(lowerq)
grade['supplied_checker_fatal_issues']=list(grade['fatal_issues'])
grade['fatal_issues_scope']='The supplied checker and its original general soundness argument; superseded for this claim by the independent full-net proof'
grade['unresolved_fatal_issues_for_independent_claim_proof']=[]
grade['supplied_checker_verdict']='UNSOUND: actual false certificate accepted on this platform'
grade['resolution']='The final lower-bound verdict follows from a separate exact-integer full-net verification, not the supplied checker.'
grade['weakest_point']='The manually audited integer implementation, especially the centre-box derivative enclosures and their inheritance, and the fixed-width overflow argument. These are justified in INTEGER-SOUNDNESS.md and supported by exact tests, but are not proof-assistant formalized. There is no remaining sampled-direction or floating-point gap.'
grade['independent_cpu_seconds']=float(cpu);grade['independent_nodes']=summary['nodes'];grade['initial_sample_cpu_seconds']=float(samplecpu)
grade['independent_validation']={'rational_kernel_cases':2500,'signed_division_cases':599800,'exact_observed_centres_recomputed':600}
grade['completed_local']=now
grade['evidence']+=['work/full_exact_centres.json','work/final_summary.json','work/INTEGER-SOUNDNESS.md','work/exact_audit.json']
Path('GRADE.json').write_text(json.dumps(grade,indent=2)+'\n')
md=Path('GRADE.md').read_text().replace('VERDICT: UNDECIDED','VERDICT: SOUND',1)
old='**Checkpoint: 2026-11-02, approximately 14:52 PST.** The required independent sample and mutant checks are complete. A full independent integer verification is running. This verdict will be updated only after checking its complete output. The supplied checker has a demonstrated false acceptance, so its reported full run is insufficient by itself. This does not establish that the claimed inequality is false.'
new=f'**Finalized {now}. High confidence.** The claimed lower bound is supported by a separate integer-only verification of **all 600 directions**, each over its full centre domain. The supplied floating-point checker has a demonstrated false acceptance and is **not** relied upon for this verdict. Its fatal numerical defect is superseded here by the independent full proof; it must still be fixed before using that checker as a general verifier.'
assert old in md;md=md.replace(old,new)
old='The independent full-net replay is still running; no conclusion is drawn from a partial replay.'
new=(f'The independent full-net replay completed with **600/600 VERIFIED**, indices 0..599 present once each, including all **400 new angles**. '
     f'It checked **{summary["nodes"]:,} nodes** and **{summary["leaves"]:,} accepted leaves** in **{cpudisplay} CPU seconds** '
     f'(one thread; initial sample: {samplecpudisplay} CPU seconds). The minimum whole-domain certified bound is exactly **{lowerq}**, '
     f'at least {decimal(lowerq)}. The lowest exact capture among the full replay\'s 600 retained admissible centres lies in '
     f'**[{decimal(q)}, {decimal(q,upper=True)})**, at r={best["r"]}, centre ({best["centre"][0]}, {best["centre"][1]}). '
     f'All 600 retained point captures were recomputed by the separate rational clipping oracle. '
     f'Full logs, exact point values, totals and file hashes are in `work/full.jsonl`, `work/full_exact_centres.json` and `work/final_summary.json`. '
     f'The observed point minimum and certified whole-domain lower bound are different quantities; no exact global minimum is asserted.')
assert old in md;md=md.replace(old,new)
old='**Current weakest point and confidence:** the remaining directions cannot be inferred from this sample, and the original numerical checker cannot supply the missing rigorous coverage. Confidence is high in the exact premises, sample and mutant rejections. A SOUND verdict requires completion and audit of the independent full-net replay.'
new='**Exact weakest point and confidence:** high confidence in the claimed bound, conditional on the independently written integer verifier and compiler. The remaining trust boundary is its manual code/proof audit, especially the centre-box derivative enclosures, their inheritance, and the fixed-width overflow argument documented in `work/INTEGER-SOUNDNESS.md`. This is not a proof-assistant formalization. All 600 direction domains are covered; no numerical decision depends on floating point. The demonstrated defects in the supplied checker remain fatal to relying on its original general soundness argument, but no longer leave a gap in this independently established claim.'
assert old in md;md=md.replace(old,new)
Path('GRADE.md').write_text(md)
assert load('GRADE.json')['verdict']=='SOUND'
assert Path('GRADE.md').read_text().count('VERDICT: SOUND')==1
print(json.dumps({k:v for k,v in summary.items() if k not in ('indices','minimum_observed_capture','source_and_evidence_sha256')},indent=2))
